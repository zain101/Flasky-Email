__author__ = 'zainul'


from flask import Flask, render_template
from flask.ext.bootstrap import Bootstrap
from flask.ext.mail import Mail
from flask.ext.moment import Moment
from flask.ext.sqlalchemy import SQLAlchemy
from config import config
from config import  config

'''
This constructor imports most Flask  extension currently in use, without intializing them with any application instance...
'''
bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()

def create_app(config_name):  #this is an application factory which takes as an argument the application config to be used...
    app= Flask(__name__)
    #first config is module and second one is dict
    #This(config['config_name') dict recturn a class-name as class-OBJ{obj created by from_object} and its variable...
    app.config.from_object(config['config_name'])
    # class-name.method_name  b'coz init_app is a @staticmethod
    config['config_name'].init_app(app)

    #intializing the extenisons

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)

    return app

