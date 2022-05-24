from .base import *

'''Development setting file, assigned in main function'''

DEBUG = True

LOCAL = '127.0.0.1'

ALLOWED_HOSTS = [LOCAL]

# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
