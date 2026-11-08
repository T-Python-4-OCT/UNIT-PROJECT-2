from django.shortcuts import render
from django.http import Http404

from .data_loader import get_cities, get_heritage


def home(request):
    cities = get_cities()

    return render(request, "home.html", {
        "cities": cities[:3]
    })


def city_list(request):
    cities = get_cities()

    return render(request, "cities/city_list.html", {
        "cities": cities
    })


def city_detail(request, slug):
    cities = get_cities()

    city = next(
        (item for item in cities if item["slug"] == slug),
        None
    )

    if city is None:
        raise Http404("المدينة غير موجودة")

    return render(request, "cities/city_detail.html", {
        "city": city
    })


def about(request):
    return render(request, "pages/about.html")


def history(request):
    return render(request, "pages/history.html")


def heritage(request):
    items = get_heritage()

    return render(request, "pages/heritage.html", {
        "items": items
    })


def tourism(request):
    cities = get_cities()

    return render(request, "pages/tourism.html", {
        "cities": cities
    })