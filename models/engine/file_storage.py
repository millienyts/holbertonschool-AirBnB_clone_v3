#!/usr/bin/python3
"""
FileStorage class for serializing instances to a JSON file & deserializing back to instances.
"""

import json
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

# Dictionary to map class names to their corresponding classes
classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class FileStorage:
    """A class for managing serialization and deserialization of instances."""

    __file_path = "file.json"  # Path to the JSON file
    __objects = {}  # Dictionary to store all objects by <class name>.id

    def all(self, cls=None):
        """
        Returns a dictionary of all objects, optionally filtered by class.
        """
        if cls is not None:
            return {key: value for key, value in self.__objects.items()
                    if isinstance(value, cls)}
        return self.__objects

    def get(self, cls, id):
    """Retrieve one object"""
    key = "{}.{}".format(cls.__name__, id)
    return self.__objects.get(key, None)

    def count(self, cls=None):
    """Count number of objects in storage"""
    if cls:
        count = 0
        for key in self.__objects:
            if key.split('.')[0] == cls.__name__:
                count += 1
        return count
    return len(self.__objects)

    def new(self, obj):
        """Adds the object to the storage."""
        if obj is not None:
            key = obj.__class__.__name__ + "." + obj.id
            self.__objects[key] = obj

    def save(self):
        """Serializes __objects to the JSON file."""
        json_objects = {key: obj.to_dict() for key, obj in self.__objects.items()}
        with open(self.__file_path, 'w') as f:
            json.dump(json_objects, f)

    def reload(self):
        """Deserializes the JSON file to __objects."""
        try:
            with open(self.__file_path, 'r') as f:
                json_data = json.load(f)
            for key, data in json_data.items():
                cls_name = data["__class__"]
                self.__objects[key] = classes[cls_name](**data)
        except Exception:
            pass

    def delete(self, obj=None):
        """Deletes an object from storage if it exists."""
        if obj is not None:
            key = obj.__class__.__name__ + '.' + obj.id
            self.__objects.pop(key, None)

    def close(self):
        """Reloads the objects from JSON file."""
        self.reload()
