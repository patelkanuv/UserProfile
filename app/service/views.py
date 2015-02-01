#!/usr/bin/env python

import os
from datetime import datetime
from flask import session, request, redirect, url_for, flash, jsonify
from flask.ext.login import current_user, login_user, login_required, logout_user
from lib.utility.common import random_password, email_password
from app import create_app
from app.auth.forms import LoginForm, ForgetPasswordForm
from . import service
from .. import db
from ..models import User

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

@service.route('/', methods=['GET', 'POST'])
def service_index():
    data = dict()
    if current_user.is_authenticated():
       data = { 'sid' : session.sid,
                'user_signed_in' : True,
                'message' : 'Welcome, ' + current_user.username,
                'email' : current_user.email
        }
    else:
        data = { 'sid' : session.sid,
                'user_signed_in' : False,
                'message' : 'Please sign in.'
        }
    return jsonify(data)

@service.route('/login', methods=['POST'])
def service_login():
    data = dict()
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('service.service_index'))
        data = { 'error':'Invalid username or password.'}
    else:
        data = { 'error' : form.errors }
    return jsonify(data)

@service.route('/logout', methods=['GET', 'POST'])
@login_required
def service_logout():
    logout_user()
    data = { 'sid' : session.sid,
             'user_signed_in' : False,
             'message' : 'You have been logged out.'
        }
    return jsonify(data)