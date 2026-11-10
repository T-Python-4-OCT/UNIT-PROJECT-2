import re

from django import template
from django.conf import settings
from django.templatetags.static import static
from django.utils.html import escape, format_html
from django.utils.safestring import SafeData, mark_safe

from saudi_atlas.projects.content import highlight, map_geometry

register = template.Library()


@register.simple_tag
def video_url(slug):
    return f"{settings.ATLAS_VIDEO_BASE_URL}/{slug}.mp4"


def _srcset(image, ext):
    return ", ".join(
        f"{static(image['src'] + '-' + str(width) + '.' + ext)} {width}w" for width in image["widths"]
    )


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
        _srcset(image, "avif"),
        sizes,
        _srcset(image, "webp"),
        sizes,
        static(f"{image['src']}-{fallback_width}.webp"),
        "" if decorative else image["alt"],
        image["width"],
        image["height"],
        image.get("focal", "50% 50%"),
        image["color"],
        mark_safe(loading),
    )


@register.simple_tag
def image_url(image, width=1600):
    if not image:
        return ""
    chosen = max((w for w in image["widths"] if w <= width), default=image["widths"][0])
    return static(f"{image['src']}-{chosen}.webp")


@register.filter
def marked(text, terms):
    return mark_safe(
        "".join(
            format_html("<mark>{}</mark>", segment) if matched else escape(segment)
            for segment, matched in highlight(str(text), terms or [])
        )
    )


@register.filter
def word_reveal(text):
    trusted = isinstance(text, SafeData)
    pieces = []
    index = 0
    for part in re.split(r"( +)", str(text)):
        if not part:
            continue
        if part.strip(" ") == "":
            pieces.append(part)
            continue
        word = mark_safe(part) if trusted else part
        pieces.append(
            format_html(
                '<span class="word" style="--i: {}"><span class="word-inner">{}</span></span>', index, word
            )
        )
        index += 1
    return mark_safe("".join(pieces))


@register.filter
def accent_style(project):
    accent = project["accent"]
    style = format_html("--accent-light: {}; --accent-dark: {};", accent["light"], accent["dark"])
    if project.get("texture"):
        style += format_html(" --texture: url({});", static(project["texture"]))
    return style


@register.simple_tag
def shade_position():
    terrain = map_geometry()["terrain"]
    left = terrain["x"] / 1440 * 100
    top = terrain["y"] / 552 * 100
    width = terrain["columns"] * terrain["cell"] / 1440 * 100
    height = terrain["rows"] * terrain["cell"] / 552 * 100
    return f"left: {left:.4f}%; top: {top:.4f}%; width: {width:.4f}%; height: {height:.4f}%"
