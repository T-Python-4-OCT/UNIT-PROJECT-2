from django.shortcuts import redirect
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme


def change_theme(request):
    current_theme = request.COOKIES.get('diriyah_theme', 'dark')

    if current_theme == 'dark':
        new_theme = 'light'
    else:
        new_theme = 'dark'

    destination = request.POST.get('next', '')

    if not url_has_allowed_host_and_scheme(
        url=destination,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure()
    ):
        destination = reverse('main:home')

    response = redirect(destination)

    response.set_cookie(
        'diriyah_theme',
        new_theme,
        max_age=365 * 24 * 60 * 60,
        samesite='Lax',
        httponly=True,
        secure=request.is_secure()
    )

    return response
