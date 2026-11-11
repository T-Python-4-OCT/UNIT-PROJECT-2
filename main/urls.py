from django.urls import path

from . import views

app_name = 'main'
urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('places/', views.places, name='places'),
    path('places/<slug:slug>/', views.place_detail, name='place_detail'),
    path('events/', views.events, name='events'),
    path('history/', views.history, name='history'),
    path('projects/', views.projects, name='projects'),
    path('projects/<slug:slug>/', views.project_detail, name='project_detail'),
    path('gallery/', views.gallery, name='gallery'),
    path('search/', views.search, name='search'),
    path('theme/', views.toggle_theme, name='toggle_theme'),
]