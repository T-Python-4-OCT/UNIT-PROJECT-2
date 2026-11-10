from django.http import Http404, HttpRequest
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme

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
    """Switch light/dark mode, save it in a cookie, then return to the same page."""
    next_url = request.GET.get("next", "/")
    if not url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        next_url = "/"
    new_theme = "light" if request.COOKIES.get("theme") == "dark" else "dark"
    response = redirect(next_url)
    response.set_cookie("theme", new_theme, max_age=60 * 60 * 24 * 365)
    return response
