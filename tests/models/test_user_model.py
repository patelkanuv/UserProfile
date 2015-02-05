#!/usr/bin/env python

import unittest

from app.models.user import User
from flask import current_app
from app import create_app, db
from test_basics import BasicsTestCase

class UserModelTestCase(BasicsTestCase):
    def test_password_setter(self):
        u = User(password = 'cat')
        self.assertTrue(u.password_hash is not None)
        
    def test_no_password_getter(self):
        u = User(password = 'cat')
        with self.assertRaises(AttributeError):
            u.password
            
    def test_password_verification(self):
        u = User(password = 'cat')
        self.assertTrue(u.verify_password('cat'))
        self.assertFalse(u.verify_password('dog'))
        
    def test_password_salts_are_random(self):
        u = User(password='cat')
        u2 = User(password='cat')
        self.assertTrue(u.password_hash != u2.password_hash)
        
    def test_generate_confirmation_token(self):
        u = User(id = 1, password='cat')
        token = u.generate_confirmation_token()
        self.assertTrue(token is not None)
        
    def test_confirm_token(self):
        u = User(id = 2, email = 'abc@example.com', password='cat123', username = 'Test')
        token = u.generate_confirmation_token()
        self.assertTrue(token is not None)
        self.assertTrue(u.confirm(token))
        print u
        
    def test_verify_password(self):
        u = User(id = 2, email = 'abc@example.com', password='cat123', username = 'Test')
        self.assertTrue(u.verify_password('cat123'))
        u.set_password('CAT123')
        self.assertTrue(u.verify_password('CAT123'))
        
    def test_confirm_token_exception(self ):
        u = User(id = 2, email = 'abc@example.com', password='cat123', username = 'Test')
        token = u.generate_confirmation_token()
        self.assertFalse(u.confirm(token+'abc'))
        
    def test_confirm_token_invalid(self ):
        u = User(id = 2, email = 'abc@example.com', password='cat123', username = 'Test')
        token = u.generate_confirmation_token()
        u.id = 5
        self.assertFalse(u.confirm(token))