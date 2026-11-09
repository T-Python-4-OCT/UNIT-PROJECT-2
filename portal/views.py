"""Views: read the JSON content and hand it to the templates."""
import json
from pathlib import Path

from django.http import Http404
from django.shortcuts import render

DATA_DIR = Path(__file__).resolve().parent / "data"


def load_json(filename):
    """Return the parsed content of a file in the data folder."""
    try:
        with open(DATA_DIR / filename, encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError as error:
        raise Http404(f"Missing data file: {filename}") from error


def find_page_content(site, slug):
    """Return the content for a slug that is registered in site.json."""
    entry = next((page for page in site["pages"] if page["slug"] == slug), None)
    if entry is None:
        raise Http404(f"Unknown page: {slug}")

    content = load_json(entry["data_file"])
    if "section" in entry:
        content = content.get(entry["section"])
        if content is None:
            raise Http404(f"Missing section '{entry['section']}' in {entry['data_file']}")
    return content


def build_journey(site, home_content):
    """Join each journey step with its page title from site.json."""
    titles = {page["slug"]: page["title"] for page in site["pages"]}
    return [
        {"slug": step["slug"], "title": titles[step["slug"]], "teaser": step["teaser"]}
        for step in home_content["journey"]["steps"]
    ]


def home(request):
    site = load_json("site.json")
    home_content = load_json("home.json")
    context = {
        "site": site,
        "home": home_content,
        "journey_steps": build_journey(site, home_content),
        "current_slug": "",
    }
    return render(request, "portal/home.html", context)


def content_page(request, slug):
    site = load_json("site.json")
    context = {
        "site": site,
        "page": find_page_content(site, slug),
        "current_slug": slug,
    }
    return render(request, "portal/page.html", context)


def page_not_found(request, exception):
    context = {"site": load_json("site.json")}
    return render(request, "portal/404.html", context, status=404)
