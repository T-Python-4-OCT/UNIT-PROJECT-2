import json
from datetime import date
from functools import cache
from pathlib import Path

from django.urls import reverse


DATA_FILE = Path(__file__).parent / "data" / "projects.json"


@cache
def records():
    return json.loads(DATA_FILE.read_text(encoding="utf-8-sig"))


@cache
def map_projects():
    return json.loads(DATA_FILE.with_name("atlas-map.json").read_text(encoding="utf-8"))["projects"]


def localized_projects(language):
    return [localize(record, language) for record in records()]


@cache
def feature_records():
    return json.loads(DATA_FILE.with_name("project-features.json").read_text(encoding="utf-8"))


def localized_features(project, language):
    features = feature_records().get(project["slug"])
    if not features:
        return {}
    gallery = [localized_image(image, language) for image in features["gallery"]]
    video = features.get("video")
    if video:
        video = {
            **video,
            "title": video["title"][language],
            "description": video["description"][language],
        }
    return {
        "details": [
            {"title": detail["title"][language], "body": detail["body"][language]}
            for detail in features["details"]
        ],
        "gallery": gallery,
        "video": video,
    }


def localized_image(image, language):
    return {
        **image,
        "alt": image["alt"][language],
        "caption": image.get("caption", {}).get(language),
        "edit_note": image.get("edit_note", {}).get(language),
    }


def localize(record, language):
    project = {
        field: record[field][language] for field in ("name", "category", "region", "summary")
    }
    project["slug"] = record["slug"]
    project["map_label"] = map_projects().get(record["slug"], {}).get("label")
    project["url"] = reverse("project", kwargs={"slug": record["slug"]})
    project["highlights"] = [highlight[language] for highlight in record["highlights"]]
    project["milestones"] = [
        {
            "iso": milestone["date"],
            "date": date.fromisoformat(milestone["date"]) if len(milestone["date"]) > 4 else None,
            "text": milestone["text"][language],
        }
        for milestone in record["milestones"]
    ]
    image = record.get("image")
    project["image"] = localized_image(image, language) if image else None
    return project
