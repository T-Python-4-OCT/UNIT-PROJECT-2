from django.urls import path

from . import views

app_name = "kingdom"

urlpatterns = [
    path("", views.home, name="home"),

    path("cities/", views.city_list, name="city_list"),
    path("cities/<slug:slug>/", views.city_detail, name="city_detail"),

    path("about/", views.about, name="about"),
    path("history/", views.history, name="history"),
    path("heritage/", views.heritage, name="heritage"),
    path("tourism/", views.tourism, name="tourism"),
]