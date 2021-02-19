from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent

SECRET_KEY = '_'
DEBUG = False
INSTALLED_APPS = ['db.DbConfig' if
		  os.environ.get('manage') == 'true' else 'db.db.DbConfig']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / '../db.sqlite',
    }
}

