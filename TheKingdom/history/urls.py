from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("era/<slug:era>/", views.state_detail, name="state_detail"),
    path("ruler/<slug:slug>/", views.ruler_detail, name="ruler_detail"),
    path("about/", views.about, name="about"),
]
