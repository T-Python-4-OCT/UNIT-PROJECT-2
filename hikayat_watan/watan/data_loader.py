"""
قراءة المحتوى من ملف JSON بدلاً من قاعدة البيانات.

يُعاد تحميل الملف تلقائياً إذا تغيّر وقت تعديله، فيمكنك تعديل
content.json أثناء تشغيل الخادم ورؤية النتيجة بتحديث الصفحة.
"""
import json
import threading

from django.conf import settings

_lock = threading.Lock()
_cache = {"mtime": None, "data": None}


def _prepare(data):
    """يضيف حقولاً مساعدة (ترتيب، روابط تضمين، فهارس) فوق بيانات JSON."""
    eras = data["eras"]
    cities = data["cities"]

    for i, era in enumerate(eras):
        era["order"] = i + 1

    for i, city in enumerate(cities):
        city["order"] = i + 1
        video = city.get("video") or {}
        yt = (video.get("youtube_id") or "").strip()
        video["embed_url"] = f"https://www.youtube-nocookie.com/embed/{yt}?rel=0" if yt else ""
        city["video"] = video

    data["_eras_by_slug"] = {e["slug"].lower(): e for e in eras}
    data["_cities_by_slug"] = {c["slug"].lower(): c for c in cities}

    regions = {}
    for c in cities:
        regions.setdefault(c["region_key"], c["region"])
    data["regions"] = [{"key": k, "label": v} for k, v in regions.items()]
    return data


def load_content():
    path = settings.CONTENT_FILE
    mtime = path.stat().st_mtime
    with _lock:
        if _cache["data"] is None or _cache["mtime"] != mtime:
            with path.open(encoding="utf-8") as fh:
                _cache["data"] = _prepare(json.load(fh))
            _cache["mtime"] = mtime
        return _cache["data"]


def get_site():
    return load_content()["site"]


def get_eras():
    return load_content()["eras"]


def get_cities():
    return load_content()["cities"]


def get_era(slug):
    return load_content()["_eras_by_slug"].get((slug or "").lower())


def get_city(slug):
    return load_content()["_cities_by_slug"].get((slug or "").lower())


def neighbours(items, current):
    """يرجع (السابق، التالي) لعنصر داخل قائمة مرتبة، أو None عند الأطراف."""
    idx = next((i for i, it in enumerate(items) if it["slug"] == current["slug"]), None)
    if idx is None:
        return None, None
    prev_item = items[idx - 1] if idx > 0 else None
    next_item = items[idx + 1] if idx < len(items) - 1 else None
    return prev_item, next_item
