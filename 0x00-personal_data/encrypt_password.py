#!/usr/bin/env python3
"""
This module provides a function to hash a password using bcrypt.
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hashes a password using bcrypt and returns the salted,
    hashed password as a byte string.

    :param password: The password to hash.
    :return: The salted, hashed password as a byte string.
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed


def is_valid(hashed: bytes, password: str) -> bool:
    """
    Validate that the provided password matches the hashed password.

    :param hashed_password: The hashed password to check against.
    :param password: The plain text password to validate.
    :return: True if the password matches the hashed password, False otherwise.
    """
    return bcrypt.checkpw(password.encode(), hashed)
