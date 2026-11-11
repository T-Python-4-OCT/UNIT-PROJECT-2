from django.urls import path
from . import views

app_name = "kingdom"

urlpatterns = [
    path("", views.home, name="home"),
    path("city/<slug:slug>/", views.city_detail, name="city_detail"),
    path("history/", views.history, name="history"),
    path("history/<slug:slug>/", views.history_detail, name="history_detail"),
    path("about/", views.about, name="about"),
]
