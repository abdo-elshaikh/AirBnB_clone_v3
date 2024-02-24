#!/usr/bin/python3
"""This module defines a class User"""
import os
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import hashlib
from models.base_model import BaseModel, Base


class User(BaseModel, Base):
    """This class defines a user by various attributes"""
    __tablename__ = 'users'
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship('Place', backref='user',
                              cascade='all, delete, delete-orphan')
        reviews = relationship('Review', backref='user',
                               cascade='all, delete, delete-orphan')
    else:
        email = ''
        password = ''
        first_name = ''
        last_name = ''

    def __init__(self, *args, **kwargs):
        """Initializes a new user"""
        super().__init__(*args, **kwargs)

    @property
    def password(self):
        """Retrieves password for user"""
        return self.__password

    @password.setter
    def password(self, value):
        """Sets password for user"""
        self.__password = hashlib.md5(value.encode()).hexdigest()

    def to_dict(self, passwd=None):
        """ Return dictionary representation of User."""
        user_dict = super().to_dict()
        if passwd:
            user_dict['password'] = passwd
        return user_dict
