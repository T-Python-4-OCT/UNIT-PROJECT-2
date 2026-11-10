from django.http import Http404, HttpRequest
from django.shortcuts import redirect, render

from .data import CITIES, COUNTDOWN_TARGET, EXPLORE, STATS, get_city


def home_view(request: HttpRequest):
    return render(request, "main/home.html", {
        "cities": CITIES,
        "stats": STATS,
        "explore": EXPLORE,
        "countdown_target": COUNTDOWN_TARGET,
    })


def city_view(request: HttpRequest, slug):
    city = get_city(slug)
    if city is None:
        raise Http404("City not found")
    return render(request, "main/coming_soon.html", {"title": city["name"]})


def stadiums_view(request: HttpRequest):
    return render(request, "main/coming_soon.html", {"title": "الملاعب"})


def stadium_view(request: HttpRequest, slug):
    return render(request, "main/coming_soon.html", {"title": "الملعب"})


def history_view(request: HttpRequest):
    return render(request, "main/coming_soon.html", {"title": "الأخضر في المونديال"})


def journey_view(request: HttpRequest):
    return render(request, "main/coming_soon.html", {"title": "رحلة الاستضافة"})


def about_view(request: HttpRequest):
    return render(request, "main/coming_soon.html", {"title": "عن الموقع"})


def toggle_theme_view(request: HttpRequest):
    # Dark mode with cookies is added in the next commit
    return redirect(request.GET.get("next", "/"))
