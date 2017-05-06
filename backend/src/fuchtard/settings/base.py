"""
Django settings for fuchtard project.

Generated by 'django-admin startproject' using Django 1.9.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
from envparse import env

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY', default='9t!sc1+#0zh@%c+xyiq&dlg_ri-_*7jfl!tg!lt#c0+1s9e6%p')
HASHID_FIELD_SALT = env('HASHID_FIELD_SALT', default='6^y3*fv!fq4z@n2-i!hy-hgi0x*+3qmf@ylqtkv&x932(-8wi+')

HASHID_FIELD_ALLOW_INT = False


DEBUG = False

INTERNAL_IPS = [
    '127.0.0.1',
]

ALLOWED_HOSTS = [
    'localhost',
    'maxisushi.kz',
    'www.maxisushi.kz',
    'mechanar.maxisushi.kz',
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django_extensions',
    'adminsortable',
    'corsheaders',
    'debug_toolbar',
    'rest_framework',
    'rest_framework.authtoken',
    'main',
    'food',
    'order',
    'api',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'fuchtard.urls'

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
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'fuchtard.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'fuchtard',
        'USER': 'fuchtard',
        'PASSWORD': 'fuchtard',
        'HOST': 'db',
        'PORT': '',
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Asia/Almaty'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, '..', '..', 'static_content', 'static', )

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, '..', '..', 'static_content', 'media', )


ADMINS = [
    ('robox', 'roboxv+maxi@gmail.com')
]

# TELEGRAM BOT
TELEGRAM_BOT_API_TOKEN = env('TELEGRAM_BOT_API_TOKEN', default='248042210:AAF7O2ryYuhxIvqegx3U0pEPrPTUrgPmvFA')
TELEGRAM_BOT_NOTIFICATION_CHANNEL_ID = '-1001067984566'

# EMAIL
EMAIL_BACKEND = 'sparkpost.django.email_backend.SparkPostEmailBackend'
DEFAULT_FROM_EMAIL = 'noreply@maxisushi.kz'
SERVER_EMAIL = 'server@maxisushi.kz'

SPARKPOST_API_KEY = env('SPARKPOST_API_KEY', default='fc52712a253df3d28d69fdb10fd521271c36eb09')
FUCHTARD_ORDERS_EMAIL = 'order@maxisushi.kz'
FUCHTARD_NOREPLY_EMAIL = 'Maxi Sushi <noreply@maxisushi.kz>'

SITE_DOMAIN = 'maxisushi.kz'
# Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissions',
    ],
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
}

# LOGGING
LOGGING = {
    'version': 1,
    'handlers': {
        'mail_admins': {
            'class': 'main.utils.CustomAdminEmailHandler',
            'level': 'ERROR',
        }
    },
    'loggers': {
        'django': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
        },
    },
}