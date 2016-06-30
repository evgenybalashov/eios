from .base import *


DB_PASS = get_env_variable("DB_PASS")
DEBUG = True

ALLOWED_HOSTS = ['eios.muctr.ru']

DATABASES = {
    "default": {
    "ENGINE": "django.db.backends.mysql",
    "NAME": "eios",
    "USER": "eiosusr",
    "PASSWORD": DB_PASS,
    "HOST": "dbs-pub.muctr.inside",
    "PORT": "",
    }
}


STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "staticfiles", "static")

MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), "staticfiles", "media")