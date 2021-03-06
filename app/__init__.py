#!/usr/bin/env python

from flask import Flask, render_template
from flask.ext.bootstrap import Bootstrap
from flask.ext.mail import Mail
from flask.ext.moment import Moment
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.session import Session
from UserProfileConfig import config
import wtforms_json

wtforms_json.init()
bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()


login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'service.service_login'


def create_app(config_name):
    app = Flask(__name__)
    
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    Session(app)
    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    
    # attach routes and custom error pages here
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint, url_prefix='/userapi')
    
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/userapi/auth')

    from .service import service as service_blueprint
    app.register_blueprint(service_blueprint, url_prefix='/userapi/service')
    
    return app