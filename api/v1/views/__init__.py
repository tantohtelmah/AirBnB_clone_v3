#!/usr/bin/python3
"""Create a flask application for the API"""

from flask import Blueprint
import json


def format_response(data=None, status=200):
    """ Format responses as pretty json"""
    return (json.dumps(data, indent=4), status)


app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
from api.v1.views.users import *
from api.v1.views.places import *
from api.v1.views.places_reviews import *
from api.v1.views.places_amenities import *
