import socket

from .translations import UI


def get_lan_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except OSError:
        return ""


def get_lang(request):
    lang = request.COOKIES.get("lang", "ar")
    if lang not in UI:
        lang = "ar"
    return lang


def language(request):
    lang = get_lang(request)

    if lang == "ar":
        direction = "rtl"
        other_lang = "en"
    else:
        direction = "ltr"
        other_lang = "ar"

    return {
        "lang": lang,
        "dir": direction,
        "other_lang": other_lang,
        "t": UI[lang],
        "lan_ip": get_lan_ip(),
    }
