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
        if not key: return None
        self.cache_server.set(self.decoded_string(key), value, expiry)
        
    def get(self, key):
        """
        This method is used to retrieve a value
        from the memcache server
        """
        if not key: return None
        return self.cache_server.get(self.decoded_string(key))
    
    def delete(self, key):
        """
        This method is used to delete a value from the
        memcached server. Lazy delete
        """
        if not key: return None
        self.cache_server.delete(self.decoded_string(key))
        
    def decoded_string(self, key):
        new_key = key.encode('utf-8')
        return new_key