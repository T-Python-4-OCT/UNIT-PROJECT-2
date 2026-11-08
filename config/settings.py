import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv("ATLAS_SECRET_KEY", "django-insecure-atlas-local-development-key")
DEBUG = os.getenv("ATLAS_DEBUG", "1") == "1"
ALLOWED_HOSTS = ["127.0.0.1", "localhost", "[::1]", "testserver"]
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

INSTALLED_APPS = ["django.contrib.staticfiles", "projects"]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
]
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {"context_processors": ["django.template.context_processors.request"]},
    },
]

LANGUAGE_CODE = "en"
LANGUAGES = [("en", "English"), ("ar", "العربية")]
LOCALE_PATHS = [BASE_DIR / "locale"]
TIME_ZONE = "Asia/Riyadh"

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "collected-static"
STATICFILES_DIRS = [BASE_DIR / "static"]
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedStaticFilesStorage"},
}
WHITENOISE_IMMUTABLE_FILE_TEST = r"^/static/build/assets/.+-[A-Za-z0-9_-]{8,}\.[A-Za-z0-9]+$"
VITE_DEV_ORIGIN = "http://127.0.0.1:5173" if DEBUG and os.getenv("ATLAS_VITE_DEV") == "1" else ""
