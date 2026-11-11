from copy import deepcopy

from django.http import Http404
from django.shortcuts import render
from django.utils.translation import get_language

from .data import CITIES
from .history_data import (
    HISTORY_MILESTONES,
    SAUDI_KINGS,
    HISTORY_GALLERY,
    NATIONAL_DAYS,
    HISTORY_SOURCES,
)
from .history_chapters import HISTORY_CHAPTERS
from .localization import (
    CITY_EN,
    HISTORY_MILESTONES_EN,
    SAUDI_KINGS_EN,
    HISTORY_GALLERY_EN,
    NATIONAL_DAYS_EN,
    HISTORY_SOURCES_EN,
    HISTORY_CHAPTERS_EN,
)


def is_english():
    return get_language() == "en"


def get_cities():
    cities = deepcopy(CITIES)
    if is_english():
        for city in cities:
            english_copy = CITY_EN.get(city["slug"], {})
            city.update(english_copy)
            for index, image in enumerate(city["gallery"]):
                captions = english_copy.get("gallery_captions", [])
                if index < len(captions):
                    image["caption"] = captions[index]
    return cities


def get_history_chapters():
    chapters = deepcopy(HISTORY_CHAPTERS)
    if is_english():
        for chapter in chapters:
            chapter.update(HISTORY_CHAPTERS_EN.get(chapter["slug"], {}))
    return chapters


def get_history_content():
    milestones = deepcopy(HISTORY_MILESTONES)
    kings = deepcopy(SAUDI_KINGS)
    gallery = deepcopy(HISTORY_GALLERY)
    national_days = deepcopy(NATIONAL_DAYS)
    sources = deepcopy(HISTORY_SOURCES)

    if is_english():
        for item, english_item in zip(milestones, HISTORY_MILESTONES_EN):
            item.update(english_item)
        for index, (item, english_item) in enumerate(zip(kings, SAUDI_KINGS_EN)):
            item.update(english_item)
            if index in (0, 1, 2, 3, 4, 6):
                item["image_credit"] = "Saudi Press Agency"
            else:
                item["image_credit"] = "U.S. Department of Defense"
        for item, english_item in zip(gallery, HISTORY_GALLERY_EN):
            item.update(english_item)
        for item, english_item in zip(national_days, NATIONAL_DAYS_EN):
            item.update(english_item)
        for item, english_item in zip(sources, HISTORY_SOURCES_EN):
            item.update(english_item)

    return milestones, kings, gallery, national_days, sources


def home(request):
    cities = get_cities()
    return render(request, "kingdom/home.html", {
        "cities": cities,
        "featured_cities": cities,
        "history_chapters": get_history_chapters(),
    })


def city_detail(request, slug):
    cities = get_cities()
    city_index = next((index for index, item in enumerate(cities) if item["slug"] == slug), None)
    if city_index is None:
        raise Http404("City not found" if is_english() else "المدينة غير موجودة")

    city = cities[city_index]
    # Rotate the list so each city page suggests the next three destinations.
    rotated_cities = cities[city_index + 1:] + cities[:city_index]
    related_cities = rotated_cities[:3]
    return render(request, "kingdom/city_detail.html", {
        "city": city,
        "related_cities": related_cities,
    })


def history(request):
    milestones, kings, gallery, national_days, sources = get_history_content()
    return render(request, "kingdom/history.html", {
        "milestones": milestones,
        "kings": kings,
        "gallery": gallery,
        "national_days": national_days,
        "sources": sources,
        "chapters": get_history_chapters(),
    })


def history_detail(request, slug):
    chapter = next((item for item in get_history_chapters() if item["slug"] == slug), None)
    if chapter is None:
        raise Http404("History chapter not found" if is_english() else "الصفحة التاريخية غير موجودة")
    return render(request, "kingdom/history_detail.html", {"chapter": chapter})


def about(request):
    return render(request, "kingdom/about.html", {"history_chapters": get_history_chapters()})
