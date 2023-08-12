#!/usr/bin/python3
"""__init__ magic method for models directory"""
from models.engine.file_storage import FileStorage

"""Create a unique FileStorage instance for your application"""
storage = FileStorage()

"""Call the reload() method on the storage variable"""
storage.reload()
