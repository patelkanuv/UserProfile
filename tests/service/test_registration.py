#!/usr/bin/env python

import unittest
import json

from flask import url_for
from tests.test_basics import BasicsTestCase
from app.models.user import User
from app import db

class UserRegisterServiceTests(BasicsTestCase):
    def test_users_can_register(self):
        response = self.client.post(url_for('service.service_register'),
                                    content_type='application/json',
                                    data=json.dumps({'email': 'registerjoe@joes.com', 'password': 'k12345',
                                          'username':'Register', 'password2':'k12345'}))
        self.assertTrue('A confirmation email has been sent to you by email.' in response.data )
    
        response = self.client.post(url_for('service.service_login'), follow_redirects=True,
                                    content_type='application/json',
                                    data=json.dumps({'email': 'registerjoe@joes.com', 'password': 'k12345'}))
        self.assertTrue('You have not confirmed your account yet' in response.data)
        
    def test_users_cant_register(self):
        response = self.client.post(url_for('service.service_register'),
                                     content_type='application/json',
                                    data = json.dumps({'email': '', 'password': '',
                                          'username':'', 'password2':''}))
        self.assertTrue('This field is required.' in response.data )
        
        response = self.client.post(url_for('service.service_register'),
                                    content_type='application/json',
                                    data = json.dumps({'email': 'registerjoejoes.com', 'password': 'k12345',
                                          'username':'Register', 'password2':'k12345'}))
        self.assertTrue('Invalid email address.' in response.data )
        
        response = self.client.post(url_for('service.service_register'),
                                    content_type='application/json',
                                    data = json.dumps({'email': 'registerjoe@joes.com', 'password': 'k12345',
                                          'username':'Register', 'password2':'k123456'}))
        self.assertTrue('Passwords must match.' in response.data )
        
    def test_unauthorised_page(self):
        response = self.client.get(url_for('service.service_logout'), follow_redirects=True)
        response = self.client.get(url_for('service.unconfirmed'), follow_redirects=True)
        self.assertTrue(response.status_code == 200)
        self.assertTrue('Please sign in.' in response.data )
        
    def test_resend_confirmation_token(self):
        u = User(username='Joe', email='regjoe2@joes.com', password='k12345', confirmed = False)
        db.session.add(u)
        db.session.commit()
        
        response = self.client.post(url_for('service.service_login'), follow_redirects=True,
                                    content_type='application/json',
                                    data = json.dumps({'email': 'regjoe2@joes.com', 'password': 'k12345'}))
        
        self.assertTrue('You have not confirmed your account yet' in response.data)
        
        token = u.generate_confirmation_token()
        response = self.client.get(url_for('service.service_resend_confirmation'),
                              content_type='application/json', follow_redirects=True)
        
        self.assertTrue('A new confirmation email has been sent to you by email.' in response.data)
        
        response = self.client.get(url_for('service.service_confirm', token = token),
                                   content_type='application/json',follow_redirects=True)
        
        self.assertTrue('You have confirmed your account' in response.data)
        
        response = self.client.get(url_for('service.service_confirm', token = token))
        self.assertTrue('Your account is already confirmed' in response.data)
    
    def test_reset_password(self):
        u = User(username='Joe', email='regjoe3@joes.com', password='k12345', confirmed = True)
        db.session.add(u)
        db.session.commit()
        
        response = self.client.post(url_for('service.service_login'), follow_redirects=True, 
                                    content_type='application/json',
                                    data = json.dumps({'email': 'regjoe3@joes.com', 'password': 'k12345'}))
        
        response = self.client.post(url_for('service.service_reset_password'),
                                    content_type='application/json',
                                    data= json.dumps({'password':'', 'password2':''}), follow_redirects=True)
        self.assertTrue('This field is required' in response.data)
        
        response = self.client.post(url_for('service.service_reset_password'),
                                    content_type='application/json',
                                    data = json.dumps({'password':'j12345', 'password2':'j123456'}), follow_redirects=True)
        self.assertTrue('Passwords must match.' in response.data)
        
        response = self.client.post(url_for('service.service_reset_password'),
                                    content_type='application/json',
                                    data = json.dumps({'password':'j123456', 'password2':'j123456'}), follow_redirects=True)
        self.assertTrue('Your password changed successfully' in response.data)
        
if __name__ == '__main__':
    unittest.main()