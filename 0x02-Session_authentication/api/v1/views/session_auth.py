#!/usr/bin/env python3
"""
This module provides a Flask view to handle session authentication.
"""

from flask import Flask, jsonify, request, abort
from models.user import User
import os

app = Flask(__name__)


@app.route('/api/v1/auth_session/login', methods=['POST'],
           strict_slashes=False)
def login():
    """
    Handles POST requests for session-based login authentication.

    Returns:
        JSON response with user data or error messages.
    """

    email = request.form.get('email')
    password = request.form.get('password')

    if not email:
        return jsonify({"error": "email missing"}), 400

    if not password:
        return jsonify({"error": "password missing"}), 400

    users = User.search({"email": email})
    if not users or len(users) == 0:
        return jsonify({"error": "no user found for this email"}), 404

    user = users[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    session_id = auth.create_session(user.id)
    user_json = user.to_json()

    response = jsonify(user_json)
    session_name = os.getenv('SESSION_NAME')
    response.set_cookie(session_name, session_id)

    return response
