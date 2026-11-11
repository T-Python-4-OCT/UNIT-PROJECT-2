from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path("", views.home, name="home"),
    path("pre-oil/", views.pre_oil, name="pre_oil"),
    path("discovery/", views.discovery, name="discovery"),
    path("aramco/", views.aramco, name="aramco"),
    path("ownership/", views.ownership, name="ownership"),
    path("society/", views.society, name="society"),
    path("vision/", views.vision, name="vision"),
    path("mode/<str:mode>/", views.mode_view, name="mode_view"),
]