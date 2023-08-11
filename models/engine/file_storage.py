#!usr/bin/python3

import json
import os.path
import re


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
        return self.__objects

    def new(self, obj):
        """
        Sets in __objects the obj with key <obj class name>.id.

        :param obj: An object to be stored.
        """
        key = f"{obj.__class__.__name__}.{obj.id}"
        self.__objects[key] = obj
        self.save()

    def save(self):
        """
        Serializes __objects to the JSON file (path: __file_path).
        """
        obj_dict = {key: obj.to_dict() for key, obj in self.__objects.items()}
        with open(self.__file_path, 'w') as file:
            json.dump(obj_dict, file)

    def reload(self):
        """
        Deserializes the JSON file to __objects (only if the JSON file exists).
        """
        if os.path.exists(self.__file_path):
            with open(self.__file_path, 'r') as file:
                obj_dict = json.load(file)
                for key, value in obj_dict.items():
                    class_name, obj_id = key.split('.')
                    module_name = "models." + self.camel_to_snake(class_name)
                    module = __import__(module_name, fromlist=[class_name])
                    cls = globals().get(class_name)
                    if cls is not None:
                        instance = cls(**value)
                        self.__objects[key] = instance
