import os

from foodgram.settings.components.common import BASE_DIR

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR.parent, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR.parent, 'media')

DATA_ROOT = os.path.join(BASE_DIR.parent, 'data')
