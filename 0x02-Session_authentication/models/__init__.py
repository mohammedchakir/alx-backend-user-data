#!/usr/bin/env python3
"""
Initialization of the models package
"""
from models.user_session import Base, UserSession
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class Storage:
    """
    Storage class that handles interaction with the database
    """
    def __init__(self):
        self.__engine = create_engine("sqlite:///sessions.db", echo=True)
        Base.metadata.create_all(self.__engine)
        self.__session = sessionmaker(bind=self.__engine)()

    def add(self, obj):
        """
        Add an object to the current database session
        """
        self.__session.add(obj)
        self.__session.commit()

    def delete(self, obj=None):
        """
        Delete an object from the current database session
        """
        if obj:
            self.__session.delete(obj)
            self.__session.commit()

    def all(self, cls):
        """
        Query all objects of a given class from the database
        """
        return self.__session.query(cls).all()

    def get(self, cls, id):
        """
        Query an object by its ID from the database
        """
        return self.__session.query(cls).filter_by(id=id).first()

    def filter_by(self, cls, **kwargs):
        """
        Query an object by filtering using keyword arguments
        """
        return self.__session.query(cls).filter_by(**kwargs).first()
