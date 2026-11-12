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
    path("preferences/theme/", views.set_theme, name="set_theme"),
    path("preferences/language/", views.set_language, name="set_language"),
]
