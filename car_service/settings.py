import os
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# COMMON SETTINGS
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "qwe123")

DEBUG = os.getenv("DEBUG") == "True"
DEVELOPMENT = os.getenv("DEVELOPMENT") == "True"

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", default="127.0.0.1").split(",")
WSGI_APPLICATION = "car_service.wsgi.application"
INSTALLED_APPS = [
    "drf_spectacular",
    "drf_spectacular_sidecar",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework.authtoken",
    "drf_yasg",
    "djoser",
    "django_filters",
    "corsheaders",
    "api.apps.ApiConfig",
    "autoservice.apps.AutoserviceConfig",
    "core.apps.CoreConfig",
    "users.apps.UsersConfig",
    "order.apps.OrderConfig",
]
if DEVELOPMENT is True:
    INSTALLED_APPS.append("django_extensions")

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

CORS_ORIGIN_ALLOW_ALL = True
if DEVELOPMENT is False:
    CORS_URLS_REGEX = r"^/api/.*$"

ROOT_URLCONF = "car_service.urls"

GEOIP_PATH = os.path.join(BASE_DIR, "static/geoip")

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# Database settings
if DEVELOPMENT:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": "db.sqlite3",
        },
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("DB_NAME", "postgres"),
            "USER": os.getenv("POSTGRES_USER", "postgres"),
            "PASSWORD": os.getenv("POSTGRES_PASSWORD", "postgres"),
            "HOST": os.getenv("DB_HOST", "db"),
            "PORT": os.getenv("DB_PORT", "5432"),
        },
    }


# DRF settings
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ],
    # Для использования drf_spectacular (документации)
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    #'UPLOADED_FILES_USE_URL': False
}
# Для использования drf_spectacular (документации)
SPECTACULAR_SETTINGS = {
    # настройки для хоста закомментированы
    "TITLE": "Find Car Service API",
    "DESCRIPTION": "Документация для веб приложения find-car-service.ru",
    "VERSION": "1.0.0",
    "SWAGGER_UI_DIST": "SIDECAR",
    "SWAGGER_UI_FAVICON_HREF": "SIDECAR",
    "REDOC_DIST": "SIDECAR",
}

# SIMPLE_JWT = {
#     'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
#     'AUTH_HEADER_TYPES': ('Bearer',),
# }

DJOSER = {
    "SERIALIZERS": {
        "user": "api.v1.users.serializers.CustomUserSerializer",
        "current_user": "api.v1.users.serializers.CustomCurrentUserSerializer",
        "user_create": "api.v1.users.serializers.CustomUserSerializer",
        "user_create_password_retype": "api.v1.users.serializers.CustomUserSerializer",
    },
    "PERMISSIONS": {
        "user": ["rest_framework.permissions.IsAuthenticated"],
        "user_list": ["rest_framework.permissions.IsAuthenticated"],
    },
    "USER_CREATE_PASSWORD_RETYPE": True,
    "SEND_ACTIVATION_EMAIL": True,
    "SET_PASSWORD_RETYPE": True,
    "PASSWORD_RESET_CONFIRM_RETYPE": True,
    "ACTIVATION_URL": "api/v1/auth/users/activate/{uid}/{token}/",
}


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

AUTH_USER_MODEL = "users.CustomUser"
AUTHENTICATION_BACKENDS = ("users.backends.AuthBackend",)
ADMIN_MODEL_EMPTY_VALUE = "-пусто-"


if DEVELOPMENT:
    EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
    EMAIL_FILE_PATH = os.path.join(BASE_DIR, "sent_emails")
else:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = "smtp.yandex.ru"
    EMAIL_PORT = 465
    EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
    EMAIL_USE_SSL = True
    DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
    SERVER_EMAIL = EMAIL_HOST_USER
    EMAIL_ADMIN = EMAIL_HOST_USER


# Internationalization settings
LANGUAGE_CODE = "ru-RU"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "collected_static"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

DEFAULT_MAXLEN_CHARFIELD = 250

# Constants settings cars.apps
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
WORKING_TIME_MAX_LENGTH = 5

# Constants users.apps
USERNAME_MAX_LENGTH = 40
EMAIL_MAX_LENGTH = 80
PHONE_MAX_LENGTH = 12
FIRST_NAME_MAX_LENGTH = 40
LAST_NAME_MAX_LENGTH = 40

# Constants order.apps
MAX_LENGTH_INFO = 200
MAX_LENGTH_TASK = 200
MAX_LENGTH_CAR = 50

# Other constants
NUMBER_WEEK = {
    0: "Понедельник",
    1: "Вторник",
    2: "Среда",
    3: "Четверг",
    4: "Пятница",
    5: "Суббота",
    6: "Воскресенье",
}

# File upload settints
FILE_UPLOAD_MAX_MEMORY_SIZE = 26214400
