from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("projects/<slug:slug>/", views.project, name="project"),
    path("timeline/", views.timeline, name="timeline"),
    path("compare/", views.compare, name="compare"),
    path("search/", views.search, name="search"),
    path("credits/", views.credits, name="credits"),
    path("404/", views.not_found, name="not_found"),
]
