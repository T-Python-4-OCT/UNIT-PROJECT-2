"""
URL configuration for SaudiProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from SaudiApp import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.home, name='home'),

    path('kingdom/', views.kingdom, name='kingdom'),
    path('tourism-entertainment/', views.tourism_entertainment, name='tourism_entertainment'),
    path('sports/', views.sports, name='sports'),
    path('culture/', views.culture, name='culture'),
    path('i18n/', include('django.conf.urls.i18n')),
    path('red-sea/', views.red_sea, name='red_sea'),
    path('alula/', views.alula, name='alula'),
    path('diriyah/', views.diriyah, name='diriyah'),
    path('al-ahsa/', views.al_ahsa, name='al_ahsa'),
]