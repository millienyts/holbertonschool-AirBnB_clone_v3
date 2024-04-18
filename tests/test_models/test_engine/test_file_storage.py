#!/usr/bin/python3
"""
Contains TestFileStorageDocs classes for docs and style checks.
"""

from datetime import datetime
import inspect
import json
import os
import pep8
import unittest

from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models.engine import file_storage

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
        super().__init__(methodName)
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

    def test_get_existing_object(self):
        """Test get method with FileStorage and an existing object"""
        # Create an instance of FileStorage
        storage = FileStorage()

        # Create an instance of BaseModel
        obj = BaseModel()
        obj.id = "test_id"
        obj.save()

        # Get the object from the storage
        retrieved_obj = storage.get(BaseModel, "test_id")

        # Check if the retrieved object is the same as the original object
        self.assertIs(retrieved_obj, obj)

if __name__ == '__main__':
    unittest.main()
