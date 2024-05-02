#!/usr/bin/python3
"""module to handle amenity API request"""
from models.amenity import Amenity
from flask import request, jsonify, make_response, abort
from api.v1.views import app_views
from models import storage


@app_views.route("/amenities", methods=['GET'], strict_slashes=False)
def get_amenities():
    """method to get all amenities"""
    amenities = [obj.to_dict() for obj in storage.all(Amenity).values()]
    return jsonify(amenities)


@app_views.route("/amenities/<amenity_id>",
                 methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    """method to get amenity by id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        return amenity.to_dict()
    abort(404)


@app_views.route("/amenities/<amenity_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """method to delete amenity by id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        amenity.delete()
        storage.save()
        return {}
    abort(404)


@app_views.route("/amenities", methods=['POST'],
                 strict_slashes=False)
def create_amenity():
    """method to create a new amenity"""
    data = request.get_json(silent=True)
    if data is None:
        abort(400, "Not a JSON")
    if 'name' not in data.keys():
        abort(400, "Missing name")
    new_amenity = Amenity(**data)
    new_amenity.save()
    return new_amenity.to_dict(), 201


@app_views.route("/amenities/<amenity_id>", methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """method to update amenity"""
    data = request.get_json(silent=True)
    if data is None:
        abort(400, "Not a JSON")
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        for key, val in data.items():
            if key not in ["id", "created_at", "updated_at"]:
                setattr(amenity, key, val)
        amenity.save()
        return amenity.to_dict()
    abort(404)
