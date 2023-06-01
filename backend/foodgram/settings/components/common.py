import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent

load_dotenv()

load_dotenv(os.path.join(BASE_DIR.parent, 'infra/.env'), verbose=True)

SECRET_KEY = os.environ.get('SECRET_KEY', default='H3R3-Y0UR-S3CR3T-K3Y')

DEBUG = os.environ.get('TEST_ENVIRONMENT', default=False) == 'True'

ALLOWED_HOSTS = [
    os.environ.get('ALLOWED_HOSTS', default='*'),
    'localhost',
    '127.0.0.1',
]

ROOT_URLCONF = "foodgram.urls"

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'foodgram.wsgi.application'

STATIC_URL = '/static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'users.User'
