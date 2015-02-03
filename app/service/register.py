#!/usr/bin/env python

import sys
import re
import json

from flask import jsonify, redirect, session, request, url_for
from flask.ext.login import login_user, login_required, current_user
from lib.externalAuth.oauth import OAuthSignIn
from lib.utility.common import random_password, email_password, send_email
from . import service
from ..main import main
from ..models import User
from app.auth.forms import RegistrationForm, ResetPasswordForm
from app import db

@service.before_app_request
def before_request():
    #print "service", request.url
    #print session.sid
    if current_user.is_authenticated() and not current_user.confirmed \
        and request.content_type == u'application/json' \
        and not re.search('service/auth', request.url):
        return redirect(url_for('service.unconfirmed'))

@service.route('/auth/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous() or current_user.confirmed:
        return redirect(url_for('service.service_index'))
    data = { 'error' : 'User is unconfirmed, access denied.', 'success': False }
    return jsonify(data)

@service.route('/auth/register', methods=['GET', 'POST'])
def service_register():
    params = json.loads(request.get_data(cache=False, as_text=True))
    data = dict()
    form = RegistrationForm.from_json(params)
    if form.validate_on_submit():
        user = User(email    = form.email.data,
                    username = form.username.data,
                    password = form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm Your Account',
            'auth/email/confirm', user=user, token=token)
        data = { 'message' : 'A confirmation email has been sent to you by email.',
                 'success': True }
    else:
        data = { 'error' : form.errors, 'success': False }
        
    return jsonify(data)

@service.route('/auth/confirm/<token>')
@login_required
def service_confirm(token):
    message = ''
    success = True
    if current_user.confirmed:
        message = 'Your account is already confirmed.'
    else :
        if current_user.confirm(token):
            message ='You have confirmed your account. Thanks!'
        else:
            message = 'Your confirmation link is invalid or has expired.'
            success = False
    return jsonify({ 'success': success, 'message': message})

@service.route('/auth/reset/password', methods=['POST'])
@login_required
def service_reset_password():
    params = json.loads(request.get_data(cache=False, as_text=True))
    form = ResetPasswordForm.from_json(params)
    if form.validate_on_submit():
        current_user.set_password(form.password.data)
        db.session.add(current_user)
        db.session.commit()
        data = { 'message' : 'Your password changed successfully.',
                 'success': True }
    else:
        data = { 'error' : form.errors, 'success': False }
    return jsonify(data)

@service.route('/auth/resendConfirmToken')
@login_required
def service_resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account', 'auth/email/confirm', 
               user = current_user, token = token)
    data = {'message' : 'A new confirmation email has been sent to you by email.',
            'success': True }
    return jsonify(data)