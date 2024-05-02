#!/usr/bin/python3
""" State API endpoints """

from flask import abort, request, jsonify, make_response
from models.state import State
from models import storage
from api.v1.views import app_views, format_response


@app_views.route("/states", methods=['GET'], strict_slashes=False)
@app_views.route("/states/<state_id>", methods=['GET'], strict_slashes=False)
def get_states(state_id=None):
    if state_id:
        state = storage.get(State, state_id)
        if state:
            return state.to_dict()
        abort(404)

    """get all states"""
    states = [obj.to_dict() for obj in storage.all(State).values()]
    return format_response(states)


@app_views.route("/states/<state_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """ deletes a state by id if it exist else raise 404"""
    state = storage.get(State, state_id)
    if state:
        state.delete()
        storage.save()
        return {}
    abort(404)


@app_views.route("/states", methods=['POST'], strict_slashes=False)
def create_state():
    """method to create a new state"""
    data = request.get_json(silent=True)
    if data is None:
        abort(400, "Not a JSON")
    if 'name' not in data:
        abort(400, "Missing name")
    state = State(**data)
    state.save()

    return state.to_dict(), 201


@app_views.route("/states/<state_id>", methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """method to update state by id"""
    data = request.get_json(silent=True)
    if data is None:
        abort(400, "Not a JSON")
    state = storage.get(State, state_id)
    if state:
        for key, val in data.items():
            if key not in ["id", "created_at", "updated_at"]:
                setattr(state, key, val)
        state.save()
        return state.to_dict(), 200
    abort(404)
