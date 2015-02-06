#!/usr/bin/env python

from flask import current_app
from app import db

class Search(db.Model):
    __tablename__   = 'master_search'
    id              = db.Column(db.Integer, primary_key = True)
    user_id         = db.Column(db.Integer, db.ForeignKey('users.id'))
    time            = db.Column(db.DateTime, default = db.func.now())
    
    def __str__(self):
        return '<Search : id %s user_id %s time %s>' % (self.id, self.user_id, self.time)
    
class SearchQuery(db.Model):
    __tablename__   = 'master_search_query'
    id              = db.Column(db.Integer, primary_key = True)
    master_search_id= db.Column(db.Integer, db.ForeignKey('master_search.id'))
    adult           = db.Column(db.Integer, default = 1)
    child           = db.Column(db.Integer, default = 0)
    infant          = db.Column(db.Integer, default = 0)
    trip_type       = db.Column(db.String)
    trip_class      = db.Column(db.String)
    search          = db.relationship('Search', backref = db.backref('query', uselist=False))
    
    def __str__(self):
        return '<SearchQuery : id %s search id %s adult %s type %s class %s>'\
        % (self.id, self.master_search_id, self.adult, self.trip_type, self.trip_class)
    
class SearchRoutes(db.Model):
    __tablename__   = 'master_search_routes'
    id              = db.Column(db.Integer, primary_key = True)
    master_search_id= db.Column(db.Integer, db.ForeignKey('master_search.id'))
    from_airport    = db.Column(db.String)
    to_airport      = db.Column(db.String)
    date            = db.Column(db.DateTime)
    ordinal         = db.Column(db.Integer, default = 1)
    search          = db.relationship('Search', backref = db.backref('routes', uselist = True))
    
    def __str__(self):
        return '<SearchQuery : id %s search id %s from %s to %s date %s>'\
        % (self.id, self.master_search_id, self.from_airport, self.to_airport, self.date)
    