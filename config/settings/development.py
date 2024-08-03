from .base import *
import os

SECRET_KEY = "b#s*_o(3t3ai_k(c5po@h7a=nj5#vjkd3u7ckhnx@)mi=8fn67"

SECRET_KEY = 'django-insecure-1!-kgq*o@m26z&32k%(*m8ouez6(z7&)_9_*r-5_y)ytsk_=c!'


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
