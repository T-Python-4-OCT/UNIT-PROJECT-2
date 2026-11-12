"""روابط تطبيق main — كل الروابط مسمّاة وتُستدعى في القوالب عبر {% url 'main:...' %}."""
from django.urls import path

from . import views

app_name = "main"

urlpatterns = [
    path("", views.home, name="home"),
    path("old-riyadh/", views.old_riyadh, name="old_riyadh"),
    path("king-abdulaziz/", views.king, name="king"),
    path("participants/", views.participants, name="participants"),
    # رابط ديناميكي: صفحة لكل مشارك حسب الـ slug
    path("participants/<slug:slug>/", views.person_detail, name="person"),
    path("story/", views.story, name="story"),
    # رابط ديناميكي: صفحة لكل فصل من فصول القصة
    path("story/<slug:slug>/", views.chapter_detail, name="chapter"),
    path("masmak-tour/", views.tour, name="tour"),
    path("timeline/", views.timeline, name="timeline"),
    path("museum/", views.museum, name="museum"),
    path("quiz/", views.quiz, name="quiz"),
]
