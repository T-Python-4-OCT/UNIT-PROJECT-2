from django.http import HttpRequest
from django.shortcuts import redirect, render


def mode_view(request: HttpRequest, mode):
    '''Switch between light and dark modes and save the preference in a cookie.'''

    response = redirect(request.GET.get("next", "/"))

    if mode == "light":
        response.set_cookie("mode", "light")
    elif mode == "dark":
        response.set_cookie("mode", "dark")

    return response


def home(request):
    return render(request, "main/home.html")


def pre_oil(request):
    return render(request, "main/pre_oil.html")


def discovery(request):
    return render(request, "main/discovery.html")


def aramco(request):
    return render(request, "main/aramco.html")


def control(request):
    return render(request, "main/control.html")


def society(request):
    return render(request, "main/society.html")


def vision(request):
    return render(request, "main/vision.html")