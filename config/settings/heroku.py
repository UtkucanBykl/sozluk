import os

import django_heroku

from .base import *

SECRET_KEY = os.environ.get('SECRET_KEY', '1234')

django_heroku.settings(locals())
