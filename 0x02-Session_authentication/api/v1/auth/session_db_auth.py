#!/usr/bin/env python3
"""
SessionDBAuth module
"""
from datetime import datetime, timedelta
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from models import storage


class SessionDBAuth(SessionExpAuth):
    """
    SessionDBAuth class for managing session IDs stored in a database
    """
    def create_session(self, user_id=None) -> str:
        """
        Create a session ID and store it in the database
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        new_session = UserSession(user_id=user_id, session_id=session_id)
        storage.new(new_session)
        storage.save()
        return session_id

    def user_id_for_session_id(self, session_id=None) -> str:
        """
        Return the User ID by requesting UserSession in the
        database based on session_id
        """
        if session_id is None:
            return None

        user_session = storage.get(UserSession, session_id)
        if user_session is None:
            return None

        if self.session_duration <= 0:
            return user_session.user_id

        if user_session.created_at + timedelta(
                    seconds=self.session_duration) < datetime.utcnow():
            return None

        return user_session.user_id

    def destroy_session(self, request=None) -> bool:
        """
        Destroy the UserSession based on the Session ID from the request cookie
        """
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        user_session = storage.get(UserSession, session_id)
        if user_session is None:
            return False

        storage.delete(user_session)
        storage.save()
        return True
