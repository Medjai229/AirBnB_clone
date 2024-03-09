#!/usr/bin/python3
"""
File: file_storage.py
Description: a module that stores the data
"""

import json
from models.base_model import BaseModel

class FileStorage:
    """
    """

    __file_path = hbnb_info.json
    __objects = {}

    def all(self):
        """
        """
        return self.__objects

    def new(self, obj):
        """
        """
        key = f"{obj.__class__.__name__}.{obj.id}"
        self.__objects[key] = obj

    def save(self):
        """
        """
        with open(self.__file_path, 'w', encoding="UTF-8") as my_file:
            obj_dict = {
                    obj: self.__objects[obj].
                    to_dict() for obj in self.__objects.key()
                    }
            json.dumps(obj_dict, my_file)

    def reload(self):
        """
        """
        try:
            with open(self.__file_path) as my_file:
                obj_dict = json.loads(my_file)
                for obj in obj_dict.values():
                    name = obj["__class__"]
                    del obj["__class__"]
                    self.new(eval(name)(**obj))
