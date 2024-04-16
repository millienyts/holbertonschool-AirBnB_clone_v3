#!/usr/bin/python3

"""
Contains TestFileStorageDocs classes for documentation and style checks.
"""

from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources="/*", origins="0.0.0.0")


@app.teardown_appcontext
def teardown_db(exception):
    """ This module teardown connection to db"""
    storage.close()


@app.errorhandler(404)
def not_found_json_output(exception):
    """
    Returns JSON {'error': 'Not found'}, 404
    when a 404 error occurs
    """
    return {'error': 'Not found'}, 404


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = getenv('HBNB_API_PORT', '5000')
    app.run(host=host, port=port, threaded=True)
