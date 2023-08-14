#!/usr/bin/python3

import unittest
import os
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel


class TestFileStorage(unittest.TestCase):

    def setUp(self):
        self.storage = FileStorage()
        self.base_model = BaseModel()
        self.base_model_key = (
            f"{self.base_model.__class__.__name__}.{self.base_model.id}"
        )

    def tearDown(self):
        if os.path.exists(FileStorage._FileStorage__file_path):
            os.remove(FileStorage._FileStorage__file_path)

    def test_all_method(self):
        self.assertIsInstance(self.storage.all(), dict)

    def test_new_method(self):
        self.storage.new(self.base_model)
        self.assertIn(self.base_model_key, self.storage.all())

    def test_save_and_reload_methods(self):
        self.storage.new(self.base_model)
        self.storage.save()

        new_storage = FileStorage()
        new_storage.reload()

        self.assertIn(self.base_model_key, new_storage.all())


if __name__ == '__main__':
    unittest.main()
