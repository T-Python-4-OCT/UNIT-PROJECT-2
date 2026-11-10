from django.http import Http404
from django.shortcuts import render
from django.utils.translation import get_language
from .data import INDUSTRIES, AWARDS, ACHIEVEMENTS, MILESTONES, AWARD_WINNERS, SECTOR_STORIES, MAP_CITIES, SAUDI_REGIONS
from . import data_en


def _content():
    if get_language() == "en":
        return data_en
    return None


def home(request):
    content = _content()
    industries = content.INDUSTRIES if content else INDUSTRIES
    return render(request, "industry/home.html", {"industries": industries[:4]})


def industry_list(request):
    content = _content()
    return render(request, "industry/industries.html", {"industries": content.INDUSTRIES if content else INDUSTRIES})


def map_view(request):
    content = _content()
    cities = content.MAP_CITIES if content else MAP_CITIES
    regions = content.SAUDI_REGIONS if content else SAUDI_REGIONS
    sectors = sorted({sector for city in cities for sector in city["sectors"]})
    return render(request, "industry/map.html", {
        "cities": cities,
        "regions": regions,
        "sector_options": sectors,
    })


def industry_detail(request, slug):
    content = _content()
    industries = content.INDUSTRIES if content else INDUSTRIES
    stories = content.SECTOR_STORIES if content else SECTOR_STORIES
    index = next((i for i, item in enumerate(industries) if item["slug"] == slug), None)
    if index is None:
        raise Http404("القطاع غير موجود")
    industry = industries[index]
    context = {
        "industry": industry,
        "previous_industry": industries[index - 1] if index > 0 else None,
        "next_industry": industries[index + 1] if index + 1 < len(industries) else None,
        **stories.get(slug, {}),
    }
    return render(request, "industry/detail.html", context)


def awards(request):
    content = _content()
    if content:
        return render(request, "industry/awards.html", {
            "awards": content.AWARDS,
            "achievements": content.ACHIEVEMENTS,
            "milestones": content.MILESTONES,
            "award_winners": content.AWARD_WINNERS,
        })
    return render(request, "industry/awards.html", {
        "awards": AWARDS,
        "achievements": ACHIEVEMENTS,
        "milestones": MILESTONES,
        "award_winners": AWARD_WINNERS,
    })


def about(request):
    return render(request, "industry/about.html")
