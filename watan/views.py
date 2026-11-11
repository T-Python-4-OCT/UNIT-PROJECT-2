from django.http import Http404
from django.shortcuts import redirect, render

from . import data_loader as dl


def home(request):
    content = dl.load_content()
    context = {
        "intro": content["intro"],
        "stats": content["stats"],
        "eras": content["eras"],
        "cities": content["cities"],
    }
    return render(request, "watan/home.html", context)


def history(request):
    return render(request, "watan/history.html", {"eras": dl.get_eras()})


def era_detail(request, era_slug):
    era = dl.get_era(era_slug)
    if era is None:
        raise Http404("المرحلة التاريخية غير موجودة")
    if era_slug != era["slug"]:  # /history/ANCIENT/ -> /history/ancient/
        return redirect("watan:era_detail", era_slug=era["slug"], permanent=True)

    prev_era, next_era = dl.neighbours(dl.get_eras(), era)
    related = [dl.get_city(s) for s in era.get("related_cities", [])]
    context = {
        "era": era,
        "prev_era": prev_era,
        "next_era": next_era,
        "related_cities": [c for c in related if c],
    }
    return render(request, "watan/era_detail.html", context)


def cities(request):
    content = dl.load_content()
    return render(request, "watan/cities.html",
                  {"cities": content["cities"], "regions": content["regions"]})


def city_detail(request, city_slug):
    city = dl.get_city(city_slug)
    if city is None:
        raise Http404("المدينة غير موجودة")
    if city_slug != city["slug"]:  # /city/Riyadh/ -> /city/riyadh/
        return redirect("watan:city_detail", city_slug=city["slug"], permanent=True)

    all_cities = dl.get_cities()
    prev_city, next_city = dl.neighbours(all_cities, city)
    context = {
        "city": city,
        "prev_city": prev_city,
        "next_city": next_city,
        "other_cities": [c for c in all_cities if c["slug"] != city["slug"]],
    }
    return render(request, "watan/city_detail.html", context)


def about(request):
    return render(request, "watan/about.html", {"about": dl.load_content()["about"]})


def page_not_found(request, exception=None):
    return render(request, "watan/404.html", status=404)
