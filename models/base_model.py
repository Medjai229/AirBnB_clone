#!/usr/bin/python3
"""
File: base_model.py
Description: module that contains one class BaseClass
"""

from datatime import datatime
from uuid import uuid4

class BaseModel:
    """
    """

    def __init__(self):
        """
        """
        self.id = str(uuid4())
        self.created_at = datetime.now()
        self.updated_at = datatime.now()

    def save(self):
        """
        """
        self.updated_at = datatime.now()

    def to_dict(self):
        """
        """
        self_dict = self.__dict__.copy()
        self_dict["__class__"] = self.__class__.__name__
        self_dict["created_at"] = self_dict["created_at"].isoformat()
        self_dict["updated_at"] = self_dict["updated_at"].isoformat()
        return self_dict

    def __str__(self):
        """    
        """
        return f"[{self.__class__.__name_}_] ({self.id}) {self.__dict__}"
