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
from imageai.Prediction import ImagePrediction
import numpy as np
import cv2
import imutils
from PIL import Image

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

def constellation():
    try:
        bd = request.args.get("bd")
        rkey = "const_" + bd
        if not current_app.config["REDIS_DB"].exists(rkey):
            dayOfYear = datetime.strptime(bd, "%D-%M-%Y").timetuple().tm_yday

            #right ascension and declinaiton come from the birthday
            ra = dayOfYear/365*360
            dec = (dayOfYear/365*180)-90

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
            img = np.array(pil_image) 
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
                cv2.circle(img, (cX, cY), 5, (255, 255, 0), -1)
                # For each star, add the center and the angle wrt x-axis of the ray pointing
                # to the center
                angle = np.arctan2(cY-centerPoint[1], cX-centerPoint[0])
                stars = np.append(stars,[[cX,cY,angle]], axis=0)

            # Sort the stars by the angle
            stars = stars[1:,:]
            stars = stars[stars[:,-1].argsort()]
            stars = stars[:,:-1].astype(np.int32)

            # Connect the dots
            cv2.fillPoly(img, np.array([stars]), (255,0,0))

            cv2.imwrite('prediction_image.jpg', img)

            executionPath = os.getcwd()

            prediction = ImagePrediction()
            prediction.setModelTypeAsSqueezeNet()
            prediction.setModelPath(os.path.join(executionPath,
                "squeezenet_weights_tf_dim_ordering_tf_kernels.h5"))
            prediction.loadModel()
            predictions, probabilities = prediction.predictImage(os.path.join(executionPath,"prediction_image.jpg"), result_count=10)

            imagePath = ""
            predictionList = predictions
            current_app.config["REDIS_DB"].hset(rkey, "imagePath", imagePath)
            current_app.config["REDIS_DB"].hset(rkey, "predictionList", predictionList)
        else: 
            imagePath = current_app.config["REDIS_DB"].hget(rkey, "imagePath").decode('utf-8')
            predictionList = current_app.config["REDIS_DB"].hget(rkey,"predictionList")

        data = {
            "metadata": { 
                "gen_at": time.strftime("%d %m, %H:%M:%S"),
                "input_bd": bd
            }, 
            "image_path": imagePath, 
            "predictionList": predictionList
        }

        l.info("successfully generated horoscope")

        return jsonify(data=data), 200
    except Exception as e: 
        l.exception("An error occured in constellation generation | {}".format(str(e)))

        return jsonify(error=["Could not find your future in the stars"]), 500
        


