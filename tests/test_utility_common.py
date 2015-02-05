#!/usr/bin/env python

from lib.utility.common import random_password, email_password, send_email
from tests.test_basics import BasicsTestCase
from app.models.user import User
from flask.ext.mail import Message

class UtilityCommonTestCase(BasicsTestCase):
    
    def test_random_password(self):
        first_random = random_password()
        self.assertTrue(first_random is not None)
        second_random = random_password()
        self.assertNotEqual(first_random, second_random)
        #print first_random
        #print second_random
        
    def test_email_password(self):
        u = User(username='Joe', email='joe@joes.com', password='k12345', confirmed = True)
        msg = email_password(user = u, password = '1234', reset = False)
        self.assertIsInstance(msg, Message)
        
    def test_send_mail(self):
        user = User(username='Joe', email='joe@joes.com', password='k12345', confirmed = True)
        subject  = 'Your Flasky account credentials'
        template = 'auth/email/oauth_confirm'
        msg = send_email(user.email, subject, template, user = user, password = '12345')
        self.assertIsInstance(msg, Message)