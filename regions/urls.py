from django.urls import path
from . import views

app_name = "regions"

urlpatterns = [
    path("", views.home, name="home"),
    path("region/<slug:slug>/", views.region_detail, name="region_detail"),
    path("our-roots/", views.our_roots, name="our_roots"),
    path("toggle-theme/", views.toggle_theme, name="toggle_theme"),

]