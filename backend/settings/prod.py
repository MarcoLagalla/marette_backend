""" Production Settings """
import json
import os
import dj_database_url
from django.core.exceptions import ImproperlyConfigured

from .dev import *


with open(os.path.join(BASE_DIR, 'secrets.json')) as secrets_file:
    secrets = json.load(secrets_file)


def get_secret(setting, secrets=secrets):
    """Get secret setting or fail with ImproperlyConfigured"""
    try:
        return secrets[setting]
    except KeyError:
        raise ImproperlyConfigured("Set the {} setting".format(setting))

############
# DATABASE #
############
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': get_secret('DB_NAME'),
        'USER': get_secret('DB_USER'),
        'PASSWORD': get_secret('DB_PWD'),
        'HOST': get_secret('DB_HOST'),
        'PORT': '5432',
    }
}



############
# SECURITY #
############
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



DEBUG = True #bool(os.getenv('DJANGO_DEBUG', ''))

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', SECRET_KEY)

# Set to your Domain here (eg. 'django-vue-template-demo.herokuapp.com')
ALLOWED_HOSTS = ['*']


CORS_ORIGIN_ALLOW_ALL = True
# If this is used then `CORS_ORIGIN_WHITELIST` will not have any effect
CORS_ALLOW_CREDENTIALS = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
#SECURE_SSL_REDIRECT = True
SITE_ID = 1


AWS_ACCESS_KEY_ID = get_secret('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = get_secret('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = 'marette-static-bucket'
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_LOCATION = 'static'

# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'marette_backend/static'),
# ]
STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
MEDIA_URL = 'https://%s/media/' % (AWS_S3_CUSTOM_DOMAIN)
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
DEFAULT_FILE_STORAGE = 'backend.settings.storage_backends.MediaStorage'

# EMAIL_BACKEND = 'django_amazon_ses.EmailBackend'
#
# AWS_SES_ACCESS_KEY_ID = get_secret('AWS_SES_ACCESS_KEY_ID')
# AWS_SES_SECRET_ACCESS_KEY = get_secret('AWS_SES_SECRET_ACCESS_KEY')
#
# AWS_SES_REGION = 'eu-central-1'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'marette.dev@gmail.com'
EMAIL_HOST_PASSWORD = 'marette123'
EMAIL_PORT = 587

DOMAIN = 'marette.ovh'
EMAIL_RESET_PASSWORD_BASE_URL = f'https://{DOMAIN}/resetpass'
EMAIL_ACTIVATE_ACCOUNT_BASE_URL = f'https://{DOMAIN}/activate'
