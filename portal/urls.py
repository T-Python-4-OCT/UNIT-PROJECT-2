from django.urls import path
from . import views

app_name = "portal"

urlpatterns = [
    path("", views.home, name="home"),
    path("language/", views.set_language, name="set_language"),
    path("<slug:slug>/", views.content_page, name="page"),
]