from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path('project/<slug:slug>/',views.project_detail, name='project_detail'),
    path('theme/', views.set_theme, name='set_theme'),
    path('about/', views.about, name='about'),
    path('language/', views.set_language, name='set_language'),
]