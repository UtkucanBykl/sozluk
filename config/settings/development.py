
from .base import *

SECRET_KEY = '1234'

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

DJANGO_SUPERUSER_PASSWORD = "qazwsxç1234"