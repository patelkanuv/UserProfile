#!/usr/bin/env python

from flask import jsonify, redirect, session, request, url_for
from flask.ext.login import login_user, login_required, current_user
from app.models.user import User
from app.models.booking import Booking
from . import service
from .. import db

@service.route('/bookings/')
@login_required
def service_bookings():
    bookings = list(booking.serialize for booking in current_user.bookings)
    return jsonify(bookings = bookings)