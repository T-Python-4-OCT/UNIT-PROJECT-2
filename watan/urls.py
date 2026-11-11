from django.urls import path

from . import views

app_name = "watan"

urlpatterns = [
    path("", views.home, name="home"),
    path("history/", views.history, name="history"),
    path("history/<slug:era_slug>/", views.era_detail, name="era_detail"),
    path("cities/", views.cities, name="cities"),
    path("city/<slug:city_slug>/", views.city_detail, name="city_detail"),
    path("about/", views.about, name="about"),
]
