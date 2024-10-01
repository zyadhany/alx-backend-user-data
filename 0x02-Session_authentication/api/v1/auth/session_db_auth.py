#!/usr/bin/env python3
"""Auth class to manage the API authentication"""

from api.v1.auth.session_exp_auth import SessionExpAuth
from typing import TypeVar
from uuid import uuid4
from os import getenv
from models.user import User
from models.user_session import UserSession
import datetime

SESSION_DURATION = getenv('SESSION_DURATION')


class SessionDBAuth (SessionExpAuth):
    """ Session DB Auth class """
    def create_session(self, user_id=None):
        """ Creates a Session ID for a user_id """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ Returns a User ID based on a Session ID """
        user_id = UserSession.search({"session_id": session_id})
        if user_id:
            return user_id
        return None

    def destroy_session(self, request=None):
        """ Deletes the user session / logout """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        user_sessions = UserSession.search({'session_id': session_id})
        if not user_sessions:
            return False
        user_sessions[0].remove()
        return True
