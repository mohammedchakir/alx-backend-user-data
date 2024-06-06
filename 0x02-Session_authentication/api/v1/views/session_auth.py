#!/usr/bin/env python3
"""
Session authentication views.
"""
from flask import jsonify, request, abort, make_response
from api.v1.views import app_views
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """ POST /api/v1/auth_session/login
    Return:
      - User object JSON represented
      - 400 if email or password is missing
      - 404 if no user found with email
      - 401 if the password is wrong
    """
    from api.v1.app import auth

    email = request.form.get('email')
    password = request.form.get('password')

    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400

    user = User.search({"email": email})
    if not user:
        return jsonify({"error": "no user found for this email"}), 404
    user = user[0]

    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    session_id = auth.create_session(user.id)
    user_dict = user.to_dict()
    response = make_response(jsonify(user_dict))
    session_name = getenv("SESSION_NAME")
    response.set_cookie(session_name, session_id)

    return response
