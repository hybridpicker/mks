# Fixed test_settings.py - Complete test configuration
from mks.settings import *

# Override database settings for testing with all required keys
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mks',
        'USER': 'postgres',
        'PASSWORD': 'Ax9kl3',
        'HOST': 'localhost',
        'PORT': '5432',
        'TEST': {
            'NAME': 'test_mks',
            'USER': 'postgres',
            'PASSWORD': 'Ax9kl3',
            'HOST': 'localhost',
            'PORT': '5432',
            'CHARSET': None,
            'COLLATION': None,
            'MIRROR': None,
            'CREATE_DB': True,
        },
        'ATOMIC_REQUESTS': False,
        'AUTOCOMMIT': True,
        'CONN_MAX_AGE': 0,
        'OPTIONS': {},
    }
}

# Disable debug mode for tests
DEBUG = False

# Enable synchronous processing for tests
TESTING = True

# Faster test execution
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# Disable logging during tests
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'null': {
            'class': 'logging.NullHandler',
        },
    },
    'root': {
        'handlers': ['null'],
    },
}
