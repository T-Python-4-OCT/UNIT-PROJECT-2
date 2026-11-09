
from django.shortcuts import render
from django.http import Http404
from .data import PLACES


def home(request):
    return render(request, 'main/home.html', {
        'places': PLACES,
    })


def about(request):
    return render(request, 'main/about.html')


def places(request):
    return render(request, 'main/places.html', {
        'places': PLACES,
    })


def place_detail(request, slug):
    place = next(
        (item for item in PLACES if item['slug'] == slug),
        None
    )

    if place is None:
        raise Http404("المكان غير موجود")

    return render(request, 'main/place_detail.html', {
        'place': place,
    })


def events(request):
    return render(request, 'main/events.html')


def history(request):
    return render(request, 'main/history.html')


def projects(request):
    return render(request, 'main/projects.html')


def project_detail(request, slug):
    return render(request, 'main/project_detail.html')


def gallery(request):
    return render(request, 'main/gallery.html')


def search(request):
    return render(request, 'main/search.html')


def toggle_theme(request):
    return render(request, 'main/home.html')
