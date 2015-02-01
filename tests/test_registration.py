#!/usr/bin/env python

import unittest
from flask import url_for
from tests.test_basics import BasicsTestCase
from app.models import User
from app import db

class UserViewsTests(BasicsTestCase):
    
    def test_registration_page(self):
        response = self.client.get(url_for('auth.register'), follow_redirects=True)
        self.assertTrue(response.status_code == 200)
        self.assertTrue('Register' in response.data )
    
    def test_registration_page_submit(self):
        response = self.client.post(url_for('auth.register'), follow_redirects=True,
                                    data={'email': 'joe@example.com', 'password': 'k12345',
                                          'password2':'k12345', 'username':'Joe'})
        self.assertTrue(response.status_code == 200)
        self.assertTrue('confirmation email has been sent to you by email' in response.data )
        
        response = self.client.post(url_for('auth.register'), follow_redirects=True,
                                    data={'email': 'joe@example.com', 'password': 'k12345',
                                          'password2':'k12345', 'username':'Joe'})
        self.assertTrue(response.status_code == 200)
        self.assertTrue('Email already registered.' in response.data )
        
        response = self.client.post(url_for('auth.register'), follow_redirects=True,
                                    data={'email': 'JOE@example.com', 'password': 'k12345',
                                          'password2':'k12345', 'username':'Joe'})
        self.assertTrue(response.status_code == 200)
        self.assertTrue('Email already registered.' in response.data )
        
        response = self.client.post(url_for('main.login'), follow_redirects=True, 
                                    data={'email': 'joe@example.com', 'password': 'k12345'})
        self.assertTrue('You have not confirmed your account yet' in response.data)
        
    def test_registration_page_invalid_submit(self):
        response = self.client.post(url_for('auth.register'), follow_redirects=True,
                                    data={'email': 'joe', 'password': 'k12345',
                                          'password2':'k12345', 'username':'Joe'})
        self.assertTrue(response.status_code == 200)
        self.assertTrue('Invalid email address.' in response.data )
        
        response = self.client.post(url_for('auth.register'), follow_redirects=True,
                                    data={'email': 'joe@example.com', 'password': 'k12345',
                                          'password2':'k12345', 'username':'Joe123'})
        self.assertTrue(response.status_code == 200)
        self.assertTrue('Usernames must have only letters' in response.data )
        
        response = self.client.post(url_for('auth.register'), follow_redirects=True,
                                    data={'email': 'joe@example.com', 'password': 'k12345',
                                          'password2':'k123456', 'username':'Joe'})
        self.assertTrue(response.status_code == 200)
        self.assertTrue('Passwords must match.' in response.data )
        
        response = self.client.post(url_for('auth.register'), follow_redirects=True,
                                    data={'email': 'joe@example.com', 'password': 'k12345',
                                          'password2':'k123456', 'username':'Joe'})
        self.assertTrue(response.status_code == 200)
        self.assertTrue('Passwords must match.' in response.data )
        
        response = self.client.post(url_for('auth.register'), follow_redirects=True,
                                    data={'email': '', 'password': '',
                                          'password2':'', 'username':''})
        self.assertTrue(response.status_code == 200)
        self.assertTrue('This field is required' in response.data )
        
        response = self.client.post(url_for('auth.register'), follow_redirects=True,
                                    data={'email': 'joe@example.com', 'password': '',
                                          'password2':'', 'username':''})
        self.assertTrue(response.status_code == 200)
        self.assertTrue('This field is required' in response.data )
        
        response = self.client.post(url_for('auth.register'), follow_redirects=True,
                                    data={'email': 'joe@example.com', 'password': 'k12345',
                                          'password2':'k12345', 'username':''})
        self.assertTrue(response.status_code == 200)
        self.assertTrue('This field is required' in response.data )
        
        response = self.client.post(url_for('auth.register'), follow_redirects=True,
                                    data={'email': 'joe@example.com', 'password': '',
                                          'password2':'', 'username':'Joe'})
        self.assertTrue(response.status_code == 200)
        self.assertTrue('This field is required' in response.data )
    
    def test_unauthorised_page(self):
        response = self.client.get(url_for('main.logout'), follow_redirects=True)
        response = self.client.get(url_for('auth.unconfirmed'), follow_redirects=True)
        self.assertTrue(response.status_code == 200)
        self.assertTrue('Stranger' in response.data )
        
    def test_resend_confirmation_token(self):
        u = User(username='Joe', email='joe2@joes.com', password='k12345', confirmed = False)
        db.session.add(u)
        db.session.commit()
        
        response = self.client.post(url_for('main.login'), follow_redirects=True, 
                                    data={'email': 'joe2@joes.com', 'password': 'k12345'})
        self.assertTrue('You have not confirmed your account yet' in response.data)
        
        token = u.generate_confirmation_token()
        response = self.client.get(url_for('auth.resend_confirmation'), follow_redirects=True)
        self.assertTrue('A new confirmation email has been sent to you by email.' in response.data)
        
        response = self.client.get(url_for('auth.confirm', token = token), follow_redirects=True)
        self.assertTrue('You have confirmed your account' in response.data)
        
        response = self.client.get(url_for('auth.confirm', token = token))
        self.assert_redirects(response, url_for('main.index'))
    
    def test_reset_password(self):
        u = User(username='Joe', email='joe3@joes.com', password='k12345', confirmed = True)
        db.session.add(u)
        db.session.commit()
        
        response = self.client.post(url_for('main.login'), follow_redirects=True, 
                                    data={'email': 'joe3@joes.com', 'password': 'k12345'})
        
        response = self.client.get(url_for('auth.reset_password'), follow_redirects=True)
        self.assertTrue('Change Password' in response.data)
        
        response = self.client.post(url_for('auth.reset_password'),
                                    data={'password':'', 'password2':''}, follow_redirects=True)
        self.assertTrue('This field is required' in response.data)
        
        response = self.client.post(url_for('auth.reset_password'),
                                    data={'password':'j12345', 'password2':'j123456'}, follow_redirects=True)
        self.assertTrue('Passwords must match.' in response.data)
        
        response = self.client.post(url_for('auth.reset_password'),
                                    data={'password':'j123456', 'password2':'j123456'}, follow_redirects=True)
        self.assertTrue('Your password changed successfully' in response.data)
    
    def test_google_oauth(self):
        response = self.client.get(url_for('auth.oauth_authorize', provider = 'google', _external=True))
        self.assertTrue('google' in response.data)
        
    def test_google_oauth_callback(self):
        response = self.client.get(url_for('auth.oauth_callback', provider = 'google', _external=True))
        self.assertTrue('Redirecting' in response.data)
        
if __name__ == '__main__':
    unittest.main()