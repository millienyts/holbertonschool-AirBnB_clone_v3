#!/usr/bin/python3
"""API endpoints for managing Place resources."""
from flask import jsonify, abort, request, make_response
from models import storage
from models.city import City
from models.user import User
from models.place import Place
from api.v1.views import app_views


@app_views.route('/cities/<string:city_id>/places', methods=['GET'], strict_slashes=False)
def list_places(city_id):
    """Returns all Place objects associated with a City."""
    city_obj = storage.get(City, city_id)
    if not city_obj:
        abort(404)
    places_list = [place.to_dict() for place in city_obj.places]
    return jsonify(places_list)


@app_views.route('/places/<string:place_id>', methods=['GET'], strict_slashes=False)
def show_place(place_id):
    """Retrieves a specific Place by its ID."""
    place_obj = storage.get(Place, place_id)
    if not place_obj:
        abort(404)
    return jsonify(place_obj.to_dict())


@app_views.route('/places/<string:place_id>', methods=['DELETE'], strict_slashes=False)
def remove_place(place_id):
    """Deletes a Place based on its ID and returns a 200 response."""
    place_to_delete = storage.get(Place, place_id)
    if not place_to_delete:
        abort(404)
    place_to_delete.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<string:city_id>/places', methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """Creates a Place within a City from JSON request data."""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    place_data = request.get_json()
    if not place_data:
        abort(400, description="Not a JSON")
    if 'user_id' not in place_data:
        abort(400, description="Missing user_id")
    user = storage.get(User, place_data['user_id'])
    if not user:
        abort(404)
    if 'name' not in place_data:
        abort(400, description="Missing name")
    new_place = Place(city_id=city_id, **place_data)
    new_place.save()
    return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route('/places/<string:place_id>', methods=['PUT'], strict_slashes=False)
def edit_place(place_id):
    """Updates an existing Place object with new JSON data."""
    place_to_update = storage.get(Place, place_id)
    if not place_to_update:
        abort(404)
    updated_data = request.get_json()
    if not updated_data:
        abort(400, description="Not a JSON")
    for key, value in updated_data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place_to_update, key, value)
    place_to_update.save()
    return jsonify(place_to_update.to_dict())
