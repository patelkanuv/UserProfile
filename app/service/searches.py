#!/usr/bin/env python

from flask import jsonify, redirect, session, request, url_for
from flask.ext.login import login_user, login_required, current_user
from app.models.search import Search, SearchQuery, SearchRoutes
from app.models.user import User
from . import service
from .. import db

@service.route('/searches')
@login_required
def service_searches():
    searches = list(result.serialize for result in current_user.searches)
    return jsonify(searches = searches)