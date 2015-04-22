__author__ = 'zainul'


from flask import render_template
from . import main

'''
Same as Flask.errorhandler, but for Blueprints .
It works for the complete application rather the only blueprint (the place where error orignated)
'''
@main.app_errorhandler(400)
def page_not_found(e):
    return render_template('404.html'), 404


@main.app_errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@main.app_errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403