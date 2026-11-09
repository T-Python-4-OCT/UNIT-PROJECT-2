from django.conf.urls.i18n import i18n_patterns
from django.urls import include, path

from saudi_atlas.projects import views

urlpatterns = [
    path("robots.txt", views.robots, name="robots"),
    path("sitemap.xml", views.sitemap, name="sitemap"),
]
urlpatterns += i18n_patterns(path("", include("saudi_atlas.projects.urls")), prefix_default_language=False)
handler404 = "saudi_atlas.projects.views.not_found"
