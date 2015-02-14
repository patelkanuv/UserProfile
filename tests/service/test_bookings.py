#!/usr/bin/env python

import unittest
import json
import datetime

from flask import url_for
from tests.test_basics import BasicsTestCase
from app.models.booking import Booking
from app.models.user import User
from app import db

class UserSearchesServiceTests(BasicsTestCase):
        
    def test_users_booking(self):
        u = User(username='Joe', email='bookingjoe@joes.com', password='k12345', confirmed = True)
        db.session.add(u)
        db.session.commit()
        
        response = self.client.post(url_for('service.service_login'),
                                    content_type='application/json',
                                    data = json.dumps({'email': 'bookingjoe@joes.com', 'password': 'k12345'}))
        self.assertTrue('/userapi/service/?SID' in response.data)
        
        response = self.client.get(url_for('service.service_bookings'),
                                    content_type='application/json')
        self.assertTrue('bookings' in response.data )
        
        booking = Booking(user = u, PNR = 'APPLE1')
        db.session.add(booking)
        db.session.commit()
        
        response = self.client.get(url_for('service.service_bookings'),
                                    content_type='application/json')
        #print response.data
        self.assertTrue('APPLE1' in response.data )
        
if __name__ == '__main__':
    unittest.main()