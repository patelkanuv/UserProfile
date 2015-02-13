#!/usr/bin/env python

import os
import json

from datetime import datetime
from flask import session, request, redirect, url_for, flash, jsonify
from flask.ext.login import current_user, login_user, login_required, logout_user
from lib.utility.common import random_password, email_password
from app import create_app
from app.auth.forms import LoginForm, ForgetPasswordForm
from . import service
from .. import db
from app.models.user import User
from lib.data.user import UserCache

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

@service.route('/login/', methods=['GET','POST'])
def service_login():
    
    params = dict()
    try:
        params = json.loads(request.get_data(cache=False, as_text=True))
    except Exception:
        return redirect(url_for('service.service_index'))
    
    data = dict()
    form = LoginForm.from_json(params)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user is not None and user.verify_password(form.password.data):
            userCache = UserCache()
            userCache.cache_user(user, session.sid)
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('service.service_index', SID = session.sid))
        data = { 'error': { 'message' : ['Invalid username or password.']}, 'success': False}
    else:
        data = { 'error' : form.errors, 'success': False }
    return jsonify(data)

@service.route('/logout/')
@login_required
def service_logout():
    sid = request.args.get('SID')
    userCache = UserCache()
    userCache.delete_user(sid)
    
    logout_user()
    data = { 'sid' : session.sid,
             'user_signed_in' : False,
             'message' : 'You have been logged out.'
        }
    return jsonify(data)

@service.route('/resend/credentials/', methods=['GET', 'POST'])
def service_resend_credentials():
    params = json.loads(request.get_data(cache=False, as_text=True))
    data = dict()
    form = ForgetPasswordForm.from_json(params)
    if form.validate_on_submit():
        password = random_password()
        user = User.query.filter_by(email = form.email.data.lower()).first()
        if not user:
            data = { 'error' : { 'message' : ['No such registered user.']}, 'success': False }
            return jsonify(data)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        email_password(user = user, password = password, reset=True)
        data = { 'message' : 'Your new credentials has been sent to your registered email.',
                 'success' : True}
    else:
        data = { 'error' : form.errors, 'success': False }
    return jsonify(data)
