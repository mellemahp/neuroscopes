""" SOME STUFF 

"""
# start import # 

# std lib 
import logging

# third party
from flask import Flask 


# local 
from config import config

# end imports #

def new_app(config_selector): 
    """ Creates a new flask app instance 

    :param config_selector: version of application to deploy ('dev', 'test', etc)
    :type config_selector: str

    """
    app = Flask(__name__) 

    # add configuration parameters to application
    app.config.from_object(config[config_selector])

    # add any blueprints 
    from .example import example as example_blueprint
    app.register_blueprint(example_blueprint)

    # other setup 