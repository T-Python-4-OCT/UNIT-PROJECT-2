from django.shortcuts import render, redirect
from django.http import HttpRequest
from .data.sites import sites
import random
from .data.people import people, explorers


def home_view(request: HttpRequest):
    return render(request, "main/home.html", {"sites": sites})


def sites_view(request: HttpRequest):
    selected = request.GET.get("region")
    query = request.GET.get("q", "").strip()

    regions = []
    for site in sites:
        if site["region"] not in regions:
            regions.append(site["region"])

    result = []
    for site in sites:
        if selected and site["region"] != selected:
            continue

        text = site["name"] + " " + site["region"] + " " + site["tagline"]
        if query and query not in text:
            continue

        result.append(site)

    return render(request, "main/sites.html", {
        "sites": result,
        "regions": regions,
        "selected": selected,
        "query": query,
    })

def site_detail_view(request: HttpRequest, slug):
    for site in sites:
        if site["slug"] == slug:
            others = []
            for other in sites:
                if other["slug"] != slug:
                    others.append(other)
            return render(request, "main/site_detail.html", {
                "site": site,
                "others": random.sample(others, 3),
                "is_favorite": slug in get_favorites(request),
            })
    return render(request, "main/404.html", status=404)

def toggle_theme(request: HttpRequest):
    current = request.COOKIES.get("theme", "light")
    new_theme = "light" if current == "dark" else "dark"

    next_url = request.META.get("HTTP_REFERER") or "/"
    response = redirect(next_url)
    response.set_cookie("theme", new_theme, max_age=60 * 60 * 24 * 30)
    return response

def get_favorites(request):
    value = request.COOKIES.get("favorites", "")
    if value == "":
        return []
    return value.split(",")


def toggle_favorite(request, slug):
    favorites = get_favorites(request)
    if slug in favorites:
        favorites.remove(slug)
    else:
        favorites.append(slug)
    response = redirect(request.META.get("HTTP_REFERER", "/"))
    response.set_cookie("favorites", ",".join(favorites), max_age=60 * 60 * 24 * 30)
    return response


def favorites_view(request):
    favorites = get_favorites(request)
    result = []
    for site in sites:
        if site["slug"] in favorites:
            result.append(site)
    return render(request, "main/favorites.html", {"sites": result})

def about_view(request: HttpRequest):
    return render(request, "main/about.html", {"people": people, "explorers": explorers})