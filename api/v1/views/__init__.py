#!/usr/bin/python3
"""Module containing the views for the API."""
from flask import Blueprint


from .index import *
from .states import *
from .cities import *
from .users import *
from .places import *
from .amenities import *
from .places_reviews import *
from .places_amenities import *

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")
