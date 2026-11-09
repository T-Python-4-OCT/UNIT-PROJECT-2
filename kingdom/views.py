from copy import deepcopy

from django.http import Http404
from django.shortcuts import render
from django.utils.translation import get_language

from .data import CITIES, STORIES
from .history_data import (
    HISTORY_MILESTONES,
    SAUDI_KINGS,
    HISTORY_GALLERY,
    NATIONAL_DAYS,
    HISTORY_SOURCES,
)
from .localization import (
    CITY_EN,
    STORY_EN,
    HISTORY_MILESTONES_EN,
    SAUDI_KINGS_EN,
    HISTORY_GALLERY_EN,
    NATIONAL_DAYS_EN,
    HISTORY_SOURCES_EN,
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


def get_stories():
    stories = deepcopy(STORIES)
    if is_english():
        for story in stories:
            story.update(STORY_EN.get(story["slug"], {}))
    return stories


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
    stories = get_stories()
    return render(request, "kingdom/home.html", {
        "cities": cities,
        "featured_cities": cities,
        "stories": stories,
    })


def city_detail(request, slug):
    city = next((item for item in get_cities() if item["slug"] == slug), None)
    if city is None:
        raise Http404("City not found" if is_english() else "المدينة غير موجودة")
    return render(request, "kingdom/city_detail.html", {"city": city})


def stories(request):
    return render(request, "kingdom/stories.html", {"stories": get_stories()})


def story_detail(request, slug):
    story = next((item for item in get_stories() if item["slug"] == slug), None)
    if story is None:
        raise Http404("Story not found" if is_english() else "القصة غير موجودة")
    return render(request, "kingdom/story_detail.html", {"story": story})


def about(request):
    return render(request, "kingdom/about.html")


def history(request):
    milestones, kings, gallery, national_days, sources = get_history_content()
    return render(request, "kingdom/history.html", {
        "milestones": milestones,
        "kings": kings,
        "gallery": gallery,
        "national_days": national_days,
        "sources": sources,
    })
