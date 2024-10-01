#!/usr/bin/env python3
"""Auth class to manage the API authentication"""

from api.v1.auth.session_auth import SessionAuth
from typing import TypeVar
from uuid import uuid4
from os import getenv
from models.user import User
import datetime

SESSION_DURATION = getenv('SESSION_DURATION')


class SessionExpAuth (SessionAuth):
    """Session Exp Auth class"""
    def __init__(self):
        """Constructor"""
        self.session_duration = 0
        if SESSION_DURATION:
            try:
                self.session_duration = int(SESSION_DURATION)
            except Exception:
                self.session_duration = 0
                pass

    def create_session(self, user_id: str = None) -> str:
        """Creates a Session ID for a user_id"""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        self.user_id_by_session_id[session_id] = {
            'user_id': user_id,
            'created_at': datetime.datetime.now()
        }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Returns a User ID based on a Session ID"""
        if session_id is None:
            return None
        session_dict = self.user_id_by_session_id.get(session_id)
        if session_dict is None:
            return None
        if self.session_duration <= 0:
            return session_dict.get('user_id')
        if 'created_at' not in session_dict:
            return None
        if (datetime.datetime.now() -
           session_dict.get('created_at')).seconds > self.session_duration:
            return None
        return session_dict.get('user_id')
