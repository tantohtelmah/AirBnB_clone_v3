#!/usr/bin/python3
""" Defines routes"""

from flask import jsonify
from api.v1.views import app_views, format_response
from models import storage


@app_views.route("/status", methods=["GET"])
def status():
    """ Route to status"""

    return format_response({"status": "OK"})


@app_views.route("/stats", methods=["GET"])
def stats():
    """ Route to count objects"""

    storage.all()
    return format_response(storage.statInfo)
