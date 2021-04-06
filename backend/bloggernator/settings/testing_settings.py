from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'some super secret key'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


MEDIA_URL = '/testing/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'testing/media')


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# EMAIL
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = ''
EMAIL_PORT = '587'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False


# GOOGLE RECAPTCHA
GOOGLE_RECAPTCHA_PUBLIC_KEY = ''
GOOGLE_RECAPTCHA_SECRET_KEY = ''


CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = (
    'http://localhost:4200',
)