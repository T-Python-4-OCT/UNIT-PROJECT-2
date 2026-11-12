import json
import os
import re
import runpy
import struct
import unicodedata
from datetime import date
from unittest import mock
from urllib.parse import urlsplit

from django.conf import settings
from django.test import SimpleTestCase
from django.urls import resolve, reverse
from django.utils.html import escape
from django.utils.translation import gettext, override

from .content import (
    ARABIC_FOLD,
    ContentError,
    _fold,
    coordinates,
    degrees_to_map,
    highlight,
    map_geometry,
    map_to_degrees,
    records,
    search,
    search_terms,
    timeline,
    totals,
    validate,
)

LANGUAGES = {"en": ("", "ltr"), "ar": ("/ar", "rtl")}
SLUGS = ["neom", "qiddiya", "diriyah", "roshn", "the-red-sea", "amaala", "alula"]
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
                self.assertContains(home, "data-atlas-link data-project=", count=7)
                self.assertContains(home, "data-anchor-x=", count=6)
                self.assertContains(home, "data-atlas-toggle")
                self.assertContains(
                    home, 'id="map" aria-labelledby="atlas-title" data-atlas data-expedition', count=1
                )
                self.assertContains(home, '<li class="project-row" data-project=', count=7)
                self.assertContains(home, 'class="project-index shell" id="projects"', count=1)
                self.assertContains(home, '<a class="skip-link skip-tour" href="#after-tour">', count=1)
                self.assertContains(home, 'id="after-tour"', count=1)
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
                    self.assertContains(
                        response, f"https://pub-c2c16b46c0b84def87264751bdbab348.r2.dev/{record['slug']}.mp4"
                    )
                    self.assertNotContains(response, '<source src="/static/atlas/videos/')
                    self.assertNotContains(response, "autoplay")
                    self.assertContains(response, 'fetchpriority="high"', count=1)
                    for track in record["video"]["captions"]:
                        self.assertContains(response, f'srclang="{track["lang"]}" label="{track["label"]}">')
                    self.assertNotRegex(response.content.decode(), r"<track[^>]* default")

    def test_project_page_plate_layout(self):
        slugs = [record["slug"] for record in records()]
        for language, (prefix, direction) in LANGUAGES.items():
            with self.subTest(language=language), override(language):
                for index, record in enumerate(records()):
                    slug = record["slug"]
                    following = slugs[(index + 1) % len(slugs)]
                    previous = slugs[index - 1]
                    html = self.client.get(reverse("project", kwargs={"slug": slug})).content.decode()

                    self.assertEqual(html.count("data-plate-rail"), 1)
                    self.assertEqual(html.count('aria-label="%s"' % gettext("On this page")), 1)
                    self.assertLess(html.index('class="detail-intro"'), html.index("data-plate-rail"))
                    self.assertLess(html.index("data-plate-rail"), html.index('id="story-title"'))

                    self.assertNotIn('class="rail-coordinates"', html)
                    self.assertIn(
                        record["region"][language], html.split("data-plate-rail", 1)[1].split("</nav>", 1)[0]
                    )

                    self.assertIn("data-gallery-strip", html)
                    self.assertIn("data-gallery-steps hidden", html)
                    self.assertEqual(html.count("data-project-photo"), len(record["gallery"]))
                    for photo in record["gallery"]:
                        self.assertIn(f'width="{photo["width"]}" height="{photo["height"]}"', html)

                    timeline = html.split('<ol class="timeline">', 1)[1].split("</ol>", 1)[0]
                    self.assertEqual(timeline.count("<li>"), len(record["milestones"]))
                    self.assertEqual(timeline.count("<time "), len(record["milestones"]))

                    band = re.search(
                        r'<a class="next-plate" href="([^"]+)" rel="next" data-plate="([^"]+)"', html
                    )
                    self.assertIsNotNone(band)
                    self.assertEqual(band.groups(), (f"{prefix}/projects/{following}/", following))
                    self.assertEqual(html.count('rel="next"'), 1)
                    self.assertEqual(html.count('rel="prev"'), 1)
                    self.assertIn(f'href="{prefix}/projects/{previous}/" rel="prev"', html)
                    pager = html.split('class="next-plate"', 1)[1].split("</a>", 1)[0]
                    self.assertIn('sizes="100vw"', pager)
                    self.assertIn('loading="lazy"', pager)
                    self.assertNotIn("fetchpriority", pager)
                    self.assertIn('alt=""', pager)

    def test_plate_transition_boot_script(self):
        html = self.client.get(reverse("project", kwargs={"slug": "neom"})).content.decode()
        head = html.split("</head>", 1)[0]

        self.assertEqual(head.count("onpagereveal"), 1)
        self.assertNotIn('<script type="module">', head.split("onpagereveal", 1)[0].rsplit("<script", 1)[-1])
        home = self.client.get(reverse("home")).content.decode()
        self.assertEqual(home.count('data-plate="'), 2 * len(SLUGS))

    def test_full_bleed_bands_use_no_viewport_width_arithmetic(self):
        for path in (settings.BASE_DIR / "saudi_atlas" / "projects" / "frontend" / "styles").glob("*.css"):
            with self.subTest(stylesheet=path.name):
                rules = re.sub(r"/\*.*?\*/", "", path.read_text(encoding="utf-8"), flags=re.S)
                self.assertIsNone(re.search(r"50vw", rules))

    def test_timeline_filter(self):
        response = self.client.get(reverse("timeline"), {"project": "diriyah"})
        self.assertContains(response, 'aria-current="true"', count=1)
        self.assertContains(response, "2010")
        self.assertNotContains(response, "NEOM Bay Airport began operating.")
        unknown = self.client.get(reverse("timeline"), {"project": "unknown"})
        self.assertContains(unknown, "NEOM Bay Airport began operating.")

    def test_home_figures_and_timeline_chart(self):
        home = self.client.get(reverse("home"))
        figures = totals()
        self.assertEqual(figures["projects"], len(SLUGS))
        self.assertContains(home, f"<dd>{figures['milestones']}</dd>")
        self.assertContains(home, f"<dd>{figures['first_year']}–{figures['last_year']}</dd>")

        html = home.content.decode()
        self.assertLess(html.index("data-expedition"), html.index('class="hero-figures"'))
        self.assertLess(html.index('id="after-tour"'), html.index('class="hero-figures"'))
        chart = self.client.get(reverse("timeline"))
        self.assertContains(chart, 'class="lane-dot"', count=figures["milestones"])
        filtered = self.client.get(reverse("timeline"), {"project": "diriyah"})
        self.assertContains(filtered, 'class="lane-dot"', count=3)

    def test_timeline_dots_link_to_their_entries(self):
        for language, (prefix, direction) in LANGUAGES.items():
            for selected in (None, "qiddiya"):
                with self.subTest(language=language, project=selected), override(language):
                    html = self.client.get(
                        reverse("timeline"), {"project": selected} if selected else {}
                    ).content.decode()
                    nav = html.split("data-scrubber", 1)[1].split("</nav>", 1)[0]
                    self.assertNotIn('role="img"', html)
                    targets = re.findall(r'<a class="lane-dot" href="#([^"]+)"', nav)
                    entries = re.findall(r'<li id="(m-[a-z-]+-\d+)" tabindex="-1"', html)
                    self.assertEqual(sorted(targets), sorted(entries))
                    self.assertEqual(len(targets), 3 if selected else totals()["milestones"])

                    names = re.findall(r'<span class="visually-hidden">([^<]+)</span></a>', nav)
                    self.assertEqual(len(names), len(targets))
                    if language == "en":
                        if selected:
                            self.assertIn("Qiddiya, 23 April 2026: Aquarabia opened to the public.", names)
                        else:
                            self.assertIn("NEOM, 2019: NEOM Bay Airport began operating.", names)
                    else:
                        self.assertTrue(all("،" in name for name in names))

    def test_timeline_lane_rows_keep_targets_apart(self):
        from .content import LANE_GAP_YEARS, _year_position, milestone_lanes

        for lane in milestone_lanes("en")["lanes"]:
            rows = {}
            for dot in lane["dots"]:
                rows.setdefault(dot["row"], []).append(_year_position(dot["iso"]))
            for positions in rows.values():
                for before, after in zip(positions, positions[1:]):
                    self.assertGreaterEqual(after - before, LANE_GAP_YEARS)

    def test_search(self):
        for language, (prefix, direction) in LANGUAGES.items():
            with self.subTest(language=language), override(language):
                path = reverse("search")
                self.assertEqual(path, f"{prefix}/search/")
                empty = self.client.get(path)
                self.assertContains(empty, f'<html lang="{language}" dir="{direction}">')
                self.assertNotContains(empty, 'class="result"')
                missing = self.client.get(path, {"q": "zzzz"})
                self.assertNotContains(missing, 'class="result"')
        hegra = self.client.get("/search/", {"q": "  HEGRA  facade "})
        self.assertContains(hegra, 'class="result"', count=1)
        self.assertContains(hegra, 'href="/projects/alula/#gallery-title"')
        self.assertContains(hegra, 'href="/ar/search/?q=')
        self.assertContains(hegra, '<link rel="canonical" href="http://testserver/search/">')
        escaped = self.client.get("/search/", {"q": '"><script>'})
        self.assertNotContains(escaped, '<script>"')
        self.assertNotContains(escaped, '"><script>')

    def test_search_partial_and_marks(self):
        full = self.client.get("/search/", {"q": "unesco"})
        self.assertIn("X-Atlas-Partial", full["Vary"])
        self.assertContains(full, "<mark>UNESCO</mark>")
        self.assertContains(full, "data-live-search")
        self.assertContains(full, "2 projects match")
        partial = self.client.get("/search/", {"q": "unesco"}, headers={"X-Atlas-Partial": "results"})
        self.assertIn("X-Atlas-Partial", partial["Vary"])
        self.assertNotContains(partial, "<html")
        self.assertContains(partial, "<mark>UNESCO</mark>")
        self.assertContains(partial, 'id="results-title"')
        none = self.client.get("/search/", {"q": "zzzz"}, headers={"X-Atlas-Partial": "results"})
        self.assertContains(none, 'data-announce="No results"')
        with override("ar"):
            arabic = self.client.get(reverse("search"), {"q": "الحجر"})
            self.assertContains(arabic, "<mark>الحِجر</mark>")
            self.assertContains(arabic, "مشروع واحد مطابق")

        hostile = self.client.get("/search/", {"q": "<b>unesco</b>"}).content.decode()
        self.assertNotIn("<b>", hostile)
        self.assertIn("&lt;b&gt;unesco&lt;/b&gt;", hostile)

    def test_arabic_result_counts_use_every_plural_form(self):
        from django.utils.translation import ngettext

        expected = {
            1: "مشروع واحد مطابق",
            2: "مشروعان مطابقان",
            3: "3 مشاريع مطابقة",
            11: "11 مشروعًا مطابقًا",
            100: "100 مشروع مطابق",
        }
        with override("ar"):
            for count, text in expected.items():
                self.assertEqual(
                    ngettext("%(counter)s project matches", "%(counter)s projects match", count)
                    % {"counter": count},
                    text,
                )

    def test_search_ranking_and_arabic_folding(self):
        self.assertEqual(search("qiddiya", "en")[0]["project"]["slug"], "qiddiya")
        self.assertEqual(
            [result["project"]["slug"] for result in search("unesco", "en")], ["alula", "diriyah"]
        )
        self.assertEqual(search("الحجر", "ar")[0]["project"]["slug"], "alula")
        self.assertEqual(search("", "en"), [])

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
                    self.assertContains(
                        response, f'<html lang="{language}" dir="{direction}">', status_code=404
                    )
                    self.assertContains(response, gettext("Page not found"), status_code=404)
                    self.assertContains(response, f'href="{prefix}/"', status_code=404)
                    self.assertContains(response, f'href="{prefix}/projects/neom/"', status_code=404)

                    self.assertContains(
                        response,
                        f'<h1 class="page-title" id="error-title">{gettext("Off the map")}</h1>',
                        status_code=404,
                    )
                    self.assertContains(response, "atlas/media/atlas-poster.svg", status_code=404)
                    self.assertContains(response, "data-off-map-marker", count=1, status_code=404)
                    self.assertContains(
                        response,
                        f'<form class="search-form" role="search" action="{prefix}/search/" method="get">',
                        status_code=404,
                    )
                    self.assertContains(response, 'name="q"', status_code=404)
                    html = (
                        response.content.decode()
                        .split('class="not-found-projects"', 1)[1]
                        .split("</ul>", 1)[0]
                    )
                    self.assertEqual(len(re.findall(rf'href="{prefix}/projects/[a-z-]+/"', html)), len(SLUGS))
                    self.assertNotIn("<canvas", response.content.decode())

    def test_compare_is_one_table(self):
        for language, (prefix, direction) in LANGUAGES.items():
            with self.subTest(language=language), override(language):
                html = self.client.get(reverse("compare")).content.decode()
                self.assertEqual(html.count("<table"), 1)
                self.assertIn('<caption id="compare-caption">', html)
                self.assertIn('role="region" aria-labelledby="compare-caption" tabindex="0"', html)
                self.assertEqual(html.count('<th scope="col">'), 7)
                self.assertEqual(html.count('<th scope="row">'), len(SLUGS))
                for label in (
                    "Region",
                    "Focus",
                    "Status",
                    "First milestone",
                    "Latest milestone",
                    "Key facts",
                ):
                    self.assertIn(f'<th scope="col">{gettext(label)}</th>', html)
                rows = re.findall(r'<th scope="row">\s*<a class="compare-project" href="([^"]+)">', html)
                self.assertEqual(rows, [f"{prefix}/projects/{slug}/" for slug in SLUGS])
                for record in records():
                    self.assertIn(record["milestones"][-1]["text"][language], html)
                    for fact in record["facts"]:
                        self.assertIn(
                            f"<dt>{fact['label'][language]}</dt><dd>{fact['value'][language]}</dd>", html
                        )
                self.assertNotIn("compare-card", html)

    def test_joined_names_use_the_language_punctuation(self):
        templates = settings.BASE_DIR / "saudi_atlas" / "projects" / "templates"
        for template in templates.rglob("*.html"):
            with self.subTest(template=template.name):
                source = re.sub(
                    r"{%\s*blocktranslate.*?endblocktranslate\s*%}",
                    "",
                    template.read_text(encoding="utf-8"),
                    flags=re.S,
                )
                self.assertNotRegex(source, r"(\}\}|%\})\s*[,:.]\s*(\{\{|\{%)")

    def test_sitemap_and_robots(self):
        sitemap = self.client.get("/sitemap.xml")
        self.assertEqual(sitemap["Content-Type"], "application/xml")

        self.assertEqual(sitemap.content.decode().count("<url>"), 2 * (len(ROUTES) + 1 + len(SLUGS)))
        self.assertContains(sitemap, "http://testserver/ar/projects/amaala/")
        robots = self.client.get("/robots.txt")
        self.assertContains(robots, "Sitemap: http://testserver/sitemap.xml")

    def test_template_messages_are_translated(self):
        pattern = re.compile(r"""{%\s+translate\s+(['"])(.*?)\1\s+%}""")
        with override("ar"):
            for template in (settings.BASE_DIR / "saudi_atlas" / "projects" / "templates").rglob("*.html"):
                for _, message in pattern.findall(template.read_text(encoding="utf-8")):
                    with self.subTest(template=template.name, message=message):
                        translated = gettext(message)
                        self.assertNotEqual(translated, message)
                        self.assertRegex(translated, r"[؀-ۿ]")


class SettingsTests(SimpleTestCase):
    def load_settings(self, **environment):
        base = {
            key: value
            for key, value in os.environ.items()
            if not key.startswith("ATLAS_") and key != "RENDER_EXTERNAL_HOSTNAME"
        }
        with mock.patch.dict(os.environ, {**base, **environment}, clear=True):
            return runpy.run_path(str(settings.BASE_DIR / "saudi_atlas" / "settings.py"))

    def test_local_defaults_without_render(self):
        loaded = self.load_settings()
        self.assertEqual(loaded["ALLOWED_HOSTS"], ["127.0.0.1", "localhost", "[::1]", "testserver"])
        self.assertEqual(loaded["CSRF_TRUSTED_ORIGINS"], [])

    def test_render_hostname_is_added_to_hosts_and_origins(self):
        loaded = self.load_settings(RENDER_EXTERNAL_HOSTNAME="atlas-example.onrender.com", ATLAS_DEBUG="0")
        self.assertEqual(
            loaded["ALLOWED_HOSTS"],
            ["127.0.0.1", "localhost", "[::1]", "testserver", "atlas-example.onrender.com"],
        )
        self.assertEqual(loaded["CSRF_TRUSTED_ORIGINS"], ["https://atlas-example.onrender.com"])

    def test_render_hostname_extends_explicit_hosts_without_duplicates(self):
        loaded = self.load_settings(
            RENDER_EXTERNAL_HOSTNAME="atlas-example.onrender.com",
            ATLAS_ALLOWED_HOSTS="atlas.example.org,atlas-example.onrender.com",
            ATLAS_CSRF_TRUSTED_ORIGINS="https://atlas.example.org",
        )
        self.assertEqual(loaded["ALLOWED_HOSTS"], ["atlas.example.org", "atlas-example.onrender.com"])
        self.assertEqual(
            loaded["CSRF_TRUSTED_ORIGINS"],
            ["https://atlas.example.org", "https://atlas-example.onrender.com"],
        )

    def test_blank_render_hostname_changes_nothing(self):
        loaded = self.load_settings(RENDER_EXTERNAL_HOSTNAME="  ")
        self.assertNotIn("", loaded["ALLOWED_HOSTS"])
        self.assertEqual(loaded["CSRF_TRUSTED_ORIGINS"], [])

    def test_render_host_is_served_and_unknown_hosts_are_refused(self):
        with self.settings(ALLOWED_HOSTS=["atlas-example.onrender.com"]):
            self.assertEqual(
                self.client.get("/robots.txt", HTTP_HOST="atlas-example.onrender.com").status_code, 200
            )
            self.assertEqual(self.client.get("/robots.txt", HTTP_HOST="elsewhere.example").status_code, 400)


class CreditsTests(SimpleTestCase):
    TITLES = {"en": "Credits", "ar": "المصادر والحقوق"}

    def test_credits_page_in_both_languages(self):
        for language, (prefix, direction) in LANGUAGES.items():
            with self.subTest(language=language), override(language):
                path = reverse("credits")
                self.assertEqual(path, f"{prefix}/credits/")
                self.assertEqual(resolve(path).url_name, "credits")
                response = self.client.get(path)
                self.assertEqual(response.status_code, 200)
                self.assertTemplateUsed(response, "credits.html")
                self.assertContains(response, f'<html lang="{language}" dir="{direction}">')
                self.assertContains(response, f'<h1 class="page-title">{self.TITLES[language]}</h1>')
                self.assertContains(response, f"<title>{self.TITLES[language]} | ")
                self.assertContains(response, 'hreflang="ar" href="http://testserver/ar/credits/"')

                self.assertContains(
                    response,
                    '<a href="https://commons.wikimedia.org/wiki/File:At-Turaif_District.jpg" lang="en" dir="ltr">At-Turaif District</a>',
                )
                self.assertContains(response, '<span lang="en" dir="ltr">Xiquinho Silva</span>')
                self.assertContains(
                    response,
                    '<a class="credits-name" href="https://creativecommons.org/licenses/by/2.0/" lang="en" dir="ltr">CC BY 2.0</a>',
                )
                self.assertContains(
                    response, "Red Sea’s Northern Harrat Beach in Umluj, Saudi Arabia (2025)</a>"
                )
                self.assertContains(response, '<span lang="en" dir="ltr">Saudi Press Agency (SPA)</span>')
                self.assertContains(
                    response,
                    '<a class="credits-name" href="https://creativecommons.org/licenses/by-sa/4.0/" lang="en" dir="ltr">CC BY-SA 4.0</a>',
                )
                self.assertContains(response, 'href="https://cc.spa.gov.sa/fr/terms/1220"')
                for record in records():
                    self.assertContains(response, f'<a href="{record["video"]["source_url"]}">')

                self.assertContains(
                    response,
                    '<a class="credits-name" href="https://www.roshn.sa/communities/sedra" lang="en" dir="ltr">roshn.sa</a>',
                    count=4,
                )
                for name in (
                    "ETOPO 2022",
                    "Natural Earth 1:50m",
                    "IBM Plex Sans Arabic",
                    "Instrument Serif",
                    "Amiri",
                    "SIL Open Font License 1.1",
                ):
                    self.assertContains(response, name)

                self.assertNotContains(response, 'id="credits-software-title"')

                self.assertNotContains(response, 'target="_blank"')
                self.assertNotRegex(response.content.decode(), r'href="[^"]*[?&](utm_|fbclid|gclid)')
                self.assertContains(
                    response, f'<a href="{path}" aria-current="page">{self.TITLES[language]}</a>'
                )

    def test_credits_link_is_in_the_footer_only(self):
        for language, (prefix, _) in LANGUAGES.items():
            with self.subTest(language=language), override(language):
                credits_path = reverse("credits")
                paths = [reverse(name) for name in ("home", "timeline", "compare", "search", "credits")]
                paths += [reverse("project", kwargs={"slug": "neom"}), f"{prefix}/no-such-page/"]
                for path in paths:
                    html = self.client.get(path).content.decode()
                    before, found, footer = html.partition('<footer class="site-footer">')
                    self.assertTrue(found, path)
                    self.assertIn(f'<a href="{credits_path}"', footer, path)
                    self.assertNotIn(f'href="{credits_path}"', before, path)

    def test_things_to_do_cards(self):
        for language in ("en", "ar"):
            with self.subTest(language=language), override(language):
                for record in records():
                    html = self.client.get(
                        reverse("project", kwargs={"slug": record["slug"]})
                    ).content.decode()
                    things = record.get("things_to_do", [])
                    self.assertEqual(html.count('class="thing-card"'), len(things), record["slug"])
                    for thing in things:
                        for key in ("name", "brief", "price"):
                            if key in thing:
                                self.assertIn(escape(thing[key][language]), html)
                        self.assertIn(f"{thing['image']['src']}-", html)
        alula = next(record for record in records() if record["slug"] == "alula")
        self.assertEqual(alula["things_to_do"][0]["price"]["en"], "From SAR 95 per person")

        red_sea = self.client.get(reverse("project", kwargs={"slug": "the-red-sea"})).content.decode()
        self.assertEqual(red_sea.count('class="thing-card"'), 3)
        self.assertNotIn('class="thing-price"', red_sea)

    def test_project_pages_carry_no_credits(self):
        for record in records():
            response = self.client.get(reverse("project", kwargs={"slug": record["slug"]}))
            self.assertNotContains(response, 'id="sources-title"')
            for marker in ("Xiquinho Silva", "creativecommons.org", "Wikimedia Commons", "CC BY"):
                self.assertNotContains(response, marker)

    def test_recorded_credits_match_the_project_media(self):
        from .views import credits_data

        data = credits_data()
        media = {
            record["slug"]: {
                item["src"]
                for item in [
                    record["image"],
                    *record.get("gallery", []),
                    *(thing["image"] for thing in record.get("things_to_do", [])),
                ]
            }
            for record in records()
        }
        stills = {src for sources in data["film_stills"].values() for src in sources}
        photographs = {photo["src"] for photo in data["photographs"]}
        for slug, sources in data["film_stills"].items():
            self.assertLessEqual(set(sources), media[slug], slug)
        for photo in data["photographs"]:
            self.assertIn(photo["src"], media[photo["project"]])
        self.assertFalse(stills & photographs)

    def test_sitemap_lists_credits_with_alternates(self):
        sitemap = self.client.get("/sitemap.xml").content.decode()
        self.assertIn("<loc>http://testserver/credits/</loc>", sitemap)
        self.assertIn("<loc>http://testserver/ar/credits/</loc>", sitemap)
        self.assertIn('hreflang="ar" href="http://testserver/ar/credits/"', sitemap)


class MapTests(SimpleTestCase):
    def test_projection_round_trips(self):
        for x, y in [(468.1, 50.0), (791.0, 268.4), (1035.8, 515.5)]:
            with self.subTest(point=(x, y)):
                back = degrees_to_map(*map_to_degrees(x, y))
                self.assertAlmostEqual(back[0], x, places=6)
                self.assertAlmostEqual(back[1], y, places=6)

    def test_anchors_fall_inside_the_kingdom(self):
        anchored = {
            slug: entry["anchor"] for slug, entry in map_geometry()["projects"].items() if "anchor" in entry
        }
        self.assertEqual(len(anchored), len(SLUGS) - 1)
        for slug, anchor in anchored.items():
            with self.subTest(slug=slug):
                latitude, longitude = map_to_degrees(*anchor)
                self.assertTrue(16 <= latitude <= 33, latitude)
                self.assertTrue(34 <= longitude <= 56, longitude)
        latitude, longitude = map_to_degrees(*anchored["diriyah"])
        self.assertLess(abs(latitude - 24.73), 0.3)
        self.assertLess(abs(longitude - 46.57), 0.3)
        self.assertEqual(coordinates(anchored["diriyah"]), {"lat": "24.7", "lon": "46.6"})
        self.assertIsNone(coordinates(None))

    def test_terrain_metadata_matches_heightmap(self):
        terrain = map_geometry()["terrain"]
        for path, color_type in [
            (settings.BASE_DIR / "saudi_atlas" / "projects" / "frontend" / "assets" / "saudi-height.png", 0),
            (settings.BASE_DIR / "saudi_atlas" / "projects" / "static" / "atlas" / "media" / "atlas-relief-shade.png", 4),
        ]:
            with self.subTest(path=path.name):
                data = path.read_bytes()
                self.assertEqual(data[:8], b"\x89PNG\r\n\x1a\n")
                self.assertEqual(data[12:16], b"IHDR")
                width, height, depth, kind = struct.unpack(">IIBB", data[16:26])
                self.assertEqual(
                    (width, height, depth, kind), (terrain["columns"], terrain["rows"], 8, color_type)
                )

    def test_map_captions_skip_position_details(self):
        sentences = {
            "en": "Approximate position: 24.7° N, 46.6° E.",
            "ar": "الموقع التقريبي: ⁦24.7°⁩ شمالًا، ⁦46.6°⁩ شرقًا.",
        }
        relief = "vertically exaggerated"
        for language, sentence in sentences.items():
            with self.subTest(language=language), override(language):
                diriyah = self.client.get(reverse("project", kwargs={"slug": "diriyah"}))
                self.assertNotContains(diriyah, sentence.split(":")[0])
                self.assertNotContains(diriyah, relief)
                self.assertContains(diriyah, "atlas/media/atlas-relief-shade.png")
                home = self.client.get(reverse("home"))
                self.assertNotContains(home, relief)
                self.assertContains(home, "atlas/media/atlas-relief-shade.png")

    def test_hillshade_stays_off_first_load(self):
        for path in (reverse("home"), reverse("project", kwargs={"slug": "diriyah"})):
            with self.subTest(path=path):
                html = self.client.get(path).content.decode()
                scripted = re.sub(r"<noscript>.*?</noscript>", "", html, flags=re.S)
                self.assertRegex(
                    scripted, r'<img class="atlas-shade" data-src="[^"]*atlas-relief-shade\.png"'
                )
                self.assertNotRegex(scripted, r'\ssrc="[^"]*atlas-relief-shade\.png"')
                self.assertRegex(
                    html,
                    r'<noscript><img class="atlas-shade" src="[^"]*atlas-relief-shade\.png"[^>]*loading="lazy"',
                )


class ContentTests(SimpleTestCase):
    def test_dataset_validates(self):
        self.assertTrue(validate())

    def test_project_order_and_shape(self):
        self.assertEqual([record["slug"] for record in records()], SLUGS)
        for record in records():
            with self.subTest(slug=record["slug"]):
                self.assertGreaterEqual(len(record["highlights"]), 3)
                self.assertGreaterEqual(len(record["milestones"]), 3)
                self.assertGreaterEqual(len(record["facts"]), 3)
                self.assertTrue(record["gallery"])
                dates = [
                    date.fromisoformat(m["date"] if len(m["date"]) == 10 else f"{m['date']}-01-01")
                    for m in record["milestones"]
                ]
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
            import saudi_atlas.projects.content as content

            content.records = lambda: [record]
            with self.assertRaises(ContentError):
                content.validate(check_files=False)
        finally:
            content.records = records
            records.cache_clear()

    def test_highlight_maps_folded_matches_to_the_original_text(self):
        def marks(text, query):
            return [segment for segment, matched in highlight(text, search_terms(query)) if matched]

        self.assertEqual(marks("Hegra, UNESCO listed in 2008", "unesco"), ["UNESCO"])

        self.assertEqual(marks("الحِجر، مدرج في اليونسكو", "الحجر"), ["الحِجر"])
        self.assertEqual(marks("زار الحجرَ أمس", "الحجر"), ["الحجرَ"])

        self.assertEqual(marks("القدية", "القديه"), ["القدية"])
        self.assertEqual(marks("Café Diriyah", "cafe"), ["Café"])

        segments = highlight("Six Senses Southern Dunes", search_terms("six dunes"))
        self.assertEqual(segments, [("Six", True), (" Senses Southern ", False), ("Dunes", True)])
        self.assertEqual(marks("Red Sea Global", "red re"), ["Red"])
        self.assertEqual("".join(segment for segment, _ in segments), "Six Senses Southern Dunes")

        self.assertEqual(highlight("AlUla", []), [("AlUla", False)])
        self.assertEqual(highlight("AlUla", ["zzz"]), [("AlUla", False)])

    def test_marked_filter_escapes_every_segment(self):
        from .templatetags.atlas import marked

        html = marked('<script>alert("x")</script> unesco', search_terms("unesco <script>"))
        self.assertNotIn("<script>", html)
        self.assertIn("<mark>&lt;script&gt;</mark>", html)
        self.assertIn("<mark>unesco</mark>", html)
        self.assertEqual(marked("Fish & Chips", ["chips"]), "Fish &amp; <mark>Chips</mark>")

    def test_word_reveal_filter_escapes_and_keeps_the_text(self):
        from html import unescape

        from .templatetags.atlas import word_reveal

        html = word_reveal('<b>Fish</b> &  "Chips"')
        self.assertNotIn("<b>", html)
        self.assertIn(
            '<span class="word" style="--i: 0"><span class="word-inner">&lt;b&gt;Fish&lt;/b&gt;</span></span>',
            html,
        )
        self.assertIn('<span class="word" style="--i: 1"><span class="word-inner">&amp;</span></span>', html)
        self.assertIn('<span class="word-inner">&quot;Chips&quot;</span>', html)

        self.assertEqual(unescape(re.sub(r"<[^>]+>", "", html)), '<b>Fish</b> &  "Chips"')

        arabic = word_reveal("البحر الأحمر")
        self.assertEqual(re.findall(r'<span class="word-inner">([^<]*)</span>', arabic), ["البحر", "الأحمر"])
        self.assertEqual(
            word_reveal("العلا"),
            '<span class="word" style="--i: 0"><span class="word-inner">العلا</span></span>',
        )

    def test_hero_headlines_are_word_wrapped(self):
        for language in LANGUAGES:
            with self.subTest(language=language), override(language):
                pages = [(reverse("home"), gettext("Seven projects across Saudi Arabia"))]
                pages += [
                    (reverse("project", kwargs={"slug": record["slug"]}), record["name"][language])
                    for record in records()
                ]
                for path, title in pages:
                    html = self.client.get(path).content.decode()
                    heading = re.search(r"<h1 [^>]*>(.*?)</h1>", html, re.S).group(1)
                    self.assertEqual(heading.count('class="word"'), len(title.split(" ")))
                    self.assertEqual(re.sub(r"<[^>]+>", "", heading), title)

    def test_fold_is_unchanged_by_the_character_map(self):
        for text in ("الحِجر", "Café UNESCO", "مدينة ـالعلا", "ﻹ", "Straße"):
            with self.subTest(text=text):
                folded = unicodedata.normalize("NFKD", text.casefold())
                folded = "".join(char for char in folded if not unicodedata.combining(char)).translate(
                    ARABIC_FOLD
                )
                self.assertEqual(_fold(text), folded)

    def test_timeline_is_chronological(self):
        entries = timeline("en")
        self.assertEqual([entry["iso"] for entry in entries], sorted(entry["iso"] for entry in entries))
        self.assertEqual(len(entries), sum(len(record["milestones"]) for record in records()))
