from . import example
from flask import render_template

@example.app_errorhandler(404)
def not_found_error(e): 
    render_template("error_pages/404.html"), 404