#!/usr/bin/env python

import unittest
import json
import datetime

from flask import url_for
from tests.test_basics import BasicsTestCase
from app.models.search import Search, SearchQuery, SearchRoutes
from app.models.user import User
from app import db

class UserSearchesServiceTests(BasicsTestCase):
        
    def test_users_searches(self):
        u = User(username='Joe', email='searchesjoe@joes.com', password='k12345', confirmed = True)
        db.session.add(u)
        db.session.commit()
        
        response = self.client.post(url_for('service.service_login'),
                                    content_type='application/json',
                                    data = json.dumps({'email': 'searchesjoe@joes.com', 'password': 'k12345'}))
        self.assert_redirects(response, url_for('service.service_index'))
        
        response = self.client.get(url_for('service.service_searches'),
                                    content_type='application/json')
        self.assertTrue('searches' in response.data )
        
        search = Search(user = u)
        query  = SearchQuery(search = search, trip_type = 'OneWay', trip_class = 'Business')
        route  = SearchRoutes(search = search, from_airport = 'YYZ', to_airport = 'LHR',
                              date = datetime.date(2015, 03, 11))
        db.session.add(search)
        db.session.add(query)
        db.session.add(route)
        db.session.commit()
        
        response = self.client.get(url_for('service.service_searches'),
                                    content_type='application/json')
        self.assertTrue('YYZ' in response.data )
        
if __name__ == '__main__':
    unittest.main()