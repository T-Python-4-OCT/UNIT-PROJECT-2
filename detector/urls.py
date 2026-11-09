from django.urls import path

from detector import views

app_name = "detector"

urlpatterns = [
    path("", views.detector_home, name="home"),
    path("pdf/", views.check_pdf, name="pdf"),
    path("history/", views.history, name="history"),
    path("history/<int:check_id>/", views.check_detail, name="detail"),
]
