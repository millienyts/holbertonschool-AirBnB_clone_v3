"""Index module for Flask app."""

from api.v1.views import app_views
from flask import jsonify

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def api_status():
    """Endpoint that returns the status of the API."""
    return jsonify({"status": "OK"})
