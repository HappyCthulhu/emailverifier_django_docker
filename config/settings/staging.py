from .base import *

DEBUG = True

ALLOWED_HOSTS = []
CORS_ORIGIN_ALLOW_ALL = True

DATABASES = {
    'default': {
        'NAME': 'email_verifier',
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'USER': 'dev',
        'PASSWORD': 'dev',
        'HOST': '127.0.0.1',
        'PORT': 5432,
    },
}

SITE_ID = 1

INSTALLED_APPS += [
    'drf_yasg',
]

# REDIS related settings
REDIS_HOST = 'localhost'
REDIS_PORT = '6379'
BROKER_URL = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/0'
BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}
CELERY_RESULT_BACKEND = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/0'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': ROOT_DIR.parent / 'cache' / 'default',
        'TIMEOUT': 60 * 60 * 24 * 6,
    },
}

