from .base import *

'''Development setting file, assigned in main function'''

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']

# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
