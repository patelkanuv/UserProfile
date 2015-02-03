#!/usr/bin/env python

import os
from datetime import datetime
from flask import render_template, session, request, redirect, url_for, make_response, flash
from flask.ext.login import login_user, login_required, logout_user
from lib.utility.common import random_password, email_password
from app import create_app
from app.auth.forms import LoginForm, ForgetPasswordForm
from . import main
from .. import db
from ..models import User

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

@main.route('/')
def index():
    response = make_response(render_template('index.html', name = session.get('name')))
    return response

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.content_type == u'application/json':
        return redirect(url_for('service.service_index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password.')
    return render_template('auth/login.html', form = form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))

@main.route('/resend/credentials', methods=['GET', 'POST'])
def resend_credentials():
    form = ForgetPasswordForm()
    if form.validate_on_submit():
        password = random_password()
        user = User.query.filter_by(email = form.email.data.lower()).first()
        if not user:
            flash('No such registered user.')
            return redirect(url_for('main.index'))
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        email_password(user = user, password = password, reset=True)
        flash('Your new credentials has been sent to your registered email.')
        return redirect(url_for('main.index'))
    return render_template('auth/forget_password.html', form = form)