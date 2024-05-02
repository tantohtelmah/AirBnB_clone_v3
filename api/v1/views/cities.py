#!/usr/bin/python3
"""Module to handle rest api actions to city"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models.city import City
from models.state import State
from models import storage


@app_views.route("/states/<state_id>/cities", methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    """method to get all cities in a given state_id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route("/cities/<city_id>", methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """method to get a city by id"""
    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict())
    abort(404)


@app_views.route("/cities/<city_id>", methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """method to delete city"""
    city = storage.get(City, city_id)
    if city:
        city.delete()
        storage.save()
        return {}
    abort(404)


@app_views.route("/states/<state_id>/cities", methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """method to create new city under a given state"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    data = request.get_json(silent=True)
    if data is None:
        abort(400, "Not a JSON")
    if 'name' not in data:
        abort(400, "Missing name")

    data["state_id"] = state_id
    kwargs = {key: val for key,
              val in data.items() if key in ["name", "state_id"]}
    city = City(**kwargs)
    city.save()
    return city.to_dict(), 201


@app_views.route("/cities/<city_id>", methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """method to update city"""
    data = request.get_json(silent=True)
    if data is None:
        abort(400, "Not a JSON")
    city = storage.get(City, city_id)
    if city:
        for key, val in data.items():
            if key not in ['id', 'state_id', 'created_at', 'updated_at']:
                setattr(city, key, val)
        city.save()
        return city.to_dict(), 200
    abort(404)
