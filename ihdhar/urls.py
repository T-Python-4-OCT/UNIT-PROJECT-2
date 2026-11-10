"""Main URL map: every app has its own urls.py."""

from django.urls import include, path

urlpatterns = [
    path("", include("main.urls")),
    path("detector/", include("detector.urls")),
    path("reports/", include("reports.urls")),
]

handler404 = "main.views.page_not_found"
