from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path("", views.home_view, name="home_view"),
    path("sites/", views.sites_view, name="sites_view"),
    path("site/<slug:slug>/", views.site_detail_view, name="site_detail_view"),
    path("toggle-theme/", views.toggle_theme, name="toggle_theme"),
    path("favorites/", views.favorites_view, name="favorites_view"),
    path("favorite/<slug:slug>/", views.toggle_favorite, name="toggle_favorite"),
    path("about/", views.about_view, name="about_view"),
]