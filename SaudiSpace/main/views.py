from django.shortcuts import render

import json

from pathlib import Path 

from django.shortcuts import redirect

from django.http import Http404

# Create your views here.

def toggle_theme(request):
    if request.method == 'POST':

        theme = request.POST.get('theme')

        if theme in ['dark', 'light']:

            response = redirect(request.META.get('HTTP_REFERER', '/'))

            response.set_cookie(
                'theme',
                theme,
                max_age=60 * 60 * 24 * 365,
                httponly=True,
                samesite='Lax'
            )

            return response

    return redirect('home')

def home(request):
    return render(request, 'main/home.html')


def astronauts(request):
    return render(request, 'main/astronauts.html')


def missions(request):
    return render(request, 'main/missions.html')


def satellites(request):
    data = get_satellites()

    return render(request, 'main/satellites.html', {
        'satellites': data
    })


def research(request):
    return render(request, 'main/research.html')


def future(request):
    return render(request, 'main/future.html')



def rayyanah(request):
    return render(request, 'main/astronauts_data/rayyanah.html')

def ali_alqarni(request):
    return render(request, 'main/astronauts_data/ali_alqarni.html')


def ali_alghamdi(request):
    return render(request, 'main/astronauts_data/ali_alghamdi.html')


def mariam_fardous(request):
    return render(request, 'main/astronauts_data/mariam_fardous.html')

def get_satellites():
    file_path = Path(__file__).resolve().parent / 'data' / 'satellites.json'

    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)
    
def satellite_detail(request, slug):
    data = get_satellites()

    satellite = next(
        (item for item in data if item['id'] == slug),
        None
    )

    if satellite is None:
        raise Http404("Satellite not found")

    return render(request, 'main/satellite_detail.html', {
        'satellite': satellite
    })
    
    import json
from pathlib import Path
from django.http import Http404
from django.shortcuts import render


def get_planets():
    file_path = Path(__file__).resolve().parent / 'data' / 'planets.json'

    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


def astronomy(request):
    planets = get_planets()

    return render(request, 'main/astronomy.html', {
        'planets': planets
    })


def planet_detail(request, slug):
    planets = get_planets()

    planet = next(
        (item for item in planets if item['id'] == slug),
        None
    )

    if planet is None:
        raise Http404("Planet not found")

    return render(request, 'main/planet_detail.html', {
        'planet': planet
    })