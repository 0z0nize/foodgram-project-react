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
    'recipes.apps.RecipesConfig',
]
