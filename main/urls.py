from django.urls import path

from main import views

app_name = "main"

urlpatterns = [
    path("", views.home, name="home"),
    path("guide/", views.guide, name="guide"),
    path("faq/", views.faq, name="faq"),
]
