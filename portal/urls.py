from django.urls import path
from . import views

app_name = "portal"

urlpatterns = [
    path("", views.home, name="home"),
    path("language/", views.set_language, name="set_language"),
    # Must stay above the slug pattern, otherwise "feedback" is read as a page slug.
    path("feedback/", views.feedback, name="feedback"),
    path("<slug:slug>/", views.content_page, name="page"),
]