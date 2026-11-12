from django.urls import path

from . import views

app_name = "catalog"

urlpatterns = [
    path("industries/", views.industries, name="industries"),
    path("industries/<slug:slug>/", views.industry_detail, name="industry_detail"),
    path("companies/", views.companies, name="companies"),
    path("companies/<slug:slug>/", views.company_detail, name="company_detail"),
    path("industrial-cities/", views.industrial_cities, name="industrial_cities"),
    path("industrial-cities/<slug:slug>/", views.industrial_city_detail, name="industrial_city_detail"),
    path("made-in-saudi/", views.made_in_saudi, name="made_in_saudi"),
    path(
        "made-in-saudi/<slug:slug>/",
        views.product_detail,
        name="product_detail"
    ),
]
