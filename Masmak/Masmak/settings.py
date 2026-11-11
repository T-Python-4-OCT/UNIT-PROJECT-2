"""
إعدادات مشروع «المصمك | قصة استرداد الرياض».

قرارات تصميمية مقصودة:
- بلا قاعدة بيانات (DATABASES = {}) وبلا Django Admin أو auth أو sessions.
- المحتوى بيانات ثابتة في main/data/*.json يحمّلها main/content.py.
- الملفات الثابتة (CSS / JS / SVG / الصور الأصلية) داخل main/static/main/.
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "django-insecure-masmak-dev-only-change-this-key-before-deploying",
)

DEBUG = os.environ.get("DJANGO_DEBUG", "1") == "1"

ALLOWED_HOSTS = (
    ["*"] if DEBUG else os.environ.get("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
)

INSTALLED_APPS = [
    "django.contrib.staticfiles",
    "main",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "Masmak.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "main.context_processors.site",
            ],
        },
    },
]

WSGI_APPLICATION = "Masmak.wsgi.application"

# لا قاعدة بيانات — المشروع يعمل بالكامل من ملفات JSON.
DATABASES = {}

LANGUAGE_CODE = "ar"
TIME_ZONE = "Asia/Riyadh"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
