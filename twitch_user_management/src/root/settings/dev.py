from __future__ import absolute_import

import django
from decouple import Csv

from .base import *  # NOSONAR

DEBUG = True
BUILD_NUMBER = config('BUILD_NUMBER', default='', cast=str)
# Sessions & CSRF
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=Csv())
CSRF_TRUSTED_ORIGINS = config('CSRF_TRUSTED_ORIGINS', default='http://localhost', cast=Csv())
CSRF_COOKIE_HTTPONLY = config('CSRF_COOKIE_HTTPONLY', default=True, cast=bool)
CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', default=True, cast=bool)
SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default=True, cast=bool)
SESSION_COOKIE_AGE = config('SESSION_COOKIE_AGE', default=60 * 60 * 8, cast=int)
CSRF_COOKIE_SAMESITE = config('CSRF_COOKIE_SAMESITE', cast=str, default='Strict')
SESSION_COOKIE_SAMESITE = config('SESSION_COOKIE_SAMESITE', cast=str, default='Strict')
# Postgres DB
DATABASES['default']['HOST'] = config('DB_HOST', default='localhost')
DATABASES['default']['PORT'] = config('DB_PORT', default='5312')
DATABASES['default']['NAME'] = config('DB_NAME', default='samta')
DATABASES['default']['USER'] = config('DB_USER', default='usr_samta')
DATABASES['default']['PASSWORD'] = config('DB_PASSWORD', default='123456')

CACHES['default']['LOCATION'] = config('CACHE_LOCATION', cast=str, default='localhost:11245')
SECRET_KEY = config(
    'SECRET_KEY',
    cast=str,
    default='$5uq@2)dvyk6r7@j(p2e*rs1%_vjf7que!zpak4-ht7v21u4f#',  # NOSONAR
)

# Debug Toolbar Configurations
INSTALLED_APPS += ['debug_toolbar']

MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')
INTERNAL_IPS = ['127.0.0.1']
DEBUG_TOOLBAR_CONFIG = {'SHOW_COLLAPSED': True, 'SHOW_TEMPLATE_CONTEXT': True, 'TOOLBAR_LANGUAGE': 'en'}

# Logging Configuration
DJANGO_LOG_LEVEL = config('DJANGO_LOG_LEVEL', default='INFO', cast=str)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'file_formatter': {
            'format': '{levelname} [{asctime}]: {message} [{name} {funcName} line:{lineno}]\n',
            'datefmt': '%Y-%m-%d %H:%M',
            'style': '{',
        },
        'json': {'()': 'root.loggers.JsonFormatter', 'datefmt': '%Y-%m-%d %H:%M:%S'},
    },
    'filters': {
        'django_server_messages': {
            '()': 'root.loggers.IgnoreDjangoServer',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': DJANGO_LOG_LEVEL,
            'class': 'rich.logging.RichHandler',
            'filters': ['django_server_messages', 'require_debug_true'],
            'rich_tracebacks': True,
            'tracebacks_suppress': [django],
            'show_path': False,
            'tracebacks_show_locals': True,
            'log_time_format': '[%Y-%m-%d %H:%M]',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': DJANGO_LOG_LEVEL,
        },
        'django': {
            'handlers': ['console'],
            'level': DJANGO_LOG_LEVEL,
        },
        'django.security.*': {
            'handlers': ['console'],
            'level': DJANGO_LOG_LEVEL,
        },
        'django.security.csrf': {
            'handlers': ['console'],
            'level': DJANGO_LOG_LEVEL,
        },
    },
}

SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
