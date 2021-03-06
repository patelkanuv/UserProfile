#!/usr/bin/env python

from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask.ext.login import UserMixin
from flask import current_app, session
from app import login_manager, db
from lib.data.user import UserCache

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@login_manager.request_loader
def load_user_from_request(request):
    sid = request.args.get('SID')
    user_cache = UserCache()
    user_id = user_cache.get_user(sid)
    #print sid, " - ", user_id
    if not user_id:
        return None
    user = User.query.get(int(user_id))
    if user:
        session.sid = sid
        return user
    return None

class User(UserMixin, db.Model):
    __tablename__   = 'users'
    id              = db.Column(db.Integer, primary_key = True)
    email           = db.Column(db.String(64), unique=True, index=True)
    username        = db.Column(db.String(64), index=True)
    password_hash   = db.Column(db.String(128))
    confirmed       = db.Column(db.Boolean, default = False)
    
    def __str__(self):
        return '<User : ID %s Email %s confirmed %s>' % (self.id, self.email, self.confirmed)
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    #TODO, replace this with Memcached
    def generate_confirmation_token(self, expiration = 86400):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})
    
    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except Exception:
            return False
        if (data.get('confirm') != self.id):
            return False
        
        self.confirmed = True
        db.session.add(self)
        return True