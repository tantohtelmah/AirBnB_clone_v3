#!/usr/bin/python3

from flask import Blueprint
import json


app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")


def format_response(data=None, status=200):
    """ Format responses as pretty json"""
    return (json.dumps(data, indent=4), status)


from api.v1.views.index import *
from api.v1.views.states import *
from models.base_model import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
from api.v1.views.users import *
