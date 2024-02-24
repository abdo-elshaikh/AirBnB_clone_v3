#!/usr/bin/python3
"""Module containing the Place view for the API"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from models.place import Place
from models.user import User

@app_views.route('/cities/<city_id>/places', methods=['GET'])
def get_places(city_id):
    """Retrieve all Place objects."""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = city.places
    return jsonify([place.to_dict() for place in places])


@app_views.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    """Retrieve a specific Place object."""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """Delete a Place object."""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    """Create a new Place object."""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    if 'user_id' not in data:
        abort(400, "Missing user_id")
    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)
    if 'name' not in data:
        abort(400, "Missing name")
    place = Place(**data)
    place.city_id = city_id
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """Update a Place object."""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    ignore = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200

@app_views.route('/places_search', methods=['POST'])
def places_search():
    """Search for places based on JSON data."""
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    if not data.get('states') and not data.get('cities'):
        abort(400, "Missing states")
    states = data.get('states', [])
    cities = data.get('cities', [])
    amenities = data.get('amenities', [])
    if not states and not cities:
        places = storage.all(Place).values()
        return jsonify([place.to_dict() for place in places])
    places = []
    for state in states:
        for city in cities:
            for place in storage.all(Place).values():
                if place.city_id == city and place.state_id == state:
                    places.append(place.to_dict())
    for amenity in amenities:
        for place in storage.all(Place).values():
            if place.amenity_ids and amenity in place.amenity_ids:
                if place not in places:
                    places.append(place.to_dict())
    return jsonify(places)
