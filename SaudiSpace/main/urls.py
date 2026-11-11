from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('astronauts/', views.astronauts, name='astronauts'),
    path('missions/', views.missions, name='missions'),
    path('satellites/', views.satellites, name='satellites'),
    path('research/', views.research, name='research'),
    path('future/', views.future, name='future'),
    path('toggle-theme/', views.toggle_theme, name='toggle_theme'),
    path('astronauts/rayyanah/', views.rayyanah, name='rayyanah'),
    path('astronauts/ali-alqarni/', views.ali_alqarni, name='ali_alqarni'),
    path('astronauts/ali-alghamdi/', views.ali_alghamdi, name='ali_alghamdi'),
    path('astronauts/mariam-fardous/', views.mariam_fardous, name='mariam_fardous'),
    path('satellites/', views.satellites, name='satellites'),
    path( 'satellites/<slug:slug>/',views.satellite_detail,    name='satellite_detail'),
    path('astronomy/', views.astronomy, name='astronomy'),
    path('astronomy/<slug:slug>/', views.planet_detail, name='planet_detail'),
    ]
