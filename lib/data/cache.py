#!/usr/bin/env python

import memcache

class MemCache():
    
    def __init__(self, servers=['localhost:11211']):
        self.cache_server = memcache.Client(servers)
        
    def set(self, key, value, expiry = 3600):
        """
        This method is used to set a new value
        in the memcache server.
        """
        self.cache_server.set(key, value, expiry)
        
    def get(self, key):
        """
        This method is used to retrieve a value
        from the memcache server
        """
        return self.cache_server.get(key)
    
    def delete(self, key):
        """
        This method is used to delete a value from the
        memcached server. Lazy delete
        """
        self.cache_server.delete(key)