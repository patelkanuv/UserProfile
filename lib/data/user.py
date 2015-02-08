#!/usr/bin/env python

from lib.data.cache import MemCache

class UserCache():
    def __init__(self):
        self.cache = MemCache()
        self.namespace = 'UserCache:'
        
    def cache_user_id(self, user, sid):
        self.cache.set(self.namespace+sid, user.id, 29 * 24 * 3600)
        #print sid, " set"
    def get_user_id(self, sid):
        #print "reading ", sid
        try:
            return self.cache.get(self.namespace+sid)
        except:
            #print "reading error"
            return None
    
    def delete_user(self, sid):
        try:
            return self.cache.delete(self.namespace+sid)
        except:
            print "Problem in deleting"
            return None