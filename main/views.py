"""Views of the main app: home, guide and FAQ."""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from main.content import CHANNELS, FAQ, SCAM_TYPES, TIPS


def home(request: HttpRequest) -> HttpResponse:
    # The context is a dictionary: every key becomes a variable in the template
    context = {"name": "احذر", "slogan": "قبل ما تضغط… احذر."}
    return render(request, "main/home.html", context)


def guide(request: HttpRequest) -> HttpResponse:
    context = {"tips": TIPS, "scam_types": SCAM_TYPES, "channels": CHANNELS}
    return render(request, "main/guide.html", context)


def faq(request: HttpRequest) -> HttpResponse:
    return render(request, "main/faq.html", {"faq": FAQ})
