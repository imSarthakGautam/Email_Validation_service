# config/settings/dev.py

from .base import *

DEBUG = False

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Optionally: use a different DB, email backend, etc.
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
