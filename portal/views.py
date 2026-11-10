import json
from pathlib import Path

from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

DATA_DIR = Path(__file__).resolve().parent / "data"

UI_TEXT = {
    "en": {
        "dark_mode": "Dark mode",
        "light_mode": "Light mode",
        "dark_aria": "Switch to dark mode",
        "light_aria": "Switch to light mode",
        "sources": "Sources",
        "as_of": "As of",
        "checked": "Checked",
        "page_not_found": "Page not found",
        "page_not_found_text": "The page you are looking for does not exist.",
        "back_home": "Back to the homepage",
        "toggle_navigation": "Toggle navigation",
        "source": "Source",
    },
    "ar": {
        "dark_mode": "الوضع الداكن",
        "light_mode": "الوضع الفاتح",
        "dark_aria": "التبديل إلى الوضع الداكن",
        "light_aria": "التبديل إلى الوضع الفاتح",
        "sources": "المصادر",
        "as_of": "حتى",
        "checked": "تاريخ التحقق",
        "page_not_found": "الصفحة غير موجودة",
        "page_not_found_text": "عذرًا، الصفحة التي تبحث عنها غير موجودة.",
        "back_home": "العودة إلى الصفحة الرئيسية",
        "toggle_navigation": "فتح أو إغلاق القائمة",
        "source": "المصدر",
    },
}


def get_language(request):
    "Return the selected language"
    language = request.session.get("language", "en")
    return language if language in ("en", "ar") else "en"


def get_common_context(request):
    "Return values shared by all pages"
    language = get_language(request)
    return {
        "language": language,
        "direction": "rtl" if language == "ar" else "ltr",
        "ui": UI_TEXT[language],
    }


def load_json(filename, language="en"):
    "Load localized JSON, falling back to English if a translation is missing."
    localized_file = DATA_DIR / language / filename

    if language == "ar" and localized_file.exists():
        file_path = localized_file
    else:
        file_path = DATA_DIR / filename

    try:
        with open(file_path, encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError as error:
        raise Http404(f"Missing data file: {filename}") from error


def find_page_content(site, slug, language="en"):
    """Return the content for a slug registered in site.json."""
    entry = next((page for page in site["pages"] if page["slug"] == slug), None)
    if entry is None:
        raise Http404(f"Unknown page: {slug}")

    content = load_json(entry["data_file"], language)

    if "section" in entry:
        content = content.get(entry["section"])
        if content is None:
            raise Http404(
                f"Missing section '{entry['section']}' in {entry['data_file']}"
            )

    return content


def build_journey(site, home_content):
    "Join each journey step with its localized page title."
    titles = {page["slug"]: page["title"] for page in site["pages"]}
    return [
        {
            "slug": step["slug"],
            "title": titles[step["slug"]],
            "teaser": step["teaser"],
        }
        for step in home_content["journey"]["steps"]
    ]


def resolve_sources(page, site):
    "Number the page's sources and tag each item with its source number."
    references = {
        reference["id"]: reference for reference in site["references"]
    }

    page["source_refs"] = [
        {**references[source_id], "number": number}
        for number, source_id in enumerate(page["sources"], start=1)
    ]

    numbers = {
        ref["id"]: ref["number"] for ref in page["source_refs"]
    }

    for section in page["sections"]:
        for item in section["items"]:
            if "source" in item:
                item["source_number"] = numbers[item["source"]]

    return page


def home(request):
    language = get_language(request)
    site = load_json("site.json", language)
    home_content = load_json("home.json", language)

    context = {
        **get_common_context(request),
        "site": site,
        "home": home_content,
        "journey_steps": build_journey(site, home_content),
        "current_slug": "",
    }

    return render(request, "portal/home.html", context)


def content_page(request, slug):
    language = get_language(request)
    site = load_json("site.json", language)

    context = {
        **get_common_context(request),
        "site": site,
        "page": resolve_sources(
            find_page_content(site, slug, language), site
        ),
        "current_slug": slug,
    }

    return render(request, "portal/page.html", context)


@require_POST
def set_language(request):
    "Save the selected language and return to the previous page."
    language = request.POST.get("language")

    if language in ("en", "ar"):
        request.session["language"] = language

    next_url = request.META.get("HTTP_REFERER")

    if not next_url or not url_has_allowed_host_and_scheme(
        next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        next_url = reverse("portal:home")

    return HttpResponseRedirect(next_url)


def page_not_found(request, exception):
    language = get_language(request)
    context = {
        **get_common_context(request),
        "site": load_json("site.json", language),
    }

    return render(request, "portal/404.html", context, status=404)