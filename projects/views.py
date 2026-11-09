from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import get_language, override

from .content import find_project, localized_projects, timeline as timeline_entries

LANGUAGE_CODES = ("en", "ar")


def page_context(request, route, active=None, **kwargs):
    current = get_language()
    paths = {}
    for code in LANGUAGE_CODES:
        with override(code):
            paths[code] = reverse(route, kwargs=kwargs)
    alternate = "en" if current == "ar" else "ar"
    query = request.GET.urlencode()
    suffix = f"?{query}" if query and route == "timeline" else ""
    return {
        "language_paths": paths,
        "absolute_paths": {code: request.build_absolute_uri(path) for code, path in paths.items()},
        "canonical_url": request.build_absolute_uri(paths[current]) + suffix,
        "alternate_language": alternate,
        "alternate_url": paths[alternate] + suffix,
        "active": active,
        "nav_projects": localized_projects(current),
    }


def home(request):
    context = page_context(request, "home", active="home")
    context["projects"] = context["nav_projects"]
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
            years.append({"year": entry["year"], "entries": []})
        years[-1]["entries"].append(entry)
    context.update(years=years, selected=selected, entry_count=len(entries))
    return render(request, "timeline.html", context)


def compare(request):
    context = page_context(request, "compare", active="compare")
    return render(request, "compare.html", context)


def not_found(request, exception=None):
    return render(request, "404.html", page_context(request, "not_found"), status=404)


def robots(request):
    sitemap = request.build_absolute_uri("/sitemap.xml")
    return HttpResponse(f"User-agent: *\nAllow: /\nSitemap: {sitemap}\n", content_type="text/plain")


def sitemap(request):
    routes = [("home", {}), ("timeline", {}), ("compare", {})]
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
