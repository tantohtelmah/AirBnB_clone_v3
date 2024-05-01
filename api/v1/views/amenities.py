#!/usr/bin/python3
""" State API endpoints """

from flask import abort, request
from models import storage
from api.v1.views import app_views, format_response
from models.amenity import Amenity


@app_views.route("/amenities/", methods=["GET"], strict_slashes=False)
def get_amenities():
    """ Retrieves all Amenity objects """
    amenities = [obj.to_dict() for obj in storage.all(Amenity).values()]
    return format_response(amenities)


@app_views.route("/amenities/<amenity_id>", methods=["GET"],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """ Retrieves a specific Amenity objects"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return format_response(amenity_id.to_dict())


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """ Deletes a specific Amenity objects"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return format_response({})


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def create_amenity():
    """ Creates a Amenity object"""
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    if 'name' not in data:
        abort(400, description="Missing name")
    instance = Amenity(**data)
    instance.save()
    return format_response(instance.to_dict(), 201)


@app_views.route("/amenities/<amenity_id>", methods=["PUT"],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """ updates a State object"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    if 'name' not in data:
        abort(400, description="Missing name")
    for key, value in data.items():
        setattr(amenity, key, value)
    storage.save()
    return format_response(amenity.to_dict())
