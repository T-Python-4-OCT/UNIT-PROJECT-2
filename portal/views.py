import json
import time
from pathlib import Path

from django.http import Http404, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_http_methods, require_POST

from .forms import FeedbackForm, SearchForm
from .search import search_pages

DATA_DIR = Path(__file__).resolve().parent / "data"

# One feedback message per session per minute.
FEEDBACK_COOLDOWN_SECONDS = 60

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
        "feedback": "Share your feedback",
        "search": "Search",
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
        "feedback": "شاركنا رأيك",
        "search": "بحث",
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


def search(request):
    language = get_language(request)
    site = load_json("site.json", language)
    text = load_json("search.json", language)

    form = None
    results = None

    # Only validate once a search was actually sent; an empty visit just shows the box.
    if "q" in request.GET:
        form = SearchForm(request.GET, text=text)

        if form.is_valid():
            pages = [
                (page["slug"], find_page_content(site, page["slug"], language))
                for page in site["pages"]
            ]
            results = search_pages(pages, form.cleaned_data["q"])
    else:
        form = SearchForm(text=text)

    context = {
        **get_common_context(request),
        "site": site,
        "text": text,
        "form": form,
        # Shown back in the search box; Django escapes it in the template.
        "query": request.GET.get("q", ""),
        "results": results,
        "current_slug": "search",
    }

    return render(request, "portal/search.html", context)


def sent_feedback_recently(request):
    "True if this session sent feedback less than a minute ago."
    last_sent = request.session.get("feedback_last_sent")
    return last_sent is not None and time.time() - last_sent < FEEDBACK_COOLDOWN_SECONDS


@require_http_methods(["GET", "POST"])
def feedback(request):
    language = get_language(request)
    text = load_json("feedback.json", language)

    if request.method == "POST":
        form = FeedbackForm(request.POST, text=text)

        if form.is_valid():
            if sent_feedback_recently(request):
                form.add_error(None, text["errors"]["too_fast"])
            else:
                form.save(language=language)
                request.session["feedback_last_sent"] = time.time()
                request.session["feedback_success"] = True
                # Post/Redirect/Get: refreshing the page will not resend the form.
                return redirect("portal:feedback")
    else:
        form = FeedbackForm(text=text)

    context = {
        **get_common_context(request),
        "site": load_json("site.json", language),
        "text": text,
        "form": form,
        "success": request.session.pop("feedback_success", False),
        "current_slug": "feedback",
    }

    return render(request, "portal/feedback.html", context)


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