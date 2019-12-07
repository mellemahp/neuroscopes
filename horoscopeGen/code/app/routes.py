"""/app/routes.py

Description: Route definition for horoscope generator
Project: Fauxstrology
Author: Hunter Mellema
Date: 12/7/2019

"""
#=== Start imports ===# 

# third party
from flask import current_app, jsonify, request
from textgenrnn import textgenrnn

# std lib
import logging
import time
import re
from random import randint

#=== End imports ===# 

l = logging.getLogger(__name__)

BD_REGEX = "^((0|1)\d{1})-((0|1|2)\d{1})-((19|20)\d{2})"
VAL_REG = re.compile(BD_REGEX)

def horoscope(): 
    try:
        # get birthday and check if exists
        bd = request.args.get("bd")

        if not bd: 
            return jsonify(error=["Please provide a birthday for our oracle to divine the future for"]), 400

        if VAL_REG.match(bd) is None: 
            return jsonify(error=["Birthday formatting is incorrect. Please use MM-DD-YYYY format"]), 400

        rkey = "hs_" + bd
        if not current_app.config["REDIS_DB"].exists(rkey):
            fortune_net = textgenrnn('app/fortunes_clean_dedupe.hdf5')
            fortune_list = fortune_net.generate(
                3, return_as_list=True, temperature=.6
            ) 
            fortune = ''.join([i + ' ' for i in fortune_list])  
            lucky_numbers = ''.join(["{}".format(randint(0, 9)) for n in range(6)])
            current_app.config["REDIS_DB"].hset(rkey, "fortune", fortune)
            current_app.config["REDIS_DB"].hset(rkey, "lucky_numbers", lucky_numbers)
        else: 
            fortune = current_app.config["REDIS_DB"].hget(rkey, "fortune").decode('utf-8')
            lucky_numbers = current_app.config["REDIS_DB"].hget(rkey, "lucky_numbers")

        l.error(lucky_numbers)
        lucky_number_list = [int(lucky_numbers[n:n+2]) for n in range(6) if n % 2 == 0]

        data = {
            "metadata": { 
                "gen_at": time.strftime("%d %m, %H:%M:%S"),
                "input_bd": bd
            }, 
            "horoscope": fortune, 
            "lucky_numbers": lucky_number_list
        }

        l.info("successfully generated horoscope")

        return jsonify(data=data), 200
    

    except Exception as e: 
        l.exception("An error occured in horoscope generation | {}".format(str(e)))

        return jsonify(error=["Could not find your future in the stars"]), 500