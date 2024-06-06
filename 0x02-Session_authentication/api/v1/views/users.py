#!/usr/bin/env python3
"""
User views module
"""
from flask import jsonify, request, abort
from models.user import User
from api.v1.views import app_views


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """
    Retrieve a User object
    """
    if user_id == 'me':
        if request.current_user is None:
            abort(404)
        return jsonify(request.current_user.to_dict())

    user = User.get(user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """
    Retrieve all User objects
    """
    users = User.all()
    return jsonify([user.to_dict() for user in users])


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """
    Create a new User object
    """
    from flask import request
    if not request.json:
        abort(400, "Missing email")
    if 'email' not in request.json:
        abort(400, "Missing email")
    if 'password' not in request.json:
        abort(400, "Missing password")

    user = User(**request.json)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """
    Update a User object
    """
    from flask import request
    user = User.get(user_id)
    if user is None:
        abort(404)

    for key, value in request.json.items():
        setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """
    Delete a User object
    """
    user = User.get(user_id)
    if user is None:
        abort(404)
    user.delete()
    return jsonify({})
