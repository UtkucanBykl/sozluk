
from .base import *

SECRET_KEY = '1234'

DOCKER = os.environ.get('DJANGO_DOCKER')

if DOCKER:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'sozluk_db',
            'USER': 'utkucanbiyikli',
            'PASSWORD': 'qazwsx.1234',
            'HOST': 'db',
            'PORT': 5432,
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'mydatabase',
        }
    }

DJANGO_SUPERUSER_PASSWORD = "qazwsxç1234"