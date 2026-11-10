"""URL routes for the website application."""
from django.urls import path

from . import views

app_name = "website"

urlpatterns = [
    path("", views.home, name="home"),
    path("identity/", views.identity, name="identity"),
    path("digital-design/", views.digital_design, name="digital_design"),
    path("architecture/", views.architecture, name="architecture"),
    path("graphic-design/", views.graphic_design, name="graphic_design"),
    path("product-design/", views.product_design, name="product_design"),
    path("contemporary/", views.contemporary, name="contemporary"),
]
