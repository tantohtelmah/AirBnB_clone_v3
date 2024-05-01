#!/usr/bin/python3
""" User API endpoints """

from flask import abort, request
from models import storage
from api.v1.views import app_views, format_response
from models.user import User


@app_views.route("/users/", methods=["GET"], strict_slashes=False)
def users():
    """ Retrieves all User objects """
    users = [user.to_dict() for user in storage.all(User).values()]
    return format_response(users)


@app_views.route("/users/<user_id>", methods=["GET"], strict_slashes=False)
def get_user(user_id):
    """ Retrieves a specific User objects"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return format_response(user.to_dict())


@app_views.route("/users/<user_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_user(user_id):
    """ Deletes a specific User objects"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return format_response({})


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def create_user():
    """ Creates a User object"""
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    if 'email' not in data:
        abort(400, description="Missing email")
    if 'password' not in data:
        abort(400, description="Missing password")
    instance = User(**data)
    instance.save()
    return format_response(instance.to_dict(), 201)


@app_views.route("/users/<user_id>", methods=["PUT"], strict_slashes=False)
def update_user(user_id):
    """ updates a User object"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")

    ignore = ['id', 'email', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore:
            setattr(user, key, value)
    storage.save()
    return format_response(user.to_dict())
