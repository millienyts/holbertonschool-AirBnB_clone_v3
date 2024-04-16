#!/usr/bin/python3
"""
Contains TestFileStorageDocs classes for docs and style checks.
"""

from datetime import datetime
import inspect
import models
from models.engine import file_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import os
import pep8
import unittest

FileStorage = file_storage.FileStorage
classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class TestFileStorageDocs(unittest.TestCase):
    """Docs and style tests for FileStorage class"""

    @classmethod
    def setUpClass(cls):
        """Set up for doc tests"""
        cls.fs_f = inspect.getmembers(FileStorage, inspect.isfunction)

    def test_pep8_conformance_file_storage(self):
        """Check if file_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/file_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors.")

    def test_pep8_conformance_test_file_storage(self):
        """Check if test_file_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_file_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors.")

    def test_file_storage_module_docstring(self):
        """Check if file_storage.py has a docstring"""
        self.assertIsNot(file_storage.__doc__, None,
                         "file_storage.py needs a docstring")
        self.assertTrue(len(file_storage.__doc__) >= 1,
                        "file_storage.py needs a docstring")

    def test_file_storage_class_docstring(self):
        """Check if FileStorage class has a docstring"""
        self.assertIsNot(FileStorage.__doc__, None,
                         "FileStorage class needs a docstring")
        self.assertTrue(len(FileStorage.__doc__) >= 1,
                        "FileStorage class needs a docstring")

    def test_fs_func_docstrings(self):
        """Check for docstrings in FileStorage methods"""
        for func in self.fs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""

    def __init__(self, methodName: str = "runTest"):
        """
        Wipe out previous json file data before tests.
        """
        unittest.TestCase.__init__(self, methodName)
        self.storage = FileStorage()
        self.storage._FileStorage__objects = {}
        self.storage.save()

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_all_returns_dict(self):
        """Test if all returns the FileStorage.__objects attr"""
        new_dict = self.storage.all()
        self.assertEqual(type(new_dict), dict)
        self.assertIs(new_dict, self.storage._FileStorage__objects)
        self.assertEqual({}, self.storage.all())

    def test_get(self):
        """
        Test if 'self.storage.get' returns an instance of class 'cls'
        with 'id' as its 'id' field if it's in 'self.storage',
        'None' if not, and raises TypeError if 'cls' isn't a class
        or if 'id' isn't a str.
        """
        target = BaseModel()
        self.storage.new(target)
        self.assertEqual(target, self.storage.get(BaseModel, target.id))
        self.assertIsNone(self.storage.get(Amenity, target.id))
        self.assertIsNone(self.storage.get(BaseModel, '<wrong id format>'))
        with self.assertRaises(TypeError):
            self.storage.get(5, None)
        with self.assertRaises(TypeError):
            self.storage.get(Place, 3.14)
        self.storage.delete(target)
        self.assertEqual({}, self.storage.all())
        self.storage.save()

    def test_count(self):
        """
        Test if 'FileStorage.count' counts instances of 'cls' or
        returns the correct amount of objects in 'storage.all()'
        when 'cls' is None, and raises 'TypeError'
        if 'cls' isn't a class.
        """
        target_base_model = BaseModel()
        target_amenity = Amenity(name="tv")
        target_state = State(name="California")
        self.storage.new(target_base_model)
        self.storage.new(target_amenity)
        self.storage.new(target_state)
        self.assertEqual(1, self.storage.count(BaseModel))
        self.assertEqual(1, self.storage.count(Amenity))
        self.assertEqual(1, self.storage.count(State))
        self.assertEqual(0, self.storage.count(Place))
        self.assertEqual(0, self.storage.count(Review))
        self.assertEqual(0, self.storage.count(User))
        self.assertEqual(3, self.storage.count())
        self.assertEqual(3, self.storage.count(None))
        with self.assertRaises(TypeError):
            self.storage.count(complex())
            self.storage.count(True)
            self.storage.count("")
        self.storage.delete(target_state)
        self.storage.delete(target_amenity)
        self.storage.delete(target_base_model)
        self.assertEqual({}, self.storage.all())
        self.storage.save()

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_new(self):
        """Test if new adds an object to FileStorage.__objects attr"""
        storage = FileStorage()
        save = FileStorage._FileStorage__objects
        FileStorage._FileStorage__objects = {}
        test_dict = {}
        for key, value in classes.items():
            with self.subTest(key=key, value=value):
                instance = value()
                instance_key = instance.__class__.__name__ + "." + instance.id
                storage.new(instance)
                test_dict[instance_key] = instance
                self.assertEqual(test_dict, storage._FileStorage__objects)
        FileStorage._FileStorage__objects = save

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_save(self):
        """Test if save properly saves objects to file.json"""
        storage = FileStorage()
        new_dict = {}
        for key, value in classes.items():
            instance = value()
            instance_key = instance.__class__.__name__ + "." + instance.id
            new_dict[instance_key] = instance
        save = FileStorage._FileStorage__objects
        FileStorage._FileStorage__objects = new_dict
        storage.save()
        FileStorage._FileStorage__objects = save
        for key, value in new_dict.items():
            new_dict[key] = value.to_dict()
        string = json.dumps(new_dict)
        with open("file.json", "r") as f:
            js = f.read()
        self.assertEqual(json.loads(string), json.loads(js))
