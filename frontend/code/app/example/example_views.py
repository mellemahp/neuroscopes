from flask import render_template
from . import example

@example.route("/example/")
def example_route(): 
    return render_template("example.html"), 200