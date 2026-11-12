import json
import time
from pathlib import Path

from django.http import Http404, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_http_methods, require_POST

from .forms import FeedbackForm, QuizForm, SearchForm
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
        "not_found_hint": "Try a search, or pick one of the pages below.",
        "toggle_navigation": "Toggle navigation",
        "source": "Source",
        "feedback": "Share your feedback",
        "search": "Search",
        "home": "Home",
        "tools": "Tools",
        "about_project": "About the project",
        "about_project_text": "A bilingual Django project that follows how the Ministry of Interior's services moved from the counter to the screen, with a source for every figure.",
        "back_to_top": "Back to top",
        "quiz": "Quiz",
        "quiz_cta": "Think you know the story? Eight questions, one from each part of the site.",
        "quiz_button": "Take the quiz",
        "built_with": "Built with Django as a Tuwaiq Academy project.",
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
        "not_found_hint": "جرّب البحث، أو اختر إحدى الصفحات أدناه.",
        "toggle_navigation": "فتح أو إغلاق القائمة",
        "source": "المصدر",
        "feedback": "شاركنا رأيك",
        "search": "بحث",
        "home": "الرئيسية",
        "tools": "أدوات",
        "about_project": "عن المشروع",
        "about_project_text": "مشروع Django ثنائي اللغة يتتبع انتقال خدمات وزارة الداخلية من الشباك إلى الشاشة، مع مصدر لكل رقم.",
        "back_to_top": "العودة للأعلى",
        "quiz": "اختبر معلوماتك",
        "quiz_cta": "تظن أنك تعرف القصة؟ ثمانية أسئلة، سؤال من كل جزء في الموقع.",
        "quiz_button": "ابدأ الاختبار",
        "built_with": "بُني باستخدام Django ضمن مشروع في أكاديمية طويق.",
    },
}


def get_language(request):
    "Return the selected language"
    language = request.session.get("language", "en")
    return language if language in ("en", "ar") else "en"


def build_nav_menu(site):
    """
    Group the pages for the navbar dropdowns.
    1. Start one empty group for each entry in site["nav_groups"].
    2. Put every page into the group named by its "group" key.
    3. Keep the group's slugs so the template can highlight the open section.
    """
    groups = [{**group, "pages": [], "slugs": []} for group in site.get("nav_groups", [])]
    by_id = {group["id"]: group for group in groups}

    for page in site["pages"]:
        group = by_id.get(page.get("group"))
        if group is not None:
            group["pages"].append(page)
            group["slugs"].append(page["slug"])

    return [group for group in groups if group["pages"]]


def get_common_context(request, site=None):
    "Return values shared by all pages: language, direction, UI text, site data and the navbar menu."
    language = get_language(request)
    if site is None:
        site = load_json("site.json", language)

    return {
        "language": language,
        "direction": "rtl" if language == "ar" else "ltr",
        "ui": UI_TEXT[language],
        "site": site,
        "nav_menu": build_nav_menu(site),
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


def build_journey(site, home_content, language):
    "Join each journey step with its localized page title and its header photo."
    titles = {page["slug"]: page["title"] for page in site["pages"]}
    return [
        {
            "slug": step["slug"],
            "title": titles[step["slug"]],
            "teaser": step["teaser"],
            # The photo already set for that page's header, so it lives in one place only
            "image": find_page_content(site, step["slug"], language).get("header_image"),
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


def add_comparison_bars(page):
    """
    Prepare "comparison" sections (two bars per figure, e.g. 2016 vs 2025).
    1. The larger of the two numbers fills the whole bar (100%).
    2. The other bar is drawn in proportion to it.
    3. The change is shown as a percentage, rounded to a whole number.
    """
    for section in page["sections"]:
        if section["type"] != "comparison":
            continue

        for item in section["items"]:
            largest = max(item["from"], item["to"])
            item["from_width"] = round(item["from"] / largest * 100, 1)
            item["to_width"] = round(item["to"] / largest * 100, 1)
            item["change"] = round((item["to"] - item["from"]) / item["from"] * 100)

    return page


def home(request):
    """
    Home page.
    1. Read the chosen language from the session.
    2. Load the shared site data and the home page content (JSON).
    3. Add each journey card's title and photo, then render home.html.
    """
    language = get_language(request)
    site = load_json("site.json", language)
    home_content = load_json("home.json", language)

    context = {
        **get_common_context(request, site),
        "home": home_content,
        "journey_steps": build_journey(site, home_content, language),
        "current_slug": "",
    }

    return render(request, "portal/home.html", context)


def content_page(request, slug):
    """
    One view for every content page (dynamic URL: /<slug>/).
    1. Find the page's content in its JSON file (404 if the slug is unknown).
    2. Number its sources so every figure links to where it came from.
    3. Size the bars of any comparison section.
    4. Render the shared page.html template.
    """
    language = get_language(request)
    site = load_json("site.json", language)

    context = {
        **get_common_context(request, site),
        "page": add_comparison_bars(
            resolve_sources(find_page_content(site, slug, language), site)
        ),
        "current_slug": slug,
    }

    return render(request, "portal/page.html", context)


def search(request):
    """
    Site search (GET /search/?q=...).
    1. Validate the query with SearchForm.
    2. Collect every page's content and score it with search_pages.
    3. Render results, or the form's error message.
    """
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
        **get_common_context(request, site),
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
    """
    Feedback page.
    GET: show an empty form.
    POST: validate it, block a second message within a minute, save it to the
    database, then redirect (Post/Redirect/Get) so a refresh does not resend.
    """
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
        "text": text,
        "form": form,
        "success": request.session.pop("feedback_success", False),
        "current_slug": "feedback",
    }

    return render(request, "portal/feedback.html", context)


@require_http_methods(["GET", "POST"])
def quiz(request):
    """
    Knowledge quiz (GET shows the questions, POST checks the answers).
    1. Build QuizForm from quiz.json in the current language.
    2. On a valid POST, mark every answer and count the correct ones.
    3. Keep the visitor's best score in the session.
    4. Pick a short message for the score level, then render the review.
    """
    language = get_language(request)
    text = load_json("quiz.json", language)
    form = QuizForm(request.POST or None, quiz=text)
    review = None
    score = 0

    if request.method == "POST" and form.is_valid():
        review = form.review()
        score = sum(item["is_correct"] for item in review)
        request.session["quiz_best"] = max(score, request.session.get("quiz_best", 0))

    total = len(text["questions"])
    # Four levels: under half, half or more, all but one or two, all correct
    if score == total:
        level = 3
    elif score >= total - 2:
        level = 2
    elif score >= total / 2:
        level = 1
    else:
        level = 0

    context = {
        **get_common_context(request),
        "text": text,
        "form": form,
        "review": review,
        "score": score,
        "total": total,
        "score_percent": round(score / total * 100),
        "message": text["levels"][level],
        "best": request.session.get("quiz_best"),
        "current_slug": "quiz",
    }

    return render(request, "portal/quiz.html", context)


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
    "Custom 404 page in the visitor's language (used when DEBUG is False)."
    return render(request, "portal/404.html", get_common_context(request), status=404)