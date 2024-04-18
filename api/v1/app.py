#!/usr/bin/python3
"""API endpoints for managing User entities."""
from flask import Flask, jsonify, abort, request, make_response
from models import storage
from models.user import User
from api.v1.views import app_views


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def list_users():
    """Returns all User instances as JSON objects."""
    all_users = [u.to_dict() for u in storage.all(User).values()]
    return jsonify(all_users)


@app_views.route('/users/<string:user_id>', methods=['GET'], strict_slashes=False)
def retrieve_user(user_id):
    """Fetches a User instance by ID, returns JSON or 404 if not found."""
    user_instance = storage.get(User, user_id)
    if user_instance is None:
        abort(404)
    return jsonify(user_instance.to_dict())


@app_views.route('/users/<string:user_id>', methods=['DELETE'], strict_slashes=False)
def remove_user(user_id):
    """Deletes a User instance by ID, returns empty JSON response on success."""
    user_to_delete = storage.get(User, user_id)
    if user_to_delete is None:
        abort(404)
    user_to_delete.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def add_user():
    """Creates a new User instance"""
    user_data = request.get_json()
    if not user_data:
        abort(400, description="Not a JSON")
    if 'email' not in user_data:
        abort(400, description="Missing email")
    if 'password' not in user_data:
        abort(400, description="Missing password")
    new_user = User(**user_data)
    new_user.save()
    return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<string:user_id>', methods=['PUT'], strict_slashes=False)
def modify_user(user_id):

    existing_user = storage.get(User, user_id)
    if existing_user is None:
        abort(404)
    update_data = request.get_json()
    if not update_data:
        abort(400, description="Not a JSON")
    for key, value in update_data.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(existing_user, key, value)
    existing_user.save()
    return jsonify(existing_user.to_dict())
