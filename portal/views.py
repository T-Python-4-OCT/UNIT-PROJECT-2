from django.shortcuts import render, redirect


def home(request):
    return render(request, 'portal/home.html')


def toggle_theme(request):
    if request.method == 'POST':
        current_theme = request.COOKIES.get('theme', 'dark')

        new_theme = 'light' if current_theme == 'dark' else 'dark'

        response = redirect(request.META.get('HTTP_REFERER', 'home'))
        response.set_cookie('theme', new_theme, max_age=31536000)

        return response

    return redirect('home')
def digital_transformation(request):
    return render(request, 'portal/digital_transformation.html')

def smart_technologies(request):
    return render(request, 'portal/smart_technologies.html')

def digital_government(request):
    return render(request, 'portal/digital_government.html')

def cybersecurity_development(request):
    return render(request, 'portal/cybersecurity_development.html')

def national_cybersecurity(request):
    return render(request, 'portal/national_cybersecurity.html')

def cyber_threats(request):
    return render(request, 'portal/cyber_threats.html')

def future_innovation(request):
    return render(request, 'portal/future_innovation.html')

def digital_identity(request):
    return render(request, 'portal/digital_identity.html')