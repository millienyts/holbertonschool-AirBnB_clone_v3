#!/usr/bin/python3
""" FileStorage class module. """

import json
from models.base_model import BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

model_classes = {
    "Amenity": Amenity,
    "BaseModel": BaseModel,
    "City": City,
    "Place": Place,
    "Review": Review,
    "State": State,
    "User": User
}


class FileStorage:
    """ Serializes and deserializes JSON. """

    __file_path = 'file.json'  # JSON file path
    __objects = {}  # Store all objects

    def all(self, cls=None):
        """ Dictionary of all objects. """
        if cls:
            return {k: v for k, v in self.__objects.items()
                    if isinstance(v, cls) or k.split('.')[0] == cls}
        return self.__objects

    def new(self, obj):
        """ Add obj to storage. """
        if obj:
            self.__objects[f'{type(obj).__name__}.{obj.id}'] = obj

    def save(self):
        """ Serialize __objects to JSON. """
        with open(self.__file_path, 'w') as f:
            json.dump({k: v.to_dict() for k, v in self.__objects.items()}, f)

    def reload(self):
        """ Deserialize JSON to __objects. """
        try:
            with open(self.__file_path, 'r') as f:
                objs = json.load(f)
            for k, v in objs.items():
                self.__objects[k] = model_classes[v['__class__']](**v)
        except FileNotFoundError:
            pass  # File not found, pass

    def delete(self, obj=None):
        """ Delete obj from __objects. """
        obj_key = f'{type(obj).__name__}.{obj.id}'
        self.__objects.pop(obj_key, None)

    def close(self):
        """ Deserialize JSON file to objects. """
        self.reload()

    def get(self, cls, id):
        """ Retrieve one object. """
        return self.__objects.get(f'{cls}.{id}') if cls and id else None

    def count(self, cls=None):
        """ Count objects in storage. """
        return len(self.all(cls))
