from .base import *


DB_PASS = get_env_variable("DB_PASS")
DEBUG = False

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