import os
from foodgram.settings.components.common import BASE_DIR

DATABASES = {
    'default': {
        'ENGINE': os.environ.get(
            'DB_ENGINE', default='django.db.backends.sqlite3'
        ),
        'NAME': os.environ.get('POSTGRES_DB', BASE_DIR / 'db.sqlite3'),
        'USER': os.environ.get('POSTGRES_USER', default='postgres'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', default='postgres'),
        'HOST': os.environ.get('DB_HOST', default='db'),
        'PORT': os.environ.get('DB_PORT', default='5432'),
    }
}
