__author__ = 'zainul'


from flask import Flask, render_template
from flask.ext.bootstrap import Bootstrap
from flask.ext.mail import Mail
from flask.ext.moment import Moment
from flask.ext.sqlalchemy import SQLAlchemy
from config import config
from flask.ext.login import LoginManager
'''
This constructor imports most Flask  extension currently in use, without intializing them with any application instance...
'''
bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

'''this is an application factory which takes as an argument the application config to be used...'''
def create_app(config_name):
    # config_name = 'default'
    app = Flask(__name__)
    print config_name
    '''first config is module and second one is dict
    This(config['config_name') dict return a class-name as class-OBJ{obj created by from_object} and its variable... '''

    app.config.from_object(config[config_name])
    # class-name.method_name  b'coz init_app is a @staticmethod
    config[config_name].init_app(app)

    '''intializing the extenisons'''

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    xx = raw_input("inside create app")

    # importing blueprint
    from .main import main as main_blueprint
    print main_blueprint.name
    xx = raw_input("inside create app impoted blueprint" )
    app.register_blueprint(main_blueprint)
    xx = raw_input("inside create app after registration" )

    ''' Attaching auth blueprint to the application factory'''
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app

