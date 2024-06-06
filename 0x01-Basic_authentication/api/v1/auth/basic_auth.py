#!/usr/bin/env python3
"""
Basic Authentication module for the API.
"""
from api.v1.auth.auth import Auth
import base64
from typing import Tuple, TypeVar
from models.user import User


class BasicAuth(Auth):
    """
    BasicAuth class to manage basic authentication for the API.
    """

    def extract_base64_authorization_header(self, auth_header: str) -> str:
        """
        Extract the Base64 part of the Authorization header for Basic
        Authentication.

        :param authorization_header: The Authorization header string.
        :return: The Base64 part of the Authorization header,
        or None if not found.
        """
        if auth_header is None or not isinstance(auth_header, str):
            return None

        if not auth_header.startswith("Basic "):
            return None

        return auth_header.split(" ")[1]

    def decode_base64_authorization_header(self, b64_auth_header: str) -> str:
        """
        Decode the Base64 Authorization header.

        :param base64_authorization_header: Base64 Authorization header string.
        :return: The decoded value as UTF-8 string, or None if not valid Base64
        """
        if b64_auth_header is None or not isinstance(b64_auth_header, str):
            return None

        try:
            decoded_bytes = base64.b64decode(b64_auth_header)
            decoded_str = decoded_bytes.decode('utf-8')
            return decoded_str
        except Exception:
            return None

    def extract_user_credentials(self,
                                 d_b64_auth_header: str) -> Tuple[str, str]:
        """
        Extract user email and password from the decoded Base64
        authorization header.

        :param decoded_base64_authorization_header: The decoded Base64
        Authorization header string.
        :return: A tuple containing user email and password, or (None, None)
        if not found.
        """
        if d_b64_auth_header is None or not isinstance(d_b64_auth_header, str):
            return None, None

        if ":" not in d_b64_auth_header:
            return None, None

        user_email, user_password = d_b64_auth_header.split(":", 1)
        return user_email, user_password

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """
        Return the User instance based on email and password.

        :param user_email: The user's email address.
        :param user_pwd: The user's password.
        :return: The User instance if authentication is successful,
        None otherwise.
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        try:
            users = User.search({"email": user_email})
            if not users:
                return None

            for user in users:
                if user.is_valid_password(user_pwd):
                    return user
        except Exception:
            return None

        return None

    def current_user(self, request=None) -> User:
        """
        Retrieve the User instance for a request.

        :param request: The Flask request object.
        :return: The User instance if authenticated, otherwise None.
        """
        if request is None:
            return None

        authorization_header = request.headers.get("Authorization")
        if not authorization_header:
            return None

        base64_header = self.extract_base64_authorization_header(
            authorization_header)
        if not base64_header:
            return None

        decoded_header = self.decode_base64_authorization_header(base64_header)
        if not decoded_header:
            return None

        user_email, user_pwd = self.extract_user_credentials(decoded_header)
        if user_email is None or user_pwd is None:
            return None

        return self.user_object_from_credentials(user_email, user_pwd)
