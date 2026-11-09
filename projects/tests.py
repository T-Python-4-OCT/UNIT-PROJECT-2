import re
from datetime import date
from urllib.parse import urlsplit

from django.conf import settings
from django.contrib.staticfiles import finders
from django.test import SimpleTestCase
from django.urls import resolve, reverse
from django.utils.translation import gettext, override

from .content import feature_records, records


LANGUAGES = {"en": ("", "ltr"), "ar": ("/ar", "rtl")}
SLUGS = ["neom", "qiddiya", "diriyah", "roshn", "the-red-sea", "amaala"]


class ProjectPagesTests(SimpleTestCase):
    def test_named_routes_and_localized_pages(self):
        for language, (prefix, direction) in LANGUAGES.items():
            with self.subTest(language=language), override(language):
                path = reverse("home")
                self.assertEqual(path, f"{prefix}/")
                self.assertEqual(resolve(path).url_name, "home")
                response = self.client.get(path)
                self.assertTemplateUsed(response, "home.html")
                self.assertTemplateUsed(response, "base.html")
                self.assertContains(response, f'<html lang="{language}" dir="{direction}">')
                self.assertContains(response, 'data-atlas-link data-project=', count=6)
                self.assertContains(response, 'data-atlas-toggle')
                self.assertContains(response, 'data-atlas-status')
                self.assertContains(response, 'atlas/media/atlas-poster.svg')
                self.assertContains(response, gettext("Saudi Arabia’s giga-projects"))
                self.assertLessEqual(len(gettext(
                    "An illustrated guide to six Saudi developments, from Najdi heritage and new communities to mountain landscapes and the Red Sea coast."
                ).split()), 30)

                for record in records():
                    slug = record["slug"]
                    with self.subTest(slug=slug):
                        path = reverse("project", kwargs={"slug": slug})
                        self.assertEqual(path, f"{prefix}/projects/{slug}/")
                        self.assertEqual(resolve(path).url_name, "project")
                        self.assertContains(response, f'href="{path}"')
                        self.assertContains(response, record["category"][language])
                        self.assertContains(response, record["highlights"][0][language])
                        detail = self.client.get(path)
                        self.assertTemplateUsed(detail, "project.html")
                        self.assertTemplateUsed(detail, "base.html")
                        self.assertContains(detail, f'<html lang="{language}" dir="{direction}">')
                        self.assertContains(detail, record["name"][language])
                        self.assertContains(detail, record["summary"][language])
                        target = f"/projects/{slug}/" if language == "ar" else f"/ar/projects/{slug}/"
                        self.assertContains(detail, f'class="language-switch" href="{target}"')
                        self.assertNotContains(detail, 'id="sources-title"')
                        self.assertNotContains(detail, record["sources"][0]["url"])
                        video = feature_records()[slug]["video"]
                        self.assertContains(detail, video["path"])
                        self.assertContains(detail, '<video controls preload="none"')
                        self.assertNotContains(detail, "autoplay")
                        self.assertNotContains(detail, "data-project-viewer")

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

    def test_template_messages_are_translated(self):
        pattern = re.compile(r"""{%\s+translate\s+(['"])(.*?)\1\s+%}""")
        with override("ar"):
            for template in (settings.BASE_DIR / "templates").rglob("*.html"):
                for _, message in pattern.findall(template.read_text(encoding="utf-8")):
                    with self.subTest(template=template.name, message=message):
                        translated = gettext(message)
                        self.assertNotEqual(translated, message)
                        self.assertRegex(translated, r"[\u0600-\u06ff]")


class ProjectContentTests(SimpleTestCase):
    def assert_localized(self, value, word_limit=None):
        self.assertEqual(set(value), set(LANGUAGES))
        for text in value.values():
            self.assertTrue(text.strip())
            self.assertNotRegex(text, r"—|…|[!?]{2,}")
            if word_limit:
                self.assertLessEqual(len(text.split()), word_limit)
        self.assertRegex(value["ar"], r"[\u0600-\u06ff]")

    def assert_https_url(self, value):
        parts = urlsplit(value)
        self.assertEqual(parts.scheme, "https")
        self.assertTrue(parts.netloc)

    def test_dataset_contains_all_six_valid_projects(self):
        self.assertEqual([record["slug"] for record in records()], SLUGS)
        for record in records():
            with self.subTest(slug=record["slug"]):
                for field in ("name", "category", "region"):
                    self.assert_localized(record[field])
                self.assert_localized(record["summary"], word_limit=45)

                self.assertLessEqual(len(record["highlights"]), 3)
                for highlight in record["highlights"]:
                    self.assert_localized(highlight)

                self.assertLessEqual(len(record["milestones"]), 3)
                dates = []
                for milestone in record["milestones"]:
                    self.assertRegex(milestone["date"], r"^\d{4}(-\d{2}-\d{2})?$")
                    value = milestone["date"]
                    dates.append(date.fromisoformat(f"{value}-01-01" if len(value) == 4 else value))
                    self.assert_localized(milestone["text"])
                self.assertEqual(dates, sorted(dates))

                self.assertTrue(record["sources"])
                for source in record["sources"]:
                    self.assert_https_url(source["url"])
                    self.assertRegex(source["verified"], r"^\d{4}-\d{2}-\d{2}$")
                    date.fromisoformat(source["verified"])
                    self.assert_localized(source["label"])

                image = record.get("image")
                if image:
                    self.assertTrue(finders.find(image["path"]))
                    self.assert_localized(image["alt"])
                    if "caption" in image:
                        self.assert_localized(image["caption"])

    def test_project_gallery_and_film_assets(self):
        for slug in SLUGS:
            with self.subTest(slug=slug):
                features = feature_records()[slug]
                self.assertTrue(features["gallery"])
                for photo in features["gallery"]:
                    self.assertTrue(finders.find(photo["path"]))
                    self.assert_localized(photo["caption"])
                    self.assert_localized(photo["alt"])
                video = features["video"]
                self.assertTrue(finders.find(video["path"]))
                if video.get("captions"):
                    self.assertTrue(finders.find(video["captions"]))
                self.assertIn(video["duration"], range(20, 61))
                self.assertRegex(video["youtube_id"], r"^[A-Za-z0-9_-]{11}$")
                self.assertGreaterEqual(video["start"], 0)
                self.assertEqual(video["end"] - video["start"], video["duration"])
                self.assert_https_url(video["source_url"])
                self.assert_localized(video["title"])
                self.assert_localized(video["description"])
