#!/usr/bin/python3
"""DBStorage class module."""

from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models.base_model import Base
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

entity_classes = {
    "Amenity": Amenity,
    "City": City,
    "Place": Place,
    "Review": Review,
    "State": State,
    "User": User
}


class DBStorage:
    """MySQL database interaction."""

    __engine = None
    __session = None

    def __init__(self):
        """Initialize DBStorage."""
        user = getenv('HBNB_MYSQL_USER')
        pwd = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST')
        db = getenv('HBNB_MYSQL_DB')
        env = getenv('HBNB_ENV')

        self.__engine = create_engine(
            f'mysql+mysqldb://{user}:{pwd}@{host}/{db}')
        if env == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query current session."""
        queried_data = {}
        for entity in entity_classes:
            if cls is None or cls in {entity_classes[entity], entity}:
                for obj in self.__session.query(entity_classes[entity]).all():
                    key = f'{type(obj).__name__}.{obj.id}'
                    queried_data[key] = obj
        return queried_data

    def new(self, obj):
        """Add object to session."""
        if obj:
            self.__session.add(obj)

    def save(self):

        self.__session.commit()

    def delete(self, obj=None):
        """Delete object from session."""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Reload session data."""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
            bind=self.__engine, expire_on_commit=False)
        ScopedSession = scoped_session(session_factory)
        self.__session = ScopedSession()

    def close(self):
        """Close session."""
        self.__session.remove()
