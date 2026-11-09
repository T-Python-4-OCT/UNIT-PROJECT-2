import json
import re
from datetime import date
from functools import cache
from pathlib import Path

from django.conf import settings
from django.contrib.staticfiles import finders
from django.urls import reverse
from django.utils.translation import override

DATA_DIR = Path(__file__).parent / "data"
PROJECT_DIR = DATA_DIR / "projects"
LANGUAGES = ("en", "ar")
STATUS_KEYS = {"operational", "partly-open", "phased", "planned"}
LOCALIZED = ("name", "category", "region", "tagline", "summary")
WORD_LIMITS = {"summary": 45, "tagline": 8}
HEX = re.compile(r"^#[0-9a-f]{6}$")
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
        if record.get("image"):
            _image(record["image"], f"{where}.image", errors, check_files)
        for index, image in enumerate(record.get("gallery", [])):
            _image(image, f"{where}.gallery[{index}]", errors, check_files)
        video = record.get("video")
        if video:
            _localized(video.get("title"), f"{where}.video.title", errors)
            _localized(video.get("description"), f"{where}.video.description", errors)
            if check_files:
                for key in ("path", "poster"):
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


def localize(record, language):
    project = {field: record[field][language] for field in LOCALIZED}
    project.update(
        slug=record["slug"],
        order=record["order"],
        accent=record["accent"],
        status={"key": record["status"]["key"], "label": record["status"]["label"][language]},
        map_label=map_geometry()["projects"].get(record["slug"], {}).get("label"),
        url=reverse("project", kwargs={"slug": record["slug"]}),
        facts=[{"label": fact["label"][language], "value": fact["value"][language]} for fact in record["facts"]],
        highlights=[text[language] for text in record["highlights"]],
        details=[{"title": item["title"][language], "body": item["body"][language]} for item in record["details"]],
        milestones=[
            {"iso": item["date"], "year": item["date"][:4], "date": _milestone_date(item["date"]), "text": item["text"][language]}
            for item in record["milestones"]
        ],
        image=localized_image(record.get("image"), language),
        gallery=[localized_image(image, language) for image in record.get("gallery", [])],
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


def debug_validate():
    if settings.DEBUG:
        validate()
