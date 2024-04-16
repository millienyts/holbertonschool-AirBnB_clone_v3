#!/usr/bin/python3
"""
API Status Page Blueprint Package
Containing the Flask Blueprint Object 'app_views'
"""
from flask import Blueprint, Flask, abort, render_template

app_views = Blueprint('app_views', __name__, url_prefix="/api/v1")

from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
from api.v1.views.places import *
from api.v1.views.users import *
from api.v1.views.places_reviews import *
