#!/usr/bin/env python3
"""
Authentication module for the API.
"""
from flask import request


class Auth:
    """
    Auth class to manage API authentication.
    """

    def require_auth(self, path: str, excluded_paths: list) -> bool:
        """
        Check if authentication is required for a given path.

        :param path: The path to check.
        :param excluded_paths: List of paths that don't require authentication.
        :return: True if authentication is required, False otherwise.
        """
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True

        # Make paths slash tolerant
        path = path.rstrip("/") + "/"

        return path not in excluded_paths

    def authorization_header(self, request=None) -> str:
        """
        Get the Authorization header from the request.

        :param request: The Flask request object.
        :return: None for now, as this method will be implemented later.
        """
        if request is None or 'Authorization' not in request.headers:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None):
        """
        Get the current user based on the request.

        :param request: The Flask request object.
        :return: None for now, as this method will be implemented later.
        """
        # For now, return None
        return None


if __name__ == "__main__":
    a = Auth()
    print(a.require_auth("/api/v1/status/", ["/api/v1/status/"]))
    print(a.authorization_header())
    print(a.current_user())
