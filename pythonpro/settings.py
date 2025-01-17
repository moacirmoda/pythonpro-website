"""
Django settings for pythonpro project.

Generated by 'django-admin startproject' using Django 2.0b1.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

import os
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from functools import partial

import sentry_sdk
from decouple import Csv, config
from dj_database_url import parse as dburl
from sentry_sdk.integrations.django import DjangoIntegration

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default=[], cast=Csv())

# Control subscriptions ads and payment.
SUBSCRIPTIONS_OPEN = config('SUBSCRIPTIONS_OPEN', cast=bool)

PAGARME_CRYPTO_KEY = config('PAGARME_CRYPTO_KEY')
PAGARME_API_KEY = config('PAGARME_API_KEY')


PAGSEGURO_PAYMENT_PLAN = config('PAGSEGURO_PAYMENT_PLAN')

# Email Configuration

DEFAULT_FROM_EMAIL = 'renzo@python.pro.br'

EMAIL_BACKEND = config('EMAIL_BACKEND')
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')

# Login Config

LOGIN_REDIRECT_URL = LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = 'login'

# Application definition

INSTALLED_APPS = [
    'pythonpro.core',
    'pythonpro.discourse',
    'pythonpro.modules',
    'pythonpro.promos',
    'pythonpro.payments',
    'pythonpro.cohorts',
    'pythonpro.mailchimp',
    'pythonpro.dashboard',
    'rolepermissions',
    'ordered_model',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'collectfast',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'pythonpro.core.middleware.SSLMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROLEPERMISSIONS_MODULE = 'pythonpro.core.roles'

if DEBUG:
    INSTALLED_APPS.append('debug_toolbar')
    MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')
    INTERNAL_IPS = ['127.0.0.1']

# Discourse config
DISCOURSE_BASE_URL = 'https://forum.python.pro.br/'
DISCOURSE_SSO_SECRET = config('DISCOURSE_SSO_SECRET')

ROOT_URLCONF = 'pythonpro.urls'

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
                'pythonpro.core.context_processors.global_settings',
                'pythonpro.modules.context_processors.global_settings',
                'pythonpro.cohorts.context_processors.global_settings',
                'pythonpro.payments.context_processors.global_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'pythonpro.wsgi.application'

# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
default_db_url = 'sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')

if 'localhost' not in ALLOWED_HOSTS:
    dburl = partial(dburl, conn_max_age=600, ssl_require=True)

DATABASES = {
    'default': config('DATABASE_URL', default=default_db_url, cast=dburl),
}

# Password validation
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators

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

AUTH_USER_MODEL = 'core.User'

# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Configuration for dev environment
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles')
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
COLLECTFAST_ENABLED = False

# STORAGE CONFIGURATION IN S3 AWS
# ------------------------------------------------------------------------------
# Uploaded Media Files
# ------------------------------------------------------------------------------
AWS_ACCESS_KEY_ID = config('DJANGO_AWS_ACCESS_KEY_ID', default=False)
if AWS_ACCESS_KEY_ID:  # pragma: no cover
    COLLECTFAST_ENABLED = True
    INSTALLED_APPS.append('s3_folder_storage')
    INSTALLED_APPS.append('storages')
    AWS_SECRET_ACCESS_KEY = config('DJANGO_AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = config('DJANGO_AWS_STORAGE_BUCKET_NAME')
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400', }
    AWS_PRELOAD_METADATA = True
    AWS_AUTO_CREATE_BUCKET = False
    AWS_QUERYSTRING_AUTH = True
    AWS_S3_CUSTOM_DOMAIN = None

    AWS_DEFAULT_ACL = 'private'

    # AWS cache settings, don't change unless you know what you're doing:
    AWS_EXPIRY = 60 * 60 * 24 * 7

    # Revert the following and use str after the above-mentioned bug is fixed in
    # either django-storage-redux or boto
    control = f'max-age={AWS_EXPIRY:d}, s-maxage={AWS_EXPIRY:d}, must-revalidate'

    # Upload Media Folder
    DEFAULT_FILE_STORAGE = 's3_folder_storage.s3.DefaultStorage'
    DEFAULT_S3_PATH = 'media'
    MEDIA_ROOT = f'/{DEFAULT_S3_PATH}/'
    MEDIA_URL = f'//s3.amazonaws.com/{AWS_STORAGE_BUCKET_NAME}/{DEFAULT_S3_PATH}/'

    # Static Assets
    # ------------------------------------------------------------------------------
    STATICFILES_STORAGE = 's3_folder_storage.s3.StaticStorage'
    STATIC_S3_PATH = 'static'
    STATIC_ROOT = f'/{STATIC_S3_PATH}/'
    STATIC_URL = f'//s3.amazonaws.com/{AWS_STORAGE_BUCKET_NAME}/{STATIC_S3_PATH}/'
    ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

# ------------------------------------------------------------------------------

# Configuring Sentry
SENTRY_DSN = config('SENTRY_DSN', default=None)

if SENTRY_DSN:  # pragma: no cover
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()]
    )

# Mailchimp Configuration

MAILCHIMP_API_KEY = config('MAILCHIMP_API_KEY')
MAILCHIMP_LIST_ID = config('MAILCHIMP_LIST_ID')
