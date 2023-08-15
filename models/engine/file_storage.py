#!usr/bin/python3

import json
import os.path
import re
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """
    A class that serializes instances to a JSON file
    and deserializes JSON file to instances.
    """

    __file_path = "file.json"
    __objects = {}

    @staticmethod
    def camel_to_snake(name):
        """
        Convert a camel case string to lowercase with underscores.

        :param name: The input string in camel case.
        :return: The converted string in lowercase with underscores.
        """
        name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()

    def all(self):
        """
        Returns the dictionary __objects.

        :return: A dictionary containing all stored objects.
        """
        return FileStorage.__objects

    def new(self, obj):
        """
        Sets in __objects the obj with key <obj class name>.id.

        :param obj: An object to be stored.
        """
        key = f"{obj.__class__.__name__}.{obj.id}"
        FileStorage.__objects[key] = obj

    def classes(self):
        """Returns a dictionary of valid classes and their references."""

        classes = {"BaseModel": BaseModel,
                   "User": User,
                   "State": State,
                   "City": City,
                   "Amenity": Amenity,
                   "Place": Place,
                   "Review": Review
                   }
        return classes

    def attributes(self):
        """Returns the valid attributes and their types for classname."""
        attributes = {
            "BaseModel": {"id": str,
                          "created_at": datetime.datetime,
                          "updated_at": datetime.datetime},
            "User": {"email": str,
                     "password": str,
                     "first_name": str,
                     "last_name": str},
            "State": {"name": str},
            "City": {"state_id": str,
                     "name": str},
            "Amenity": {"name": str},
            "Place":
                    {"city_id": str,
                     "user_id": str,
                     "name": str,
                     "description": str,
                     "number_rooms": int,
                     "number_bathrooms": int,
                     "max_guest": int,
                     "price_by_night": int,
                     "latitude": float,
                     "longitude": float,
                     "amenity_ids": list},
            "Review":
                    {"place_id": str,
                     "user_id": str,
                     "text": str}
                    }
        return attributes

    def save(self):
        """
        Serializes __objects to the JSON file
        (path: __file_path).
        """
        obj_dict = {key: obj.to_dict()
                    for key, obj in FileStorage.__objects.items()}
        with open(FileStorage.__file_path, 'w') as file:
            json.dump(obj_dict, file)

    def reload(self):
        """
        Deserialize the JSON file __file_path
        to __objects, if it exists.
        """
        try:
            with open(FileStorage.__file_path) as f:
                objdict = json.load(f)
                for o in objdict.values():
                    cls_name = o["__class__"]
                    del o["__class__"]
                    self.new(eval(cls_name)(**o))
        except FileNotFoundError:
            return
