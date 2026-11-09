import json
import re
from datetime import date
from urllib.parse import urlsplit

from django.conf import settings
from django.test import SimpleTestCase
from django.urls import resolve, reverse
from django.utils.translation import gettext, override

from .content import ContentError, records, timeline, validate

LANGUAGES = {"en": ("", "ltr"), "ar": ("/ar", "rtl")}
SLUGS = ["neom", "qiddiya", "diriyah", "roshn", "the-red-sea", "amaala"]
ROUTES = ["home", "timeline", "compare"]


class PageTests(SimpleTestCase):
    def test_named_routes_render_in_both_languages(self):
        for language, (prefix, direction) in LANGUAGES.items():
            with self.subTest(language=language), override(language):
                for name in ROUTES:
                    path = reverse(name)
                    self.assertEqual(resolve(path).url_name, name)
                    response = self.client.get(path)
                    self.assertEqual(response.status_code, 200)
                    self.assertTemplateUsed(response, "base.html")
                    self.assertContains(response, f'<html lang="{language}" dir="{direction}">')
                    self.assertContains(response, '<link rel="canonical" href="http://testserver')
                    self.assertContains(response, 'hreflang="ar" href="http://testserver/ar/')
                    self.assertContains(response, 'property="og:image"')
                home = self.client.get(reverse("home"))
                self.assertContains(home, "data-atlas-link data-project=", count=6)
                self.assertContains(home, "data-atlas-toggle")
                self.assertContains(home, "atlas/media/atlas-poster.svg")
                self.assertContains(home, 'fetchpriority="high"', count=1)
                self.assertNotContains(home, "—")

    def test_project_pages(self):
        for language, (prefix, direction) in LANGUAGES.items():
            with self.subTest(language=language), override(language):
                for record in records():
                    slug = record["slug"]
                    path = reverse("project", kwargs={"slug": slug})
                    self.assertEqual(path, f"{prefix}/projects/{slug}/")
                    response = self.client.get(path)
                    self.assertTemplateUsed(response, "project.html")
                    self.assertContains(response, f'<html lang="{language}" dir="{direction}">')
                    for field in ("name", "tagline", "summary"):
                        self.assertContains(response, record[field][language])
                    for fact in record["facts"]:
                        self.assertContains(response, fact["value"][language])
                    self.assertContains(response, record["accent"]["light"])
                    self.assertContains(response, 'rel="prev"')
                    self.assertContains(response, 'rel="next"')
                    self.assertContains(response, 'aria-current="page"')
                    target = f"/projects/{slug}/" if language == "ar" else f"/ar/projects/{slug}/"
                    self.assertContains(response, f'class="language-switch" href="{target}"')
                    self.assertNotContains(response, 'id="sources-title"')
                    self.assertNotContains(response, record["sources"][0]["url"])
                    self.assertContains(response, f'poster="/static/{record["video"]["poster"]}"')
                    self.assertContains(response, '<video controls preload="none"')
                    self.assertNotContains(response, "autoplay")
                    self.assertContains(response, 'fetchpriority="high"', count=1)
                    for track in record["video"]["captions"]:
                        default = " default" if track["lang"] == language else ""
                        self.assertContains(response, f'srclang="{track["lang"]}" label="{track["label"]}"{default}>')

    def test_timeline_filter(self):
        response = self.client.get(reverse("timeline"), {"project": "diriyah"})
        self.assertContains(response, 'aria-current="true"', count=1)
        self.assertContains(response, "2010")
        self.assertNotContains(response, "NEOM Bay Airport began operating.")
        unknown = self.client.get(reverse("timeline"), {"project": "unknown"})
        self.assertContains(unknown, "NEOM Bay Airport began operating.")

    def test_english_is_default_even_with_arabic_browser_preferences(self):
        self.client.cookies[settings.LANGUAGE_COOKIE_NAME] = "ar"
        response = self.client.get("/", headers={"Accept-Language": "ar"})
        self.assertContains(response, '<html lang="en" dir="ltr">')

    def test_missing_pages_have_localized_recovery_links(self):
        for language, (prefix, direction) in LANGUAGES.items():
            with self.subTest(language=language), override(language):
                for suffix in ("/projects/unknown/", "/unmatched/path/", "/404/"):
                    response = self.client.get(prefix + suffix)
                    self.assertTemplateUsed(response, "404.html")
                    self.assertContains(response, f'<html lang="{language}" dir="{direction}">', status_code=404)
                    self.assertContains(response, gettext("Page not found"), status_code=404)
                    self.assertContains(response, f'href="{prefix}/"', status_code=404)
                    self.assertContains(response, f'href="{prefix}/projects/neom/"', status_code=404)

    def test_sitemap_and_robots(self):
        sitemap = self.client.get("/sitemap.xml")
        self.assertEqual(sitemap["Content-Type"], "application/xml")
        self.assertEqual(sitemap.content.decode().count("<url>"), 2 * (len(ROUTES) + len(SLUGS)))
        self.assertContains(sitemap, "http://testserver/ar/projects/amaala/")
        robots = self.client.get("/robots.txt")
        self.assertContains(robots, "Sitemap: http://testserver/sitemap.xml")

    def test_template_messages_are_translated(self):
        pattern = re.compile(r"""{%\s+translate\s+(['"])(.*?)\1\s+%}""")
        with override("ar"):
            for template in (settings.BASE_DIR / "templates").rglob("*.html"):
                for _, message in pattern.findall(template.read_text(encoding="utf-8")):
                    with self.subTest(template=template.name, message=message):
                        translated = gettext(message)
                        self.assertNotEqual(translated, message)
                        self.assertRegex(translated, r"[؀-ۿ]")


class ContentTests(SimpleTestCase):
    def test_dataset_validates(self):
        self.assertTrue(validate())

    def test_project_order_and_shape(self):
        self.assertEqual([record["slug"] for record in records()], SLUGS)
        for record in records():
            with self.subTest(slug=record["slug"]):
                self.assertEqual(len(record["highlights"]), 3)
                self.assertGreaterEqual(len(record["milestones"]), 3)
                self.assertGreaterEqual(len(record["facts"]), 3)
                self.assertTrue(record["gallery"])
                dates = [date.fromisoformat(m["date"] if len(m["date"]) == 10 else f"{m['date']}-01-01") for m in record["milestones"]]
                self.assertEqual(dates, sorted(dates))
                for source in record["sources"]:
                    self.assertEqual(urlsplit(source["url"]).scheme, "https")

    def test_copy_rules_and_digits(self):
        text = json.dumps([record for record in records()], ensure_ascii=False)
        self.assertNotRegex(text, r"—|…|[!?]{2,}")
        self.assertNotRegex(text, r"[٠-٩]")

    def test_validation_reports_missing_arabic(self):
        record = json.loads(json.dumps(records()[0]))
        record["tagline"]["ar"] = ""
        try:
            import projects.content as content

            content.records = lambda: [record]
            with self.assertRaises(ContentError):
                content.validate(check_files=False)
        finally:
            content.records = records
            records.cache_clear()

    def test_timeline_is_chronological(self):
        entries = timeline("en")
        self.assertEqual([entry["iso"] for entry in entries], sorted(entry["iso"] for entry in entries))
        self.assertEqual(len(entries), sum(len(record["milestones"]) for record in records()))
