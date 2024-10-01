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
        if session_id is None:
            return None

        user_sessions = None
        try:
            user_session = UserSession.search({'session_id': session_id})
        except Exception:
            return None
        
        user_sessions = user_session[0]
        if not user_sessions or len(user_sessions) == 0:
            return None
        user_session = user_sessions[0]
        if self.session_duration <= 0:
            return user_session.user_id
        if user_session.created_at + \
           datetime.timedelta(seconds=self.session_duration) \
           < datetime.datetime.now():
            return None
        return user_session.user_id

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
