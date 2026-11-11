from django import template
from django.templatetags.static import static

register = template.Library()


@register.simple_tag
def asset(path):
    """
    يحوّل مسار ملف ثابت (مثل img/riyadh-day.svg) إلى رابط static،
    أما الروابط الكاملة (https://...) فتُترك كما هي — لتتمكن من استخدام صور
    أو فيديوهات مستضافة على الإنترنت (CDN) من ملف JSON.
    """
    if not path:
        return ""
    path = str(path)
    if path.startswith(("http://", "https://", "//", "data:")):
        return path
    return static(path)


@register.filter
def pad2(value):
    """1 -> 01"""
    try:
        return f"{int(value):02d}"
    except (TypeError, ValueError):
        return value
