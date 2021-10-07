# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS

import json
import os
import pprint

RESOURCE_BUCKET = os.environ.get('RESOURCE_BUCKET')

locations = {}
locationsByBeer = {}


def load_data():
    global locations_data, locations
    with open("data/locations.json") as location_file_obj:
        locations_data = location_file_obj.read()
    locations = json.loads(locations_data)

    for location in locations:
        for key, value in location.items():
            if key == "Beers":
                for beer in value:
                    if beer in locationsByBeer:
                        locations = locationsByBeer[beer]
                    else:
                        locations = []
                    locations.append(location)
                    locationsByBeer[beer] = locations

# -- Logging
class LoggingMiddleware(object):
    def __init__(self, app):
        self._app = app

    def __call__(self, environ, resp):
        errorlog = environ['wsgi.errors']
        pprint.pprint(('REQUEST', environ), stream=errorlog)

        def log_response(status, headers, *args):
            pprint.pprint(('RESPONSE', status, headers), stream=errorlog)
            return resp(status, headers, *args)

        return self._app(environ, log_response)
# -- End Logging

# -- Exceptions
class BadRequest(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

# -- Handlers
app = Flask(__name__)
corps = CORS(app)

@app.errorhandler(BadRequest)
def handle_bad_request(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.route('/')
def index():
    return 'Locations Service is running'


@app.route('/locations/all')
def get_locations():
    return jsonify(locations)

@app.route('/locations')
def get_locations_by_beer():
    beer_name = request.args.get('beerName')
    if not beer_name:
        raise BadRequest('beerName is required')

    if not beer_name in locationsByBeer:
        raise BadRequest('beerName not found')

    return jsonify(locationsByBeer[beer_name])


if __name__ == '__main__':
    app.wsgi_app = LoggingMiddleware(app.wsgi_app)
    load_data()

    app.run(debug=True, host='0.0.0.0', port=80)
