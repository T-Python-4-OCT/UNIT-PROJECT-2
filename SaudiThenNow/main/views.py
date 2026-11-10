from django.shortcuts import render, redirect
from django.http import Http404
from django.utils.http import url_has_allowed_host_and_scheme
from .translations import load_json, get_lang, localize


TOPIC_ORDER = ["riyadh", "transport", "economy", "education", "tourism", "events", "digital"]


def get_topics(request):
    lang = get_lang(request)
    return [localize(load_json(f"topics/{slug}.json"), lang) for slug in TOPIC_ORDER]


def go_back(request):
    next_url = request.GET.get("next", "/")
    if not url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        next_url = "/"
    return redirect(next_url)


def home_view(request):
    return render(request, "main/index.html", {"topics": get_topics(request)})


def topic_view(request, slug):
    topics = get_topics(request)

    for topic in topics:
        if topic["slug"] == slug:
            others = [other for other in topics if other["slug"] != slug]
            templates = [f"main/topics/{slug}.html", "main/topics/topic_base.html"]
            return render(request, templates, {"topic": topic, "others": others})

    raise Http404("Topic not found")


def timeline_view(request):
    return render(request, "main/timeline.html")


def about_view(request):
    return render(request, "main/about.html")


def theme_view(request):
    response = go_back(request)

    if request.COOKIES.get("theme") == "dark":
        response.set_cookie("theme", "light", max_age=60 * 60 * 24 * 365)
    else:
        response.set_cookie("theme", "dark", max_age=60 * 60 * 24 * 365)

    return response


def lang_view(request, lang):
    response = go_back(request)

    if lang in ("en", "ar"):
        response.set_cookie("lang", lang, max_age=60 * 60 * 24 * 365)

    return response
