#!/usr/bin/python3

import uuid
from datetime import datetime
from models.__init__ import storage


class BaseModel:
    """
    A base class that defines common attributes and methods for other classes.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the BaseModel using *args and **kwargs
        for attribute assignment.

        :param args: Unused variable-length argument list.
        :param kwargs: Keyword arguments for attribute assignment.
        """
        if kwargs:
            for key, value in kwargs.items():
                if key == '__class__':
                    continue
                if key == 'created_at' or key == 'updated_at':
                    value = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f')
                setattr(self, key, value)
            self.created_at = datetime.strptime(
                    kwargs.get('created_at', datetime.now().isoformat()),
                    '%Y-%m-%dT%H:%M:%S.%f'
                    )
            self.updated_at = datetime.strptime(
                    kwargs.get('updated_at', datetime.now().isoformat()),
                    '%Y-%m-%dT%H:%M:%S.%f'
                    )
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = self.created_at
            storage.new(self)

    def __str__(self):
        """
        Return a string representation of the object.

        :return: A formatted string containing class name
        , id, and attribute dictionary.
        """
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """
        Update the `updated_at` attribute with the current datetime.
        and call the save method on storage
        """
        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """
        Convert the object's attributes to a
        dictionary with the required format.

        :return: A dictionary containing keys/values of instance attributes.
        """
        obj_dict = self.__dict__.copy()
        obj_dict['__class__'] = self.__class__.__name__
        obj_dict['created_at'] = self.created_at.isoformat()
        obj_dict['updated_at'] = self.updated_at.isoformat()
        return obj_dict


""" Create an instance of the BaseModel"""
base_model_instance = BaseModel()

""" Convert the instance to a dictionary using the to_dict method"""
base_model_dict = base_model_instance.to_dict()
