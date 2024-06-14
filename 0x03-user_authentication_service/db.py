#!/usr/bin/env python3
"""
DB module
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from user import Base, User


class DB:
    """
    DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance"""
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object"""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Adds a new user to the database.
        Args:
            email (str): The email of the user.
            hashed_password (str): The hashed password of the user.
        Returns:
            User: The created user object.
        """
        new_user = User(email=email, hashed_password=hashed_password)
        # add new user and commit to database
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """Finds a user by arbitrary keyword arguments.
        Args:
            kwargs: Arbitrary keyword arguments to filter users.
        Returns:
            User: The first user object found.
        Raises:
            NoResultFound: If no user is found.
            InvalidRequestError: If query arguments are invalid.
        """
        if not kwargs:
            raise InvalidRequestError

        user = self._session.query(User).filter_by(**kwargs).first()
        if not user:
            raise NoResultFound
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """Updates a user's attributes.
        Args:
            user_id (int): The ID of the user to update.
            kwargs: Arbitrary keyword arguments of attributes to update.
        Returns:
            None
        Raises:
            ValueError: If an argument does not correspond to a user attribute.
        """
        user = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            if not hasattr(user, key):
                raise ValueError
            setattr(user, key, value)

        self._session.commit()
        return None
