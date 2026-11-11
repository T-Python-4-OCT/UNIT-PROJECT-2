from datetime import date
from django.shortcuts import render, redirect
from django.http import Http404, HttpRequest
from django.contrib.staticfiles import finders
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from .translations import load_json, get_lang, localize


def get_topics(request: HttpRequest):
    lang = get_lang(request)
    return [localize(topic, lang) for topic in load_json("topics.json")]


def collect(topics, field, key):
    items = {}

    for topic in topics:
        for item in topic.get(field, []):
            entry = items.setdefault(item[key], {**item, "topics": []})
            entry["topics"].append(topic)

    return sorted(items.values(), key=lambda entry: entry["year"])


def go_back(request: HttpRequest):
    next_url = request.GET.get("next", "/")
    if not url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        next_url = "/"
    return redirect(next_url)


def home_view(request: HttpRequest):
    topics = get_topics(request)
    moments = []

    for event in collect(topics, "timeline", "text"):
        topic = event["topics"][0]
        moments.append({
            "year": int(event["year"]),
            "text": event["text"],
            "icon": topic["icon"],
            "url": reverse("main:topic", args=[topic["slug"]]),
        })

    context = {
        "topics": topics,
        "moments": moments,
        "first_year": moments[0]["year"],
        "this_year": date.today().year,
    }
    return render(request, "main/index.html", context)


def topic_view(request: HttpRequest, slug: str):
    topics = get_topics(request)

    for topic in topics:
        if topic["slug"] == slug:
            others = [other for other in topics if other["slug"] != slug]
            return render(request, f"main/topics/{slug}.html", {"topic": topic, "others": others})

    raise Http404("Topic not found")


def timeline_view(request: HttpRequest):
    topics = get_topics(request)
    slides = []

    for event in collect(topics, "timeline", "text"):
        year = int(event["year"])

        if year < 1938:
            era = "before"
        elif year < 2016:
            era = "oil"
        else:
            era = "vision"

        slides.append({**event, "era": era})

    for item in collect(topics, "future", "title"):
        slides.append({**item, "text": item["title"], "era": "future", "future": True})

    for slide in slides:
        if not finders.find(slide["image"]):
            slide["image"] = None

    context = {"topics": topics, "slides": slides, "this_year": date.today().year}
    return render(request, "main/timeline.html", context)


def about_view(request: HttpRequest):
    topics = get_topics(request)
    milestones = collect(topics, "timeline", "text") + collect(topics, "future", "title")
    context = {"topics": topics, "milestone_count": len(milestones)}
    return render(request, "main/about.html", context)


def theme_view(request: HttpRequest):
    response = go_back(request)

    if request.COOKIES.get("theme") == "dark":
        response.set_cookie("theme", "light", max_age=60 * 60 * 24 * 365)
    else:
        response.set_cookie("theme", "dark", max_age=60 * 60 * 24 * 365)

    return response


def lang_view(request: HttpRequest, lang: str):
    response = go_back(request)

    if lang in ("en", "ar"):
        response.set_cookie("lang", lang, max_age=60 * 60 * 24 * 365)

    return response
