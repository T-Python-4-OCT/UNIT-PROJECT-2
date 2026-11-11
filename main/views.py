from django.http import Http404, HttpRequest
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme

from .history_data import LEGENDS, MOMENTS, TOURNAMENTS, summary
from .journey_data import BID_NUMBERS, MILESTONES, ROADMAP
from .data import CITIES, COUNTDOWN_TARGET, EXPLORE, STADIUMS, STATS, get_city, get_stadium, stadiums_in


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
    other_cities = [c for c in CITIES if c["slug"] != slug]
    return render(request, "main/city.html", {
        "city": city,
        "stadiums": stadiums_in(slug),
        "other_cities": other_cities,
    })


def stadiums_view(request: HttpRequest):
    # Query parameters: ?city=riyadh  and  ?sort=capacity
    city_slug = request.GET.get("city", "")
    sort = request.GET.get("sort", "")

    stadiums = stadiums_in(city_slug) if get_city(city_slug) else list(STADIUMS)
    if sort == "capacity":
        stadiums = sorted(stadiums, key=lambda s: s["capacity"], reverse=True)

    total = sum(s["capacity"] for s in stadiums)
    return render(request, "main/stadiums.html", {
        "stadiums": stadiums,
        "cities": CITIES,
        "selected_city": get_city(city_slug),
        "sort": sort,
        "total_capacity": f"{total:,}",
    })


def stadium_view(request: HttpRequest, slug):
    stadium = get_stadium(slug)
    if stadium is None:
        raise Http404("Stadium not found")
    city = get_city(stadium["city"])
    neighbours = [s for s in stadiums_in(stadium["city"]) if s["slug"] != slug]
    return render(request, "main/stadium.html", {
        "stadium": stadium,
        "city": city,
        "neighbours": neighbours,
    })


def history_view(request: HttpRequest):
    return render(request, "main/history.html", {
        "tournaments": TOURNAMENTS,
        "moments": MOMENTS,
        "legends": LEGENDS,
        "summary": summary(),
    })


def journey_view(request: HttpRequest):
    return render(request, "main/journey.html", {
        "milestones": MILESTONES,
        "roadmap": ROADMAP,
        "bid_numbers": BID_NUMBERS,
    })


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
