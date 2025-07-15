from .base import *  # NOSONAR

DEBUG = False
BUILD_NUMBER = config('BUILD_NUMBER', default='', cast=str)

# CORS
CORS_ORIGIN_ALLOW_ALL = config('CORS_ALLOWED_ORIGINS', default=True, cast=bool)
CORS_ALLOWED_ORIGINS = config('CORS_ALLOWED_ORIGINS', default='', cast=Csv())

# Sessions & CSRF
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='*', cast=Csv())
CSRF_TRUSTED_ORIGINS = config('CSRF_TRUSTED_ORIGINS', default='http://localhost', cast=Csv())
CSRF_COOKIE_HTTPONLY = config('CSRF_COOKIE_HTTPONLY', default=True, cast=bool)
CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', default=True, cast=bool)
SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default=True, cast=bool)
SESSION_COOKIE_HTTPONLY = config('SESSION_COOKIE_HTTPONLY', default=True, cast=bool)
SESSION_COOKIE_AGE = config('SESSION_COOKIE_AGE', default=60 * 60 * 1, cast=int)
CSRF_COOKIE_SAMESITE = config('CSRF_COOKIE_SAMESITE', cast=str, default='Strict')
SESSION_COOKIE_SAMESITE = config('SESSION_COOKIE_SAMESITE', cast=str, default='Strict')
# DB
DATABASES['default']['HOST'] = config('DB_HOST', default='db')
DATABASES['default']['PORT'] = config('DB_PORT', default='5432')
DATABASES['default']['NAME'] = config('DB_NAME', default='user_management')
DATABASES['default']['USER'] = config('DB_USER', default='user_management')
DATABASES['default']['PASSWORD'] = config('DB_PASSWORD', default='123456')

CACHES['default']['LOCATION'] = config('CACHE_LOCATION', cast=str, default='memcached:11211')
SECRET_KEY = config(
    'SECRET_KEY',
    cast=str,
    default='0z)dnuddaqcr#x=15li+(*_-ip-4t^v@8k$m6h8z1a_w5)#@j_',  # NOSONAR
)
STATIC_ROOT = config('STATIC_ROOT', cast=str, default='/static_root/')
MEDIA_ROOT = config('MEDIA_ROOT', cast=str, default='/media_root/')

# Logging Configuration
DJANGO_LOG_LEVEL = config('DJANGO_LOG_LEVEL', default='INFO', cast=str)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'timestamped': {'format': '[{asctime}] [{levelname}] {message}', 'datefmt': '%Y-%m-%d %H:%M', 'style': '{'}
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'minio_stat': {
            '()': 'root.loggers.IgnoreMinioStatObject',
        },
    },
    'handlers': {
        'console': {
            'level': DJANGO_LOG_LEVEL,
            'class': 'logging.StreamHandler',
            'filters': ['require_debug_false', 'minio_stat'],
            'formatter': 'timestamped',
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
