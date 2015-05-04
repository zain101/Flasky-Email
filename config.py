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
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'eyantra2269@gmail.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'pass4eyantra'
    FLASKY_POST_PER_PAGE = 5
    FLASK_FOLLOWERS_PER_PAGE = 10
    FLASK_COMMENTS_PER_PAGE = 10
    SSL_DISABLE = True

    @staticmethod
    def init_app(app):  # configuration specific initialization can be performed
        pass


class DevelopmentConfig(Config):
    DEBUG= True
    SQLALCHEMY_DATABASE_URI =os.environ.get('DEV_DATABASE_URL') or \
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    #'postgresql://zainul:root@localhost/zainul'


class TestingConfig(Config):
    TESTING= True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        # email errors to the administrators
        import logging
        from logging.handlers import SMTPHandler
        credentials = None
        secure = None
        if getattr(cls, 'MAIL_USERNAME', None) is not None:
            credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
            if getattr(cls, 'MAIL_USE_TLS', None):
                secure = ()
        mail_handler = SMTPHandler(
            mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
            fromaddr=cls.FLASKY_MAIL_SENDER,
            toaddrs=[cls.FLASKY_ADMIN],
            subject=cls.FLASKY_MAIL_SUBJECT_PREFIX + ' Application Error',
            credentials=credentials,
            secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)


class HerokuConfig(ProductionConfig):
    SSL_DISABLE = bool(os.environ.get('SSL_DISABLE'))

    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # handle proxy server headers
        from werkzeug.contrib.fixers import ProxyFix
        app.wsgi_app = ProxyFix(app.wsgi_app)

        # log to stderr
        import logging
        from logging import StreamHandler
        file_handler = StreamHandler()
        file_handler.setLevel(logging.WARNING)
        app.logger.addHandler(file_handler)

        SSL_DISABLE = bool(os.environ.get('SSL_DISABLE'))

        from werkzeug.contrib.fixers import ProxyFix
        app.wsgi_app = ProxyFix(app.wsgi_app)


config= {'development': DevelopmentConfig,
         'testing': TestingConfig,
         'production': ProductionConfig,
          'heroku': HerokuConfig,
         'default': DevelopmentConfig
         }




