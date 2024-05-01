#!/usr/bin/python3

from os import abort
from flask import make_response, request
from flask import jsonify
from models.base_model import BaseModel
from models import storage
from api.v1.views import app_views, format_response
from api.v1.app import not_found
from models.city import City
from models.state import State


@app_views.route("/states/<state_id>/cities", methods=["GET"])
def city_obj(state_id):
    """ Retrieves all City objects of a State objects """
    state = storage.get(State, state_id)
    if not state:
        not_found(404)
    cities = []
    for city in state.cities:
        cities.append(city.to_dict())
    return format_response(cities)


@app_views.route("/cities/<city_id>/", methods=["GET"])
def get_city(city_id):
    """ Retrieves a specific city based on city id"""
    searched_city = storage.get(City, city_id)
    if not searched_city:
        not_found(404)
    return format_response(searched_city)


@app_views.route("/cities/<city_id>/", methods=["DELETE"])
def delete_city(city_id):
    """ Deletes a specific city based on the id provided"""
    searched_city = storage.get(City, city_id)
    if not searched_city:
        not_found(404)
    if not city_id:
        return jsonify({}), 200
    storage.delete(searched_city)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/states/<state_id>/cities", methods=["POST"])
def create_state(state_id):
    """ Creates a City object"""
    state = storage.get(State, state_id)
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")
    city_data = request.get_json()
    instance = City(**city_data)
    instance.state_id = state.id
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route("/states/<state_id>", methods=["PUT"])
def update_state(city_id):
    """ updates a city object"""
    city = storage.get(City, city_id)
    if not city_id:
        not_found()
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")
    ignore = ['id', 'state_id' 'created_at', 'updated_at']
    city_data = request.get_json()
    for key, value in city_data.items():
        if key not in ignore:
            setattr(city, key, value)
    storage.save()
    return make_response(jsonify(city.to_dict()), 200)
