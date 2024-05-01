#!/usr/bin/python3
""" City API endpoints """

from flask import request, abort
from models import storage
from api.v1.views import app_views, format_response
from models.place import Place


@app_views.route("/cities/<city_id>/places", methods=["GET"])
def city_obj(city_id):
    """ Retrieves all Places objects of a City objects """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = []
    for city in city.places:
        places.append(city.to_dict())
    return format_response(places)


@app_views.route("/places/<place_id>", methods=["GET"])
def get_city(place_id):
    """ Retrieves a specific city based on city id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return format_response(place.to_dict())


@app_views.route("/cities/<city_id>", methods=["DELETE"])
def delete_city(city_id):
    """ Deletes a specific city based on the id provided"""
    searched_city = storage.get(City, city_id)
    if not searched_city:
        abort(404)
    if not city_id:
        return format_response({})
    storage.delete(searched_city)
    storage.save()
    return format_response({})


@app_views.route("/cities/<city_id>/cities", methods=["POST"])
def create_city(city_id):
    """ Creates a City object"""
    city = storage.get(City, city_id)
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")
    city_data = request.get_json()
    instance = City(**city_data)
    instance.city_id = city.id
    instance.save()
    return format_response(instance.to_dict(), 201)


@app_views.route("/cities/<city_id>", methods=["PUT"])
def update_city(city_id):
    """ updates a city object"""
    city = storage.get(City, city_id)
    if not city_id:
        abort(404)
    city_data = request.get_json()
    if not city_data:
        abort(400, description="Not a JSON")
    if 'name' not in city_data:
        abort(400, description="Missing name")
    for key, value in city_data.items():
        setattr(city, key, value)
    storage.save()
    return format_response(city.to_dict(), 200)
