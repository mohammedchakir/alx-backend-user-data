#!/usr/bin/env python3
"""
This module contains the routes for session authentication.
"""

from flask import request, jsonify, abort
from models.user import User
import os
from api.v1.views import app_views


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """ POST /api/v1/auth_session/login
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if email is None or email == "":
        return jsonify({"error": "email missing"}), 400

    if password is None or password == "":
        return jsonify({"error": "password missing"}), 400

    user = User.search({'email': email})
    if not user:
        return jsonify({"error": "no user found for this email"}), 404

    user = user[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    session_id = auth.create_session(user.id)
    response = jsonify(user.to_json())
    session_name = os.getenv('SESSION_NAME')
    response.set_cookie(session_name, session_id)

    return response


@app_views.route('/users/me', methods=['GET'], strict_slashes=False)
def get_user():
    """ GET /api/v1/users/me
    """
    from api.v1.app import auth
    user_id = auth.get_user_id_from_request(request)
    if user_id is None:
        abort(404)
    
    user = User.get(user_id)
    if user is None:
        abort(404)

    return jsonify(user.to_json()), 200


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def auth_session_logout():
    """
    Handle the logout route for session authentication.

    Returns:
        A JSON response with an empty dictionary if logout is successful.
        Otherwise, it returns a 404 error.
    """
    from api.v1.app import auth

    if auth.destroy_session(request):
        return jsonify({}), 200
    abort(404)
