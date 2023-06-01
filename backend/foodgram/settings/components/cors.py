import os
from foodgram.settings.components.common import BASE_DIR

CORS_URLS_REGEX = r'^/api/.*$'
CORS_ALLOWED_ORIGINS = [os.environ.get('CORS_ALLOWED'),]
