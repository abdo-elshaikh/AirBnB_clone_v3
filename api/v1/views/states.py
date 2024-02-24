#!/usr/bin/python3
"""Module containing the State view for the API"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'])
def get_states():
    """Retrieve all State objects."""
    states = storage.all(State)
    return jsonify([state.to_dict() for state in states.values()])


@app_views.route('/states/<state_id>', methods=['GET'])
def get_state(state_id):
    """Retrieve a specific State object."""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """Delete a State object."""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    try:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    except Exception:
        abort(404)


@app_views.route('/states', methods=['POST'])
def create_state():
    """Create a new State object."""
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    if 'name' not in data:
        abort(400, "Missing name")
    try:
        state = State(**data)
        state.save()
        return jsonify(state.to_dict()), 201
    except Exception:
        abort(400, "Not a JSON")

@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """Update a State object."""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    try:
        state.save()
        return jsonify(state.to_dict()), 200
    except Exception:
        abort(400, "Not a JSON")
