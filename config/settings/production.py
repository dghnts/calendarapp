from .base import *
import os

DEBUG = False

# ここにメール送信設定を入力する(Sendgridを使用する場合)
EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"

EMAIL_HOST = "ここにメールのホストを書く"

DEFAULT_FROM_EMAIL = "ここに送信元メールアドレスを指定"

if "SENDGRID_API_KEY" in os.environ:
    SENDGRID_API_KEY = os.environ["SENDGRID_API_KEY"]
else:
    SENDGRID_API_KEY = "ここにAPIキーを入力"

SENDGRID_SANDBOX_MODE_IN_DEBUG = False

ALLOWED_HOSTS = ["shedule-manager.com"]

CSRF_TRUSTED_ORIGINS    = [ "https://shedule-manager.com" ]

SECRET_KEY = os.environ["SECRET_KEY"]
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.environ["POSTGRESQL_DB_NAME"],
        "USER": os.environ["POSTGRESQL_DB_USER"],
        "PASSWORD": os.environ["POSTGRESQL_DB_PASS"],
        "HOST": "localhost",
        "PORT": "",
    }
}

STATIC_ROOT = "/var/www/{}/static".format(BASE_DIR.name)

# 下記はファイルのアップロード機能を有する場合のみ
MEDIA_ROOT = "/var/www/{}/media".format(BASE_DIR.name)
