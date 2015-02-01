#!/usr/bin/env python

from flask.ext.testing import TestCase
from app import create_app, db

class BasicsTestCase(TestCase):
    
    def setUp(self):
        db.create_all()
        
    def tearDown(self):
        db.session.remove()
        db.drop_all()

    
    def create_app(self):
        app = create_app('testing')
        return app