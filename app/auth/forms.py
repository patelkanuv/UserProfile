#!/usr/bin/env python

from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError
from wtforms.validators import Required, Email, Length, Regexp, EqualTo
from ..models import User

class LoginForm(Form):
    email       = StringField('Email', validators=[Required(), Length(1,64), Email()])
    password    = PasswordField('password', validators=[Required()])
    remember_me = BooleanField('Keep me logged in')
    submit      = SubmitField('Log In')
    
class RegistrationForm(Form):
    email       = StringField('Email', validators=[Required(), Length(1, 64), Email()])
    username    = StringField('User Name', validators=[Required(), Length(1, 64),
                            Regexp('^[A-Za-z ]*$', 0,
                            'Usernames must have only letters')])
    password    = PasswordField('Password', validators=[
                            Required(), Length(6, 40), EqualTo('password2', message='Passwords must match.')])
    password2   = PasswordField('Confirm password', validators=[Required()])
    submit      = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email = field.data.lower()).first():
            raise ValidationError('Email already registered.')

class ForgetPasswordForm(Form):
    email  = StringField('Email', validators = [Required(), Length(1, 64), Email()])
    submit = SubmitField('Resend Password')
    
class ResetPasswordForm(Form):
    password    = PasswordField('New Password', validators=[
                            Required(), Length(6, 40), EqualTo('password2', message='Passwords must match.')])
    password2   = PasswordField('Confirm password', validators=[Required()])
    submit      = SubmitField('Reset Password')