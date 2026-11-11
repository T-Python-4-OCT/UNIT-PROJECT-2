from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path("", views.home_view, name="home"),
    path("topic/<slug:slug>/", views.topic_view, name="topic"),
    path("timeline/", views.timeline_view, name="timeline"),
    path("about/", views.about_view, name="about"),
    path("theme/", views.theme_view, name="theme"),
    path("lang/<str:lang>/", views.lang_view, name="lang"),
]
