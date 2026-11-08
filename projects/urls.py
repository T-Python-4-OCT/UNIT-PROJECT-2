from django.urls import path

from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("projects/<slug:slug>/", views.project, name="project"),
    path("404/", views.not_found, name="not_found"),
]
