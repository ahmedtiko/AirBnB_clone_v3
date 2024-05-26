#!/usr/bin/python3
"""
City objects view
"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State
