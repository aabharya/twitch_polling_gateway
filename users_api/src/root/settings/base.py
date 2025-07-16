"""
Django settings for user management project.
"""
from datetime import timedelta
from pathlib import Path

from decouple import Csv, config
from django.contrib.messages import constants as message_constants

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
ROOT_DIR = BASE_DIR.parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'e$8ajas8inzv%cn-r8+%)rq&mrmsn9ua=-u+lzqwf6sl&*d(6m'  # NOSONAR
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

BUILD_NUMBER = ''

ALLOWED_HOSTS = []
CSRF_TRUSTED_ORIGINS = []

# Application definition
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
]

THIRD_PARTY_APPS = [
    'django_extensions',
    'django_celery_beat',
    'django_celery_results',
    'rest_framework',
    'drf_spectacular',
    'drf_spectacular_sidecar',
    'corsheaders',
    'djoser',
]

USER_MANAGEMENT_APPS = [
    'users',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + USER_MANAGEMENT_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'root.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'root.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
    },
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Django Extensions Config
SHELL_PLUS = 'ipython'
SHELL_PLUS_PRINT_SQL = True
SHELL_PLUS_POST_IMPORTS = [
    'import datetime',
    'import json',
    'from django.core.files.storage import default_storage'
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

USE_I18N = True

USE_L10N = True

USE_TZ = True
TIME_ZONE = 'UTC'

DEFAULT_DATE_ONLY_FORMAT = '%Y-%m-%d'
DEFAULT_DATETIME_FORMAT = '%Y-%m-%d %H:%M'

# System Checks
SILENCED_SYSTEM_CHECKS = []

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = ROOT_DIR / 'static'

MEDIA_URL = '/uploads/'
MEDIA_ROOT = ROOT_DIR / 'uploads'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Rest framework
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 100,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticated',),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'EXCEPTION_HANDLER': 'root.exceptions.api_exception_handler',
    'DEFAULT_RENDERER_CLASSES': (
        'root.renderers.ORJSONRenderer',
        'rest_framework.renderers.JSONRenderer',
    )
}

SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('JWT',),
    'ACCESS_TOKEN_LIFETIME': timedelta(seconds=config('JWT_LIFETIME', default=300, cast=int)),
    'ALGORITHM': config('JWT_ALGORITHM', default='HS256'),
    'SIGNING_KEY': config('JWT_SIGNING_KEY', default='', cast=str).replace('\\n', '\n'),
    'USER_ID_FIELD': config('JWT_USER_KEY', default='', cast=str),
    'USER_ID_CLAIM': config('JWT_USER_KEY', default='', cast=str),
}

DJOSER = {
    'TOKEN_MODEL': None,
    'SERIALIZERS': {'user_create': 'users.api.v1.serializers.UserCreateSerializer'},
}


GATEWAY_PREFIX = config('GATEWAY_PREFIX', default='gateway/', cast=str)

GATEWAY_CONSUMERS = config('GATEWAY_CONSUMERS', default='', cast=Csv())

GATEWAY_USER_CREATE_TASK_NAME = config('GATEWAY_USER_CREATE_TASK_NAME', default='', cast=str)
GATEWAY_USER_UPDATE_TASK_NAME = config('GATEWAY_USER_UPDATE_TASK_NAME', default='', cast=str)

config('CORS_ALLOWED_ORIGINS', default='http://localhost:3000,http://127.0.0.1:3000', cast=Csv())
SPECTACULAR_SETTINGS = {
    'TITLE': 'User Management API',
    'DESCRIPTION': 'Endpoints to consume User Management API',
    'SCHEMA_PATH_PREFIX': f'/{GATEWAY_PREFIX}api/auth/',
    'VERSION': '1.0.0',
    'SWAGGER_UI_DIST': 'SIDECAR',
    'SWAGGER_UI_FAVICON_HREF': 'SIDECAR',
    'REDOC_DIST': 'SIDECAR',
    'SERVE_INCLUDE_SCHEMA': False,
}

# CORS Settings
CORS_ALLOWED_ORIGINS = config('CORS_ALLOWED_ORIGINS', default='http://localhost:3000,http://127.0.0.1:3000', cast=Csv())
CORS_ALLOW_CREDENTIALS = config('CORS_ALLOW_CREDENTIALS', default=True, cast=bool)
CORS_ALLOW_ALL_ORIGINS = config('CORS_ALLOW_ALL_ORIGINS', default=False, cast=bool)


DJANGO_LOG_LEVEL = 'INFO'

# Logging Configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': DJANGO_LOG_LEVEL,
            'class': 'logging.StreamHandler',
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

# Sessions and auth
AUTH_USER_MODEL = 'users.User'
AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.AllowAllUsersModelBackend']
SESSION_COOKIE_NAME = 'user_session'

CACHES = {
    'default': {
        'BACKEND': config('CACHE_BACKEND', default='django.core.cache.backends.redis.RedisCache', cast=str),
        'LOCATION': config('CACHE_LOCATION', default='redis://127.0.0.1:63790/0', cast=str),
    }
}

MESSAGE_TAGS = {
    message_constants.DEBUG: 'debug',
    message_constants.INFO: 'info',
    message_constants.SUCCESS: 'success',
    message_constants.WARNING: 'warning',
    message_constants.ERROR: 'danger',
}


# Celery Configs
CELERY_BROKER_URL = config('CELERY_BROKER_URL', default='redis://:@localhost:63790/0', cast=str)
CELERY_TIMEZONE = 'Asia/Tehran'
CELERY_RESULT_BACKEND = config('CELERY_RESULT_BACKEND', default='redis://:@localhost:63790/0', cast=str)
