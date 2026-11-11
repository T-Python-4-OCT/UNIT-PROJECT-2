from django.shortcuts import render
from django.http import Http404

from main.services import place_context, project_context
from .data import PLACES, PROJECTS
from .search_service import get_search_context
from django.views.decorators.http import require_POST
from .theme_service import change_theme


def home(request):
    return render(request, 'main/home.html', {
        'places': PLACES,
        'featured_projects': PROJECTS[:3],
    })


def about(request):
    return render(request, 'main/about.html')


def places(request):
    return render(request, 'main/places.html', {
        'places': PLACES,
    })


def place_detail(request, slug):
    return render(request, 'main/place_detail.html', place_context(slug))
    


def events(request):
    return render(request, 'main/events.html')


def history(request):
    return render(request, 'main/history.html')


def projects(request):
    return render(request, 'main/projects.html', {
        'projects': PROJECTS,
    })


def project_detail(request, slug):
    return render(request, 'main/project_detail.html', project_context(slug))



def gallery(request):
    return render(request, 'main/gallery.html')


def search(request):
    return render(
        request,
        'main/search.html',
        get_search_context(request.GET)
    )

@require_POST
def toggle_theme(request):
    return change_theme(request)