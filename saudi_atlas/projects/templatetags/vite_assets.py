import json
from functools import cache
from pathlib import Path

from django import template
from django.conf import settings
from django.templatetags.static import static
from django.utils.html import format_html, format_html_join
from django.utils.safestring import mark_safe
from django.utils.translation import get_language

register = template.Library()
ENTRY = "saudi_atlas/projects/frontend/main.js"
APP_DIR = Path(__file__).resolve().parent.parent
DISPLAY_FONTS = {"en": "instrument-serif-latin-400-normal", "ar": "amiri-arabic-400-normal"}
THEME_BOOT = mark_safe("""<script>(()=>{
  let saved;
  try { saved = localStorage.getItem('atlas-theme'); } catch {}
  if (saved !== 'light' && saved !== 'dark') {
    saved = matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }
  document.documentElement.dataset.theme = saved;
  document.documentElement.classList.add('js');
})();</script>""")


@cache
def _plate_transition():
    source = (APP_DIR / "frontend" / "scripts" / "plate-transition.js").read_text(encoding="utf-8")
    lines = (line.strip() for line in source.splitlines())
    return mark_safe(
        "<script>" + "\n".join(line for line in lines if line and not line.startswith("//")) + "</script>"
    )


@cache
def _read_manifest(path, modified):
    return json.loads(path.read_text(encoding="utf-8"))


@register.simple_tag
def vite_assets():
    if settings.VITE_DEV_ORIGIN:
        return format_html(
            '{}{}<script type="module" src="{}/static/build/@vite/client"></script>'
            '<script type="module" src="{}/static/build/{}"></script>',
            THEME_BOOT,
            _plate_transition(),
            settings.VITE_DEV_ORIGIN,
            settings.VITE_DEV_ORIGIN,
            ENTRY,
        )

    manifest_path = APP_DIR / "static" / "build" / ".vite" / "manifest.json"
    if not manifest_path.exists():
        return THEME_BOOT + _plate_transition()
    manifest = _read_manifest(manifest_path, manifest_path.stat().st_mtime_ns)
    entry = manifest[ENTRY]
    styles = format_html_join(
        "",
        '<link rel="stylesheet" href="{}">',
        ((static(f"build/{file}"),) for file in entry.get("css", [])),
    )

    wanted = DISPLAY_FONTS["ar" if get_language() == "ar" else "en"]
    preloads = format_html_join(
        "",
        '<link rel="preload" href="{}" as="font" type="font/woff2" crossorigin>',
        (
            (static(f"build/{file}"),)
            for file in entry.get("assets", [])
            if file.endswith(".woff2") and wanted in file
        ),
    )
    return format_html(
        '{}{}{}{}<script type="module" src="{}"></script>',
        THEME_BOOT,
        _plate_transition(),
        preloads,
        styles,
        static(f"build/{entry['file']}"),
    )
