#!/usr/bin/env python3
"""
UserSession model module
"""
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class UserSession(Base):
    """
    UserSession class for storing session information in the database
    """
    __tablename__ = 'user_sessions'

    id = Column(String(60), primary_key=True, nullable=False)
    user_id = Column(String(60), nullable=False)
    session_id = Column(String(60), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __init__(self, user_id: str, session_id: str):
        """
        Initialize a UserSession instance
        """
        self.user_id = user_id
        self.session_id = session_id
        self.created_at = datetime.utcnow()
