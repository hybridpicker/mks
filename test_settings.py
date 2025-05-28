# test_settings.py - Non-interactive test settings
from mks.settings import *

# Override database settings for testing to avoid prompts
DATABASES['default']['TEST'] = {
    'NAME': 'test_mks_auto',
}

# Set to use in-memory SQLite for tests (fastest option)
DATABASES['default'] = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': ':memory:',
    'TEST': {
        'NAME': ':memory:',
    }
}

# Disable debug mode for tests
DEBUG = False

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
