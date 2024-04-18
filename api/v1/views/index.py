#!/usr/bin/python3
"""
API Status Page

Contains routes for the API status page, showing the status (OK or not) and the count
of objects of each type in 'storage.all()'.

"""
from flask import Blueprint, jsonify
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review

app_views = Blueprint('app_views', __name__)


@app_views.route("/status")
def check_status():
    """ return status ok as json"""
    dict_ = {'status': "OK"}

    return jsonify(dict_)


@app_views.route('/stats')
def model_statistics():
    """
    Returns the counts of all the
    objects in 'storage.all()',
    counted by each type
    """
    return {
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User)
    }
    return jsonify(stats)
