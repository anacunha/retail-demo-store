# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

from flask import Flask
from flask import jsonify
from flask_cors import CORS

import json
import os
import pprint

RESOURCE_BUCKET = os.environ.get('RESOURCE_BUCKET')

locations = {}


def load_data():
    global locations_data, locations
    with open("data/locations.json") as location_file_obj:
        locations_data = location_file_obj.read()
    locations = json.loads(locations_data)


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


# -- Handlers
app = Flask(__name__)
corps = CORS(app)


@app.route('/')
def index():
    return 'Locations Service is running'


@app.route('/locations/all')
def get_locations():
    return jsonify(locations)


if __name__ == '__main__':
    app.wsgi_app = LoggingMiddleware(app.wsgi_app)
    load_data()

    app.run(debug=True, host='0.0.0.0', port=80)
