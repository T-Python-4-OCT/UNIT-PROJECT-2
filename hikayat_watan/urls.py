from django.urls import include, path

urlpatterns = [
    path("", include("hikayat_watan.watan.urls")),
]

# Custom 404 page
handler404 = "hikayat_watan.watan.views.page_not_found"