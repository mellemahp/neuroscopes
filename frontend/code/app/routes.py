"""/app/routes.py [Frontend]

Description: Defines views for frontend app
Project: Fauxstrology
Author: Hunter Mellema
Date: 12/7/2019

"""
#=== Start import ===# 
# third party 
from flask import render_template, request, redirect, url_for


# std library
import requests
import logging
import re
import time

#=== End import ===# 

l = logging.getLogger(__name__)

BD_REGEX = "^((0|1)\d{1})-((0|1|2)\d{1})-((19|20)\d{2})"
VAL_REG = re.compile(BD_REGEX)


def landing_page(): 
    if request.method == "GET":
        return render_template("landing.html"), 200

    if request.method == "POST": 
        try: 
            bday_list = request.form['bday'].split("-")
            bd = "{}-{}-{}".format(bday_list[1], bday_list[2], bday_list[0])
    
            return redirect(url_for('display_page', bd=bd))

        except Exception as e: 
            l.error("Error with front end | {}".format(str(e)))

            return 500

def display_page():
    try:
        # get birthday and check if exists
        bd = request.args.get("bd")

        if not bd: 
            return "No Birthday Provided", 400

        if VAL_REG.match(bd) is None: 
            return "Invalid birthday format", 400
        
        hs_res = requests.get('http://horoscopeGen:5000/', params={"bd":bd })
        hs_data = hs_res.json()['data']

        cons_res = requests.get('http://pictureGen:5000/', params={"bd":bd})
        cons_data = cons_res.json()['data']

        return render_template("display.html", 
            hs=hs_data['horoscope'], 
            ln=hs_data['lucky_numbers'], 
            image_url=cons_data['image_path'],
            coords=[cons_data['ra'],cons_data['dec']], 
            constellation=cons_data['prediction']
            )

    except Exception as e:
        l.error("Error with front end | {}".format(str(e)))

        return redirect(url_for('landing_page')), 500
