# __author__ = 'zainul'
from flask import Blueprint

main = Blueprint('main', __name__)    # __name__ gives the location.

from . import views, errors
from ..models import Permission


@main.app_context_processor
def inject_permission():
    return dict(Permission=Permission)