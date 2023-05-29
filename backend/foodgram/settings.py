import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(os.path.join(BASE_DIR.parent, 'infra/.env'), verbose=True)

SECRET_KEY = os.environ.get('SECRET_KEY', default='H3R3-Y0UR-S3CR3T-K3Y')

DEBUG = os.environ.get('TEST_ENVIRONMENT', default=False) == 'True'

ALLOWED_HOSTS = [os.environ.get('ALLOWED_HOSTS', default='*'), 'localhost', '127.0.0.1']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'djoser',
    'corsheaders',
    'users.apps.UsersConfig',
    'core.apps.CoreConfig',
    'api.apps.ApiConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
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

DATABASES = {
    'default': {
        'ENGINE': os.environ.get(
            'DB_ENGINE', default='django.db.backends.sqlite3'
        ),
        'NAME': os.environ.get('POSTGRES_DB', default=BASE_DIR / 'db.sqlite3'),
        'USER': os.environ.get('POSTGRES_USER', default='postgres'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', default='postgres'),
        'HOST': os.environ.get('DB_HOST', default='db'),
        'PORT': os.environ.get('DB_PORT', default='5432'),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'UserAttributeSimilarityValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'MinimumLengthValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'CommonPasswordValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'NumericPasswordValidator'
        )
    },
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated', 
    ],

    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    # 'DEFAULT_FILTER_BACKENDS': [
    #     'django_filters.rest_framework.DjangoFilterBackend'
    # ],
    'DEFAULT_PAGINATION_CLASS': [
        'core.pagination.CustomPagination',
    ],
}

DJOSER = {
    'LOGIN_FIELD': 'email',
    'HIDE_USERS': False,
    'PERMISSIONS': {
        'user': ['djoser.permissions.CurrentUserOrAdminOrReadOnly'],
        'user_list': ['rest_framework.permissions.IsAuthenticatedOrReadOnly'],
    },
    'SERIALIZERS': {
        'user': 'api.serializers.UserSerializer',
        'current_user': 'api.serializers.UserSerializer'
    },
}

LANGUAGE_CODE = "ru-Ru"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

PAGE_SIZE = 6

DEFAULT_FIELD_LENGTH = 150

DEFAULT_EMAIL_LENGTH = 254

AUTH_USER_MODEL = 'users.User'

CORS_ORIGIN_ALLOW_ALL = True
CORS_URLS_REGEX = r'^/api/.*$'
CORS_ALLOWED_ORIGINS = ['http://localhost:3000',] 
