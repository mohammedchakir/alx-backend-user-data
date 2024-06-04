#!/usr/bin/env python3
"""
This module contains the routes for session authentication.
"""

from flask import Blueprint, request, jsonify
from models.user import User
from os import getenv
from api.v1.views import app_views


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def auth_session_login():
    """
    Handle the login route for session authentication.

    Returns:
        A JSON response containing the user information if login is successful.
        Otherwise, it returns an error message with appropriate status code.
    """
    from api.v1.app import auth
    email = request.form.get('email')
    password = request.form.get('password')

    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400

    user = User.search({"email": email})
    if not user or len(user) == 0:
        return jsonify({"error": "no user found for this email"}), 404

    user = user[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    session_id = auth.create_session(user.id)
    user_dict = user.to_json()
    response = jsonify(user_dict)
    cookie_name = getenv("SESSION_NAME")
    response.set_cookie(cookie_name, session_id)

    return response
