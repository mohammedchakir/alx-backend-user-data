#!/usr/bin/env python3
"""Auth module"""

import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4

from typing import Union


def _hash_password(password: str) -> str:
    """Hashes a password using bcrypt.
    Args:
        password (str): The password to hash.
    Returns:
        bytes: The salted hash of the password.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """Generates a new UUID.
    Returns:
        str: The string representation of the UUID.
    """
    id = uuid4()
    return str(id)


class Auth:
    """
    Auth class to interact with the authentication database.
    """

    def __init__(self):
        """Initializes a new Auth instance."""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a new user with email and password.
        Args:
            email (str): The email of the user.
            password (str): The password of the user.
        Returns:
            User: The newly created user object.
        Raises:
            ValueError: If a user with the provided email already exists.
        """
        try:
            # Check if user with given email already exists
            self._db.find_user_by(email=email)
            # If no exception, user exists
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            # If no user found, proceed to create a new user
            hashed_password = _hash_password(password)
            new_user = self._db.add_user(email, hashed_password)
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """Validates login credentials.
        Args:
            email (str): The email of the user.
            password (str): The password of the user.
        Returns:
            bool: True if the credentials are valid, False otherwise.
        """
        try:
            # find the user with the given email
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        # check validity of password
        return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password)

    def create_session(self, email: str) -> str:
        """Creates a session for the user.
        Args:
            email (str): The email of the user.
        Returns:
            Union[str, None]: The session ID as a string,
            or None if the user is not found.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        else:
            user.session_id = _generate_uuid()
            return user.session_id

    def get_user_from_session_id(self, session_id: str) -> User:
        """Retrieve user based on session ID.
        Args:
            session_id (str): The session ID to retrieve the user.
        Returns:
            User: The corresponding user object if found, else None.
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        else:
            return user

    def destroy_session(self, user_id: str) -> None:
        """function for destroy session"""
        try:
            user = self._db.find_user_by(id=user_id)
        except NoResultFound:
            return None
        else:
            user.session_id = None
            return None

    def get_reset_password_token(self, email: str) -> str:
        """Get the reset password token for a user.
        Args:
            email (str): The email of the user.

        Returns:
            str: The reset password token generated for the user.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError
        else:
            user.reset_token = _generate_uuid()
            return user.reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """Updates the password for a user.
        Args:
            reset_token (str): The reset token associated with the user.
            password (str): The new password to be set.
        Raises:
            ValueError: If no user is found with the given reset token.
        Returns:
            None
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError
        else:
            user.hashed_password = _hash_password(password)
            user.reset_token = None
            return None
