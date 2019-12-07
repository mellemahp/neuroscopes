"""SOME INFO 

"""
# start import # 

# third party
from waitress import serve

# local 
from app import new_app

# end imports #

if __name__ == "__main__":
    # TODO: change this to have multiple modes for a real deployment
    app = new_app('default')
    serve(app, host="0.0.0.0", port=5000)