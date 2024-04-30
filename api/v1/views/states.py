#!/usr/bin/python3
""" State routes"""

from os import abort
from flask import make_response, request
from flask import jsonify
from models import storage
from api.v1.views import app_views, format_response
from models.state import State


@app_views.route("/states/", methods=["GET"])
def states():
    """ Retrieves all State objects """
    all_states = storage.all(State).values()
    states = []
    for state in all_states:
        states.append(state.to_dict())
    return format_response(states)


@app_views.route("/states/<state_id>", methods=["GET"])
def get_state(state_id):
    """ Retrieves a specific State objects"""
    state = storage.get(State, state_id)
    if not state:
        from api.v1.app import not_found  # brought this here
        return not_found()  # added return
    return format_response(state.to_dict())


@app_views.route("/states/<state_id>", methods=["DELETE"])
def delete_state(state_id):
    """ Deletes a specific State objects"""
    state = storage.get(State, state_id)
    if not state:
        from api.v1.app import not_found  # brought this here
        return not_found()
    storage.delete(state)
    storage.save()
    return format_response({})


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create_state():
    """ Creates a State object"""
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")
    state = request.get_json()
    instance = State(**state)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route("/states/<state_id>", methods=["PUT"])
def update_state(state_id):
    """ updates a State object"""
    state = storage.get(State, state_id)
    if not state_id:
        from api.v1.app import not_found  # brought this here
        return not_found()
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")
    ignore = ['id', 'created_at', 'updated_at']
    state = request.get_json()
    for key, value in state.items():
        if key not in ignore:
            setattr(state, key, value)
    storage.save()
    return format_response(state.to_dict())
