import os
from pathlib import Path
from dotenv import load_dotenv


load_dotenv()

BASE_DIR = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

LOAD_INGR_PATH = BASE_DIR / "data" / "ingredients.csv"

SECRET_KEY = '@jgrh$-_rvho6i#pf%^em***d7duxd6kg6pbh8k%n$&=o1mht%'


DEBUG = True

ALLOWED_HOSTS = ['*']

AUTH_USER_MODEL = 'users.User'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'djoser',
    'rest_framework.authtoken',
    'api.apps.ApiConfig',
    'recipes.apps.RecipesConfig',
    'users.apps.UsersConfig',
    'colorfield',
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

ROOT_URLCONF = 'foodgram.urls'

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
        'ENGINE': os.getenv('DB_ENGINE', default='django.db.backends.postgresql'),
        'NAME': os.getenv('DB_NAME', default='foodgram'),
        'USER': os.getenv('POSTGRES_USER', default='postgres'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', default='Okhnovsky'),
        'HOST': os.getenv('DB_HOST', default='127.0.0.1'),
        'PORT': os.getenv('DB_PORT', default=5432)
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES':
    ['rest_framework.authentication.TokenAuthentication', ],

    'DEFAULT_PERMISSION_CLASSES':
    ['rest_framework.permissions.IsAuthenticatedOrReadOnly', ],
}


DJOSER = {
    'LOGIN_FIELD': 'email',
    'HIDE_USERS': False,
    'PERMISSIONS': {
        'recipe': ('api.permissions.IsAuthorStaffOrReadOnly,',),
        'recipe_list': ('api.permissions.IsAuthorStaffOrReadOnly',),
        'user': ('api.permissions.IsOwnerUserOrReadOnly',),
        'user_list': ('api.permissions.IsOwnerUserOrReadOnly',),
    },
    'SERIALIZERS': {
        'user': 'api.serializers.UserSerializer',
        'user_list': 'api.serializers.UserSerializer',
        'current_user': 'api.serializers.UserSerializer',
        'user_create': 'api.serializers.UserSerializer',
    },
}


# media
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
