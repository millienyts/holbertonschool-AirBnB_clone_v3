#!/usr/bin/python3
"""Script for Blueprint for flask"""


from flask import Blueprint
from api.v1.views.index import app_views
from api.v1.views.states import app_views as states_views
from api.v1.views.places import app_views as places_views
from api.v1.views.places_reviews import app_views as places_reviews_views
from api.v1.views.cities import app_views as cities_views
from api.v1.views.amenities import app_views as amenities_views
from api.v1.views.users import app_views as users_views

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
