
import json
from pathlib import Path

from django.http import Http404, JsonResponse
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST


DATA_FILE = Path(__file__).resolve().parent / "data" / "regions.json"


def load_regions():
    with DATA_FILE.open(encoding="utf-8") as file:
        return json.load(file)


def home(request):
    regions = load_regions()

    return render(
        request,
        "regions/home.html",
        {"regions": regions.items()},
    )


def region_detail(request, slug):
    regions = load_regions()
    region = regions.get(slug)

    if region is None:
        raise Http404("المنطقة غير موجودة")

    region["slug"] = slug

    return render(
        request,
        "regions/region_detail.html",
        {"region": region},
    )


def our_roots(request):
    return render(request, "regions/our_roots.html")


@require_POST
def toggle_theme(request):
    current_theme = request.COOKIES.get("theme", "light")
    new_theme = "light" if current_theme == "dark" else "dark"

    is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"

    if is_ajax:
        response = JsonResponse({"theme": new_theme})
    else:
        next_url = request.POST.get("next", "/")

        if not url_has_allowed_host_and_scheme(
            next_url,
            allowed_hosts={request.get_host()},
            require_https=request.is_secure(),
        ):
            next_url = "/"

        response = redirect(next_url)

    response.set_cookie(
        "theme",
        new_theme,
        max_age=60 * 60 * 24 * 30,
        httponly=True,
        samesite="Lax",
        secure=request.is_secure(),
    )

    return response
