import os

from django.conf import settings

from .data import CITIES

STATIC_DIR = os.path.join(settings.BASE_DIR, "main", "static", "main")


def _version(path):
    """File's last-modified time; it changes on every edit, so the browser reloads the file."""
    try:
        return int(os.path.getmtime(os.path.join(STATIC_DIR, path)))
    except OSError:
        return 0


def site_data(request):
    """Data available in every template."""
    return {
        "nav_cities": CITIES,                       # navbar dropdown + footer links
        "css_version": _version("css/style.css"),   # cache-busting for style.css
        "js_version": _version("js/main.js"),       # cache-busting for main.js
    }
