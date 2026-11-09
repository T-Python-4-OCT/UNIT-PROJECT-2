from django.urls import path

from detector import views

app_name = "detector"

urlpatterns = [
    path("", views.detector_home, name="home"),
]
