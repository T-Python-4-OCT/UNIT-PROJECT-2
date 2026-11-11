from django.contrib import admin
from django.templatetags.static import static
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    # Browsers request /favicon.ico on their own; send them to the SVG icon.
    path("favicon.ico", RedirectView.as_view(url=static("portal/img/favicon.svg"), permanent=True)),
    path("", include("portal.urls")),
]

handler404 = "portal.views.page_not_found"
