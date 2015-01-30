#!/usr/bin/env python

import sys

from flask import render_template, redirect, session, request, url_for, flash
from flask.ext.login import login_user, login_required, current_user
from lib.externalAuth.oauth import OAuthSignIn
from lib.utility.common import random_password, email_password, send_email
from . import auth
from ..main import main
from ..models import User
from .forms import RegistrationForm, ResetPasswordForm
from app import db

@auth.before_app_request
def before_request():
    #print session.sid
    if current_user.is_authenticated() and not current_user.confirmed \
        and request.endpoint[:5] != 'auth.':
        return redirect(url_for('auth.unconfirmed'))

@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous() or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')

@auth.route('/reset/password', methods=['GET', 'POST'])
@login_required
def reset_password():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        current_user.set_password(form.password.data)
        db.session.add(current_user)
        db.session.commit()
        flash('Your password changed successfully.')
        return redirect(url_for('main.index'))
    return render_template('auth/reset_password.html', form=form)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email = form.email.data,
                    username = form.username.data,
                    password = form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm Your Account',
            'auth/email/confirm', user=user, token=token)
        flash('A confirmation email has been sent to you by email.')
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', form = form)

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('You have confirmed your account. Thanks!')
    else:
        flash('Your confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))

@auth.route('/resendConfirmToken')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email('auth/email/confirm', 'Confirm Your Account', user, token=token)
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('main.index'))

@auth.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous():
        return redirect(url_for('main.index'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()

@auth.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous():
        return redirect(url_for('main.index'))
    oauth = OAuthSignIn.get_provider(provider)
    social_id, username, email = oauth.callback()
    if social_id is None:
        flash('Authentication failed.')
        return redirect(url_for('main.index'))
    user = User.query.filter_by(email = email).first()
    if not user:
        password = random_password()
        user = User(username = username, email = email, password = password, confirmed = True)
        db.session.add(user)
        db.session.commit()
        email_password(user = user, password = password)
    login_user(user, True)
    return redirect(url_for('main.index'))