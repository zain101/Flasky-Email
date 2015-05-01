__author__ = 'zainul'
import os
'''
This is a global config file added to test for different states like DBS etc
'''
basedir = os.path.abspath(os.path.dirname(__file__))

# This is the base class for other, which contain common config to all.
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN= True
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky-zain]'
    FLASKY_MAIL_SENDER = 'zainul.sayed28@gmail.com'
    FLASKY_ADMIN = 'zainul.sayed28@gmail.com'
    MAIL_SERVER= 'smtp.gmail.com'
    MAIL_PORT=  465
    MAIL_USE_TLS= False
    MAIL_USE_SSL= True
    MAIL_USERNAME= os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD= os.environ.get('MAIL_PASSWORD')
    FLASKY_POST_PER_PAGE = 5
    FLASK_FOLLOWERS_PER_PAGE = 10
    FLASK_COMMENTS_PER_PAGE = 10


    @staticmethod
    def init_app(app):  # configuration specific initialization can be performed
        pass


class DevelopmentConfig(Config):
    DEBUG= True
    SQLALCHEMY_DATABASE_URI =os.environ.get('DEV_DATABASE_URL') or \
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')


class TestingConfig(Config):
    TESTING= True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config= {'development': DevelopmentConfig,
         'testing': TestingConfig,
         'production': ProductionConfig,

         'default': DevelopmentConfig
         }

