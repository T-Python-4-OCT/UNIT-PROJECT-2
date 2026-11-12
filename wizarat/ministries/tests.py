import json

from django.test import SimpleTestCase
from django.urls import reverse

from .data_loader import (
    DATA_DIR,
    IMAGE_DIR,
    add_images,
    get_ministries,
    get_quiz_questions,
    get_random_facts,
)
from .views import youtube_embed_url


class MinistryPagesTests(SimpleTestCase):
    def test_youtube_urls_are_safely_converted_to_privacy_friendly_embeds(self):
        video_id = "XdtPmrf3sxI"

        self.assertEqual(
            youtube_embed_url(f"https://youtu.be/{video_id}"),
            f"https://www.youtube-nocookie.com/embed/{video_id}",
        )
        self.assertEqual(
            youtube_embed_url(f"https://www.youtube.com/watch?v={video_id}"),
            f"https://www.youtube-nocookie.com/embed/{video_id}",
        )
        self.assertEqual(
            youtube_embed_url("https://example.com/watch?v=XdtPmrf3sxI"),
            "",
        )

    def test_ministry_data_is_valid_and_has_matching_details(self):
        ministries = json.loads((DATA_DIR / "ministries.json").read_text(encoding="utf-8"))
        details = json.loads((DATA_DIR / "details.json").read_text(encoding="utf-8"))
        slugs = {ministry["slug"] for ministry in ministries}

        self.assertEqual(len(slugs), len(ministries))
        self.assertEqual(slugs, set(details))

    def test_homepage_and_ministry_pages_load(self):
        ministries = get_ministries()

        home_response = self.client.get(reverse("ministries:home"))
        self.assertEqual(home_response.status_code, 200)
        self.assertContains(home_response, "data-walk-hero")
        for layer in ("wl-sky", "wl-far", "wl-mid", "wl-ground", "wl-front"):
            self.assertContains(home_response, f"wl {layer}")
        self.assertNotContains(home_response, "youtube-nocookie.com")
        self.assertContains(home_response, 'data-assistant')
        self.assertEqual(len(home_response.context["chatbot_ministries"]), 13)
        for ministry in ministries:
            with self.subTest(slug=ministry["slug"]):
                response = self.client.get(
                    reverse("ministries:detail", args=[ministry["slug"]])
                )
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, 'data-assistant')
                self.assertNotContains(response, "class=\"detail-hero-video\"")
                self.assertContains(response, "detail-hero-picture")

    def test_all_additional_pages_load(self):
        routes = (
            "ministries:timeline",
            "ministries:compare",
            "ministries:quiz",
        )
        for route in routes:
            with self.subTest(route=route):
                self.assertEqual(self.client.get(reverse(route)).status_code, 200)

    def test_ministry_directory_lists_every_ministry_with_a_detail_link(self):
        response = self.client.get(reverse("ministries:directory"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["directory_ministries"]), 13)
        for ministry in get_ministries():
            with self.subTest(slug=ministry["slug"]):
                self.assertContains(response, reverse("ministries:detail", args=[ministry["slug"]]))

    def test_compare_and_custom_not_found_pages_load(self):
        response = self.client.get(
            reverse("ministries:compare"), {"first": "foreign", "second": "health"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "وزارة الخارجية")
        self.assertContains(response, "وزارة الصحة")

        missing = self.client.get("/not-found/")
        self.assertEqual(missing.status_code, 404)
        self.assertContains(missing, "لم نعثر على هذه الصفحة", status_code=404)

    def test_existing_ministry_images_are_resolved(self):
        for ministry in get_ministries():
            with self.subTest(slug=ministry["slug"]):
                self.assertTrue(ministry["cover"])
                self.assertTrue((IMAGE_DIR.parent.parent / ministry["cover"]).is_file())
                self.assertTrue(ministry["gallery"])
                for image in ministry["gallery"]:
                    self.assertTrue((IMAGE_DIR.parent.parent / image["url"]).is_file())
                    for variant in image["webp"]:
                        self.assertTrue((IMAGE_DIR.parent.parent / variant["url"]).is_file())
                for variant in ministry["cover_webp"]:
                    self.assertTrue((IMAGE_DIR.parent.parent / variant["url"]).is_file())

    def test_missing_image_data_has_an_empty_fallback_path(self):
        ministry = add_images({"slug": "ministry-without-an-image"})

        self.assertEqual(ministry["cover"], "")
        self.assertEqual(ministry["gallery"], [])
        self.assertEqual(ministry["cover_webp"], [])

    def test_every_ministry_has_expected_json_fields(self):
        expected_fields = {
            "timeline",
            "services",
            "achievements",
            "facts",
            "video_url",
            "vision_goals",
        }
        ministries = get_ministries()
        self.assertEqual(len(ministries), 13)
        for ministry in ministries:
            with self.subTest(slug=ministry["slug"]):
                self.assertTrue(expected_fields.issubset(ministry))
                self.assertTrue(ministry["timeline"])
                self.assertTrue(ministry["vision_goals"])

    def test_fact_and_quiz_json_references_are_valid(self):
        ministry_slugs = {item["slug"] for item in get_ministries()}
        for fact in get_random_facts():
            self.assertIn(fact["ministry"]["slug"], ministry_slugs)
            self.assertTrue(fact["text"])
        for question in get_quiz_questions():
            self.assertIn(question["answer"], ministry_slugs)
            self.assertEqual(len(question["choices"]), 3)
            self.assertIn(question["answer"], {choice["slug"] for choice in question["choices"]})

    def test_search_finds_ministries_by_name_task_and_spelling_variants(self):
        response = self.client.get(reverse("ministries:search"), {"q": "الصحة"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["results"][0]["slug"], "health")

        by_task = self.client.get(reverse("ministries:search"), {"q": "الميزانية"})
        self.assertIn("finance", [item["slug"] for item in by_task.context["results"]])

        variant = self.client.get(reverse("ministries:search"), {"q": "الحج والعمره"})
        self.assertIn("hajj", [item["slug"] for item in variant.context["results"]])

        empty = self.client.get(reverse("ministries:search"), {"q": "كلمةغيرموجودة"})
        self.assertEqual(empty.context["results"], [])
        self.assertContains(self.client.get(reverse("ministries:search")), "data-site-search")

    def test_navbar_has_search_and_theme_toggle(self):
        response = self.client.get(reverse("ministries:home"))
        self.assertContains(response, 'data-bs-target="#searchModal"')
        self.assertContains(response, 'id="themeToggle" class="btn theme-btn"')
        self.assertNotContains(response, "footer-theme")
        self.assertNotContains(response, "data-a11y")
        self.assertNotContains(response, "عن المشروع")

    def test_unknown_ministry_returns_not_found(self):
        response = self.client.get(reverse("ministries:detail", args=["unknown"]))

        self.assertEqual(response.status_code, 404)
