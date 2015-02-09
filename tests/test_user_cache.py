#!/usr/bin/env python

import unittest
import os
import sys
sys.path.append(os.path.split(os.path.abspath(os.path.dirname(__file__)))[0])

from lib.data.user import UserCache
from app.models.user import User

class MemCacheTestCase(unittest.TestCase):
    def setUp(self):
        self.cache = UserCache()
    
    def test_user_cache_object(self):
        self.assertTrue(self.cache is not None)
        self.assertIsInstance(self.cache, UserCache)
        
    def test_set_user(self):
        u = User(id = 101, username='Joe', email='joe@joes.com', password='k12345', confirmed = True)
        self.cache.cache_user(u, 'Test')
        self.assertEqual(self.cache.get_user('Test'), 101)
        
    def test_delete_user(self):
        u = User(id = 101, username='Joe', email='joe@joes.com', password='k12345', confirmed = True)
        self.cache.cache_user(u, 'Test1')
        self.assertEqual(self.cache.get_user('Test1'), 101)
        self.cache.delete_user('Test1')
        self.assertNotEqual(self.cache.get_user('Test1'), 101)
    