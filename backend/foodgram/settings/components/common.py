import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent

load_dotenv()

load_dotenv(os.path.join(BASE_DIR.parent, 'infra/.env'), verbose=True)

SECRET_KEY = os.environ.get('DJANGO_KEY', default='H3R3-Y0UR-S3CR3T-K3Y')

DEBUG = True  # os.environ.get('TEST_ENVIRONMENT', default=False) == 'True'

ALLOWED_HOSTS = [
    '62.84.124.211',
    'localhost',
    'backend',
    '127.0.0.1',
]
#     os.environ.get('ALLOWED_HOSTS', default='*'),
# ]

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

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
