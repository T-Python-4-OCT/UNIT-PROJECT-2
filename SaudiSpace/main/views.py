from django.shortcuts import render
 
# Create your views here.
from django.shortcuts import redirect


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
    return render(request, 'main/satellites.html')


def astronomy(request):
    return render(request, 'main/astronomy.html')


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