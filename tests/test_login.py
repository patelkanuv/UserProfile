#!/usr/bin/env python

from flask import url_for
from tests.test_basics import BasicsTestCase
from app.models import User
from app import db

class UserViewsTests(BasicsTestCase):
    
    def test_users_can_login(self):
        u = User(username='Joe', email='joe@joes.com', password='k12345', confirmed = True)
        db.session.add(u)
        db.session.commit()
        
        response = self.client.post(url_for('main.login'),
                                    data={'email': 'joe@joes.com', 'password': 'k12345'})
        self.assert_redirects(response, url_for('main.index'))
    
    def test_users_can_logout(self):
        response = self.client.get(url_for('main.logout'), follow_redirects=True)
        self.assertTrue(response.status_code == 200)
        self.assertTrue('You have been logged out' in response.data )
        
    def test_index_page(self):
        response = self.client.get(url_for('main.index'), follow_redirects=True)
        self.assertTrue(response.status_code == 200)
        self.assertTrue('Sign In' in response.data )
        
    def test_users_can_login_unconfirmed(self):
        u = User(username='Joe', email='joe1@joes.com', password='k12345', confirmed = False)
        db.session.add(u)
        db.session.commit()
        
        response = self.client.post(url_for('main.login'), follow_redirects=True, 
                                    data={'email': 'joe1@joes.com', 'password': 'k12345'})
        self.assertTrue('You have not confirmed your account yet' in response.data)
        
    def test_users_can_login_unconfirmed_confirmed(self):
        u = User(username='Joe', email='joe2@joes.com', password='k12345', confirmed = False)
        db.session.add(u)
        db.session.commit()
        
        response = self.client.post(url_for('main.login'), follow_redirects=True, 
                                    data={'email': 'joe2@joes.com', 'password': 'k12345'})
        self.assertTrue('You have not confirmed your account yet' in response.data)
        
        token = u.generate_confirmation_token()
        
        response = self.client.get(url_for('auth.confirm', token = token), follow_redirects=True)
        self.assertTrue('You have confirmed your account' in response.data)
        
    def test_users_resend_password(self):
        self.test_users_can_logout()
        response = self.client.get(url_for('main.resend_credentials'))
        self.assertTrue('Forget Password' in response.data)
        
    def test_users_resend_password_submit(self):
        self.test_users_can_logout()
        u = User(username='Joe', email='krishna@joes.com', password='k12345', confirmed = True)
        db.session.add(u)
        db.session.commit()
        
        response = self.client.post(url_for('main.resend_credentials'), data={'email': 'krishna@joes.com'},
                                    follow_redirects=True)
        self.assertTrue('Your new credentials has been sent to your registered email' in response.data)
        