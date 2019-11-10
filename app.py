
import sys
import time
from flask_cors import CORS
from bson import json_util
from flask import Flask, make_response, jsonify
from flask import Response
from flask_restful import Api, reqparse
from flasgger import Swagger, NO_SANITIZER
from werkzeug.exceptions import HTTPException, BadRequest

from main.controllers.mutant import mutant
from main.controllers.stats import stats

app = Flask(__name__)
app.url_map.strict_slashes = False # fix trailing slash
CORS(app) #enable cors
#api = Api(app,  prefix="/ml/api/v1") #ml api version 1
api = Api(app)
swagger = Swagger(app, sanitizer=NO_SANITIZER)
app.config.from_object("config.Config")
api.add_resource(mutant,  '/mutant/')
api.add_resource(stats,  '/stats/')
         
def run(actually_run=True):  
    if actually_run:        
        app.run(debug=True, host='0.0.0.0', port=5000)
    
    else:
        return app
    

@app.errorhandler(404)
def not_found(error):
    """
    Gives error message when any invalid url are requested.
    Args:
        error (string):
    Returns:
        Error message.
    """
    header = {"success":False, "code": 404, "message":"Page not found", "version":"2.0.0", "timestamp": int(time.time())}
    return make_response(jsonify({"header" : header, "body":{}}), 404)


@app.errorhandler(403)
def forbidden(error):
    """
    Gives error message when is not mutant.
    Args:
        error (string):
    Returns:
        Error message.
    """
    header = {"success":False, "code": 403, "message":"Forbidden", "version":"2.0.0", "timestamp": int(time.time())}
    return make_response(jsonify({"header" : header, "body":{"Forbidden"}}), 403)


if __name__ == '__main__':
    app.run()
