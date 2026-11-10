from django.contrib import admin
from django.urls import include, path
from industry import views

urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("industries/", views.industry_list, name="industry_list"),
    path("map/", views.map_view, name="industrial_map"),
    path("industry/<slug:slug>/", views.industry_detail, name="industry_detail"),
    path("awards/", views.awards, name="awards"),
    path("about/", views.about, name="about"),
]
