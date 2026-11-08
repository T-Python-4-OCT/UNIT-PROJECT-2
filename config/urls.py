from django.conf.urls.i18n import i18n_patterns
from django.urls import include, path

urlpatterns = i18n_patterns(path("", include("projects.urls")), prefix_default_language=False)
handler404 = "projects.views.not_found"
