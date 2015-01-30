#!/usr/bin/env python

import unittest
from lib.utility.common import random_password

class UtilityCommonTestCase(unittest.TestCase):
    
    def test_random_password(self):
        first_random = random_password()
        self.assertTrue(first_random is not None)
        second_random = random_password()
        self.assertNotEqual(first_random, second_random)
        #print first_random
        #print second_random