# __author__ = 'zainul'
from flask import Blueprint

main = Blueprint('main', __name__)    # __name__ gives the location.

from . import views, errors