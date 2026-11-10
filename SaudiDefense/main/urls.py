from . import views
from django.urls import path

app_name = "main"

urlpatterns = [
    path("", views.home_view, name="home_view"),
    path("sector/<sector_name>/", views.sector_view, name="sector_view"),
    path("company/<company_name>/", views.company_view, name="company_view"),
    path("vision/", views.vision_view, name="vision_view"),
    path("history/", views.history_view, name="history_view"),
    path("events/", views.events_view, name="events_view"),
    path("lang/<lang_code>/", views.set_language_view, name="set_language_view"),
]
