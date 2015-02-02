#!/usr/bin/env python

from flask import url_for
from tests.test_basics import BasicsTestCase
from app.main.errors import internal_server_error

class ErrorViewsTests(BasicsTestCase):
    
    def test_not_found(self):
        response = self.client.get('/userapi/abc')
        self.assertEqual(response.status_code, 404)
        
    def test_internal_server_error(self):
        response = internal_server_error('')
        self.assertTrue('Internal Server Error' in response[0] )