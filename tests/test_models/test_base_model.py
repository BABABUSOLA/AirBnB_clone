#!/usr/bin/python3
import unittest
from datetime import datetime
from models.base_model import BaseModel


class TestBaseModel(unittest.TestCase):

    def setUp(self):
        self.base_model = BaseModel()

    def test_initial_attributes(self):
        self.assertIsInstance(self.base_model.id, str)
        self.assertIsInstance(self.base_model.created_at, datetime)
        self.assertIsInstance(self.base_model.updated_at, datetime)

    def test_save_method(self):
        initial_updated_at = self.base_model.updated_at
        self.base_model.save()
        self.assertNotEqual(self.base_model.updated_at, initial_updated_at)

    def test_to_dict_method(self):
        obj_dict = self.base_model.to_dict()
        self.assertIsInstance(obj_dict, dict)
        self.assertIn('__class__', obj_dict)
        self.assertIn('created_at', obj_dict)
        self.assertIn('updated_at', obj_dict)
        self.assertEqual(obj_dict['__class__'], 'BaseModel')

    def test_str_method(self):
        obj_str = str(self.base_model)
        self.assertIn('[BaseModel]', obj_str)
        self.assertIn(self.base_model.id, obj_str)

    def test_init_with_kwargs(self):
        kwargs = {
            'id': 'test_id',
            'created_at': '2023-08-01T12:34:56.789012',
            'updated_at': '2023-08-02T12:34:56.789012'
        }
        base_model = BaseModel(**kwargs)
        self.assertEqual(base_model.id, 'test_id')
        self.assertEqual(base_model.created_at,
                         datetime(2023, 8, 1, 12, 34, 56, 789012))
        self.assertEqual(base_model.updated_at,
                         datetime(2023, 8, 2, 12, 34, 56, 789012))


if __name__ == '__main__':
    unittest.main()
