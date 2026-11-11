from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('', views.home, name='home'),
    path('projects/', views.all_projects, name='all_projects'),
    path('project/<slug:project_slug>/', views.project_detail, name='project_detail'),
    path('about/', views.about, name='about'),
    path('theme/<str:theme>/', views.set_theme, name='set_theme'),
]
