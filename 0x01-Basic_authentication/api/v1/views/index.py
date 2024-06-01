#!/usr/bin/env python3
"""
Module of Index views.
"""
from flask import jsonify, abort
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status() -> str:
    """
    GET /api/v1/status

    Return the status of the API.

    :return: JSON response with API status.
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats/', methods=['GET'], strict_slashes=False)
def stats() -> str:
    """
    GET /api/v1/stats

    Return the number of each object.

    :return: JSON response with object statistics.
    """
    from models.user import User
    stats = {}
    stats['users'] = User.count()
    return jsonify(stats)


@app_views.route('/unauthorized', methods=['GET'], strict_slashes=False)
def unauthorized() -> str:
    """
    GET /api/v1/unauthorized

    Raise a 401 error to test the unauthorized error handler.

    :return: None
    """
    abort(401)
