#!/usr/bin/env python

import unittest
from flask import url_for
from tests.test_basics import BasicsTestCase
from app.models import User
from app import db

class UserLoginServiceTests(BasicsTestCase):
    
    def test_service_index(self):
        response = self.client.get(url_for('service.service_index'))
        self.assertTrue(': false' in response.data )
        self.assertTrue('Please sign in.' in response.data )
        
    def test_users_can_login(self):
        u = User(username='Joe', email='joe@joes.com', password='k12345', confirmed = True)
        db.session.add(u)
        db.session.commit()
        
        response = self.client.post(url_for('service.service_login'),
                                    data={'email': 'joe@joes.com', 'password': 'k12345'})
        self.assert_redirects(response, url_for('service.service_index'))
        
        response = self.client.post(url_for('service.service_login'),
                                    data={'email': 'joe@joes.com', 'password': 'k12345'}, follow_redirects=True)
        self.assertTrue('Welcome, Joe' in response.data )
    
    def test_users_failed_login(self):
        u = User(username='Joe', email='joe11@joes.com', password='k12345', confirmed = True)
        db.session.add(u)
        db.session.commit()
        
        response = self.client.post(url_for('service.service_login'),
                                    data={'email': 'joe', 'password': 'k12345'})
        self.assertTrue('Invalid email address.' in response.data )
        
        response = self.client.post(url_for('service.service_login'),
                                    data={'email': 'joe11@joes.com', 'password': ''}, follow_redirects=True)
        self.assertTrue('This field is required.' in response.data )
        
        response = self.client.post(url_for('service.service_login'),
                                    data={'email': '', 'password': ''}, follow_redirects=True)
        self.assertTrue('This field is required.' in response.data )
        
        response = self.client.post(url_for('service.service_login'),
                                    data={'email': '', 'password': '123456'}, follow_redirects=True)
        self.assertTrue('This field is required.' in response.data )
        
        response = self.client.post(url_for('service.service_login'),
                                    data={'email': 'joe11@joes.com', 'password': '123456'}, follow_redirects=True)
        self.assertTrue('Invalid username or password.' in response.data )
    
    def test_logout(self):
        client = self.create_app().test_client()
        #print client
        response = client.get(url_for('service.service_logout'), content_type='application/json',  follow_redirects=True)
        self.assertTrue(': false' in response.data )
        
    def test_users_can_resend_credentials(self):
        response = self.client.post(url_for('service.service_resend_credentials'),
                                    data={'email': 'ghjoe@joes.com'})
        self.assertTrue('No such registered user.' in response.data )
        
        u = User(username='Joe', email='ghjoe@joes.com', password='k12345', confirmed = True)
        db.session.add(u)
        db.session.commit()
        
        response = self.client.post(url_for('service.service_resend_credentials'),
                                    data={'email': 'joes.com'})
        self.assertTrue('Invalid email address.' in response.data )
        
        response = self.client.post(url_for('service.service_resend_credentials'),
                                    data={'email': ''})
        self.assertTrue('This field is required.' in response.data )
        
        response = self.client.post(url_for('service.service_resend_credentials'),
                                    data={'email': 'ghjoe@joes.com'})
        self.assertTrue('Your new credentials has been sent to your registered email.' in response.data )
        
if __name__ == '__main__':
    unittest.main()