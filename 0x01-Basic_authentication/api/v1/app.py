#!/usr/bin/env python3
"""
Route module for the API.
"""
from os import getenv
from api.v1.views import app_views
from api.v1.auth.auth import Auth
from flask import Flask, jsonify, request, abort
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

auth = None
auth_type = getenv("AUTH_TYPE")
if auth_type:
    if auth_type == "auth":
        from api.v1.auth.auth import Auth
        auth = Auth()


@app.before_request
def before_request():
    if auth is None:
        return

    excluded_paths = ['/api/v1/status/', '/api/v1/unauthorized/',
                      '/api/v1/forbidden/']
    if request.path in excluded_paths:
        return

    if auth.require_auth(request.path, excluded_paths):
        auth_header = auth.authorization_header(request)
        if auth_header is None:
            abort(401)
        if auth.current_user(request) is None:
            abort(403)


@app.errorhandler(404)
def not_found(error) -> str:
    """
    Not found handler.

    :param error: The error object.
    :return: JSON response with error message and 404 status code.
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """
    Unauthorized handler.

    :param error: The error object.
    :return: JSON response with error message and 401 status code.
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """
    Forbidden handler.

    :param error: The error object.
    :return: JSON response with error message and 403 status code.
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
