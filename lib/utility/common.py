#!/usr/bin/env python

import M2Crypto
import string
from app import mail
from flask import current_app
from flask.ext.mail import Message
from flask import render_template

def random_password(length=6):
    chars = string.ascii_uppercase + string.digits + string.ascii_lowercase
    password = ''
    for i in range(length):
        password += chars[ord(M2Crypto.m2.rand_bytes(1)) % len(chars)]
    return password

def email_password(user, password, reset = False):
    subject  = 'Your Flasky account credentials'
    template = 'auth/email/oauth_confirm'
    
    if reset == True:
        subject  = 'Your Flasky account credentials are reset'
        
    send_email(user.email, subject, template, user = user, password = password)

def send_email(to, subject, template, **kwargs):
    msg = Message(current_app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,
    sender = current_app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    #msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    if not current_app.config['TESTING']:
        mail.send(msg)