"""/frontend.py [Frontend]

Description: Entrypoint for frontend service
Project: Fauxstrology
Author: Hunter Mellema
Date: 12/7/2019

"""
#=== Start imports ===# 

# third party
from waitress import serve

# local 
from app import new_app

#=== End imports ===# 


if __name__ == "__main__":
    app = new_app()
    serve(app, host="0.0.0.0", port=5000)