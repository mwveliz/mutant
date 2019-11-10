
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

###################################
# Wrap the Api with swagger.docs. It is a thin wrapper around the Api class that adds some swagger smarts
###################################

app = Flask(__name__)
app.url_map.strict_slashes = False # fix trailing slash
CORS(app) #enable cors
#api = Api(app,  prefix="/ml/api/v1") #ml api version 1
api = Api(app)

swagger = Swagger(app, sanitizer=NO_SANITIZER)


app.config.from_object("config.Config")
api.add_resource(mutant,  '/mutant/')
api.add_resource(stats,  '/stats/')



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


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
