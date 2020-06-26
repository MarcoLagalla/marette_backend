"""
Django settings for project project.

Generated by 'django-admin startproject' using Django 2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
#from . import private_settings

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
SETTINGS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(SETTINGS_DIR)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'verybadsecret!!!'    # todo SECRET_KEY = private_settings.key

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'admin_reorder',
    'localflavor',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',  # < Per Whitenoise, to disable built in
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'django_extensions',
    'backend.webapp.apps.WebappConfig',
    'backend.account.apps.AccountConfig',
    'phonenumber_field',
    'rest_framework.authtoken',
    'django_resized',
    'django_cleanup',
    'storages',
]


MIDDLEWARE = [
    'admin_reorder.middleware.ModelAdminReorder',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
}

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Add dist to
        'DIRS': ['public'],    #'DIRS': [os.path.join(BASE_DIR, 'webapp/templates')],
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

WSGI_APPLICATION = 'backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'it-it'
TIME_ZONE = 'Europe/Rome'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

# When Vue Builds, path will be `/static/css/...` so we will have Django Serve
# In Production, it's recommended use an alternative approach such as:
# http://whitenoise.evans.io/en/stable/django.html?highlight=django

MIDDLEWARE_CLASSES = (
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.locale.LocaleMiddleware',
)

STATIC_URL = '/static/'
# Place static in the same location as webpack build files
STATIC_ROOT = os.path.join(BASE_DIR, 'public', 'static')
STATICFILES_DIRS = []

MEDIA_ROOT = os.path.join(BASE_DIR, 'public', 'media')
MEDIA_URL = '/media/'
##########
# STATIC #
##########

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Insert Whitenoise Middleware at top but below Security Middleware
# MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware',)
# http://whitenoise.evans.io/en/stable/django.html#make-sure-staticfiles-is-configured-correctly


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

#DATE_INPUT_FORMATS = ['%d/%m/%Y']

CRISPY_TEMPLATE_PACK = 'bootstrap4'

PHONENUMBER_DB_FORMAT = 'NATIONAL'
PHONENUMBER_DEFAULT_REGION = 'IT'


ADMIN_REORDER = (
    # Keep original label and models
    'sites',

    # Reorder app models authtoken.models import Token
    {'app': 'auth', 'models': ('auth.User', 'auth.Group', 'authtoken.Token'),},
    {'app': 'account', 'models': ('account.Customer', 'account.Business')},
    {'app': 'webapp', 'label': 'Marette', 'models': ('webapp.Restaurant','webapp.Category',)},
    {'app': 'webapp', 'label': 'Restaurant',
     'models': ('webapp.Product',
                'webapp.ProductDiscount',
                'webapp.RestaurantDiscount',
                'webapp.ProductTag',
                'webapp.Menu',
                'webapp.MenuEntry',
                'webapp.Picture',
                'webapp.CustomerVote',)},
    {'app': 'webapp', 'label': 'RestaurantComponents',
     'models': ('webapp.RestaurantComponents',
                'webapp.HomeComponent',
                'webapp.MenuComponent',
                'webapp.EventiComponent',
                'webapp.GalleriaComponent',
                'webapp.VetrinaComponent',
                'webapp.ContattaciComponent',
                'webapp.OrarioApertura',
                'webapp.GiornoApertura',
                'webapp.FasciaOraria')},
    {'app': 'webapp', 'label': 'MarketPlace', 'models': ('webapp.Order', 'orders.OrderNotification',)},
)

DJANGORESIZED_DEFAULT_FORMAT_EXTENSIONS = {'PNG': ".png"}

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


EMAIL_BACKEND = 'django_amazon_ses.EmailBackend'

AWS_SES_ACCESS_KEY_ID = 'AKIAQNN5ZBLSYTGMMBVR'
AWS_SES_SECRET_ACCESS_KEY = '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'

AWS_SES_REGION = 'eu-central-1'

EMAIL_RESET_PASSWORD_BASE_URL = 'http://localhost:8080/resetpass'
EMAIL_ACTIVATE_ACCOUNT_BASE_URL = 'http://localhost:8080/activate'