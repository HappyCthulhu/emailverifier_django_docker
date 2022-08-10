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

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
        'json': {
            'format': '{ "loggerName":"%(name)s", "timestamp":"%(asctime)s", "fileName":"%(filename)s", "logRecordCreationTime":"%(created)f", '
                      '"functionName":"%(funcName)s", "levelNo":"%(levelno)s", "lineNo":"%(lineno)d", "time":"%(msecs)d", "levelName":"%(levelname)s", "message":"%(message)s"}',
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'sql.file': {
            'level': 'DEBUG',
            'class': 'common.logging.Utf8FileHandler',
            'filename': ROOT_DIR.parent / 'log' / 'sql.log',
        },
        'error.file': {
            'level': 'ERROR',
            'class': 'common.logging.Utf8FileHandler',
            'filename': ROOT_DIR.parent / 'log' / 'error.log',
        },
    },
    'loggers': {
        'django.db.backends': {
            'level': 'DEBUG',
            # 'handlers': ['console'],
            'handlers': ['sql.file', ],
        },
        'default': {
            'level': 'DEBUG',
            # 'handlers': ['console', 'loggly', ]
            'handlers': ['console', 'error.file']
        },
    }
}

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

PROXY_TOKEN = 'vigd38lm64'
PROXY_DOMAIN = 'http://127.0.0.1:8031/'