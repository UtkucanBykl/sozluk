import os

import django_heroku

from .base import *

DEBUG = False
ALLOWED_HOSTS = ["*"]

SECRET_KEY = os.environ.get('SECRET_KEY', '12534')

django_heroku.settings(locals())
