#!/usr/bin/env python

import unittest
import time
import os
import sys
sys.path.append(os.path.split(os.path.abspath(os.path.dirname(__file__)))[0])

from lib.data.cache import MemCache


class MemCacheTestCase(unittest.TestCase):
    def setUp(self):
        self.cache = MemCache()
    
    def test_cache_setter(self):
        self.assertTrue(self.cache is not None)
        self.assertIsInstance(self.cache, MemCache)
        
    def test_set_data(self):
        self.cache.set('Test', 'Test')
        self.assertEqual(self.cache.get('Test'), 'Test')
        
    def test_set_data_with_expiry(self):
        self.cache.set('Test1', 'Test', 1)
        time.sleep(1.1)
        self.assertNotEqual(self.cache.get('Test1'), 'Test')
        
    def test_delete_data(self):
        self.cache.set('Test', 'Test')
        self.assertEqual(self.cache.get('Test'), 'Test')
        self.cache.delete('Test')
        self.assertNotEqual(self.cache.get('Test'), 'Test')
    