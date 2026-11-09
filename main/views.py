from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'main/home.html')


def about(request):
    return render(request, 'main/about.html')


def places(request):
    return render(request, 'main/places.html')


def place_detail(request, slug):
    return render(request, 'main/place_detail.html')


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