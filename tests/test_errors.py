#!/usr/bin/env python

from flask import url_for
from tests.test_basics import BasicsTestCase

class ErrorViewsTests(BasicsTestCase):
    
    def test_not_found(self):
        response = self.client.get('/userapi/abc')
        self.assertEqual(response.status_code, 404)