from .base import *

'''Production setting file, assigned in main function'''

DEBUG = False
ALLOWED_HOSTS = [ IP_ADDRESS ]

# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
