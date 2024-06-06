#!/usr/bin/env python3
"""
User model for the users table in the database.
"""

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """
    User model for representing users in the database.
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(250), nullable=False, unique=True)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)


if __name__ == "__main__":
    from sqlalchemy.orm import sessionmaker

    engine = create_engine('sqlite:///my_database.db', echo=True)
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    print(User.__tablename__)
    for column in User.__table__.columns:
        print("{}: {}".format(column, column.type))
