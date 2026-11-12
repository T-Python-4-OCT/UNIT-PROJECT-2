import json
import os
import shutil
import sys
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "saudi_atlas.settings")

import django
from django.conf import settings
from django.template.loader import render_to_string
from django.test import Client
from django.urls import reverse, set_script_prefix
from django.utils.html import json_script
from django.utils.translation import gettext, ngettext, override

from saudi_atlas.projects.content import LOCALIZED, localized_projects


def search_index(projects):
    def snippet(results=(), query=""):
        return render_to_string("includes/search_results.html", {
            "nav_projects": projects, "results": results, "query": query, "terms": [],
        })

    cards = []
    for project in projects:
        passages = (
            [("glance", f"{fact['label']}: {fact['value']}", None) for fact in project["facts"]]
            + [("story", detail["body"], detail["title"]) for detail in project["details"]]
            + [("highlights", text, None) for text in project["highlights"]]
            + [("gallery", photo["caption"], None) for photo in [project["image"], *project["gallery"]] if photo]
            + [("milestones", item["text"], item["year"]) for item in project["milestones"]]
        )
        matches = [{"kind": kind, "text": text, "title": title} for kind, text, title in passages]
        cards.append({
            "name": project["name"],
            "headline": " ".join(project[field] for field in LOCALIZED),
            "summary": project["summary"],
            "passages": [f"{title or ''} {text}" for _, text, title in passages],
            "html": snippet([{"project": project, "matches": matches}]),
        })

    return json_script({
        "cards": cards,
        "empty": snippet(),
        "missing": snippet(query="…"),
        "heading": gettext("Results for"),
        "counts": {
            count: ngettext("%(counter)s project matches", "%(counter)s projects match", count)
            % {"counter": count}
            for count in range(1, len(projects) + 1)
        },
    }, "pages-search-index")


def export(destination, base_url):
    url = urlsplit(base_url.rstrip("/"))
    prefix = url.path
    settings.ALLOWED_HOSTS = [url.hostname]
    settings.STATIC_URL = f"{prefix}/static/"
    django.setup()
    set_script_prefix(f"{prefix}/")
    client = Client(SERVER_NAME=url.hostname, SERVER_PORT=443, SCRIPT_NAME=prefix)
    app = ROOT / "saudi_atlas/projects"

    def fetch(path, status=200, **params):
        response = client.get(path.removeprefix(prefix), params, secure=True)
        if response.status_code != status:
            raise RuntimeError(f"{path} returned {response.status_code}, expected {status}")
        return response.content.decode("utf-8")

    def write(path, html):
        file = destination / path.removeprefix(prefix).lstrip("/")
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(html, encoding="utf-8")

    def write_page(path, html):
        write(f"{path}index.html", html)

    slugs = [project["slug"] for project in localized_projects("en")]
    timeline_links = {}
    for language in ("en", "ar"):
        with override(language):
            path = reverse("timeline")
            timeline_links.update({f"{path}?project={slug}": f"{path}{slug}/" for slug in slugs})

    def rewrite_timelines(html):
        for old, new in timeline_links.items():
            html = html.replace(old, new)
        return html

    for language in ("en", "ar"):
        with override(language):
            projects = localized_projects(language)
            for route in ("home", "compare", "credits"):
                path = reverse(route)
                write_page(path, rewrite_timelines(fetch(path)))
            for slug in slugs:
                path = reverse("project", kwargs={"slug": slug})
                write_page(path, rewrite_timelines(fetch(path)))
            path = reverse("timeline")
            write_page(path, rewrite_timelines(fetch(path)))
            for slug in slugs:
                write_page(f"{path}{slug}/", rewrite_timelines(fetch(path, project=slug)))
            path = reverse("search")
            script = f'<script type="module" src="{prefix}/static/pages-search.js"></script>'
            html = fetch(path).replace("data-live-search", "data-pages-search")
            write_page(path, html.replace("</body>", f"{search_index(projects)}{script}</body>"))
            path = reverse("not_found")
            html = fetch(path, status=404)
            write_page(path, html)
            if language == "en":
                write("/404.html", html)

    write("/sitemap.xml", fetch("/sitemap.xml"))
    write("/robots.txt", f"User-agent: *\nAllow: /\nSitemap: {base_url.rstrip('/')}/sitemap.xml\n")
    write("/.nojekyll", "")
    shutil.copytree(app / "static/atlas", destination / "static/atlas", dirs_exist_ok=True)
    shutil.copytree(app / "static/build/assets", destination / "static/build/assets", dirs_exist_ok=True)
    shutil.copyfile(ROOT / ".github/pages-search.js", destination / "static/pages-search.js")

    licenses = destination / "static/licenses"
    licenses.mkdir(exist_ok=True)
    for name in ("amiri", "ibm-plex-sans", "ibm-plex-sans-arabic", "instrument-serif"):
        shutil.copyfile(ROOT / "node_modules/@fontsource" / name / "LICENSE", licenses / f"{name}-OFL.txt")
    shutil.copyfile(ROOT / "node_modules/three/LICENSE", licenses / "three-MIT.txt")


if __name__ == "__main__":
    export(Path(sys.argv[1]), sys.argv[2])
