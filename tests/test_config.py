#!/usr/bin/env python

from tests.test_basics import BasicsTestCase
from config import Config

class ConfigTests(BasicsTestCase):
    def test_TESTING(self):        
        config = Config()
        self.assertTrue(config.SECRET_KEY)
    
    def test_SQLAlchemy(self):
        config = Config()
        self.assertTrue('data-test.db' in self.create_app().config['SQLALCHEMY_DATABASE_URI'])
        
    def test_OAUTH_CREDENTIALS(self):
        config = Config()
        self.assertTrue(config.OAUTH_CREDENTIALS['facebook']['id'])
        self.assertTrue(config.OAUTH_CREDENTIALS['facebook']['secret'])
        self.assertTrue(config.OAUTH_CREDENTIALS['google']['id'])
        self.assertTrue(config.OAUTH_CREDENTIALS['google']['secret'])
        
    def test_MAIL_SERVER(self):
        config = Config()
        self.assertEqual(config.MAIL_SERVER, '192.168.3.3')
        
    def test_SECRET_KEY(self):
        config = Config()
        self.assertEqual(config.SECRET_KEY, '6b3549ce0bd972bab567612bc14c53c3')
        
    def test_SESSION_TYPE(self):
        config = Config()
        self.assertEqual(config.SESSION_TYPE, 'memcached')
    
    def test_SESSION_COOKIE_NAME(self):
        config = Config()
        self.assertEqual(config.SESSION_COOKIE_NAME, 'SID')
    
    def test_SQLALCHEMY_COMMIT_ON_TEARDOWN(self):
        config = Config()
        self.assertTrue(config.SQLALCHEMY_COMMIT_ON_TEARDOWN)
    
    def test_FLASKY_MAIL_SUBJECT_PREFIX(self):
        config = Config()
        self.assertEqual(config.FLASKY_MAIL_SUBJECT_PREFIX, '[Flasky]')    
    
    def test_FLASKY_MAIL_SENDER(self):
        config = Config()
        self.assertEqual(config.FLASKY_MAIL_SENDER, 'Flasky Admin <kanu.patel@flightnetwork.com>')
     
    def test_FLASKY_ADMIN(self):
        config = Config()
        self.assertEqual(config.FLASKY_ADMIN, 'patelkanuv@gmail.com')