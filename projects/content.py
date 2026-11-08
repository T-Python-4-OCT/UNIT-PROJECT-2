import json
from datetime import date
from functools import cache
from pathlib import Path

from django.urls import reverse


DATA_FILE = Path(__file__).parent / "data" / "projects.json"


@cache
def records():
    return json.loads(DATA_FILE.read_text(encoding="utf-8-sig"))


def localized_projects(language):
    return [localize(record, language, index) for index, record in enumerate(records(), 1)]


def localize(record, language, index):
    project = {
        field: record[field][language] for field in ("name", "category", "region", "summary")
    }
    project["slug"] = record["slug"]
    project["index"] = f"{index:02d}"
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
    project["sources"] = [
        {
            "label": source["label"][language],
            "url": source["url"],
            "verified": date.fromisoformat(source["verified"]),
        }
        for source in record["sources"]
    ]
    image = record.get("image")
    if image:
        project["image"] = {
            **image,
            "alt": image["alt"][language],
            "caption": image.get("caption", {}).get(language),
        }
    else:
        project["image"] = None
    return project
