#!/usr/bin/env python

import os
import sys
sys.path.append(os.path.split(os.path.abspath(os.path.dirname(__file__)))[0])

from wtforms_test import FormTestCase
from app.auth.forms import LoginForm, RegistrationForm, ForgetPasswordForm, ResetPasswordForm
from wtforms import fields

class TestForms(FormTestCase):
    def test_login_form(self):
        form_class = LoginForm
        self.assert_type('email', fields.StringField)
        self.assert_type('password', fields.PasswordField)
        self.assert_type('remember_me', fields.BooleanField)
        self.assert_type('submit', fields.SubmitField)
   
    def test_registration_form(self):
        form_class = RegistrationForm        
        self.assert_type('email', fields.StringField)
        self.assert_type('password', fields.PasswordField)
        self.assert_type('password2', fields.PasswordField)
        self.assert_type('username', fields.StringField)
        self.assert_type('submit', fields.SubmitField)
    
    def test_forget_password_form(self):
        form_class = ForgetPasswordForm
        self.assert_type('email', fields.StringField)
        self.assert_type('submit', fields.SubmitField)
    
    def test_reset_password_form(self):
        form_class = ResetPasswordForm
        self.assert_type('password', fields.PasswordField)
        self.assert_type('password2', fields.PasswordField)
        self.assert_type('submit', fields.SubmitField)