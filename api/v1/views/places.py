from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage, Place, City, State, Amenity


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def search_places():
    """Search for places based on JSON request body"""

    # Check if request body is valid JSON
    if not request.is_json:
        abort(400, 'Not a JSON')

    # Get JSON data from request
    data = request.get_json()

    # Get states, cities, and amenities from JSON data
    states = data.get('states', [])
    cities = data.get('cities', [])
    amenities = data.get('amenities', [])

    # Retrieve all places if JSON body is empty or each list of all keys are empty
    if not states and not cities and not amenities:
        places = storage.all(Place).values()
        return jsonify([place.to_dict() for place in places])

    # Initialize empty list to store filtered places
    filtered_places = []

    # Retrieve places based on states
    for state_id in states:
        state = storage.get(State, state_id)
        if state:
            cities.extend([city.id for city in state.cities])

    # Remove duplicate city ids
    cities = list(set(cities))

    # Retrieve places based on cities
    for city_id in cities:
        city = storage.get(City, city_id)
        if city:
            places = city.places
            filtered_places.extend(places)

    # Filter places based on amenities
    if amenities:
        filtered_places = [place for place in filtered_places if all(amenity_id in place.amenities for amenity_id in amenities)]

    return jsonify([place.to_dict() for place in filtered_places])
