#!/usr/bin/env python3

"""
Flask app module
"""

from flask import Flask, jsonify, request, abort, make_response
from auth import Auth

AUTH = Auth()

app = Flask(__name__)


@app.route("/", methods=["GET"])
def welcome():
    """Route that returns a welcome message."""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def users():
    """Endpoint to register a new user."""
    email = request.form.get("email")
    password = request.form.get("password")

    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except Exception:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"])
def login():
    """Route to log in a user and create a new session."""
    email = request.form.get("email")
    password = request.form.get("password")

    if not AUTH.valid_login(email, password):
        abort(401)

    session_id = AUTH.create_session(email)
    response = make_response(jsonify({"email": email, "message": "logged in"}))
    response.set_cookie("session_id", session_id)
    return response


if __name__ == "__main__":
    """fumction name=main"""
    app.run(host="0.0.0.0", port="5000")
