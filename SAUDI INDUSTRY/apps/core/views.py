from django.contrib.staticfiles import finders
from django.http import Http404
from django.shortcuts import render

from apps.catalog.content_loader import load_json


def home(request):
    home_data = load_json("home.json")
    industries_data = load_json("industries.json")

    industry_map = {
        industry["slug"]: industry
        for industry in industries_data["industries"]
    }

    featured_industries = [
        industry_map[slug]
        for slug in home_data["featured_industries"]
        if slug in industry_map
    ]

    context = {
        "home": home_data,
        "featured_industries": featured_industries,
    }

    return render(request, "core/home.html", context)


def load_technologies(technology_data):
    industries_data = load_json("industries.json")

    industry_lookup = {
        industry["slug"]: industry
        for industry in industries_data["industries"]
    }

    return [
        {
            **item,
            "industries": [
                industry_lookup[slug]
                for slug in item["industry_slugs"]
                if slug in industry_lookup
            ]
        }
        for item in technology_data["technologies"]
    ]


def technology(request):
    technology_data = load_json("technology.json")
    page = technology_data["page"]
    all_technologies = load_technologies(technology_data)

    search_query = request.GET.get("q", "").strip()
    selected_category = request.GET.get("category", "").strip()
    selected_industry = request.GET.get("industry", "").strip()

    categories = sorted({
        item["category"]
        for item in all_technologies
    })

    industry_options = sorted(
        {
            industry["slug"]: industry
            for item in all_technologies
            for industry in item["industries"]
        }.values(),
        key=lambda industry: industry["name"]
    )

    filtered_technologies = all_technologies

    if search_query:
        query = search_query.casefold()

        filtered_technologies = [
            item
            for item in filtered_technologies
            if query in " ".join([
                item["name"],
                item["category"],
                item["description"],
                item["overview"],
                " ".join(item["applications"]),
                " ".join(
                    industry["name"]
                    for industry in item["industries"]
                ),
            ]).casefold()
        ]

    if selected_category:
        filtered_technologies = [
            item
            for item in filtered_technologies
            if item["category"] == selected_category
        ]

    if selected_industry:
        filtered_technologies = [
            item
            for item in filtered_technologies
            if selected_industry in item["industry_slugs"]
        ]

    context = {
        "page": page,
        "technologies": filtered_technologies,
        "categories": categories,
        "industry_options": industry_options,
        "search_query": search_query,
        "selected_category": selected_category,
        "selected_industry": selected_industry,
        "total_technologies": len(all_technologies),
    }

    return render(
        request,
        "core/technology.html",
        context
    )


def technology_detail(request, slug):
    technology_data = load_json("technology.json")
    all_technologies = load_technologies(technology_data)

    item = next(
        (
            technology
            for technology in all_technologies
            if technology["slug"] == slug
        ),
        None
    )

    if item is None:
        raise Http404("Technology not found")

    return render(
        request,
        "core/technology_detail.html",
        {"technology": item}
    )


def vision2030(request):
    vision_data = load_json("vision2030.json")
    return render(
        request,
        "core/vision2030.html",
        {"vision": vision_data}
    )


def gallery(request):
    gallery_data = load_json("gallery.json")

    all_media = [
        {
            **item,
            "available": (
                bool(finders.find(item["file"]))
                if item["type"] == "image"
                else item.get("video_url", "").startswith("https://")
            )
        }
        for item in gallery_data["media"]
    ]

    available_media = [
        item for item in all_media
        if item["available"]
    ]

    pending_media = [
        item for item in all_media
        if not item["available"]
    ]

    search_query = request.GET.get("q", "").strip()
    selected_type = request.GET.get("type", "").strip()
    selected_category = request.GET.get("category", "").strip()

    categories = sorted({
        item["category"]
        for item in all_media
    })

    filtered_media = available_media

    if search_query:
        query = search_query.casefold()

        filtered_media = [
            item
            for item in filtered_media
            if query in " ".join([
                item["title"],
                item["description"],
                item["category"],
                item["origin_note"],
                item["creator"],
            ]).casefold()
        ]

    if selected_type:
        filtered_media = [
            item
            for item in filtered_media
            if item["type"] == selected_type
        ]

    if selected_category:
        filtered_media = [
            item
            for item in filtered_media
            if item["category"] == selected_category
        ]

    context = {
        "page": gallery_data["page"],
        "items": filtered_media,
        "pending_media": pending_media,
        "categories": categories,
        "search_query": search_query,
        "selected_type": selected_type,
        "selected_category": selected_category,
        "available_total": len(available_media),
        "pending_total": len(pending_media),
    }

    return render(
        request,
        "core/gallery.html",
        context
    )


def about(request):
    about_data = load_json("about.json")
    return render(
        request,
        "core/about.html",
        {"about": about_data}
    )
