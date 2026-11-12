from django.urls import path
from . import views

app_name = "ministries"

urlpatterns = [
    path("", views.home, name="home"),
    path("ministries/", views.ministry_directory, name="directory"),
    path("ministry/<slug:slug>/", views.ministry_detail, name="detail"),
    path("timeline/", views.timeline, name="timeline"),
    path("compare/", views.compare, name="compare"),
    path("quiz/", views.quiz, name="quiz"),
    path("search/", views.search, name="search"),
]