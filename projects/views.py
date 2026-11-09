from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import get_language, override

from .content import feature_records, localized_features, localized_image, localized_projects


def page_languages(route, **kwargs):
    current = get_language()
    paths = {}
    for code in ("en", "ar"):
        with override(code):
            paths[code] = reverse(route, kwargs=kwargs)
    alternate = "en" if current == "ar" else "ar"
    return {"language_paths": paths, "alternate_language": alternate, "alternate_url": paths[alternate]}


def home(request):
    language = get_language()
    context = page_languages("home")
    context["projects"] = localized_projects(language)
    panorama = next(photo for photo in feature_records()["qiddiya"]["gallery"] if photo.get("panorama"))
    context["panorama"] = localized_image(panorama, language)
    return render(request, "home.html", context)


def project(request, slug):
    language = get_language()
    projects = localized_projects(language)
    for index, record in enumerate(projects):
        if record["slug"] == slug:
            context = page_languages("project", slug=slug)
            context["project"] = {**record, **localized_features(record, language)}
            context["next_project"] = projects[(index + 1) % len(projects)] if len(projects) > 1 else None
            return render(request, "project.html", context)
    return not_found(request)


def not_found(request, exception=None):
    return render(request, "404.html", page_languages("not_found"), status=404)
