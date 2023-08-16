#!/usr/bin/python3
"""Doc
"""
from models.tmp_base_model import *
from models.tmp_base_model import BaseModel


class BaseModel(BaseModel):
    """Doc
    """

    def save(self):
        self.updated_at = datetime.utcnow()
