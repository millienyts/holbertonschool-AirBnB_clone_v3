#!/usr/bin/python3
"""Index module for Flask app."""


from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def api_status():
    """Endpoint that returns the status of the API."""
    return jsonify({"status": "OK"})


@app_views.route('/api/v1/stats', methods=['GET'], strict_slashes=False)
def get_stats():
    """Endpoint to retrieve stats of objects by type."""
    stats = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }
    print("Stats:", stats)
    return jsonify(stats)
