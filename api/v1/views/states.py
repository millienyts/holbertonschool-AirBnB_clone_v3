#!/usr/bin/python3
"""
Endpoints for "/api/v1/states" API:
GET - Retrieve all States.
POST - Create a new State.
PUT - Update an existing State.
DELETE - Remove a State.
"""
from models import storage
from models.state import State
from api.v1.views import app_views
from flask import abort, jsonify, request

@app_views.route("/states", strict_slashes=False, methods=["GET"])
def get_all_states():
    """Returns all States as JSON."""
    return jsonify([state.to_dict() for state in storage.all(State).values()])

@app_views.route("/states/<state_id>", strict_slashes=False, methods=["GET"])
def get_state(state_id):
    """Returns a State by ID as JSON, 404 if not found."""
    result = storage.get(State, state_id)
    return jsonify(result.to_dict()) if result else abort(404)

@app_views.route("/states/<state_id>", strict_slashes=False, methods=["DELETE"])
def delete_state(state_id):
    """Deletes a State by ID, returns {}, 200 if successful, 404 if not found."""
    target = storage.get(State, state_id)
    if not target:
        abort(404)
    storage.delete(target)
    storage.save()
    return jsonify({}), 200

@app_views.route("/states/", strict_slashes=False, methods=["POST"])
def create_state():
    """Creates a new State based on JSON input, returns it as JSON, 201 if successful."""
    new_state_json = request.get_json(silent=True)
    if not new_state_json or 'name' not in new_state_json:
        abort(400, "Invalid JSON or missing 'name' field")
    new_state = State(**new_state_json)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201

@app_views.route("/states/<state_id>", strict_slashes=False, methods=["PUT"])
def update_state(state_id):
    """Updates a State by ID with JSON input, returns it as JSON, 200 if successful, 404 if not found."""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    new_state_info = request.get_json(silent=True)
    if not new_state_info:
        abort(400, "Invalid JSON")
    if 'name' in new_state_info:
        state.name = new_state_info['name']
    storage.save()
    return jsonify(state.to_dict()), 200
