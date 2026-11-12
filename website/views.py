"""Render the static page templates."""
# These views render the website pages.
from django.shortcuts import render


# Show the homepage.
def home(request):
    return render(request, "website/home.html")


# Show heritage and identity.
def identity(request):
    return render(request, "website/identity.html")


# Show digital design topics.
def digital_design(request):
    return render(request, "website/digital_design.html")


# Show architecture topics.
def architecture(request):
    return render(request, "website/architecture.html")


# Show graphic design topics.
def graphic_design(request):
    return render(request, "website/graphic_design.html")


# Show products, fashion, and interiors.
def product_design(request):
    return render(request, "website/product_design.html")


# Show current design events.
def contemporary(request):
    return render(request, "website/contemporary.html")


