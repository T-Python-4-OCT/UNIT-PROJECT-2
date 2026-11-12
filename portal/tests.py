from django.test import TestCase
from django.urls import reverse

from .forms import FeedbackForm
from .models import Feedback
from .views import find_page_content, load_json

VALID_DATA = {
    "name": "Sara Ahmed",
    "email": "Sara@Example.com",
    "category": "suggestion",
    "rating": "4",
    "message": "The Absher page is clear, please add more figures for 2025.",
    "website": "",
}


def make_form(language="en", **changes):
    "Build a FeedbackForm with VALID_DATA plus the given changes."
    data = {**VALID_DATA, **changes}
    return FeedbackForm(data, text=load_json("feedback.json", language))


class FeedbackFormTests(TestCase):
    "Each test sends one kind of bad input and checks it is rejected."

    def test_valid_data_passes(self):
        form = make_form()
        self.assertTrue(form.is_valid(), form.errors)

    def test_arabic_name_is_accepted(self):
        self.assertTrue(make_form(name="معاذ العتيبي").is_valid())

    def test_name_spaces_are_collapsed(self):
        form = make_form(name="  Sara    Ahmed ")
        form.is_valid()
        self.assertEqual(form.cleaned_data["name"], "Sara Ahmed")

    def test_email_is_lowercased(self):
        form = make_form()
        form.is_valid()
        self.assertEqual(form.cleaned_data["email"], "sara@example.com")

    def test_all_fields_empty(self):
        form = FeedbackForm({}, text=load_json("feedback.json", "en"))
        self.assertFalse(form.is_valid())
        for field in ("name", "email", "category", "rating", "message"):
            self.assertIn(field, form.errors)

    def test_whitespace_only_name_is_required(self):
        self.assertIn("name", make_form(name="     ").errors)

    def test_name_too_short(self):
        self.assertIn("name", make_form(name="S").errors)

    def test_name_too_long(self):
        self.assertIn("name", make_form(name="a" * 61).errors)

    def test_name_with_digits(self):
        self.assertIn("name", make_form(name="Sara123").errors)

    def test_name_with_html(self):
        self.assertIn("name", make_form(name="<script>").errors)

    def test_invalid_email(self):
        for email in ("sara", "sara@", "@example.com", "sara@example"):
            with self.subTest(email=email):
                self.assertIn("email", make_form(email=email).errors)

    def test_tampered_category(self):
        "A value changed in DevTools that is not in the list."
        self.assertIn("category", make_form(category="hacked").errors)

    def test_rating_out_of_range(self):
        for rating in ("0", "6", "-1", "abc"):
            with self.subTest(rating=rating):
                self.assertIn("rating", make_form(rating=rating).errors)

    def test_message_too_short(self):
        self.assertIn("message", make_form(message="Too short").errors)

    def test_message_too_long(self):
        self.assertIn("message", make_form(message="a" * 1001).errors)

    def test_message_only_symbols_or_numbers(self):
        self.assertIn("message", make_form(message="1234567890 !!!! ????? ####").errors)

    def test_message_with_too_many_links(self):
        message = "See http://a.com and http://b.com and www.c.com for details."
        self.assertIn("message", make_form(message=message).errors)

    def test_honeypot_filled_is_rejected(self):
        form = make_form(website="http://spam.example")
        self.assertFalse(form.is_valid())
        self.assertTrue(form.non_field_errors())

    def test_errors_follow_the_language(self):
        form = make_form(language="ar", email="wrong")
        self.assertEqual(
            form.errors["email"][0],
            load_json("feedback.json", "ar")["errors"]["email_invalid"],
        )


class FeedbackViewTests(TestCase):
    url = reverse("portal:feedback")

    def test_page_loads_in_both_languages(self):
        for language in ("en", "ar"):
            with self.subTest(language=language):
                session = self.client.session
                session["language"] = language
                session.save()
                self.assertEqual(self.client.get(self.url).status_code, 200)

    def test_valid_post_saves_and_redirects(self):
        response = self.client.post(self.url, VALID_DATA)
        self.assertRedirects(response, self.url)
        self.assertEqual(Feedback.objects.count(), 1)
        self.assertEqual(Feedback.objects.get().email, "sara@example.com")

    def test_success_message_shows_once(self):
        self.client.post(self.url, VALID_DATA)
        first = self.client.get(self.url)
        second = self.client.get(self.url)
        self.assertTrue(first.context["success"])
        self.assertFalse(second.context["success"])

    def test_invalid_post_saves_nothing_and_keeps_input(self):
        response = self.client.post(self.url, {**VALID_DATA, "email": "wrong"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Feedback.objects.count(), 0)
        self.assertContains(response, "Sara Ahmed")

    def test_second_message_within_a_minute_is_blocked(self):
        self.client.post(self.url, VALID_DATA)
        response = self.client.post(self.url, VALID_DATA)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Feedback.objects.count(), 1)

    def test_unsupported_method_is_rejected(self):
        self.assertEqual(self.client.put(self.url).status_code, 405)


class ExistingValidationTests(TestCase):
    "Validation that was already in the site before the feedback page."

    def test_unknown_page_returns_custom_404(self):
        response = self.client.get("/not-a-real-page/")
        self.assertEqual(response.status_code, 404)

    def test_all_pages_load_in_both_languages(self):
        for language in ("en", "ar"):
            session = self.client.session
            session["language"] = language
            session.save()
            for page in load_json("site.json", language)["pages"]:
                with self.subTest(language=language, slug=page["slug"]):
                    url = reverse("portal:page", args=[page["slug"]])
                    self.assertEqual(self.client.get(url).status_code, 200)

    def test_invalid_language_is_ignored(self):
        self.client.post(reverse("portal:set_language"), {"language": "fr"})
        self.assertNotEqual(self.client.session.get("language"), "fr")

    def test_language_switch_blocks_external_redirect(self):
        response = self.client.post(
            reverse("portal:set_language"),
            {"language": "ar"},
            HTTP_REFERER="https://evil.example.com/",
        )
        self.assertRedirects(response, reverse("portal:home"), fetch_redirect_response=False)

    def test_language_switch_requires_post(self):
        self.assertEqual(self.client.get(reverse("portal:set_language")).status_code, 405)


class SearchTests(TestCase):
    url = reverse("portal:search")

    def set_language(self, language):
        session = self.client.session
        session["language"] = language
        session.save()

    def test_page_loads_without_query_and_shows_no_error(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context["form"].errors)
        self.assertIsNone(response.context["results"])

    def test_empty_query_shows_error(self):
        response = self.client.get(self.url, {"q": "   "})
        self.assertIn("q", response.context["form"].errors)

    def test_one_character_is_too_short(self):
        response = self.client.get(self.url, {"q": "a"})
        self.assertIn("q", response.context["form"].errors)

    def test_query_too_long(self):
        response = self.client.get(self.url, {"q": "a" * 81})
        self.assertIn("q", response.context["form"].errors)

    def test_symbols_only_is_rejected(self):
        response = self.client.get(self.url, {"q": "!!@@##"})
        self.assertIn("q", response.context["form"].errors)

    def test_finds_absher_in_english(self):
        response = self.client.get(self.url, {"q": "absher"})
        slugs = [result["slug"] for result in response.context["results"]]
        self.assertIn("absher", slugs)

    def test_finds_arabic_without_hamza_or_ta_marbuta(self):
        "'ابشر' should find 'أبشر', and 'الهويه' should find 'الهوية'."
        self.set_language("ar")
        for query, slug in (("ابشر", "absher"), ("الهويه الرقميه", "digital-identity")):
            with self.subTest(query=query):
                response = self.client.get(self.url, {"q": query})
                slugs = [result["slug"] for result in response.context["results"]]
                self.assertIn(slug, slugs)

    def test_no_results_is_not_an_error(self):
        response = self.client.get(self.url, {"q": "zzzqqq"})
        self.assertFalse(response.context["form"].errors)
        self.assertEqual(response.context["results"], [])

    def test_html_in_query_is_escaped(self):
        response = self.client.get(self.url, {"q": "<script>alert(1)</script>"})
        self.assertNotContains(response, "<script>alert(1)</script>", html=False)

    def test_match_is_highlighted(self):
        response = self.client.get(self.url, {"q": "absher"})
        self.assertContains(response, "<mark>")

    def test_search_url_is_not_read_as_a_page_slug(self):
        self.assertEqual(self.client.get(self.url).resolver_match.url_name, "search")


class FaviconTests(TestCase):
    def test_favicon_ico_redirects_to_svg(self):
        response = self.client.get("/favicon.ico")
        self.assertEqual(response.status_code, 301)
        self.assertTrue(response["Location"].endswith("portal/img/favicon.svg"))


class CompareSliderTests(TestCase):
    def test_home_shows_slider_in_both_languages(self):
        for language in ("en", "ar"):
            with self.subTest(language=language):
                session = self.client.session
                session["language"] = language
                session.save()
                response = self.client.get(reverse("portal:home"))
                self.assertContains(response, 'type="range"')
                self.assertContains(response, load_json("home.json", language)["compare"]["before_alt"])

    def test_slider_images_exist(self):
        from django.contrib.staticfiles import finders

        for name in ("before-office.webp", "after-app.webp"):
            with self.subTest(image=name):
                self.assertIsNotNone(finders.find(f"portal/img/{name}"))


class GalleryTests(TestCase):
    def galleries(self, language):
        "Yield (slug, gallery section) for every page that has a gallery."
        site = load_json("site.json", language)
        for page in site["pages"]:
            content = find_page_content(site, page["slug"], language)
            for section in content["sections"]:
                if section["type"] == "gallery":
                    yield page["slug"], section

    def test_every_gallery_image_exists_and_has_a_caption(self):
        from django.contrib.staticfiles import finders

        for language in ("en", "ar"):
            for slug, section in self.galleries(language):
                for item in section["items"]:
                    with self.subTest(language=language, slug=slug, image=item["image"]):
                        self.assertIsNotNone(finders.find(item["image"]))
                        self.assertTrue(item["caption"].strip())

    def test_gallery_shows_on_its_page(self):
        for slug, section in self.galleries("en"):
            with self.subTest(slug=slug):
                response = self.client.get(reverse("portal:page", args=[slug]))
                self.assertContains(response, 'class="gallery-item"', count=len(section["items"]))

    def test_home_journey_cards_have_photos(self):
        response = self.client.get(reverse("portal:home"))
        for step in response.context["journey_steps"]:
            with self.subTest(slug=step["slug"]):
                self.assertTrue(step["image"])

    def test_search_finds_words_in_captions(self):
        session = self.client.session
        session["language"] = "ar"
        session.save()
        response = self.client.get(reverse("portal:search"), {"q": "المصمك"})
        slugs = [result["slug"] for result in response.context["results"]]
        self.assertIn("moi-evolution", slugs)
