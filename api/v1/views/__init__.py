#!/usr/bin/python3

from flask import Blueprint
import json


app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")


def format_response(data=None):
    """ Format responses as pretty json"""
    return json.dumps(data, indent=4)


from api.v1.views.index import *
from api.v1.views.states import *
