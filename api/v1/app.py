#!/usr/bin/python3
"""Main module of the Flask app."""


from flask import Flask, jsonify
from os import getenv
from api.v1.views import app_views


app = Flask(__name__)
host = getenv('HBNB_API_HOST', '0.0.0.0')
port = getenv('HBNB_API_PORT', '5000')


@app.teardown_appcontext
def close_storage(exception):
    """Close the storage on teardown."""
    from models import storage
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Handler for 404 errors."""
    return jsonify({"error": "Not found"}), 404


if __name__ == '__main__':
    app.register_blueprint(app_views)
    print()
    print(app.url_map)
    print()
    app.run(host=host, port=port, threaded=True)
