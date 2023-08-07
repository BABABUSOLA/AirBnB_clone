#!usr/bin/python3

import json
import os.path


class FileStorage:
    """
    A class that serializes instances to a JSON file
    and deserializes JSON file to instances.
    """

    __file_path = "file.json"
    __objects = {}

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
                    module_name = "models." + class_name
                    module = __import__(module_name, fromlist=[class_name])
                    cls = getattr(module, class_name)
                    instance = cls(**value)
                    self.__objects[key] = instance
