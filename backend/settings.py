"""
Django settings for whereintheworld project.

Generated by 'django-admin startproject' using Django 3.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
import sys
from pathlib import Path
from typing import List

import sentry_sdk
from posthog.sentry.posthog_integration import PostHogIntegration
from sentry_sdk.integrations.django import DjangoIntegration

from backend.utils import get_from_env, get_list, str_to_bool

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-*ojrg_(s)1)r_(6u8d4#5$czit*wttor(=wx+8ldoprb9(-wbq")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = get_from_env("DEBUG", False, type_cast=str_to_bool)

TEST = (
    "test" in sys.argv or sys.argv[0].endswith("pytest") or get_from_env("TEST", False, type_cast=str_to_bool)
)  # type: bool

ALLOWED_HOSTS: List[str] = get_list(os.getenv("ALLOWED_HOSTS", ""))


# Application definition

INSTALLED_APPS = [
    "whitenoise.runserver_nostatic",  # makes sure that whitenoise handles static files in development
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.gis",
    "django_extensions",
    "rest_framework",
    "corsheaders",
    "cities",
    "social_django",
    "backend.apps.WhereInTheWorldConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "backend.urls"

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

WSGI_APPLICATION = "backend.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": "whereintheworld",
        "USER": os.getenv("DB_USER", "whereintheworld"),
        "PASSWORD": os.getenv("DB_PASSWORD", "whereintheworld"),
        "HOST": os.getenv("DB_HOST", "localhost"),
        "PORT": "5432",
    }
}

# PostGIS (M1 support)

if os.getenv("GDAL_LIBRARY_PATH") and os.getenv("GEOS_LIBRARY_PATH"):
    GDAL_LIBRARY_PATH = os.getenv("GDAL_LIBRARY_PATH")
    GEOS_LIBRARY_PATH = os.getenv("GEOS_LIBRARY_PATH")


# Authentication
# https://docs.djangoproject.com/en/3.2/topics/auth/customizing/

AUTH_USER_MODEL = "backend.User"


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
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


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/


STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATIC_URL = "/static/"
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "build/"),
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["build", "backend/templates"],
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

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# REST Framework
# https://www.django-rest-framework.org/api-guide/settings/

REST_FRAMEWORK = {
    "DATETIME_FORMAT": "%Y-%m-%dT%H:%M:%S.%fZ",
    "TEST_REQUEST_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",),
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 100,
    "EXCEPTION_HANDLER": "exceptions_hog.exception_handler",
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}

# CORS
# https://github.com/adamchainz/django-cors-headers

CORS_ALLOW_ALL_ORIGINS = True  # TODO: Allow granular CORS controls


# Django cities
# https://github.com/coderholic/django-cities

CITIES_LOCALES: List[str] = []
CITIES_POSTAL_CODES: List[str] = []
CITIES_FILES = {
    "city": {
        "filename": "cities15000.zip",
        "urls": ["http://download.geonames.org/export/dump/" + "{filename}"],
    },
}

# Social Django
# https://python-social-auth.readthedocs.io/en/latest/configuration/django.html

SOCIAL_AUTH_JSONFIELD_ENABLED = True
SOCIAL_AUTH_USER_MODEL = "backend.User"
SOCIAL_AUTH_STRATEGY = "social_django.strategy.DjangoStrategy"
SOCIAL_AUTH_STORAGE = "social_django.models.DjangoStorage"
SOCIAL_AUTH_LOGIN_REDIRECT_URL = "/"
SOCIAL_AUTH_PIPELINE = (
    "social_core.pipeline.social_auth.social_details",
    "social_core.pipeline.social_auth.social_uid",
    "social_core.pipeline.social_auth.auth_allowed",
    "social_core.pipeline.social_auth.social_user",
    "social_core.pipeline.social_auth.associate_by_email",
    "backend.api.views.social_create_user",
    "social_core.pipeline.social_auth.associate_user",
    "social_core.pipeline.social_auth.load_extra_data",
    "social_core.pipeline.user.user_details",
)
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.getenv("SOCIAL_AUTH_GOOGLE_OAUTH2_KEY")
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.getenv("SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET")
AUTHENTICATION_BACKENDS = (
    "social_core.backends.google.GoogleOAuth2",
    "django.contrib.auth.backends.ModelBackend",
)
SOCIAL_AUTH_REDIRECT_IS_HTTPS = not DEBUG


# Sentry + PostHog
# https://docs.sentry.io/platforms/python/guides/django/
# https://posthog.com/docs/integrate/server/python#sentry

if not TEST and os.getenv("SENTRY_DSN"):
    PostHogIntegration.organization = "posthog2"
    PostHogIntegration.project_id = "6135040"

    sentry_sdk.utils.MAX_STRING_LENGTH = 10_000_000
    sentry_sdk.init(
        dsn=os.environ["SENTRY_DSN"],
        integrations=[DjangoIntegration(), PostHogIntegration()],
        request_bodies="always",
        send_default_pii=False,
        environment="production",
    )  # type: ignore

    MIDDLEWARE.append("posthog.sentry.django.PosthogDistinctIdMiddleware")
    POSTHOG_DJANGO = {"distinct_id": lambda request: request.user and request.user.transactional_id}


# Business rules
# https://github.com/PostHog/whereintheworld

DISTANCE_THRESHOLD = 1.8  # 1.8 degrees is approximately 200km
MAPS_API_KEY = os.getenv("MAPS_API_KEY")
