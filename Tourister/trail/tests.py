from django.test import TestCase
from django.urls import reverse

from .data import CITIES


class PublicPageTests(TestCase):
    def test_every_destination_has_labeled_https_sources(self):
        for city in CITIES:
            with self.subTest(city=city["slug"]):
                self.assertTrue(city["historical_sources"])
                for source in city["historical_sources"]:
                    self.assertTrue(source["label"])
                    self.assertTrue(source["scope"])
                    self.assertTrue(source["url"].startswith("https://"))

    def test_homepage_renders_route_destinations(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "trail/home.html")
        for city in CITIES:
            with self.subTest(city=city["slug"]):
                self.assertContains(response, city["name"])

    def test_every_city_page_renders_its_history_sources(self):
        for city in CITIES:
            with self.subTest(city=city["slug"]):
                response = self.client.get(
                    reverse("city_detail", kwargs={"slug": city["slug"]})
                )

                self.assertEqual(response.status_code, 200)
                self.assertTemplateUsed(response, "trail/city_detail.html")
                self.assertContains(response, 'id="sources"')
                for source in city["historical_sources"]:
                    self.assertContains(response, source["label"])

    def test_unknown_city_returns_404(self):
        response = self.client.get(
            reverse("city_detail", kwargs={"slug": "unknown-city"})
        )

        self.assertEqual(response.status_code, 404)

    def test_city_navigation_uses_route_order(self):
        first_city = CITIES[0]
        middle_city = CITIES[5]
        last_city = CITIES[-1]

        first_response = self.client.get(
            reverse("city_detail", kwargs={"slug": first_city["slug"]})
        )
        middle_response = self.client.get(
            reverse("city_detail", kwargs={"slug": middle_city["slug"]})
        )
        last_response = self.client.get(
            reverse("city_detail", kwargs={"slug": last_city["slug"]})
        )

        self.assertIsNone(first_response.context["prev_city"])
        self.assertEqual(
            first_response.context["next_city"]["slug"], CITIES[1]["slug"]
        )
        self.assertEqual(
            middle_response.context["prev_city"]["slug"], CITIES[4]["slug"]
        )
        self.assertEqual(
            middle_response.context["next_city"]["slug"], CITIES[6]["slug"]
        )
        self.assertEqual(
            last_response.context["prev_city"]["slug"], CITIES[-2]["slug"]
        )
        self.assertIsNone(last_response.context["next_city"])

    def test_legal_pages_render(self):
        for page_name in ("terms", "privacy"):
            with self.subTest(page=page_name):
                response = self.client.get(reverse(page_name))
                self.assertEqual(response.status_code, 200)


class ThemeToggleTests(TestCase):
    def test_post_toggles_theme_and_redirects_to_requested_page(self):
        response = self.client.post(
            reverse("toggle_theme"), {"next": reverse("home")}
        )

        self.assertRedirects(response, reverse("home"))
        self.assertEqual(response.cookies["theme"].value, "dark")

    def test_post_toggles_dark_theme_back_to_light(self):
        self.client.cookies["theme"] = "dark"

        response = self.client.post(reverse("toggle_theme"), {"next": "/"})

        self.assertRedirects(response, "/")
        self.assertEqual(response.cookies["theme"].value, "light")

    def test_external_redirect_is_rejected(self):
        response = self.client.post(
            reverse("toggle_theme"), {"next": "https://example.com"}
        )

        self.assertRedirects(response, "/")

    def test_toggle_requires_post(self):
        response = self.client.get(reverse("toggle_theme"))

        self.assertEqual(response.status_code, 405)
