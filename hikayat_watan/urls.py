from django.urls import include, path

urlpatterns = [
    path("", include("watan.urls")),
]

# صفحة 404 مخصصة (تظهر عندما DEBUG = False)
handler404 = "watan.views.page_not_found"
