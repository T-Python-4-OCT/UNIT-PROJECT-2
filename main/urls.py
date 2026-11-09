from django.urls import path

from main import views

app_name = "main"

urlpatterns = [
    path("", views.home, name="home"),
    path("guide/", views.guide, name="guide"),
    # Path parameter: the scam key is part of the link, e.g. /guide/bank/
    path("guide/<slug:scam_key>/", views.scam_detail, name="scam_detail"),
    path("faq/", views.faq, name="faq"),
    path("feedback/", views.feedback, name="feedback"),
]
