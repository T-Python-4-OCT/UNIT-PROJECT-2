from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('city/<slug:slug>/', views.city_detail, name='city_detail'),
    path('terms/', views.terms, name='terms'),
    path('privacy/', views.privacy, name='privacy'),
    path('theme/toggle/', views.toggle_theme, name='toggle_theme'),
]