
from .base import *

SECRET_KEY = 'x'

ALLOWED_HOSTS = ["*"]
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mydb',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '',
    }
}

