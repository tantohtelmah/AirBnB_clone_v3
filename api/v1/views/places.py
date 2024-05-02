#!/usr/bin/python3
"""RESTful API view to handle actions for 'Place' objects"""

from flask import abort, request, jsonify

from api.v1.views import app_views, format_response
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.state import State
from models.user import User


@app_views.route("/cities/<city_id>/places", methods=["GET", "POST"],
                 strict_slashes=False)
def city_places_routes(city_id):
    """
    GET: Retrieves the list of all Place objects in the city where
         id == city_id
    POST: Creates a Place object in the city where id == city_id
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    if request.method == "GET":
        places = [place.to_dict() for place in city.places]
        return format_response(places)

    elif request.method == "POST":
        data = request.get_json(silent=True)
        if data is None:
            abort(400, "Not a JSON")

        user_id = data.get("user_id")
        if user_id is None:
            abort(400, "Missing user_id")

        if storage.get(User, user_id) is None:
            abort(404)

        if data.get("name") is None:
            abort(400, "Missing name")

        data["city_id"] = city_id
        place = Place(**data)
        place.save()
        return place.to_dict(), 201


@app_views.route("/places/<place_id>", methods=["GET", "PUT", "DELETE"],
                 strict_slashes=False)
def place_id_routes(place_id):
    """
    GET: Retrieves the Place where id == place_id
    PUT: Updates the Place that has id == place_id
    DELETE: Deletes the Place that has id == place_id
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if request.method == "GET":
        return place.to_dict()

    elif request.method == "PUT":
        data = request.get_json(silent=True)
        if data is None:
            abort(400, "Not a JSON")

        for key, val in data.items():
            if key not in ["id", "user_id", "city_id", "created_at",
                           "updated_at"]:
                setattr(place, key, val)
        place.save()
        return place.to_dict()

    elif request.method == "DELETE":
        place.delete()
        storage.save()
        return {}


@app_views.route("/places_search", methods=["POST"], strict_slashes=False)
def places_search():
    """
    POST: Retrieves all 'Place' objects depending on JSON
    """
    data = request.get_json(silent=True)
    if data is None:
        abort(400, "Not a JSON")

    states_ids = data.get("states")
    cities_ids = []
    places = []

    if states_ids:
        for state_id in states_ids:
            state = storage.get(State, state_id)
            if state:
                cities_ids.extend([city.id for city in state.cities])

    cities_param = data.get("cities")
    if cities_param:
        cities_ids.extend([city_id for city_id in cities_param
                          if city_id not in cities_ids])

    if len(cities_ids) < 1:
        places = storage.all(Place).values()
    else:
        for city_id in cities_ids:
            city = storage.get(City, city_id)
            if city:
                places.extend(city.places)

    amenities_ids = data.get("amenities")
    if not amenities_ids or len(amenities_ids) < 1:
        results = []
        for place in places:
            result = place.to_dict()
            result["amenities"] = [amenity.to_dict() for amenity
                                   in place.amenities]
            results.append(result)
        return jsonify(results)

    places_filtered = []
    for place in places:
        place_amenities_ids = [amenity.id for amenity in place.amenities]
        if all(amenity_id in place_amenities_ids for amenity_id
               in amenities_ids):
            place = place.to_dict()
            place["amenities"] = [amenity.to_dict() for amenity
                                  in place["amenities"]]
            places_filtered.append(place)
    return jsonify(places_filtered)
