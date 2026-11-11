from .data import ordered_cities

SOCIAL_LINKS = [
    {"name": "Instagram", "icon": "bi-instagram", "css_class": "instagram", "url": "https://www.instagram.com/visitsaudi/"},
    {"name": "YouTube", "icon": "bi-youtube", "css_class": "youtube", "url": "https://www.youtube.com/channel/UCmFRhhc6Gt8b4bSUmTzNIoA"},
    {"name": "Whatsapp", "icon": "bi-whatsapp", "css_class": "whatsapp", "url": "https://api.whatsapp.com/send?phone=966114907617"},
    {"name": "X", "icon": "bi-twitter-x", "css_class": "x", "url": "https://x.com/VisitSaudi"},
]


def theme(request):
    return {"theme": "dark" if request.COOKIES.get("theme") == "dark" else "light"}


def nav_cities(request):
    return {"cities": ordered_cities()}


def site_info(request):
    return {"social_links": SOCIAL_LINKS}