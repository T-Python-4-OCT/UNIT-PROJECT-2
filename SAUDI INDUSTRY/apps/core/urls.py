from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("technology/", views.technology, name="technology"),
    path(
        "technology/<slug:slug>/",
        views.technology_detail,
        name="technology_detail"
    ),
    path("vision-2030/", views.vision2030, name="vision2030"),
    path("gallery/", views.gallery, name="gallery"),
    path("about/", views.about, name="about"),
]
