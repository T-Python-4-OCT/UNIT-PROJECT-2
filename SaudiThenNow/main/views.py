from django.shortcuts import render, redirect
from django.http import Http404
from django.utils.http import url_has_allowed_host_and_scheme
from .data import TOPICS

def home_view(request):
    return render(request, "main/index.html", {"topics": TOPICS})


def topic_view(request, slug):
    for topic in TOPICS:
        if topic["slug"] == slug:
            return render(request, "main/topic.html", {"topic": topic})

    raise Http404("Topic not found")


def timeline_view(request):
    return render(request, "main/timeline.html")


def about_view(request):
    return render(request, "main/about.html")



def theme_view(request):
    next_url = request.GET.get("next", "/")
    if not url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        next_url = "/"

    response = redirect(next_url)

    if request.COOKIES.get("theme") == "dark":
        response.set_cookie("theme", "light", max_age=60 * 60 * 24 * 365)
    else:
        response.set_cookie("theme", "dark", max_age=60 * 60 * 24 * 365)

    return response