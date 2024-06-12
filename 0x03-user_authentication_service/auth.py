#!/usr/bin/env python3

"""
Auth module
"""

import bcrypt
from db import DB
from user import User
from typing import Union
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """Hashes a password using bcrypt.
    Args:
        password (str): The password to hash.
    Returns:
        bytes: The salted hash of the password.
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self) -> None:
        """Initializes a new Auth instance."""
        self._db = DB()

    def register_user(self, email: str, password: str) -> Union[None, User]:
        """Registers a new user.
        Args:
            email (str): The email of the user.
            password (str): The password of the user.
        Returns:
            User: The created user object.
        Raises:
            ValueError: If a user with the email already exists.
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            user = self._db.add_user(email, hashed_password)
            return user
