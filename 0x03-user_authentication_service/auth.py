#!/usr/bin/env python3
"""
Auth module
"""

from db import DB
from user import User


def _hash_password(password: str) -> str:
    """Returns a hashed password"""
    import bcrypt
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a new user
        """
        try:
            self._db.find_user_by(email=email)
        except Exception:
            return self._db.add_user(email, _hash_password(password))
        raise ValueError("User {} already exists".format(email))

    def valid_login(self, email: str, password: str) -> bool:
        """Validate user credentials
        """
        try:
            user = self._db.find_user_by(email=email)
            return user.hashed_password == _hash_password(password)
        except Exception:
            return False
