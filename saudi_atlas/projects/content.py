import json
import re
import unicodedata
from datetime import date
from functools import cache
from pathlib import Path
from urllib.parse import quote_plus, urlencode

from django.conf import settings
from django.contrib.staticfiles import finders
from django.urls import reverse
from django.utils import dateformat
from django.utils.translation import override

DATA_DIR = Path(__file__).parent / "data"
PROJECT_DIR = DATA_DIR / "projects"
LANGUAGES = ("en", "ar")
STATUS_KEYS = {"operational", "partly-open", "phased", "planned"}
LOCALIZED = ("name", "category", "region", "tagline", "summary")
WORD_LIMITS = {"summary": 45, "tagline": 8}
HEX = re.compile(r"^#[0-9a-f]{6}$")

MAPS_QUERIES = {
    "alula": "AlUla, Saudi Arabia",
    "amaala": "AMAALA, Saudi Arabia",
    "diriyah": "Diriyah, Riyadh, Saudi Arabia",
    "neom": "NEOM, Saudi Arabia",
    "qiddiya": "Qiddiya City",
    "roshn": "ROSHN community",
    "the-red-sea": "Shura Island, Red Sea, Saudi Arabia",
}


MAPS_VIEWPORTS = {"roshn": "@23.8,45.5,6z"}

MAPS_PLACE_IDS = {"qiddiya": "ChIJD3x9qw4pLz4RTWoE6tfY3Jc"}


def maps_url(slug, language):
    query = MAPS_QUERIES.get(slug)
    if not query:
        return None
    viewport = MAPS_VIEWPORTS.get(slug)
    if viewport:
        return f"https://www.google.com/maps/search/{quote_plus(query)}/{viewport}?" + urlencode(
            {"hl": language}
        )
    params = {"api": 1, "query": query}
    if slug in MAPS_PLACE_IDS:
        params["query_place_id"] = MAPS_PLACE_IDS[slug]
    return "https://www.google.com/maps/search/?" + urlencode({**params, "hl": language})


DATE = re.compile(r"^\d{4}(-\d{2}-\d{2})?$")


class ContentError(ValueError):
    pass


@cache
def records():
    items = [json.loads(path.read_text(encoding="utf-8")) for path in PROJECT_DIR.glob("*.json")]
    return sorted(items, key=lambda item: item["order"])


@cache
def map_geometry():
    return json.loads((DATA_DIR / "atlas-map.json").read_text(encoding="utf-8"))


def map_to_degrees(x, y):
    projection = map_geometry()["projection"]
    return (
        (projection["y_origin"] - y) / projection["y_per_degree"],
        (x - projection["x_origin"]) / projection["x_per_degree"],
    )


def degrees_to_map(latitude, longitude):
    projection = map_geometry()["projection"]
    return (
        projection["x_origin"] + projection["x_per_degree"] * longitude,
        projection["y_origin"] - projection["y_per_degree"] * latitude,
    )


def coordinates(anchor):
    if not anchor:
        return None
    latitude, longitude = map_to_degrees(*anchor)
    return {"lat": f"{latitude:.1f}", "lon": f"{longitude:.1f}"}


def _localized(value, where, errors):
    if not isinstance(value, dict) or any(not str(value.get(code, "")).strip() for code in LANGUAGES):
        errors.append(f"{where}: needs non-empty en and ar text")
        return False
    return True


def _image(image, where, errors, check_files):
    for key in ("src", "width", "height", "widths", "color"):
        if key not in image:
            errors.append(f"{where}: missing {key}")
            return
    _localized(image.get("alt"), f"{where}.alt", errors)
    _localized(image.get("caption"), f"{where}.caption", errors)
    if image["width"] != max(image["widths"]):
        errors.append(f"{where}: width must equal the largest rendition")
    if check_files:
        for width in image["widths"]:
            for ext in ("avif", "webp"):
                if not finders.find(f"{image['src']}-{width}.{ext}"):
                    errors.append(f"{where}: missing {image['src']}-{width}.{ext}")


def validate(check_files=True):
    errors = []
    slugs = set()
    for record in records():
        slug = record.get("slug", "?")
        where = f"projects/{slug}"
        if slug in slugs:
            errors.append(f"{where}: duplicate slug")
        slugs.add(slug)
        for field in LOCALIZED:
            if _localized(record.get(field), f"{where}.{field}", errors) and field in WORD_LIMITS:
                for code in LANGUAGES:
                    if len(record[field][code].split()) > WORD_LIMITS[field]:
                        errors.append(f"{where}.{field}.{code}: over {WORD_LIMITS[field]} words")
        accent = record.get("accent", {})
        if not (HEX.match(accent.get("light", "")) and HEX.match(accent.get("dark", ""))):
            errors.append(f"{where}.accent: needs light and dark hex colors")
        status = record.get("status", {})
        if status.get("key") not in STATUS_KEYS:
            errors.append(f"{where}.status: unknown key")
        _localized(status.get("label"), f"{where}.status.label", errors)
        for index, fact in enumerate(record.get("facts", [])):
            _localized(fact.get("label"), f"{where}.facts[{index}].label", errors)
            _localized(fact.get("value"), f"{where}.facts[{index}].value", errors)
        for index, text in enumerate(record.get("highlights", [])):
            _localized(text, f"{where}.highlights[{index}]", errors)
        for index, detail in enumerate(record.get("details", [])):
            _localized(detail.get("title"), f"{where}.details[{index}].title", errors)
            _localized(detail.get("body"), f"{where}.details[{index}].body", errors)
        for index, milestone in enumerate(record.get("milestones", [])):
            if not DATE.match(milestone.get("date", "")):
                errors.append(f"{where}.milestones[{index}]: date must be YYYY or YYYY-MM-DD")
            _localized(milestone.get("text"), f"{where}.milestones[{index}].text", errors)
        for index, source in enumerate(record.get("sources", [])):
            if not source.get("url", "").startswith("https://"):
                errors.append(f"{where}.sources[{index}]: url must use https")
            if not DATE.match(source.get("verified", "")) or len(source["verified"]) != 10:
                errors.append(f"{where}.sources[{index}]: needs a verified date")
        if not record.get("sources"):
            errors.append(f"{where}: needs at least one source")
        for key in ("logo", "texture"):
            if check_files and record.get(key) and not finders.find(record[key]):
                errors.append(f"{where}.{key}: file not found")
        if record.get("image"):
            _image(record["image"], f"{where}.image", errors, check_files)
        for index, image in enumerate(record.get("gallery", [])):
            _image(image, f"{where}.gallery[{index}]", errors, check_files)
        for index, thing in enumerate(record.get("things_to_do", [])):
            for key in ("name", "brief", "price"):
                if key != "price" or "price" in thing:
                    _localized(thing.get(key), f"{where}.things_to_do[{index}].{key}", errors)
            if thing.get("image"):
                _image(thing["image"], f"{where}.things_to_do[{index}].image", errors, check_files)
            else:
                errors.append(f"{where}.things_to_do[{index}]: needs an image")
        video = record.get("video")
        if video:
            _localized(video.get("title"), f"{where}.video.title", errors)
            _localized(video.get("description"), f"{where}.video.description", errors)
            if check_files:
                for key in ("poster",):
                    if not finders.find(video.get(key, "")):
                        errors.append(f"{where}.video.{key}: file not found")
                for track in video.get("captions", []):
                    if not finders.find(track["src"]):
                        errors.append(f"{where}.video.captions: {track['src']} not found")
    if errors:
        raise ContentError("\n".join(errors))
    return True


def localized_image(image, language):
    if not image:
        return None
    return {**image, "alt": image["alt"][language], "caption": image["caption"][language]}


def _milestone_date(value):
    return date.fromisoformat(value) if len(value) == 10 else None


def _milestones(record, language):
    items = []
    for number, item in enumerate(record["milestones"], start=1):
        day = _milestone_date(item["date"])
        items.append(
            {
                "id": f"m-{record['slug']}-{number}",
                "iso": item["date"],
                "year": item["date"][:4],
                "date": day,
                "when": dateformat.format(day, "j F Y") if day else item["date"][:4],
                "text": item["text"][language],
            }
        )
    return items


def localize(record, language):
    slug = record["slug"]
    geometry = map_geometry()
    map_project = geometry["projects"].get(slug, {})
    anchor = map_project.get("anchor")
    locator_points = [anchor] if anchor else []
    if slug == "roshn":
        locator_points = geometry["communities"]
    project = {field: record[field][language] for field in LOCALIZED}
    project.update(
        slug=slug,
        order=record["order"],
        accent=record["accent"],
        logo=record.get("logo"),
        texture=record.get("texture"),
        status={"key": record["status"]["key"], "label": record["status"]["label"][language]},
        map_label=map_project.get("label"),
        map_anchor=anchor,
        locator_points=locator_points,
        coordinates=coordinates(anchor),
        maps_url=maps_url(slug, language),
        url=reverse("project", kwargs={"slug": slug}),
        facts=[
            {"label": fact["label"][language], "value": fact["value"][language]} for fact in record["facts"]
        ],
        highlights=[text[language] for text in record["highlights"]],
        details=[
            {"title": item["title"][language], "body": item["body"][language]} for item in record["details"]
        ],
        milestones=_milestones(record, language),
        image=localized_image(record.get("image"), language),
        gallery=[localized_image(image, language) for image in record.get("gallery", [])],
        things_to_do=[
            {key: thing[key][language] for key in ("name", "brief", "price") if key in thing}
            | {"image": localized_image(thing["image"], language)}
            for thing in record.get("things_to_do", [])
        ],
    )
    video = record.get("video")
    if video:
        project["video"] = {
            **video,
            "title": video["title"][language],
            "description": video["description"][language],
            "minutes": f"{video['duration'] // 60}:{video['duration'] % 60:02d}",
        }
    return project


def localized_projects(language):
    with override(language):
        return [localize(record, language) for record in records()]


def find_project(slug, language):
    projects = localized_projects(language)
    for index, project in enumerate(projects):
        if project["slug"] == slug:
            return project, projects[index - 1], projects[(index + 1) % len(projects)]
    return None, None, None


def timeline(language):
    entries = []
    for project in localized_projects(language):
        for milestone in project["milestones"]:
            entries.append({**milestone, "project": project})
    return sorted(entries, key=lambda entry: (entry["iso"], entry["project"]["order"]))


@cache
def totals():
    items = records()
    years = [int(milestone["date"][:4]) for record in items for milestone in record["milestones"]]
    return {
        "projects": len(items),
        "milestones": len(years),
        "photographs": sum(bool(record.get("image")) + len(record.get("gallery", [])) for record in items),
        "films": sum(1 for record in items if record.get("video")),
        "first_year": min(years),
        "last_year": max(years),
    }


def _year_position(iso):
    if len(iso) == 10:
        day = date.fromisoformat(iso)
        return day.year + (day.timetuple().tm_yday - 1) / 366
    return int(iso) + 0.5


LANE_GAP_YEARS = 2.0


def _axis():
    first, last = totals()["first_year"], totals()["last_year"] + 1
    return first, last


def axis_position(value):
    first, last = _axis()
    return f"{(value - first) / (last - first) * 100:.2f}%"


def _rows(positions):
    ends, rows = [], []
    for position in positions:
        row = next((index for index, end in enumerate(ends) if position - end >= LANE_GAP_YEARS), len(ends))
        if row == len(ends):
            ends.append(position)
        else:
            ends[row] = position
        rows.append(row)
    return rows


def milestone_lanes(language, selected=None):
    first, last = _axis()
    lanes = []
    for project in localized_projects(language):
        if selected not in (None, project["slug"]):
            continue
        positions = [_year_position(item["iso"]) for item in project["milestones"]]
        rows = _rows(positions)
        count = max(rows) + 1
        dots = []
        for item, position, row in zip(project["milestones"], positions, rows):
            centre = row + 0.5 - count / 2
            stem = "" if count == 1 or centre == 0 else ("down" if centre < 0 else "up")
            dots.append(
                {**item, "at": axis_position(position), "row": row, "stem": stem, "reach": abs(centre)}
            )
        lanes.append({"project": project, "rows": count, "dots": dots})
    return {
        "first_year": first,
        "last_year": last - 1,
        "year_span": f"{100 / (last - first):.3f}%",
        "rows": sum(lane["rows"] for lane in lanes),
        "ticks": [
            {"year": year, "at": axis_position(year)} for year in range(first, last + 1) if year % 5 == 0
        ],
        "lanes": lanes,
    }


ARABIC_FOLD = str.maketrans({"ى": "ي", "ة": "ه", "ـ": None})


def _fold_char(char):
    text = unicodedata.normalize("NFKD", char.casefold())
    return "".join(part for part in text if not unicodedata.combining(part)).translate(ARABIC_FOLD)


def _fold_with_map(text):
    pieces, owners = [], []
    for index, char in enumerate(text):
        piece = _fold_char(char)
        pieces.append(piece)
        owners.extend([index] * len(piece))
    return "".join(pieces), owners


def _fold(text):
    return _fold_with_map(text)[0]


def search_terms(query):
    return _fold(query).split()


def highlight(text, terms):
    folded, owners = _fold_with_map(text)
    spans = []
    for term in terms:
        start = folded.find(term) if term else -1
        while start != -1:
            spans.append((owners[start], owners[start + len(term) - 1] + 1))
            start = folded.find(term, start + 1)
    merged = []
    for start, end in sorted(spans):
        while end < len(text) and not _fold_char(text[end]):
            end += 1
        if merged and start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    segments, cursor = [], 0
    for start, end in merged:
        if start > cursor:
            segments.append((text[cursor:start], False))
        segments.append((text[start:end], True))
        cursor = end
    if cursor < len(text) or not segments:
        segments.append((text[cursor:], False))
    return segments


def search(query, language):
    terms = search_terms(query)
    if not terms:
        return []

    def hit(text):
        folded = _fold(text)
        return all(term in folded for term in terms)

    results = []
    for project in localized_projects(language):
        passages = (
            [("glance", f"{fact['label']}: {fact['value']}", None) for fact in project["facts"]]
            + [("story", detail["body"], detail["title"]) for detail in project["details"]]
            + [("highlights", text, None) for text in project["highlights"]]
            + [
                ("gallery", photo["caption"], None)
                for photo in [project["image"], *project["gallery"]]
                if photo
            ]
            + [("milestones", item["text"], item["year"]) for item in project["milestones"]]
        )
        matches = [
            {"kind": kind, "text": text, "title": title}
            for kind, text, title in passages
            if hit(f"{title or ''} {text}")
        ]
        named = hit(project["name"])
        headline = named or hit(" ".join(project[field] for field in LOCALIZED))
        if headline or matches:
            results.append(
                {"project": project, "matches": matches, "rank": (not named, not headline, -len(matches))}
            )
    return sorted(results, key=lambda result: (result["rank"], result["project"]["order"]))


def debug_validate():
    if settings.DEBUG:
        validate()
