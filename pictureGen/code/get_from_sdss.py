# -*- coding: utf-8 -*-
"""
Created on Sat Dec  7 13:12:20 2019

@author: chels
"""
import requests
from PIL import Image
from io import BytesIO

#right ascension and declinaiton (degrees)
ra = 122.45
dec = 21.3
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
img = Image.open(BytesIO(r.content))
img.save("sdss.jpg")
