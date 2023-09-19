import os
from dotenv import load_dotenv

load_dotenv()


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'qwe123')

DEBUG = os.getenv('DEBUG') == 'True'


ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '127.0.0.1 localhost').split()


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'djoser',
    'django_filters',
    'colorfield',
    'users.apps.UsersConfig',
    'autoservice.apps.AutoserviceConfig',
    'cars',
    'core.apps.CoreConfig',
    'api.apps.ApiConfig',
    'feedback',
    'jobs',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'car_service.urls'

GEOIP_PATH = os.path.join(BASE_DIR, 'static/geoip')

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



WSGI_APPLICATION = 'car_service.wsgi.application'

if os.getenv('DEVELOPMENT', 'True') == 'True':
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": "db.sqlite3",
        },
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": os.getenv("DB_ENGINE", "django.db.backends.postgresql"),
            "NAME": os.getenv("DB_NAME", "postgres"),
            "USER": os.getenv("POSTGRES_USER", "postgres"),
            "PASSWORD": os.getenv("POSTGRES_PASSWORD", "postgres"),
            "HOST": os.getenv("DB_HOST", "db"),
            "PORT": os.getenv("DB_PORT", "5432"),
        },
    }


REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],

    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

SIMPLE_JWT = {
   'AUTH_HEADER_TYPES': ('Bearer',),
}

DJOSER = {
    "SERIALIZERS": {
        'user': 'api.v1.users.serializers.CustomUserSerializer',
        'current_user': 'api.v1.users.serializers.CustomUserSerializer',
    },
    'PERMISSIONS': {
        'user': ['rest_framework.permissions.IsAuthenticated'],
        'user_list': ['rest_framework.permissions.AllowAny'],
    },
    'USER_CREATE_PASSWORD_RETYPE': True,
    'SEND_ACTIVATION_EMAIL': True,
    'SET_PASSWORD_RETYPE': True,
    'PASSWORD_RESET_CONFIRM_RETYPE': True,
    'TOKEN_MODEL': None, 
    'ACTIVATION_URL': 'v1/auth/users/activation/{uid}/{token}/',
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


if os.getenv('DEVELOPMENT') == 'True':
    EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
    EMAIL_FILE_PATH = os.path.join(BASE_DIR, 'sent_emails')
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtp.yandex.ru'
    EMAIL_PORT = 465
    EMAIL_HOST_USER = 'todo'
    EMAIL_HOST_PASSWORD = 'todo'
    EMAIL_USE_SSL = True
    DEFAULT_FROM_EMAIL = 'some_service_email'

AUTH_USER_MODEL = 'users.CustomUser'
ADMIN_MODEL_EMPTY_VALUE = '-пусто-'


# Internationalization

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Константы
MAX_LENGTH_TRANSPORT_SLUG = 150
MAX_LENGTH_TRANSPORT_BRAND = 150
MAX_LENGTH_TRANSPORT_MODEL = 150
MAX_LENGTH_VIN = 17
MAX_LENGTH_NUMBER_OF_CAR = 9
MAX_LENGTH_ODOMETR = 10
MAX_LENGTH_JOBS_NAME = 150
MAX_LENGTH_JOBS_DESCRIPTION = 150
MAX_LENGTH_JOBS_PRICE = 5
MAX_LENGTH_JOBS_SLUG = 150

# Константы users.apps
USERNAME_MAX_LENGTH = 40
EMAIL_MAX_LENGTH = 80
PHONE_MAX_LENGTH = 12
FIRST_NAME_MAX_LENGTH = 40
LAST_NAME_MAX_LENGTH = 40
