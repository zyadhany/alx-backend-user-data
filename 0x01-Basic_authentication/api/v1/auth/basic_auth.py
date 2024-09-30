#!/usr/bin/env python3
"""Auth class to manage the API authentication"""

from api.v1.auth.auth import Auth
import base64
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """BasicAuth class to manage the API authentication"""

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Extract base64 authorization header"""
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """Decode base64 authorization header"""
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            return base64.b64decode(
                base64_authorization_header.encode('utf-8')).decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """Extract user credentials"""
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        return tuple(decoded_base64_authorization_header.split(':', 1))

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """User object from credentials"""
        if user_email is None or user_pwd is None:
            return None
        if not isinstance(user_email, str) or not isinstance(user_pwd, str):
            return None
        try:
            return User(email=user_email, pwd=user_pwd)
        except Exception:
            return None
