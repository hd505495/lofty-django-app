"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 4.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import logging.config
import os
from django.utils.log import DEFAULT_LOGGING

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-q+bvyo!nw2(4@(f*es+w50iq85y=r(&r$^=l+$9v!vyavk$26d"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "api",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    # "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "app.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "app.wsgi.application"
ASGI_APPLICATION = "app.asgi.application"


LOGGING_CONFIG = None

LOGLEVEL = os.environ.get('LOGLEVEL', 'info').upper()

# logging.config.dictConfig({
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'default': {
#             # exact format is not important, this is the minimum information
#             'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
#         },
#         # 'django.server': DEFAULT_LOGGING['formatters']['django.server'],
#     },
#     'handlers': {
#         # console logs to stderr
#         'console': {
#             'class': 'logging.StreamHandler',
#             'formatter': 'default',
#         },
#         # 'logfile': {
#         #     'class': 'logging.FileHandler',
#         #     'filename': 'logs/app.log'
#         # },
#         'logfile': {
#             # 'level':'DEBUG',
#             'class':'logging.handlers.RotatingFileHandler',
#             'filename': 'logs/app.log',
#             'maxBytes': 10485760, # 10 * 1024 * 1024
#             'backupCount': 5,
#             'formatter': 'default',
#         },
#         'requestlogfile': {
#             # 'level':'DEBUG',
#             'class':'logging.handlers.RotatingFileHandler',
#             'filename': 'logs/app.requests.log',
#             'maxBytes': 10485760, # 10 * 1024 * 1024
#             'backupCount': 5,
#             'formatter': 'default',
#         },
#         # 'django.server': DEFAULT_LOGGING['handlers']['django.server'],
#     },
#     'loggers': {
#         # default for all undefined Python modules
#         # '': {
#         #     'level': 'WARNING',
#         #     'handlers': ['console'],
#         #     'propagate': True,
#         # },
#         'django': {
#             'handlers': ['logfile'],
#             'level': 'DEBUG',
#             'propagate': True,
#         },
#         'django.request': {
#             'handlers': ['requestlogfile'],
#             'level': 'DEBUG',
#             'propagate': True,
#         },
#         # Our application code
#         'app': {
#             'level': LOGLEVEL,
#             'handlers': ['logfile'],
#             # Avoid double logging because of root logger
#             'propagate': False,
#         },
#         # Default runserver request logging
#         # 'django.server': DEFAULT_LOGGING['loggers']['django.server'],
#     },
# })


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'db',
        'PORT': 5432,
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
