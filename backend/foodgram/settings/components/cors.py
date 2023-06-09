import os

CORS_URLS_REGEX = r'^/api/.*$'
CORS_ALLOWED_ORIGINS = os.environ.get('CORS_ALLOWED').split(' ')
