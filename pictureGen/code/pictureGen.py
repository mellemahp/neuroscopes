"""pictureGen.py

Description: Entry point for pictureGen service
Project: Fauxstrology
Author: Connor Johnstone
Date: 12/7/2019

"""
#=== Start import ===# 
# third party
from waitress import serve

# local 
from app import new_app

#=== End Imports ===#

if __name__ == "__main__":
    app = new_app()
    serve(app, host="0.0.0.0", port=5000)
