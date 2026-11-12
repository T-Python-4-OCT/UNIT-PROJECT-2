"""روابط المشروع الرئيسية — يُحال كل شيء إلى تطبيق main."""
from django.urls import include, path

urlpatterns = [
    path("", include("main.urls")),
]
