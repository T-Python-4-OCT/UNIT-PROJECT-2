from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path("", views.home_view, name="home"),
    path("city/<slug:slug>/", views.city_view, name="city"),
    path("stadiums/", views.stadiums_view, name="stadiums"),
    path("stadium/<slug:slug>/", views.stadium_view, name="stadium"),
    path("history/", views.history_view, name="history"),
    path("journey/", views.journey_view, name="journey"),
    path("about/", views.about_view, name="about"),
    path("theme/", views.toggle_theme_view, name="toggle_theme"),
]
