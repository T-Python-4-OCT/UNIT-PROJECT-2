import random
import re
from urllib.parse import urlparse

from django.http import Http404
from django.shortcuts import render
from .data_loader import (
    get_ministries,
    get_ministry,
    get_all_ministries,
    get_home_features,
    get_quiz_questions,
    get_random_facts,
    get_site_content,
)


def home(request):
    features = get_home_features()
    home_video = f"https://www.youtube-nocookie.com/embed/{features['video']['video_id']}"
    ministries = get_ministries()
    years = [item["timeline"][0]["year"] for item in ministries if item["timeline"]]
    categories = sorted({item["category"] for item in ministries})
    fact = random.choice(get_random_facts())
    vision_cards = [
        {
            **pillar,
            "ministries": [
                ministry
                for ministry in ministries
                if pillar["title"] in ministry["vision_goals"]
            ],
        }
        for pillar in get_site_content()["vision_pillars"]
    ]
    return render(
        request,
        "ministries/home.html",
        {
            "ministries": ministries,
            "categories": categories,
            "ministry_count": len(ministries),
            "category_count": len(categories),
            "oldest_year": min(years) if years else "",
            "timeline_ministries": sorted(
                (item for item in ministries if item["timeline"]),
                key=lambda item: item["timeline"][0]["year"],
            ),
            "daily_fact": fact,
            "vision_pillars": vision_cards,
            "hero_video_url": youtube_background_url(home_video),
        },
    )


def ministry_directory(request):
    ministries = get_all_ministries()
    return render(
        request,
        "ministries/directory.html",
        {
            "directory_ministries": ministries,
            "directory_categories": sorted({item["category"] for item in ministries}),
        },
    )


def ministry_detail(request, slug):
    ministry = get_ministry(slug)
    if ministry is None:
        raise Http404("الوزارة غير موجودة")
    ministries = get_ministries()
    current_index = next(
        index for index, item in enumerate(ministries) if item["slug"] == slug
    )
    previous_ministry = ministries[current_index - 1] if current_index else None
    next_ministry = (
        ministries[current_index + 1]
        if current_index + 1 < len(ministries)
        else None
    )
    related = [
        item
        for item in ministries
        if item["category"] == ministry["category"] and item["slug"] != slug
    ][:3]
    return render(
        request,
        "ministries/detail.html",
        {
            "ministry": ministry,
            "previous_ministry": previous_ministry,
            "next_ministry": next_ministry,
            "related_ministries": related,
            "video_embed_url": youtube_embed_url(ministry["video_url"]),
        },
    )


def about(request):
    return render(request, "ministries/about.html")


def timeline(request):
    ministries = sorted(
        (item for item in get_ministries() if item["timeline"]),
        key=lambda item: item["timeline"][0]["year"],
    )
    return render(request, "ministries/timeline.html", {"ministries": ministries})


def compare(request):
    ministries = get_ministries()
    by_slug = {item["slug"]: item for item in ministries}
    first = by_slug.get(request.GET.get("first"))
    second = by_slug.get(request.GET.get("second"))
    selected = [first, second] if first and second and first != second else []
    return render(
        request,
        "ministries/compare.html",
        {"ministries": ministries, "selected": selected, "first": first, "second": second},
    )


def quiz(request):
    return render(
        request,
        "ministries/quiz.html",
        {"questions": get_quiz_questions()},
    )


def youtube_embed_url(url):
    if not url:
        return ""
    parsed = urlparse(url)
    if parsed.hostname not in {"www.youtube.com", "youtube.com", "youtu.be"}:
        return ""
    if parsed.hostname == "youtu.be":
        video_id = parsed.path.strip("/")
    elif parsed.path == "/watch":
        from urllib.parse import parse_qs

        video_id = parse_qs(parsed.query).get("v", [""])[0]
    else:
        match = re.fullmatch(r"/embed/([A-Za-z0-9_-]+)", parsed.path)
        video_id = match.group(1) if match else ""
    if not re.fullmatch(r"[A-Za-z0-9_-]{11}", video_id):
        return ""
    return f"https://www.youtube-nocookie.com/embed/{video_id}"


def youtube_background_url(url):
    parsed = urlparse(url)
    if parsed.hostname != "www.youtube-nocookie.com":
        return ""
    match = re.fullmatch(r"/embed/([A-Za-z0-9_-]{11})", parsed.path)
    if not match:
        return ""
    video_id = match.group(1)
    return (
        f"https://www.youtube-nocookie.com/embed/{video_id}"
        f"?autoplay=1&mute=1&controls=0&loop=1&playlist={video_id}"
        "&playsinline=1&rel=0"
    )


def page_not_found(request, exception):
    return render(request, "ministries/404.html", status=404)