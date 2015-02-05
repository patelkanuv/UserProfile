#!/usr/bin/env python

import unittest

from app.models.search import Search, SearchQuery, SearchRoutes
from flask import current_app
from app import create_app, db
from test_basics import BasicsTestCase

class SearchModelTestCase(BasicsTestCase):
    def test_search(self):
        search = Search(user_id = 2)
        self.assertIsInstance(search, Search)
        self.assertEqual(search.user_id, 2)
        
    def test_search_query(self):
        query = SearchQuery(master_search_id = 2, adult = 2, child = 1, infant = 0,
                            trip_type = 'RoundTrip', trip_class = 'Economy')
        self.assertIsInstance(query, SearchQuery)
        self.assertEqual(query.master_search_id , 2)
        self.assertEqual(query.adult , 2)
        self.assertEqual(query.child , 1)
        self.assertEqual(query.infant , 0)
        self.assertEqual(query.trip_type , 'RoundTrip')
        self.assertEqual(query.trip_class , 'Economy')
        
    def test_search_routes(self):
        routes = SearchRoutes(master_search_id  = 2, from_airport = 'YYZ', to_airport = 'JFK',
                              date = '2015-05-04', ordinal = 2)
        self.assertIsInstance(routes, SearchRoutes)
        self.assertEqual(routes.master_search_id , 2)
        self.assertEqual(routes.from_airport , 'YYZ')
        self.assertEqual(routes.to_airport , 'JFK')
        self.assertEqual(routes.date , '2015-05-04')
        self.assertEqual(routes.ordinal , 2)