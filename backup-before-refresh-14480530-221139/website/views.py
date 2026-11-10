"""Render the static page templates."""
from django.shortcuts import render


def home(request):
    return render(request, "website/home.html")


def identity(request):
    return render(request, "website/identity.html")


def digital_design(request):
    return render(request, "website/digital_design.html")


def architecture(request):
    return render(request, "website/architecture.html")


def graphic_design(request):
    return render(request, "website/graphic_design.html")


def product_design(request):
    return render(request, "website/product_design.html")


def contemporary(request):
    return render(request, "website/contemporary.html")


