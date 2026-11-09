from django.http import Http404
from .data import CITIES, CITIES_BY_SLUG, TIPS, FAQS
from django.shortcuts import render, redirect
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

@require_POST
def toggle_theme(request):
    new = "light" if request.COOKIES.get("theme") == "dark" else "dark"
    next_url = request.POST.get("next", "/")
    if not url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        next_url = "/"
    response = redirect(next_url)
    response.set_cookie("theme", new, max_age=60 * 60 * 24 * 365, samesite="Lax")
    return response

def get_ordered_cities():
    return sorted(CITIES, key=lambda c: c["order"])


def home(request):
    return render(request, "trail/home.html", {
        "cities": get_ordered_cities(),
        "tips": TIPS,
        "faqs": FAQS,
    })


def city_detail(request, slug):
    city = CITIES_BY_SLUG.get(slug)
    if city is None:
        raise Http404("المدينة غير موجودة")

    ordered = get_ordered_cities()
    i = ordered.index(city)

    return render(request, "trail/city_detail.html", {
        "city": city,
        "cities": ordered,    
        "prev_city": ordered[i - 1] if i > 0 else None,
        "next_city": ordered[i + 1] if i < len(ordered) - 1 else None,
    })