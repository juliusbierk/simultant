from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

SECRET_KEY = '_'
DEBUG = False
INSTALLED_APPS = ['db.db.DbConfig']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / '../db.sqlite',
    }
}

