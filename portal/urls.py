from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('toggle-theme/', views.toggle_theme, name='toggle_theme'),

    path(
        'digital-transformation/',
        views.digital_transformation,
        name='digital_transformation'
    ),
]