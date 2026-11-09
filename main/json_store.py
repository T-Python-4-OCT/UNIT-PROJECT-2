"""Save and load lists of records in JSON files (our 'database' for Unit 2)."""

import json
from datetime import datetime

from django.conf import settings


def _file_path(name: str):
    return settings.DATA_DIR / f"{name}.json"


def load(name: str) -> list[dict]:
    """Load all records of a file, e.g. load('reports'). Returns [] if the file is missing or broken."""
    path = _file_path(name)
    try:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []
    return data if isinstance(data, list) else []


def save(name: str, records: list[dict]) -> None:
    settings.DATA_DIR.mkdir(exist_ok=True)
    with open(_file_path(name), "w", encoding="utf-8") as file:
        json.dump(records, file, ensure_ascii=False, indent=2)


def add(name: str, record: dict) -> dict:
    """Add a new record with an id and a date, save it, and return it."""
    records = load(name)
    record["id"] = max((item["id"] for item in records), default=0) + 1
    record["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    records.append(record)
    save(name, records)
    return record


def get(name: str, record_id: int) -> dict | None:
    for record in load(name):
        if record["id"] == record_id:
            return record
    return None


def newest_first(records: list[dict]) -> list[dict]:
    return sorted(records, key=lambda record: record["id"], reverse=True)
