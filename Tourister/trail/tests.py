from pathlib import Path
from django.test import SimpleTestCase
from django.urls import reverse
from .data import CITIES


class RoutePageTests(SimpleTestCase):
    def test_route_contains_twelve_ordered_destinations(self):
        ordered = sorted(CITIES, key=lambda city: city["order"])

        self.assertEqual(len(ordered), 12)
        self.assertEqual(
            [city["slug"] for city in ordered],
            [
                "riyadh",
                "thadiq",
                "al-qassab",
                "shaqra",
                "al-majmaah",
                "az-zulfi",
                "buraidah",
                "unaizah",
                "ar-rass",
                "al-bukayriyah",
                "hail",
                "jubbah",
            ],
        )

    def test_new_destination_images_are_present(self):
        image_root = Path(__file__).resolve().parent / "static" / "img" / "cities"

        for slug in ("al-majmaah", "az-zulfi", "unaizah", "al-bukayriyah"):
            with self.subTest(city=slug):
                self.assertTrue((image_root / slug / "hero.jpg").is_file())

    def test_home_and_city_pages_render_route_and_directions(self):
        home_response = self.client.get(reverse("home"))
        home_html = home_response.content.decode()
        self.assertContains(home_response, reverse("terms"))
        self.assertContains(home_response, reverse("privacy"))
        self.assertContains(home_response, "js/page-scrollspy.js")
        self.assertNotContains(home_response, 'class="nt-tabs"')
        nav_order = [
            "الرئيسية",
            "عن المسار",
            "الخريطة والنقل",
            "الوجهات",
            "نصائح للزوار",
            "الأسئلة الشائعة",
            "المحطات",
        ]
        nav_positions = [home_html.index(label) for label in nav_order]
        self.assertEqual(nav_positions, sorted(nav_positions))
        self.assertNotContains(home_response, "خطط رحلتك")
        self.assertContains(home_response, "<strong>12</strong>", html=False)
        self.assertContains(home_response, 'class="nt-route-wrap"')
        self.assertContains(home_response, "nt-route-line")
        self.assertNotContains(home_response, "nt-route-arrow")
        self.assertContains(home_response, "بداية المسار")
        self.assertContains(home_response, "نهاية المسار")
        self.assertNotContains(home_response, "overflow-x: auto")

        for city in CITIES:
            with self.subTest(city=city["slug"]):
                response = self.client.get(
                    reverse("city_detail", args=[city["slug"]])
                )
                self.assertContains(response, city["name"])
                self.assertNotContains(response, 'class="nt-tabs"')
                self.assertContains(response, city["hero_image"])
                self.assertContains(response, "الوصول إلى")
                self.assertGreaterEqual(len(city["timeline"]), 3)
                if city["slug"] == "al-majmaah":
                    self.assertContains(
                        response,
                        "المحطة السابقة: <strong>الرياض</strong>",
                        html=False,
                    )
                    self.assertContains(response, "من الرياض إلى المجمعة")
                if city["slug"] != CITIES[0]["slug"]:
                    self.assertContains(response, "nt-access-link--driving")
                    self.assertContains(response, "nt-access-link--transit")

    def test_legal_pages_render_their_content(self):
        pages = (
            ("terms", "الشروط والأحكام", "سلامة الرحلة"),
            ("privacy", "سياسة الخصوصية", "ملفات تعريف الارتباط"),
        )
        for url_name, title, section in pages:
            with self.subTest(page=url_name):
                response = self.client.get(reverse(url_name))
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, title)
                self.assertContains(response, section)
