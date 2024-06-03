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
        if path is None or not excluded_paths:
            return True

        path = path.rstrip('/')

        for excluded_path in excluded_paths:
            if excluded_path.endswith('*'):
                if path.startswith(excluded_path[:-1]):
                    return False
            elif path == excluded_path.rstrip('/'):
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Get the Authorization header from the request.

        :param request: The Flask request object.
        :return: None for now, as this method will be implemented later.
        """
        if request is None:
            return None

        return request.headers.get("Authorization", None)

    def current_user(self, request=None):
        """
        Get the current user based on the request.

        :param request: The Flask request object.
        :return: None for now, as this method will be implemented later.
        """
        # For now, return None
        return None
