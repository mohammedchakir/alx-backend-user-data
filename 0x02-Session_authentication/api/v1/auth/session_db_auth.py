#!/usr/bin/env python3
"""
SessionDBAuth module
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from models import storage
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """
    SessionDBAuth class that stores session IDs in a database
    """
    def create_session(self, user_id=None):
        """
        Create a session and store it in the database
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        user_session = UserSession(user_id=user_id, session_id=session_id)
        storage.add(user_session)
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Retrieve a user ID from the database based on a session ID
        """
        if session_id is None:
            return None

        user_session = storage.filter_by(UserSession, session_id=session_id)
        if user_session is None:
            return None

        if self.session_duration <= 0:
            return user_session.user_id

        if user_session.created_at is None:
            return None

        if user_session.created_at + timedelta(
                    seconds=self.session_duration) < datetime.utcnow():
            return None

        return user_session.user_id

    def destroy_session(self, request=None):
        """
        Destroy a session by removing it from the database
        """
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        user_session = storage.filter_by(UserSession, session_id=session_id)
        if user_session is None:
            return False

        storage.delete(user_session)
        return True
