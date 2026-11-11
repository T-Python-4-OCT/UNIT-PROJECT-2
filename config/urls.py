"""Root URL configuration for the project."""
# These routes connect the admin and website.
from django.contrib import admin
from django.urls import include, path

# The admin and public site start from these routes.
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("website.urls")),
]
