#!/usr/bin/python3
"""
    This module defines the FileStorage class for
    serializing and deserializing instances to JSON files
"""

import json
from models.base_model import BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

classes = {
    "Amenity": Amenity,
    "BaseModel": BaseModel,
    "City": City,
    "Place": Place,
    "Review": Review,
    "State": State,
    "User": User
}


class FileStorage:
    """Serializes instances to a JSON file and
    deserializes JSON file to instances"""

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Returns the dictionary __objects"""
        return self.__objects

    def new(self, obj):
        """Sets in __objects the obj with key <obj class name>.id"""
        key = "{}.{}".format(type(obj).__name__, obj.id)
        self.__objects[key] = obj

    def save(self):
        """Serializes __objects to the JSON file (path: __file_path)"""
        with open(self.__file_path, mode="w", encoding="utf-8") as f:
            json.dump({k: v.to_dict() for k, v in self.__objects.items()}, f)

    def reload(self):
        """Deserializes the JSON file to __objects
        (only if the JSON file exists;
        otherwise, do nothing)."""
        try:
            with open(self.__file_path, mode="r", encoding="utf-8") as f:
                self.__objects = {
                    k: BaseModel(**v) for k, v in json.load(f).items()
                    }
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """Delete object"""
        if obj:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            if key in self.__objects:
                del self.__objects[key]

    def get(self, cls, id):
        """Retrieve one object"""
        if cls and id:
            key = "{}.{}".format(cls.__name__, id)
            return self.__objects.get(key)

    def count(self, cls=None):
        """Count number of objects in storage"""
        if cls is None:
            return len(self.__objects)

        else:
            if cls in classes.values():
                total_objs = 0
                keys = self.__objects.keys()
                for key in keys:
                    if str(cls.__name__) in key:
                        total_objs += 1
                return total_objs

    def close(self):
        """Call reload() method for deserializing the JSON file to objects"""
        self.reload()
