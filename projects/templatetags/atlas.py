from django import template
from django.templatetags.static import static
from django.utils.html import format_html
from django.utils.safestring import mark_safe

register = template.Library()


def _srcset(image, ext):
    return ", ".join(f"{static(image['src'] + '-' + str(width) + '.' + ext)} {width}w" for width in image["widths"])


@register.simple_tag
def picture(image, sizes="100vw", priority=False, decorative=False, css_class=""):
    if not image:
        return ""
    fallback_width = next((width for width in image["widths"] if width >= 960), image["widths"][-1])
    loading = 'fetchpriority="high"' if priority else 'loading="lazy" decoding="async"'
    return format_html(
        '<picture class="{}"><source type="image/avif" srcset="{}" sizes="{}">'
        '<source type="image/webp" srcset="{}" sizes="{}">'
        '<img src="{}" alt="{}" width="{}" height="{}" style="--focal: {}; background-color: {}" {}></picture>',
        css_class,
        _srcset(image, "avif"), sizes,
        _srcset(image, "webp"), sizes,
        static(f"{image['src']}-{fallback_width}.webp"),
        "" if decorative else image["alt"],
        image["width"], image["height"],
        image.get("focal", "50% 50%"), image["color"],
        mark_safe(loading),
    )


@register.simple_tag
def image_url(image, width=1600):
    if not image:
        return ""
    chosen = max((w for w in image["widths"] if w <= width), default=image["widths"][0])
    return static(f"{image['src']}-{chosen}.webp")


@register.filter
def accent_style(project):
    accent = project["accent"]
    return format_html("--accent-light: {}; --accent-dark: {};", accent["light"], accent["dark"])
