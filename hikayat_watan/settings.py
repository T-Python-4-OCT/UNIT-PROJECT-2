"""
إعدادات مشروع «حكاية وطن».

المشروع لا يستخدم قاعدة بيانات: كل المحتوى محفوظ في ملف JSON
(watan/data/content.json)، لذلك DATABASES فارغة وتم حذف التطبيقات
التي تحتاج إلى قاعدة بيانات (admin / auth / sessions ...).
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# للتطوير فقط. في الإنتاج عيّن متغير البيئة DJANGO_SECRET_KEY.
SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "dev-only-key-change-me-hikayat-watan-9f2c1b7e5a",
)

DEBUG = os.environ.get("DJANGO_DEBUG", "1") == "1"

ALLOWED_HOSTS = (
    ["*"] if DEBUG else os.environ.get("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
)

INSTALLED_APPS = [
    "django.contrib.staticfiles",
    "watan",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "hikayat_watan.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "watan.context_processors.site_data",
            ],
        },
    },
]

WSGI_APPLICATION = "hikayat_watan.wsgi.application"
ASGI_APPLICATION = "hikayat_watan.asgi.application"

# لا توجد قاعدة بيانات — المحتوى في ملف JSON
DATABASES = {}

# ملف المحتوى (JSON)
CONTENT_FILE = BASE_DIR / "watan" / "data" / "content.json"

LANGUAGE_CODE = "ar"
TIME_ZONE = "Asia/Riyadh"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"  # للأمر collectstatic عند النشر

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
