"""Views of the main app."""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def home(request: HttpRequest) -> HttpResponse:
    # The context is a dictionary: every key becomes a variable in the template
    context = {"name": "احذر", "slogan": "قبل ما تضغط… احذر."}
    return render(request, "main/home.html", context)
