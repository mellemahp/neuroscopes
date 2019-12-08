"""/app/__init__.py [Frontend]

Description: App factory method for frontend
Project: Fauxstrology
Author: Hunter Mellema
Date: 12/7/2019

"""
#=== Start imports ===# 

# std lib 
import logging

# third party
from flask import Flask 

# local 
from .routes import landing_page, display_page

#=== End imports ===# 

# Define Routes 
ROUTE_TABLE = {
    '/': {"fxn": landing_page, "methods": ["GET", "POST"] },
    '/horoscope/': {"fxn": display_page, "methods": ["GET"] }
}


class Config(): 
    VARIABLE=1


def new_app(): 
    """ Creates a new flask app instance 
    """
    app = Flask(__name__) 

    # add configuration parameters to application
    app.config.from_object(Config())

    # Construct Routes
    for url in ROUTE_TABLE:
        app.add_url_rule(url, methods=ROUTE_TABLE[url]["methods"], view_func=ROUTE_TABLE[url]["fxn"])

    return app