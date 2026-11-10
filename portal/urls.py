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
path(
    'smart-technologies/',
    views.smart_technologies,
    name='smart_technologies'
),
path(
    'digital-government/',
    views.digital_government,
    name='digital_government'
),
path(
    'cybersecurity-development/',
    views.cybersecurity_development,
    name='cybersecurity_development'
),
]