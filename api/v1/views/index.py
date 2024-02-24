#!/usr/bin/python3
"""Module containing the index route for the API."""
from flask import jsonify
from api.v1.views import app_views


@app_views.route("/status")
def status():
    """Return a JSON object with the status of the API."""
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def stats():
    """Return a JSON object with the number of each object by type."""
    from models.user import User
    from models.state import State
    from models.city import City
    from models.amenity import Amenity
    from models.place import Place
    from models.review import Review
    from models import storage

    return jsonify({
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User)
    })
