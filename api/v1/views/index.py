#!/usr/bin/python3
""" Defines routes"""

from flask import jsonify
from api.v1.views import app_views
from models import storage
import json


@app_views.route("/status", methods=["GET"])
def status():
    """ Route to status"""

    return jsonify({"status": "OK"})


@app_views.route("/stats", methods=["GET"])
def stats():
    """ Route to count objects"""

    storage.all()
    return (json.dumps(storage.statInfo))
