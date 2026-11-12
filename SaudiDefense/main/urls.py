from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path('history/', views.history, name='history'),
    path('sector/<slug:slug>/', views.sector_detail, name='sector_detail'),
    path('companies/', views.companies, name='companies'),
    path('vision/', views.vision, name='vision'),
    path('about/', views.about, name='about'),
    path('sectors/', views.sectors, name='sectors'),
    path('sectors/<slug:sector_slug>/', views.sector_detail, name='sector_detail'),

]