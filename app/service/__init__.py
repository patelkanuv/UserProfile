#!/usr/bin/env python

from flask import Blueprint
service = Blueprint('service', __name__)
from . import login, register