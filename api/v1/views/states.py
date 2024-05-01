#!/usr/bin/python3
""" State API endpoints """

from flask import abort, request
from models import storage
from api.v1.views import app_views, format_response
from models.state import State


@app_views.route("/states/", methods=["GET"], strict_slashes=False)
def states():
    """ Retrieves all State objects """
    states = [state.to_dict() for state in storage.all(State).values()]
    return format_response(states)


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def get_state(state_id):
    """ Retrieves a specific State objects"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return format_response(state.to_dict())


@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_state(state_id):
    """ Deletes a specific State objects"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return format_response({})


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create_state():
    """ Creates a State object"""
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    if 'name' not in data:
        abort(400, description="Missing name")
    instance = State(**data)
    instance.save()
    return format_response(instance.to_dict(), 201)


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def update_state(state_id):
    """ updates a State object"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    if 'name' not in data:
        abort(400, description="Missing name")
    for key, value in data.items():
        setattr(state, key, value)
    storage.save()
    return format_response(state.to_dict())
