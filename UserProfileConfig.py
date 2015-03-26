#!/usr/bin/env python

import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or '6b3549ce0bd972bab567612bc14c53c3'
    SESSION_TYPE = 'memcached'
    SESSION_COOKIE_NAME = 'SID'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'Flasky Admin <kanu.patel@flightnetwork.com>'
    FLASKY_ADMIN = 'patelkanuv@gmail.com'
    MAIL_SERVER = 'localhost'
    #MAIL_PORT = 587
    #MAIL_USE_TLS = True
    #MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    #MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    WTF_CSRF_ENABLED = False
    OAUTH_CREDENTIALS = {
        'facebook': {
            'id': '1548157722106884',
            'secret': '550e912621b7bc30432f3db7f6b8aa3a'
        },
        'twitter': {
            'id': 'XuaKU88ZiO9AQS0veS3Kq1KAd',
            'secret': '6u0XqvszrJ3a1yBe64urcEKBjyxdhlam09nW67uwZEmqOjG9Xh'
        },
        'google': {
            'id': '566354626811-h683j12ic2f4i722pghpfc0kk9li0poo.apps.googleusercontent.com',
            'secret': 'ABjsmUlgWxKH51dQyonL3qa9'
        }
    }
    @staticmethod
    def init_app(app):
        pass
    
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
    'sqlite:///' + os.path.join(basedir, 'data-dev.db')
    
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
    'sqlite:///' + os.path.join(basedir, 'data-test.db')
    
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    'sqlite:///' + os.path.join(basedir, 'data.db')

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
