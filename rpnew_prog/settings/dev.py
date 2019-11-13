from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'kiq_vi+kuuw6wi#amgb*8l!l$gl+e*vaj%4eidp#m3bi-@*)@f'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*']

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

WSGI_APPLICATION = 'rpnew_prog.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'rpnew_db',
        'USER': 'postgres',
        'PASSWORD': '09w5t43w',
        'HOST': 'localhost',
        'PORT': '',
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_ROOT = os.path.join(APPLICATION_DIR, 'static')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(APPLICATION_DIR, 'media')
MEDIA_URL = '/media/'

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
BASE_URL = 'https://rifondazionepodistica.it'


try:
    from .local import *
except ImportError:
    pass