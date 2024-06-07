#!/usr/bin/env python3
"""
Authentication module for the API.
"""
import os
from flask import request
import base64
from models import User


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
        if request is None:
            return None

        auth_header = self.authorization_header(request)
        if auth_header is None:
            print("No Authorization header found")
            return None

        if not auth_header.startswith("Basic "):
            print("Authorization header does not start with 'Basic '")
            return None

        encoded_credentials = auth_header.split(' ')[1]
        try:
            decoded_credentials = base64.b64decode(
                    encoded_credentials).decode('utf-8')
            email, password = decoded_credentials.split(':', 1)
        except (ValueError, base64.binascii.Error):
            print("Failed to decode credentials")
            return None

        user = User.find_by_email(email)
        if user is None:
            print(f"No user found with email: {email}")
            return None
        if not user.verify_password(password):
            print("Password verification failed")
            return None

        return user

    def session_cookie(self, request=None):
        """
        Returns the value of the session cookie
        """
        if request is None:
            return None
        session_name = os.getenv('SESSION_NAME')
        if session_name is None:
            return None
        return request.cookies.get(session_name)
