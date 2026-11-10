import socket

from .translations import UI


def get_lan_ip():
    # نعرف عنوان الجهاز في الشبكة المحلية (مثل 192.168.x.x)
    # عشان رمز QR يفتح الموقع من الجوال بدل localhost
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))   # ما يرسل شي فعلياً، بس يعرف أي شبكة نستخدم
        ip = s.getsockname()[0]
        s.close()
        return ip
    except OSError:
        return ""


def get_lang(request):
    # نقرأ اللغة من الكوكي، والافتراضي عربي
    lang = request.COOKIES.get("lang", "ar")
    if lang not in UI:
        lang = "ar"
    return lang


def language(request):
    # هذي الدالة تشتغل مع كل صفحة، وترسل للقالب:
    # lang = "ar" أو "en"
    # dir  = اتجاه الصفحة
    # t    = قاموس النصوص باللغة الحالية
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
