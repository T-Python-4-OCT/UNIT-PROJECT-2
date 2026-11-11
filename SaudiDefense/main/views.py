from django.shortcuts import render, redirect
from django.http import HttpRequest, Http404

from .context_processors import get_lang
from datetime import date

from .data import SECTORS, COMPANIES, HISTORY, EVENTS, FAQ, UPCOMING_EVENTS, CAREERS, CAREER_MAJORS

# Create your views here.
# كل البيانات في data.py بلغتين، و get_lang(request) تعطينا "ar" أو "en"


def home_view(request: HttpRequest):

    lang = get_lang(request)
    context = {"sectors": SECTORS[lang], "companies": COMPANIES[lang], "faq": FAQ[lang]}
    return render(request, "main/index.html", context)


def sector_view(request: HttpRequest, sector_name):

    lang = get_lang(request)
    if sector_name not in SECTORS[lang]:
        raise Http404("القطاع غير موجود")

    context = {"page": SECTORS[lang][sector_name]}
    return render(request, "main/details.html", context)


def company_view(request: HttpRequest, company_name):

    lang = get_lang(request)
    if company_name not in COMPANIES[lang]:
        raise Http404("الجهة غير موجودة")

    context = {"page": COMPANIES[lang][company_name]}
    return render(request, "main/details.html", context)


def vision_view(request: HttpRequest):

    return render(request, "main/vision.html")


def history_view(request: HttpRequest):

    lang = get_lang(request)
    return render(request, "main/history.html", {"history": HISTORY[lang]})


def events_view(request: HttpRequest):

    lang = get_lang(request)

    # المعارض القادمة: نحسب كم يوم باقي، ونعرض بس اللي ما بدأت للحين
    upcoming = []
    for event in UPCOMING_EVENTS[lang]:
        year, month, day = event["start"]
        days_left = (date(year, month, day) - date.today()).days
        if days_left >= 0:
            upcoming.append({**event, "days_left": days_left})

    context = {"events": EVENTS[lang], "upcoming": upcoming}
    return render(request, "main/events.html", context)


# ---------- الوظائف والتدريب ----------
def careers_view(request: HttpRequest):

    lang = get_lang(request)
    context = {"careers": CAREERS[lang], "majors": CAREER_MAJORS[lang]}
    return render(request, "main/careers.html", context)


# ---------- تغيير اللغة ----------
def set_language_view(request: HttpRequest, lang_code):

    # نرجع لنفس الصفحة اللي كان فيها المستخدم
    response = redirect(request.META.get("HTTP_REFERER", "/"))

    if lang_code in ("ar", "en"):
        response.set_cookie("lang", lang_code, max_age=60 * 60 * 24 * 365)

    return response
