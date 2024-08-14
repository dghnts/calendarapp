from .base import *
import os

SECRET_KEY = os.getenv("SECRET_KEY")

DEBUG = True

ALLOWED_HOSTS = []

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

STATIC_URL = "/static/"

EMAIL_BACKEND   = "django.core.mail.backends.console.EmailBackend"
