"""/app/routes.py

Description: Route definition for constellation generator
Project: Fauxstrology
Author: Connor Johnstone
Date: 12/7/2019

"""
#=== Start imports ===# 

# third party
from flask import current_app, jsonify, request
from textgenrnn import textgenrnn
import requests
from imageai.Prediction import ImagePrediction
import numpy as np
import cv2
import imutils
from PIL import Image
import boto3

# std lib
from io import BytesIO
import logging
import datetime
import time
import re
import os
from random import randint

#=== End imports ===# 

l = logging.getLogger(__name__)

def scrub_bytes(prediction):
    if type(prediction) is bytes:
        prediction = prediction.decode('utf-8')
    return prediction

def constellation():
    try:
        executionPath = os.getcwd()

        bd = request.args.get("bd")

        #right ascension and declinaiton come from the birthday
        dayOfYear = datetime.datetime.strptime(bd, "%m-%d-%Y").timetuple().tm_yday
        ra = (dayOfYear/365*100)+130
        dec = (dayOfYear/365*50)+5

        rkey = "const_" + bd
        if not current_app.config["REDIS_DB"].exists(rkey):

            #angular distance image will span in horizontal (width) and vertical (height)
            #directions
            width_deg = 0.25
            height_deg = 0.25

            #pixels along width and height of image
            width = 400
            height = width

            #scale is arcseconds per pixel
            scale = width_deg * 3600 / width

            #get picture from SDSS
            url = "http://skyserver.sdss.org/dr15/SkyServerWS/ImgCutout/getjpeg?ra=" + \
            str(ra) + "&dec=" + str(dec) + "&scale=" + str(scale) + \
            "&width=" + str(width) + "&height=" + str(height)
            r = requests.get(url = url)
            pil_img = Image.open(BytesIO(r.content))
            img = np.array(pil_img) 
            img = img[:, :, ::-1].copy() 

            # Number of stars to find
            numStars = 10

            # Determine the center point
            centerPoint = (img.shape[0]/2, img.shape[1]/2)

            # Convert the image to grayscale, then blur and threshold
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            blurred = cv2.GaussianBlur(gray, (5,5), 0)
            thresh = cv2.threshold(blurred, 50, 255, cv2.THRESH_BINARY)[1]

            # Find the contours in the thresholded image and pick out the brightest
            conts = cv2.findContours(thresh.copy(), 
                                      cv2.RETR_EXTERNAL,
                                      cv2.CHAIN_APPROX_SIMPLE)
            conts = imutils.grab_contours(conts);
            conts = sorted(conts, key=cv2.contourArea, reverse=True)[:numStars]

            # Pull out the center of each contour
            stars = np.array([[1,2,3]])
            for c in conts:
                M = cv2.moments(c)
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                cv2.circle(img, (cX, cY), 3, (255, 0, 255), -1)
                # For each star, add the center and the angle wrt x-axis of the ray pointing
                # to the center
                angle = np.arctan2(cY-centerPoint[1], cX-centerPoint[0])
                stars = np.append(stars,[[cX,cY,angle]], axis=0)

            # Sort the stars by the angle
            stars = stars[1:,:]
            stars = stars[stars[:,-1].argsort()]
            stars = stars[:,:-1].astype(np.int32)

            # Connect the dots
            img_overlay = img.copy()
            cv2.fillPoly(img_overlay, np.array([stars]), (255,255,255))
            cv2.addWeighted(img_overlay, 0.2, img, 0.8, 0, img)

            cv2.imwrite(os.path.join(executionPath,'prediction_image.jpg'), img)

            bucket_name = 'feauxstrology-images'
            file_name = bd + '.jpg'
            content = open(os.path.join(executionPath,'prediction_image.jpg'), 'rb')
            s3 = current_app.config['S3']
            response = s3.list_buckets()
            print(response)
            s3.upload_file('prediction_image.jpg', bucket_name, file_name)

            prediction = ImagePrediction()
            prediction.setModelTypeAsSqueezeNet()
            prediction.setModelPath(os.path.join(executionPath,
                "squeezenet_weights_tf_dim_ordering_tf_kernels.h5"))
            prediction.loadModel("fastest")
            predictions, probabilities = prediction.predictImage(os.path.join(executionPath,"prediction_image.jpg"), result_count=5)
            predictions = list(map(scrub_bytes, predictions))

            imagePath = "https://feauxstrology-images.s3.us-east-2.amazonaws.com/" + bd + ".jpg"
            current_app.config["REDIS_DB"].hset(rkey, "imagePath", imagePath)
            current_app.config["REDIS_DB"].hset(rkey, "prediction1",predictions[0])
            current_app.config["REDIS_DB"].hset(rkey, "prediction2",predictions[1])
            current_app.config["REDIS_DB"].hset(rkey, "prediction3",predictions[2])
            current_app.config["REDIS_DB"].hset(rkey, "prediction4",predictions[3])
            current_app.config["REDIS_DB"].hset(rkey, "prediction5",predictions[4])
        else: 
            imagePath = current_app.config["REDIS_DB"].hget(rkey, "imagePath").decode('utf-8')
            predictions = [
                    current_app.config["REDIS_DB"].hget(rkey, "prediction1"),
                    current_app.config["REDIS_DB"].hget(rkey, "prediction2"),
                    current_app.config["REDIS_DB"].hget(rkey, "prediction3"),
                    current_app.config["REDIS_DB"].hget(rkey, "prediction4"),
                    current_app.config["REDIS_DB"].hget(rkey, "prediction5")]

        print(predictions[0])
        print(type(predictions[0]))
        print(type("digital_clock"))
        data = {
            "metadata": { 
                "gen_at": time.strftime("%d %m, %H:%M:%S"),
                "input_bd": bd
            }, 
            "ra": ra,
            "dec": dec,
            "image_path": imagePath, 
            "prediction1": scrub_bytes(predictions[0]),
            "prediction2": scrub_bytes(predictions[1]),
            "prediction3": scrub_bytes(predictions[2]),
            "prediction4": scrub_bytes(predictions[3]),
            "prediction5": scrub_bytes(predictions[4])
        }

        l.info("successfully generated constellation")

        return jsonify(data=data), 200
    except Exception as e: 
        l.exception("An error occured in constellation generation | {}".format(str(e)))

        return jsonify(error=["Could not find your future in the stars"]), 500
        

