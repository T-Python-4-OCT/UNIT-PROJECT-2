"""
اختبارات بلا قاعدة بيانات (SimpleTestCase): تتحقق من أن كل الصفحات تعمل،
وأن الروابط الديناميكية تعيد 404 للمعرّفات غير الموجودة، وأن بيانات JSON سليمة.
التشغيل: python manage.py test
"""
from django.test import SimpleTestCase
from django.urls import reverse

from . import content

STATIC_PAGES = ["home", "old_riyadh", "king", "participants", "story", "tour", "timeline", "museum", "quiz"]


class PagesTests(SimpleTestCase):
    def test_static_pages_render(self):
        for name in STATIC_PAGES:
            with self.subTest(page=name):
                res = self.client.get(reverse("main:" + name))
                self.assertEqual(res.status_code, 200)
                self.assertContains(res, 'dir="rtl"')

    def test_every_person_page_renders(self):
        for p in content.load("people")["featured"]:
            with self.subTest(slug=p["slug"]):
                res = self.client.get(reverse("main:person", args=[p["slug"]]))
                self.assertContains(res, p["name"])

    def test_every_chapter_page_renders(self):
        for c in content.load("story")["chapters"]:
            with self.subTest(slug=c["slug"]):
                res = self.client.get(reverse("main:chapter", args=[c["slug"]]))
                self.assertContains(res, c["title"])

    def test_unknown_slugs_return_404(self):
        self.assertEqual(self.client.get(reverse("main:person", args=["unknown"])).status_code, 404)
        self.assertEqual(self.client.get(reverse("main:chapter", args=["unknown"])).status_code, 404)


class DataTests(SimpleTestCase):
    def test_roster_has_63_names(self):
        self.assertEqual(len(content.load("people")["roster"]), 63)

    def test_quiz_answers_are_valid(self):
        for q in content.load("quiz")["questions"]:
            self.assertTrue(0 <= q["answer"] < len(q["options"]))

    def test_sources_referenced_exist(self):
        known = set(content.load("sources")["items"])
        for name in ["people", "story", "tour", "timeline", "old_riyadh", "king"]:
            data = content.load(name)
            ids = list(data.get("sources", []))
            for item in data.get("featured", []) + data.get("chapters", []):
                ids += item.get("sources", [])
            for sid in ids:
                self.assertIn(sid, known, msg=f"{name}: {sid}")

    def test_media_ids_exist(self):
        items = content.load("media")["items"]
        for c in content.load("story")["chapters"]:
            if c.get("media"):
                self.assertIn(c["media"], items)
        for s in content.load("tour")["stops"]:
            if s.get("media"):
                self.assertIn(s["media"], items)
