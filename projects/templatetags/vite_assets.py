import json
from functools import cache

from django import template
from django.conf import settings
from django.templatetags.static import static
from django.utils.html import format_html, format_html_join
from django.utils.safestring import mark_safe

register = template.Library()
ENTRY = "frontend/main.js"
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
def _read_manifest(path, modified):
    return json.loads(path.read_text(encoding="utf-8"))


@register.simple_tag
def vite_assets():
    if settings.VITE_DEV_ORIGIN:
        return format_html(
            '{}<script type="module" src="{}/static/build/@vite/client"></script>'
            '<script type="module" src="{}/static/build/{}"></script>',
            THEME_BOOT, settings.VITE_DEV_ORIGIN, settings.VITE_DEV_ORIGIN, ENTRY,
        )

    manifest_path = settings.BASE_DIR / "static" / "build" / ".vite" / "manifest.json"
    if not manifest_path.exists():
        return THEME_BOOT
    manifest = _read_manifest(manifest_path, manifest_path.stat().st_mtime_ns)
    entry = manifest[ENTRY]
    styles = format_html_join(
        "", '<link rel="stylesheet" href="{}">',
        ((static(f"build/{file}"),) for file in entry.get("css", [])),
    )
    return format_html(
        '{}{}<script type="module" src="{}"></script>',
        THEME_BOOT, styles, static(f"build/{entry['file']}"),
    )
