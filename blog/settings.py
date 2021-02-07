"""
Django settings for blog project.

Generated by 'django-admin startproject' using Django 3.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv(
    "SECRET_KEY", "s#!83!8e$3s89m)r$1ghsgxbndf8=#^qt(_*o%xbq0j2t8#db5"
)

admins = os.getenv("ADMINS", "")
if admins:
    ADMINS = list(map(lambda x: tuple(x.split(",")), admins.split(";")))

DEFAULT_FROM_EMAIL = "Gab's Notes <blog@mg.gabnotes.org>"
SERVER_EMAIL = "Gab's Notes <blog@mg.gabnotes.org>"
EMAIL_SUBJECT_PREFIX = "[Blog] "
EMAIL_TIMEOUT = 30

ANYMAIL = {
    "MAILGUN_API_KEY": os.getenv("MAILGUN_API_KEY", ""),
    "MAILGUN_SENDER_DOMAIN": os.getenv("MAILGUN_SENDER_DOMAIN", ""),
    "MAILGUN_API_URL": "https://api.eu.mailgun.net/v3",
}
EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG", "true").lower() == "true"

ALLOWED_HOSTS = ["localhost"]  # Required for healthcheck
if DEBUG:
    ALLOWED_HOSTS.extend(["127.0.0.1"])

HOSTS = os.getenv("HOSTS")
if HOSTS:
    ALLOWED_HOSTS.extend(HOSTS.split(";"))

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "articles",
    "attachments",
    "anymail",
    "django_cleanup.apps.CleanupConfig",
    "compressor",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "blog.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["blog/templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "articles.context_processors.drafts_count",
                "articles.context_processors.date_format",
                "articles.context_processors.git_version",
                "articles.context_processors.analytics",
                "articles.context_processors.open_graph_image_url",
                "articles.context_processors.blog_metadata",
            ],
        },
    },
]

WSGI_APPLICATION = "blog.wsgi.application"

MEMCACHED_LOCATION = os.getenv("MEMCACHED_LOCATION")
if MEMCACHED_LOCATION:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.memcached.PyLibMCCache",
            "LOCATION": MEMCACHED_LOCATION,
        }
    }
else:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.db.DatabaseCache",
            "LOCATION": "cache",
        }
    }

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DB_BASE_DIR = os.getenv("DB_BASE_DIR", BASE_DIR)
if not DB_BASE_DIR:
    # Protect against empty strings
    DB_BASE_DIR = BASE_DIR
else:
    DB_BASE_DIR = Path(DB_BASE_DIR).resolve(strict=True)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": DB_BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Europe/Paris"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
]

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

AUTH_USER_MODEL = "articles.User"

BLOG = {
    "title": "Gab's Notes",
    "author": "Gabriel Augendre",
    "description": "My take on tech-related subjects (but not only).",
    "base_url": os.getenv("BLOG_BASE_URL", "https://gabnotes.org/"),
    "repo": {
        "commit_url": "https://git.augendre.info/gaugendre/blog/commit/{commit_sha}",
        "homepage": "https://git.augendre.info/gaugendre/blog",
        "log": "https://git.augendre.info/gaugendre/blog/commits/branch/master",
        "pipelines_url": "https://drone.augendre.info/gaugendre/blog",
    },
}

SHORTPIXEL_API_KEY = os.getenv("SHORTPIXEL_API_KEY")
SHORTPIXEL_RESIZE_WIDTH = int(os.getenv("SHORTPIXEL_RESIZE_WIDTH", 750))
SHORTPIXEL_RESIZE_HEIGHT = int(os.getenv("SHORTPIXEL_RESIZE_HEIGHT", 10000))

PLAUSIBLE_DOMAIN = os.getenv("PLAUSIBLE_DOMAIN")
GOATCOUNTER_DOMAIN = os.getenv("GOATCOUNTER_DOMAIN")

LOGIN_URL = "admin:login"

# COMPRESS_ENABLED = True  # Enable this if you want to force compression during dev
COMPRESS_FILTERS = {
    "css": [
        "compressor.filters.css_default.CssAbsoluteFilter",
        "compressor.filters.cssmin.rCSSMinFilter",
    ],
    "js": [
        "compressor.filters.jsmin.CalmjsFilter",
    ],
}
if DEBUG:
    COMPRESS_DEBUG_TOGGLE = "nocompress"

COMPRESS_OFFLINE = True
COMPRESS_OFFLINE_CONTEXT = "articles.compressor.offline_context"
