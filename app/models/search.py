#!/usr/bin/env python

from flask import current_app
from app import db
from app.models.user import User

class Search(db.Model):
    __tablename__   = 'master_search'
    id              = db.Column(db.Integer, primary_key = True)
    user_id         = db.Column(db.Integer, db.ForeignKey('users.id'))
    time            = db.Column(db.DateTime, default = db.func.now())
    user            = db.relationship('User', lazy = True, backref = db.backref('searches', uselist = True))
    
    def __str__(self):
        return '<Search : id %s user_id %s time %s>' % (self.id, self.user_id, self.time)
    
    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       
       return {
           'id'         : self.id,
           'user_id'    : self.user_id, 
           'time'       : self.time,
           'query'      : self.query.serialize,
           'routes'     : list( route.serialize for route in self.routes)
       }
    
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
    
    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'id'                 : self.id,
           'master_search_id'   : self.master_search_id, 
           'adult'              : self.adult,
           'child'              : self.child,
           'infant'             : self.infant,
           'trip_type'          : self.trip_type,
           'trip_class'         : self.trip_class
       }
    
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
    
    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'id'                 : self.id,
           'master_search_id'   : self.master_search_id, 
           'from_airport'       : self.from_airport,
           'to_airport'         : self.to_airport,
           'date'               : self.date,
           'ordinal'            : self.ordinal
       }