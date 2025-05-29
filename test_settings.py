# Test settings for Django MKS project
# This file is used specifically for running tests

from .settings import *
import os

# Test database - use SQLite for speed
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',  # In-memory database for faster tests
    }
}

# Speed up tests
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',  # Fast but insecure - only for tests
]

# Disable migrations for faster test runs
class DisableMigrations:
    def __contains__(self, item):
        return True
    
    def __getitem__(self, item):
        return None

MIGRATION_MODULES = DisableMigrations()

# Test-specific settings
DEBUG = False
TEMPLATE_DEBUG = False

# Disable logging during tests to reduce noise
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

# Email backend for tests
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

# Cache backend for tests
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

# Media files for tests
MEDIA_ROOT = os.path.join(BASE_DIR, 'test_media')

# Static files for tests
STATIC_ROOT = os.path.join(BASE_DIR, 'test_static')

# Test runner
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

# Timezone for tests
USE_TZ = True
TIME_ZONE = 'Europe/Vienna'

# Disable CSRF for API tests
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False

# Test-specific apps (if any)
# INSTALLED_APPS += ['test_app']

print("✅ Test settings loaded - using in-memory SQLite database")
