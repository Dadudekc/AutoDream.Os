"""
Django Settings for Testing - V2 Compliant Test Configuration
Minimal Django settings for test environment
V2 COMPLIANCE: Under 300-line limit, minimal configuration

@version 1.0.0 - V2 COMPLIANCE DJANGO SETTINGS
@license MIT
"""


# Django settings
SECRET_KEY = 'test-secret-key-for-testing-only'

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

USE_TZ = True

# Test-specific settings
TEST_RUNNER = 'django.test.runner.DiscoverRunner'
