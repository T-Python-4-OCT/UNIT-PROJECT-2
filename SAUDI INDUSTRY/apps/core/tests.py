
from pathlib import PurePosixPath
from unittest.mock import patch

from django.conf import settings
from django.test import SimpleTestCase
from django.urls import reverse

from apps.catalog.content_loader import load_json


class TechnologyTests(SimpleTestCase):

    def test_technology_page(self):
        response = self.client.get(
            reverse("core:technology")
        )

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(
            response,
            "core/technology.html"
        )

        self.assertEqual(
            len(response.context["technologies"]),
            6
        )

    def test_external_technology_image_url(self):
        image_url = (
            "https://res.cloudinary.com/ew4jvlxr/image/upload/"
            "v1794415616/AI_in_Manufacturing.jpg"
        )

        response = self.client.get(
            reverse("core:technology")
        )

        self.assertContains(response, f'src="{image_url}"')

        response = self.client.get(
            reverse(
                "core:technology_detail",
                args=["ai-manufacturing"]
            )
        )

        self.assertContains(response, f'src="{image_url}"')

    def test_search_case_insensitive(self):
        response = self.client.get(
            reverse("core:technology"),
            {"q": "dIgItAl TwInS"}
        )

        self.assertEqual(response.status_code, 200)

        technologies = response.context["technologies"]

        self.assertEqual(len(technologies), 1)
        self.assertEqual(
            technologies[0]["slug"],
            "digital-twins"
        )

    def test_category_filter(self):
        response = self.client.get(
            reverse("core:technology"),
            {"category": "Robotics & Automation"}
        )

        technologies = response.context["technologies"]

        slugs = {
            item["slug"]
            for item in technologies
        }

        self.assertEqual(
            slugs,
            {
                "industrial-robotics",
                "industrial-automation"
            }
        )

    def test_industry_filter(self):
        response = self.client.get(
            reverse("core:technology"),
            {"industry": "mining-metals"}
        )

        technologies = response.context["technologies"]

        slugs = {
            item["slug"]
            for item in technologies
        }

        self.assertEqual(
            slugs,
            {
                "ai-manufacturing",
                "industrial-iot",
                "digital-twins"
            }
        )

    def test_combined_filters(self):
        response = self.client.get(
            reverse("core:technology"),
            {
                "q": "PLC",
                "category": "Robotics & Automation",
                "industry": "petrochemicals"
            }
        )

        technologies = response.context["technologies"]

        self.assertEqual(len(technologies), 1)
        self.assertEqual(
            technologies[0]["slug"],
            "industrial-automation"
        )

    def test_technology_detail(self):
        response = self.client.get(
            reverse(
                "core:technology_detail",
                args=["industrial-robotics"]
            )
        )

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(
            response,
            "core/technology_detail.html"
        )

        self.assertEqual(
            response.context["technology"]["slug"],
            "industrial-robotics"
        )

        self.assertContains(response, "How It Works")
        self.assertContains(response, "Industrial Applications")
        self.assertContains(response, "Benefits")
        self.assertContains(
            response,
            "Challenges and Considerations"
        )

    def test_invalid_technology(self):
        response = self.client.get(
            reverse(
                "core:technology_detail",
                args=["unknown-technology"]
            )
        )

        self.assertEqual(response.status_code, 404)

    def test_empty_search_results(self):
        response = self.client.get(
            reverse("core:technology"),
            {"q": "technology-xyz-not-found"}
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            len(response.context["technologies"]),
            0
        )

        self.assertContains(
            response,
            "No Technologies Found"
        )

    def test_all_technology_detail_pages(self):
        technologies = load_json(
            "technology.json"
        )["technologies"]

        for item in technologies:
            with self.subTest(slug=item["slug"]):
                response = self.client.get(
                    reverse(
                        "core:technology_detail",
                        args=[item["slug"]]
                    )
                )

                self.assertEqual(
                    response.status_code,
                    200
                )

                self.assertContains(
                    response,
                    item["name"]
                )

    def test_valid_industry_relationships(self):
        technologies = load_json(
            "technology.json"
        )["technologies"]

        industries = load_json(
            "industries.json"
        )["industries"]

        industry_slugs = {
            industry["slug"]
            for industry in industries
        }

        for item in technologies:
            for slug in item["industry_slugs"]:
                self.assertIn(
                    slug,
                    industry_slugs
                )

    def test_unique_ids_and_slugs(self):
        technologies = load_json(
            "technology.json"
        )["technologies"]

        ids = [
            item["id"]
            for item in technologies
        ]

        slugs = [
            item["slug"]
            for item in technologies
        ]

        self.assertEqual(
            len(ids),
            len(set(ids))
        )

        self.assertEqual(
            len(slugs),
            len(set(slugs))
        )

    def test_technology_image_files(self):
        technologies = load_json(
            "technology.json"
        )["technologies"]

        for item in technologies:
            with self.subTest(slug=item["slug"]):
                if item["image"].startswith(("http://", "https://")):
                    continue

                image_path = (
                    settings.BASE_DIR
                    / "static"
                    / item["image"]
                )

                self.assertTrue(
                    image_path.is_file()
                )

    def test_required_technology_content(self):
        technologies = load_json(
            "technology.json"
        )["technologies"]

        for item in technologies:
            with self.subTest(slug=item["slug"]):
                self.assertTrue(item["name"])
                self.assertTrue(item["description"])
                self.assertTrue(item["overview"])
                self.assertTrue(item["how_it_works"])
                self.assertTrue(item["applications"])
                self.assertTrue(item["benefits"])
                self.assertTrue(item["considerations"])
                self.assertTrue(item["industry_slugs"])
                self.assertTrue(
                    item["source_url"].startswith("https://")
                )

    def test_saudi_program_information(self):
        page = load_json("technology.json")["page"]

        self.assertTrue(page["title"])
        self.assertTrue(page["saudi_context"])

        self.assertTrue(
            page["saudi_source_url"].startswith("https://")
        )

        response = self.client.get(
            reverse("core:technology")
        )

        self.assertContains(
            response,
            "Future Factories in Saudi Arabia"
        )

class Vision2030Tests(SimpleTestCase):

    def test_vision2030_page(self):
        response = self.client.get(
            reverse("core:vision2030")
        )

        self.assertEqual(response.status_code, 200)

    def test_vision2030_template(self):
        response = self.client.get(
            reverse("core:vision2030")
        )

        self.assertTemplateUsed(
            response,
            "core/vision2030.html"
        )

        self.assertIn("vision", response.context)

    def test_hero_and_overview(self):
        response = self.client.get(
            reverse("core:vision2030")
        )

        vision = response.context["vision"]

        self.assertTrue(vision["hero"]["title"])
        self.assertTrue(vision["overview"]["description"])

        self.assertContains(
            response,
            "Vision 2030"
        )

        self.assertContains(
            response,
            "Building a More Diverse Industrial Economy"
        )

    def test_three_vision_pillars(self):
        vision = load_json("vision2030.json")

        pillars = vision["pillars"]

        self.assertEqual(len(pillars), 3)

        pillar_names = {
            pillar["name"]
            for pillar in pillars
        }

        self.assertEqual(
            pillar_names,
            {
                "A Vibrant Society",
                "A Thriving Economy",
                "An Ambitious Nation"
            }
        )

    def test_three_targets(self):
        vision = load_json("vision2030.json")

        targets = vision["targets"]

        self.assertEqual(len(targets), 3)

        values = {
            target["value"]
            for target in targets
        }

        self.assertEqual(
            values,
            {"50%", "65%", "4,000"}
        )

    def test_target_statuses_are_distinct(self):
        vision = load_json("vision2030.json")

        targets = {
            target["value"]: target
            for target in vision["targets"]
        }

        self.assertEqual(
            targets["50%"]["status"],
            "Vision 2030 target"
        )

        self.assertEqual(
            targets["65%"]["status"],
            "Vision 2030 target"
        )

        self.assertEqual(
            targets["4,000"]["status"],
            "Program aim"
        )

        self.assertEqual(
            targets["50%"]["timeframe"],
            "2030"
        )

        self.assertNotEqual(
            targets["4,000"]["timeframe"],
            "2030"
        )

    def test_four_focus_areas(self):
        vision = load_json("vision2030.json")

        areas = vision["focus_areas"]

        self.assertEqual(len(areas), 4)

        for area in areas:
            self.assertTrue(area["title"])
            self.assertTrue(area["description"])

    def test_six_initiatives(self):
        vision = load_json("vision2030.json")

        initiatives = vision["initiatives"]

        self.assertEqual(len(initiatives), 6)

        names = {
            item["name"]
            for item in initiatives
        }

        self.assertIn(
            "National Industrial Strategy",
            names
        )

        self.assertIn(
            "Future Factories Program",
            names
        )

        self.assertIn(
            "Made in Saudi Program",
            names
        )

    def test_unique_content_ids(self):
        vision = load_json("vision2030.json")

        for key in (
            "pillars",
            "targets",
            "focus_areas",
            "initiatives"
        ):
            with self.subTest(section=key):
                ids = [
                    item["id"]
                    for item in vision[key]
                ]

                self.assertEqual(
                    len(ids),
                    len(set(ids))
                )

    def test_official_source_urls(self):
        vision = load_json("vision2030.json")

        urls = [
            vision["overview"]["source_url"]
        ]

        urls.extend(
            item["source_url"]
            for item in vision["targets"]
        )

        urls.extend(
            item["source_url"]
            for item in vision["initiatives"]
        )

        for url in urls:
            with self.subTest(url=url):
                self.assertTrue(
                    url.startswith("https://")
                )

    def test_vision_image_exists(self):
        vision = load_json("vision2030.json")

        image_path = (
            settings.BASE_DIR
            / "static"
            / vision["hero"]["image"]
        )

        self.assertTrue(
            image_path.is_file()
        )

    def test_vision_page_navigation(self):
        response = self.client.get(
            reverse("core:vision2030")
        )

        self.assertContains(
            response,
            reverse("catalog:industries")
        )

        self.assertContains(
            response,
            reverse("catalog:industrial_cities")
        )

        self.assertContains(
            response,
            reverse("catalog:made_in_saudi")
        )

        self.assertContains(
            response,
            reverse("core:technology")
        )

        self.assertContains(
            response,
            "Sources and Information"
        )


class GalleryTests(SimpleTestCase):

    def test_gallery_page(self):
        response = self.client.get(
            reverse("core:gallery")
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "core/gallery.html"
        )

        slugs = {
            item["slug"]
            for item in response.context["items"]
        }

        self.assertTrue({
            "petrochemical-processing",
            "pharmaceutical-manufacturing",
            "automotive-assembly",
            "dairy-processing",
            "mineral-and-metal-processing",
            "electrical-production",
        }.issubset(slugs))

    def test_image_filter(self):
        response = self.client.get(
            reverse("core:gallery"),
            {"type": "image"}
        )

        self.assertEqual(response.status_code, 200)

        for item in response.context["items"]:
            self.assertEqual(item["type"], "image")

    def test_video_filter(self):
        response = self.client.get(
            reverse("core:gallery"),
            {"type": "video"}
        )

        self.assertEqual(response.status_code, 200)

        for item in response.context["items"]:
            self.assertEqual(item["type"], "video")

    def test_search_case_insensitive(self):
        response = self.client.get(
            reverse("core:gallery"),
            {"q": "DaIrY"}
        )

        slugs = {
            item["slug"]
            for item in response.context["items"]
        }

        self.assertEqual(
            slugs,
            {"dairy-processing"}
        )

    def test_category_filter(self):
        response = self.client.get(
            reverse("core:gallery"),
            {"category": "Automotive"}
        )

        self.assertEqual(response.status_code, 200)

        for item in response.context["items"]:
            self.assertEqual(
                item["category"],
                "Automotive"
            )

    def test_combined_filters(self):
        response = self.client.get(
            reverse("core:gallery"),
            {
                "q": "automotive",
                "type": "image",
                "category": "Automotive"
            }
        )

        items = response.context["items"]

        self.assertEqual(len(items), 1)
        self.assertEqual(
            items[0]["slug"],
            "automotive-assembly"
        )

    def test_empty_results(self):
        response = self.client.get(
            reverse("core:gallery"),
            {"q": "missing-gallery-xyz"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(response.context["items"]),
            0
        )
        self.assertContains(
            response,
            "No Media Found"
        )

    def test_unique_ids_and_slugs(self):
        media = load_json("gallery.json")["media"]

        ids = [item["id"] for item in media]
        slugs = [item["slug"] for item in media]

        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(len(slugs), len(set(slugs)))
        self.assertEqual(len(media), 14)

    def test_safe_media_paths(self):
        media = load_json("gallery.json")["media"]

        for item in media:
            with self.subTest(slug=item["slug"]):
                path = PurePosixPath(item["file"])

                self.assertNotIn("..", path.parts)
                self.assertFalse(path.is_absolute())

                self.assertTrue(
                    item["file"].startswith(
                        ("images/", "videos/")
                    )
                )

    def test_existing_image_files(self):
        media = load_json("gallery.json")["media"]

        existing = [
            item for item in media
            if item["type"] == "image"
        ]

        for item in existing:
            with self.subTest(slug=item["slug"]):
                path = (
                    settings.BASE_DIR
                    / "static"
                    / item["file"]
                )

                self.assertTrue(path.is_file())

    def test_video_posters_exist(self):
        media = load_json("gallery.json")["media"]

        videos = [
            item for item in media
            if item["type"] == "video"
        ]

        self.assertEqual(len(videos), 5)

        for item in videos:
            with self.subTest(slug=item["slug"]):
                path = (
                    settings.BASE_DIR
                    / "static"
                    / item["poster"]
                )

                self.assertTrue(path.is_file())

    def test_licensed_media_metadata(self):
        media = load_json("gallery.json")["media"]

        licensed = [
            item for item in media
            if item["id"] > 6
        ]

        self.assertEqual(len(licensed), 8)

        for item in licensed:
            with self.subTest(slug=item["slug"]):
                self.assertTrue(item["creator"])
                self.assertTrue(
                    item["source_url"].startswith("https://")
                )
                self.assertTrue(item["license"])
                self.assertTrue(
                    item["license_url"].startswith("https://")
                )

    def test_image_preview_modal(self):
        response = self.client.get(
            reverse("core:gallery")
        )

        self.assertContains(
            response,
            'data-bs-toggle="modal"'
        )
        self.assertContains(
            response,
            "galleryPreview1"
        )

    def test_video_player_with_cdn_url(self):
        gallery_data = load_json("gallery.json")

        for item in gallery_data["media"]:
            if item["type"] == "video":
                item["video_url"] = (
                    f"https://cdn.example.test/{item['file']}"
                )

        with patch(
            "apps.core.views.load_json",
            return_value=gallery_data
        ):
            response = self.client.get(
                reverse("core:gallery"),
                {"type": "video"}
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(response.context["items"]),
            5
        )

        self.assertContains(
            response,
            "<video",
            count=5
        )

        self.assertContains(
            response,
            "https://cdn.example.test/videos/gallery/automotive-robotics.mp4"
        )

class AboutTests(SimpleTestCase):

    def test_about_page(self):
        response = self.client.get(
            reverse("core:about")
        )

        self.assertEqual(response.status_code, 200)

    def test_about_template(self):
        response = self.client.get(
            reverse("core:about")
        )

        self.assertTemplateUsed(
            response,
            "core/about.html"
        )

    def test_about_context(self):
        response = self.client.get(
            reverse("core:about")
        )

        self.assertIn("about", response.context)

        self.assertEqual(
            response.context["about"]["hero"]["title"],
            "Discover SAUDI INDUSTRY"
        )

    def test_hero_image_exists(self):
        about = load_json("about.json")

        image_path = (
            settings.BASE_DIR
            / "static"
            / about["hero"]["image"]
        )

        self.assertTrue(image_path.is_file())

    def test_mission_and_vision(self):
        response = self.client.get(
            reverse("core:about")
        )

        self.assertContains(
            response,
            "Our Mission"
        )

        self.assertContains(
            response,
            "Our Vision"
        )

    def test_seven_project_sections(self):
        about = load_json("about.json")

        sections = about["sections"]

        self.assertEqual(len(sections), 7)

        for section in sections:
            with self.subTest(section=section["title"]):
                self.assertTrue(section["title"])
                self.assertTrue(section["description"])
                self.assertTrue(section["route_name"])

    def test_section_routes_are_valid(self):
        about = load_json("about.json")

        for section in about["sections"]:
            with self.subTest(route=section["route_name"]):
                url = reverse(section["route_name"])

                self.assertTrue(url.startswith("/"))

    def test_section_links_render(self):
        response = self.client.get(
            reverse("core:about")
        )

        about = load_json("about.json")

        for section in about["sections"]:
            with self.subTest(section=section["title"]):
                self.assertContains(
                    response,
                    reverse(section["route_name"])
                )

    def test_build_process(self):
        about = load_json("about.json")

        steps = about["build_process"]

        self.assertEqual(len(steps), 4)

        for step in steps:
            self.assertTrue(step["title"])
            self.assertTrue(step["description"])

    def test_technology_stack(self):
        about = load_json("about.json")

        stack = about["technology_stack"]

        self.assertEqual(len(stack), 6)

        self.assertIn("Python", stack)
        self.assertIn("Django", stack)
        self.assertIn("Bootstrap 5", stack)

    def test_editorial_principles(self):
        about = load_json("about.json")

        principles = about["editorial_principles"]

        self.assertEqual(len(principles), 4)

        names = {
            item["title"]
            for item in principles
        }

        self.assertIn("Source Transparency", names)
        self.assertIn("Responsible Media Use", names)

        response = self.client.get(
            reverse("core:about")
        )

        self.assertContains(
            response,
            "Editorial Principles"
        )

    def test_disclaimer_and_repository(self):
        about = load_json("about.json")

        self.assertIn(
            "independent educational",
            about["disclaimer"]["text"]
        )

        self.assertTrue(
            about["repository"]["url"].startswith(
                "https://github.com/"
            )
        )

        response = self.client.get(
            reverse("core:about")
        )

        self.assertContains(
            response,
            "Educational Project Disclaimer"
        )

        self.assertContains(
            response,
            about["repository"]["url"]
        )
