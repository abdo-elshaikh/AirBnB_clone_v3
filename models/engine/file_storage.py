#!/usr/bin/python3
""" FileStorage module"""
import json
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

classes = {
    "Amenity": Amenity,
    "BaseModel": BaseModel,
    "City": City,
    "Place": Place,
    "Review": Review,
    "State": State,
    "User": User
}


class FileStorage:
    """Serializes instances to a JSON file & deserializes back to instances"""

    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """Returns the dictionary __objects."""
        if cls is not None:
            new_dict = {}
            for key, value in self.__objects.items():
                if cls == value.__class__ or cls == value.__class__.__name__:
                    new_dict[key] = value
            return new_dict
        return self.__objects

    def new(self, obj):
        """Adds a new object to the __objects dictionary."""
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        self.__objects[key] = obj

    def save(self):
        """Serializes __objects to the JSON file."""
        serialized_objects = {k: v.to_dict() for k, v
                              in self.__objects.items()}
        with open(self.__file_path, 'w') as f:
            json.dump(serialized_objects, f)

    def reload(self):
        """Deserializes the JSON file to __objects."""
        try:
            with open(self.__file_path, 'r') as f:
                data = json.load(f)
                self.__objects = {}
                for k, v in data.items():
                    cls_name = v['__class__']
                    cls = classes.get(cls_name)
                    if cls:
                        self.__objects[k] = cls(**v)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """Deletes an object from __objects."""
        if obj:
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            self.__objects.pop(key, None)

    def close(self):
        """Calls reload() method for deserializing the JSON file."""
        self.reload()

    def get(self, cls, id):
        """Retrieves an object based on class and ID."""
        key = "{}.{}".format(cls.__name__, id)
        return self.__objects.get(key)

    def count(self, cls=None):
        """Returns the count of objects in __objects."""
        if cls:
            return len(self.all(cls))
        return len(self.all())
