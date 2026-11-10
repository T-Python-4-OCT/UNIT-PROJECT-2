import json
from pathlib import Path

from django.test import SimpleTestCase
from django.urls import reverse

from .data_loader import (
    DATA_DIR,
    IMAGE_DIR,
    add_images,
    get_all_ministries,
    get_ministries,
    get_quiz_questions,
    get_random_facts,
)


class MinistryPagesTests(SimpleTestCase):
    def test_ministry_data_is_valid_and_has_matching_details(self):
        ministries = json.loads((DATA_DIR / "ministries.json").read_text(encoding="utf-8"))
        details = json.loads((DATA_DIR / "details.json").read_text(encoding="utf-8"))
        slugs = {ministry["slug"] for ministry in ministries}

        self.assertEqual(len(slugs), len(ministries))
        self.assertEqual(slugs, set(details))

    def test_homepage_and_ministry_pages_load(self):
        ministries = get_ministries()

        self.assertEqual(self.client.get(reverse("ministries:home")).status_code, 200)
        for ministry in ministries:
            with self.subTest(slug=ministry["slug"]):
                response = self.client.get(
                    reverse("ministries:detail", args=[ministry["slug"]])
                )
                self.assertEqual(response.status_code, 200)

    def test_all_additional_pages_load(self):
        routes = (
            "ministries:about",
            "ministries:timeline",
            "ministries:compare",
            "ministries:quiz",
        )
        for route in routes:
            with self.subTest(route=route):
                self.assertEqual(self.client.get(reverse(route)).status_code, 200)

    def test_ministry_directory_lists_all_twenty_four_ministries(self):
        response = self.client.get(reverse("ministries:directory"))
        directory = get_all_ministries()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(directory), 24)
        self.assertEqual(len({item["slug"] for item in directory}), 24)
        self.assertContains(response, "وزارة الحرس الوطني")
        self.assertContains(response, "وزارة الثقافة")
        self.assertContains(response, "24")

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
                    self.assertTrue((IMAGE_DIR.parent.parent / image).is_file())

    def test_missing_image_data_has_an_empty_fallback_path(self):
        ministry = add_images({"slug": "ministry-without-an-image"})

        self.assertEqual(ministry["cover"], "")
        self.assertEqual(ministry["gallery"], [])

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

    def test_unknown_ministry_returns_not_found(self):
        response = self.client.get(reverse("ministries:detail", args=["unknown"]))

        self.assertEqual(response.status_code, 404)
