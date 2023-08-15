#!/usr/bin/python3

from uuid import uuid4
from datetime import datetime
import models


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
        time_format = '%Y-%m-%dT%H:%M:%S.%f'
        self.id = str(uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        if len(kwargs) != 0:
            for key, value in kwargs.items():
                if key == 'created_at' or key == 'updated_at':
                    self.__dict__[k] = datetime.strptime(value, time_format)
                else:
                    self.__dict__[k] = value
        else:
            models.storage.new(self)

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
        models.storage.save()

    def to_dict(self):
        """
        Convert the object's attributes to a
        dictionary with the required format.

        :return: A dictionary containing keys/values of instance attributes.
        """
        obj_dict = self.__dict__.copy()
        obj_dict['created_at'] = self.created_at.isoformat()
        obj_dict['updated_at'] = self.updated_at.isoformat()
        obj_dict['__class__'] = self.__class__.__name__
        return obj_dict
