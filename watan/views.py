from django.http import Http404, JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import redirect, render

from . import data_loader as dl


def home(request):
    content = dl.load_content()
    context = {
        "intro": content["intro"],
        "stats": content["stats"],
        "eras": content["eras"],
        "cities": content["cities"],
    }
    return render(request, "watan/home.html", context)


def history(request):
    return render(request, "watan/history.html", {"eras": dl.get_eras()})


def era_detail(request, era_slug):
    era = dl.get_era(era_slug)
    if era is None:
        raise Http404("المرحلة التاريخية غير موجودة")
    if era_slug != era["slug"]:  # /history/ANCIENT/ -> /history/ancient/
        return redirect("watan:era_detail", era_slug=era["slug"], permanent=True)

    prev_era, next_era = dl.neighbours(dl.get_eras(), era)
    related = [dl.get_city(s) for s in era.get("related_cities", [])]
    context = {
        "era": era,
        "prev_era": prev_era,
        "next_era": next_era,
        "related_cities": [c for c in related if c],
    }
    return render(request, "watan/era_detail.html", context)


def cities(request):
    content = dl.load_content()
    return render(request, "watan/cities.html",
                  {"cities": content["cities"], "regions": content["regions"]})


def city_detail(request, city_slug):
    city = dl.get_city(city_slug)
    if city is None:
        raise Http404("المدينة غير موجودة")
    if city_slug != city["slug"]:  # /city/Riyadh/ -> /city/riyadh/
        return redirect("watan:city_detail", city_slug=city["slug"], permanent=True)

    all_cities = dl.get_cities()
    prev_city, next_city = dl.neighbours(all_cities, city)
    context = {
        "city": city,
        "prev_city": prev_city,
        "next_city": next_city,
        "other_cities": [c for c in all_cities if c["slug"] != city["slug"]],
    }
    return render(request, "watan/city_detail.html", context)


def about(request):
    return render(request, "watan/about.html", {"about": dl.load_content()["about"]})


# تفضيلات المستخدم: تُحفظ في Cookies فقط، دون قاعدة بيانات.
PREFERENCE_COOKIE_MAX_AGE = 60 * 60 * 24 * 365


@require_POST
def set_theme(request):
    """حفظ الوضع الداكن/الفاتح في Cookie يقرأها Django عند بناء الصفحة."""
    theme = request.POST.get("theme", "")
    if theme not in ("dark", "light"):
        return JsonResponse({"ok": False, "error": "invalid_theme"}, status=400)

    response = JsonResponse({"ok": True, "theme": theme})
    response.set_cookie(
        "watan-theme",
        theme,
        max_age=PREFERENCE_COOKIE_MAX_AGE,
        path="/",
        samesite="Lax",
        secure=request.is_secure(),
        httponly=True,
    )
    return response


@require_POST
def set_language(request):
    """حفظ اللغة في Cookie، مع ضبط Cookie الخاصة بـ Google Translate."""
    language = request.POST.get("language", "")
    if language not in ("ar", "en"):
        return JsonResponse({"ok": False, "error": "invalid_language"}, status=400)

    response = JsonResponse({"ok": True, "language": language})
    response.set_cookie(
        "watan-language",
        language,
        max_age=PREFERENCE_COOKIE_MAX_AGE,
        path="/",
        samesite="Lax",
        secure=request.is_secure(),
        httponly=True,
    )

    if language == "en":
        # Google Translate يقرأ هذه الكوكي لتطبيق الترجمة بعد إعادة تحميل الصفحة.
        response.set_cookie(
            "googtrans",
            "/ar/en",
            max_age=PREFERENCE_COOKIE_MAX_AGE,
            path="/",
            samesite="Lax",
            secure=request.is_secure(),
            httponly=False,
        )
    else:
        # حذف نسخة الكوكي الأساسية وأي نسخة مرتبطة بنطاق الموقع.
        response.delete_cookie("googtrans", path="/", samesite="Lax")
        host = request.get_host().split(":", 1)[0].lower()
        if host not in ("localhost", "127.0.0.1"):
            labels = host.split(".")
            for index in range(len(labels) - 1):
                domain = ".".join(labels[index:])
                response.delete_cookie("googtrans", path="/", domain=domain, samesite="Lax")
                response.delete_cookie("googtrans", path="/", domain="." + domain, samesite="Lax")

    return response


def page_not_found(request, exception=None):
    return render(request, "watan/404.html", status=404)
