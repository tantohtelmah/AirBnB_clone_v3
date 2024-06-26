#!/usr/bin/python3
""" User API endpoints """

from flask import abort, request
from api.v1.views import app_views, format_response
from models import storage
from models.user import User


@app_views.route("/users", methods=["GET", "POST"], strict_slashes=False)
def users_routes():
    """
    GET: Retrieves the list of all User objects
    POST: Creates a User object
    """
    if request.method == "GET":
        users = [user.to_dict() for user in storage.all(User).values()]
        return format_response(users)

    if request.method == "POST":
        data = request.get_json(silent=True)
        if data is None:
            abort(400, "Not a JSON")

        for key in ["email", "password"]:
            if data.get(key) is None:
                abort(400, "Missing {}\n".format(key))

        user = User(**data)
        user.save()
        return user.to_dict(), 201


@app_views.route("/users/<user_id>", methods=["GET", "PUT", "DELETE"],
                 strict_slashes=False)
def user_id_routes(user_id):
    """
    GET: Retrieves the User where id == user_id
    PUT: Updates the User that has id == user_id
    DELETE: Deletes the User that has id == user_id
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    if request.method == "GET":
        return user.to_dict()
    elif request.method == "PUT":
        data = request.get_json(silent=True)
        if data is None:
            abort(400, "Not a JSON")

        for key, val in data.items():
            if key not in ["id", "email", "created_at", "updated_at"]:
                setattr(user, key, val)
        user.save()
        return user.to_dict(), 200

    elif request.method == "DELETE":
        user.delete()
        storage.save()
        return {}
