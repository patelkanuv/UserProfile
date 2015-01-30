#!/usr/bin/env python

from tests.test_basics import BasicsTestCase

class ConfigTests(BasicsTestCase):
    def test_TESTING(self):
        self.assertTrue(self.create_app().config['TESTING'])
    
    def test_WTF_CSRF_ENABLED(self):
        self.assertFalse(self.create_app().config['WTF_CSRF_ENABLED'])    
    
    def test_SQLAlchemy(self):
        self.assertTrue('data-test.db' in self.create_app().config['SQLALCHEMY_DATABASE_URI'])
    def test_OAUTH_CREDENTIALS(self):
        self.assertTrue(self.create_app().config['OAUTH_CREDENTIALS']['facebook']['id'])
        self.assertTrue(self.create_app().config['OAUTH_CREDENTIALS']['facebook']['secret'])
        self.assertTrue(self.create_app().config['OAUTH_CREDENTIALS']['google']['id'])
        self.assertTrue(self.create_app().config['OAUTH_CREDENTIALS']['google']['secret'])
        
    def test_MAIL_SERVER(self):
        self.assertEqual(self.create_app().config['MAIL_SERVER'], '192.168.3.3')
        
    def test_SECRET_KEY(self):
        self.assertEqual(self.create_app().config['SECRET_KEY'], '6b3549ce0bd972bab567612bc14c53c3')
        
    def test_SESSION_TYPE(self):
        self.assertEqual(self.create_app().config['SESSION_TYPE'], 'memcached')
    
    def test_SESSION_COOKIE_NAME(self):
        self.assertEqual(self.create_app().config['SESSION_COOKIE_NAME'], 'SID')
    
    def test_SQLALCHEMY_COMMIT_ON_TEARDOWN(self):
        self.assertTrue(self.create_app().config['SQLALCHEMY_COMMIT_ON_TEARDOWN'])
    
    def test_FLASKY_MAIL_SUBJECT_PREFIX(self):
        self.assertEqual(self.create_app().config['FLASKY_MAIL_SUBJECT_PREFIX'], '[Flasky]')    
    
    def test_FLASKY_MAIL_SENDER(self):
        self.assertEqual(self.create_app().config['FLASKY_MAIL_SENDER'], 'Flasky Admin <kanu.patel@flightnetwork.com>')
     
    def test_FLASKY_ADMIN(self):
        self.assertEqual(self.create_app().config['FLASKY_ADMIN'], 'patelkanuv@gmail.com')
    
    