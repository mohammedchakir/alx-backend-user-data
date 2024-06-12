#!/usr/bin/env python3

"""
Auth module
"""

import bcrypt
from db import DB
from user import User
from typing import Union
from uuid import uuid4
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> str:
    """Hashes a password using bcrypt.
    Args:
        password (str): The password to hash.
    Returns:
        bytes: The salted hash of the password.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """
    Generates a new UUID.
    """
    id = uuid4()
    return str(id)


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
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
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))

        else:
            raise ValueError('User {} already exists'.format(email))