""" Production Settings """

import os
import dj_database_url
from .dev import *

############
# DATABASE #
############
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'marette_db',
        'USER': 'marette',
        'PASSWORD': 'marette_password_123',
        'HOST': 'ls-396698a44ff6bd681eefdd494452ba939b2513fe.coqd0e1zy3qu.eu-central-1.rds.amazonaws.com',
        'PORT': '5432',
    }
}



############
# SECURITY #
############

DEBUG = True #bool(os.getenv('DJANGO_DEBUG', ''))

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', SECRET_KEY)

# Set to your Domain here (eg. 'django-vue-template-demo.herokuapp.com')
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '18.156.16.255', 'marette.ovh']


CORS_ORIGIN_ALLOW_ALL = True
# If this is used then `CORS_ORIGIN_WHITELIST` will not have any effect
CORS_ALLOW_CREDENTIALS = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SITE_ID = 1



AWS_ACCESS_KEY_ID = 'AKIAQNN5ZBLS3KC6HOLY'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'marette-static'
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_LOCATION = 'static'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'marette_backend/static'),
]
STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
DEFAULT_FILE_STORAGE = 'backend.settings.storage_backends.MediaStorage'

EMAIL_BACKEND = 'django_amazon_ses.EmailBackend'

AWS_SES_ACCESS_KEY_ID = 'AKIAQNN5ZBLSYTGMMBVR'
AWS_SES_SECRET_ACCESS_KEY = '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'

AWS_SES_REGION = 'eu-central-1'