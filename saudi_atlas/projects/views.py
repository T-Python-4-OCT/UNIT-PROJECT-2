import json
from functools import cache
from pathlib import Path

from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils.cache import patch_vary_headers
from django.utils.html import conditional_escape, format_html
from django.utils.safestring import mark_safe
from django.utils.translation import get_language, gettext, override

from .content import (
    axis_position,
    find_project,
    localized_projects,
    milestone_lanes,
    search_terms,
    totals,
)
from .content import (
    search as search_projects,
)
from .content import (
    timeline as timeline_entries,
)

LANGUAGE_CODES = ("en", "ar")


def page_context(request, route, active=None, **kwargs):
    current = get_language()
    paths = {}
    for code in LANGUAGE_CODES:
        with override(code):
            paths[code] = reverse(route, kwargs=kwargs)
    alternate = "en" if current == "ar" else "ar"
    query = request.GET.urlencode()
    suffix = f"?{query}" if query and route in ("timeline", "search") else ""
    canonical_suffix = suffix if route == "timeline" else ""
    return {
        "language_paths": paths,
        "absolute_paths": {code: request.build_absolute_uri(path) for code, path in paths.items()},
        "canonical_url": request.build_absolute_uri(paths[current]) + canonical_suffix,
        "alternate_language": alternate,
        "alternate_url": paths[alternate] + suffix,
        "active": active,
        "nav_projects": localized_projects(current),
    }


def home(request):
    context = page_context(request, "home", active="home")
    context["projects"] = context["nav_projects"]
    context["totals"] = totals()
    return render(request, "home.html", context)


def project(request, slug):
    current, previous, following = find_project(slug, get_language())
    if current is None:
        return not_found(request)
    context = page_context(request, "project", active=slug, slug=slug)
    context.update(project=current, previous_project=previous, next_project=following)
    return render(request, "project.html", context)


def timeline(request):
    context = page_context(request, "timeline", active="timeline")
    selected = request.GET.get("project")
    slugs = {item["slug"] for item in context["nav_projects"]}
    selected = selected if selected in slugs else None
    entries = timeline_entries(get_language())
    if selected:
        entries = [entry for entry in entries if entry["project"]["slug"] == selected]
    years = []
    for entry in entries:
        if not years or years[-1]["year"] != entry["year"]:
            years.append({"year": entry["year"], "at": axis_position(int(entry["year"])), "entries": []})
        years[-1]["entries"].append(entry)
    context.update(
        years=years,
        selected=selected,
        entry_count=len(entries),
        chart=milestone_lanes(get_language(), selected),
    )
    return render(request, "timeline.html", context)


def compare(request):
    context = page_context(request, "compare", active="compare")
    return render(request, "compare.html", context)


PARTIAL_HEADER = "X-Atlas-Partial"


def search(request):
    context = page_context(request, "search", active="search")
    query = " ".join(request.GET.get("q", "").split())[:80]
    context.update(query=query, terms=search_terms(query), results=search_projects(query, get_language()))
    partial = request.headers.get(PARTIAL_HEADER) == "results"
    response = render(request, "includes/search_results.html" if partial else "search.html", context)
    patch_vary_headers(response, [PARTIAL_HEADER])
    return response


CREDITS_FILE = Path(__file__).resolve().parent / "data" / "credits.json"


@cache
def credits_data():
    return json.loads(CREDITS_FILE.read_text(encoding="utf-8"))


def _english(text):
    return format_html('<span lang="en" dir="ltr">{}</span>', text)


def _link(url, text, english=True, name=False):
    if english:
        if name:
            return format_html('<a class="credits-name" href="{}" lang="en" dir="ltr">{}</a>', url, text)
        return format_html('<a href="{}" lang="en" dir="ltr">{}</a>', url, text)
    return format_html('<a href="{}">{}</a>', url, text)


def _fill(message, **parts):
    return mark_safe(
        conditional_escape(message) % {key: conditional_escape(value) for key, value in parts.items()}
    )


def credits(request):
    context = page_context(request, "credits", active="credits")
    data = credits_data()
    media = []
    for project in context["nav_projects"]:
        slug = project["slug"]
        captions = {
            item["src"]: item["caption"]
            for item in [
                project["image"],
                *project.get("gallery", []),
                *(thing["image"] for thing in project["things_to_do"]),
            ]
        }
        photographs = []
        for photo in data["photographs"]:
            if photo["project"] != slug:
                continue
            if photo.get("licence"):
                credit = _fill(
                    gettext(
                        "%(title)s by %(author)s, licensed under %(licence)s, from Wikimedia Commons. Resized and re-encoded for the web."
                    ),
                    title=_link(photo["source_url"], photo["title"]),
                    author=_english(photo["author"]),
                    licence=_link(photo["licence_url"], photo["licence"], name=True),
                )
            else:
                credit = _fill(
                    gettext("%(title)s by %(author)s, from %(site)s. Resized and re-encoded for the web."),
                    title=_english(photo["title"]),
                    author=_english(photo["author"]),
                    site=_link(photo["source_url"], photo["site"], name=True),
                )
            if photo.get("terms_url"):
                credit = format_html(
                    "{} {}",
                    credit,
                    _link(photo["terms_url"], gettext("Saudi Press Agency reuse terms"), english=False),
                )
            photographs.append(
                {
                    "heading": gettext("Photograph: %(caption)s") % {"caption": captions[photo["src"]]},
                    "credit": credit,
                }
            )
        origin = data["film_origins"].get(slug)
        media.append(
            {
                "project": project,
                "origin": _fill(
                    gettext("“%(title)s” by %(publisher)s"),
                    title=_english(origin["title"]),
                    publisher=_english(origin["publisher"]),
                )
                if origin
                else None,
                "stills": [captions[src] for src in data["film_stills"].get(slug, [])],
                "photographs": photographs,
            }
        )
    context.update(
        media=media,
        typefaces=data["typefaces"],
    )
    return render(request, "credits.html", context)


def not_found(request, exception=None):
    return render(request, "404.html", page_context(request, "not_found"), status=404)


def robots(request):
    sitemap = request.build_absolute_uri("/sitemap.xml")
    return HttpResponse(f"User-agent: *\nAllow: /\nSitemap: {sitemap}\n", content_type="text/plain")


def sitemap(request):
    routes = [("home", {}), ("timeline", {}), ("compare", {}), ("credits", {})]
    routes += [("project", {"slug": item["slug"]}) for item in localized_projects("en")]
    urls = []
    for name, kwargs in routes:
        paths = {}
        for code in LANGUAGE_CODES:
            with override(code):
                paths[code] = request.build_absolute_uri(reverse(name, kwargs=kwargs))
        for code in LANGUAGE_CODES:
            urls.append({"loc": paths[code], "alternates": paths})
    return render(request, "sitemap.xml", {"urls": urls}, content_type="application/xml")
