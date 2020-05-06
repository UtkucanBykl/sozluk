import os

import django_heroku

from .base import *

DEBUG = True
ALLOWED_HOSTS = ["*"]

SECRET_KEY = os.environ.get('SECRET_KEY', '12534')

CORS_ORIGIN_ALLOW_ALL = True

django_heroku.settings(locals())
