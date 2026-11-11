"""
طبقة المحتوى — بديل قاعدة البيانات.

تقرأ ملفات JSON من main/data/ وتجهّز سياق كل صفحة.
بايثون خالص (لا تستورد Django) حتى يمكن اختبارها وتشغيلها مستقلة.

نظام الوسائط:
كل صورة/فيديو له مُعرّف في data/media.json ومسار متوقَّع داخل static/.
إذا وُضع الملف الأصلي في مساره يظهر تلقائياً، وإلا يُعرض رسم توضيحي
مع شارة واضحة «رسم توضيحي — الصورة الأصلية مطلوبة». لا تُعرض أي صورة
مولّدة على أنها صورة حقيقية لشخصية أو حدث.
"""
import json
from functools import lru_cache
from pathlib import Path
from urllib.parse import quote

APP_DIR = Path(__file__).resolve().parent
DATA_DIR = APP_DIR / "data"
STATIC_DIR = APP_DIR / "static"

# رابط مباشر لنسخة مصغّرة من ملف على ويكيميديا كومنز (يُستخدم حتى يُنزَّل الملف محلياً)
COMMONS_FILEPATH = "https://commons.wikimedia.org/wiki/Special:FilePath/%s?width=%d"


# ---------------------------------------------------------------- loaders
@lru_cache(maxsize=None)
def load(name):
    """يحمّل ملف JSON من مجلد البيانات (مع تخزين مؤقت)."""
    with open(DATA_DIR / f"{name}.json", encoding="utf-8") as fh:
        return json.load(fh)


def media(media_id):
    """يُرجع وصف وسيط مع حالة توفّر الملف الأصلي. لا يُخزَّن مؤقتاً كي تظهر الصور فور إضافتها."""
    if not media_id:
        return None
    entry = load("media")["items"].get(media_id)
    if entry is None:
        return None
    item = dict(entry)
    item["id"] = media_id
    path = entry.get("path")
    item["available"] = bool(path) and (STATIC_DIR / path).is_file()
    item["art_path"] = "main/img/art/%s.svg" % entry.get("art", "fort")
    item.setdefault("ratio", "wide")
    # ثلاث حالات للعرض: ملف محلي ← صورة من ويكيميديا كومنز ← رسم توضيحي
    commons = entry.get("commons")
    if commons:
        name = commons.replace(" ", "_")
        item["remote_url"] = COMMONS_FILEPATH % (quote(name), 1280)
        item["source_page"] = "https://commons.wikimedia.org/wiki/File:" + quote(name)
    remote = entry.get("remote")
    if remote and not commons:
        item["remote_url"] = remote["url"]
        item["source_page"] = remote.get("page", "")
    if item["available"]:
        item["mode"] = "local"
    elif commons or remote:
        item["mode"] = "remote"
    else:
        item["mode"] = "art"
    return item


def sources(ids):
    """يُرجع قائمة المصادر المطلوبة بالترتيب، مع ترقيم ثابت من sources.json."""
    all_items = load("sources")["items"]
    out = []
    for sid in ids or []:
        if sid in all_items:
            item = dict(all_items[sid])
            item["id"] = sid
            out.append(item)
    return out


def _page(slug):
    """بيانات رأس الصفحة (العنوان والوصف) من site.json."""
    page = dict(load("site")["pages"][slug])
    page["hero"] = media(page.get("hero"))
    page["slug"] = slug
    return page


def _with_media(items, key="media"):
    """يضيف الوسيط المحلول لكل عنصر في قائمة (نسخ لا تعدّل البيانات الأصلية)."""
    out = []
    for item in items:
        item = dict(item)
        item["m"] = media(item.get(key))
        out.append(item)
    return out


def _gates(gates):
    """يضيف اسماً مختصراً وموضع تسمية خارج السور لكل بوابة في الخريطة."""
    out = []
    for g in gates:
        g = dict(g)
        g["short"] = g["name"].replace("بوابة ", "")
        dx, dy = g["x"] - 300, g["y"] - 300
        dist = (dx * dx + dy * dy) ** 0.5 or 1
        g["lx"] = round(g["x"] + dx / dist * 40)
        g["ly"] = round(g["y"] + dy / dist * 30 + 5)
        out.append(g)
    return out


# ---------------------------------------------------------------- people helpers
def _people():
    return load("people")


PEOPLE_PHOTO = "main/media/people/%s.jpg"


def _person_photo(p):
    """صورة المشارك تُلتقط تلقائياً إن وُضعت في main/static/main/media/people/<slug>.jpg"""
    path = PEOPLE_PHOTO % p["slug"]
    if not (STATIC_DIR / path).is_file():
        return None
    return {
        "id": "person-" + p["slug"], "kind": "image", "mode": "local", "available": True,
        "path": path, "alt": "صورة أرشيفية: " + p["name"], "ratio": "portrait",
        "caption": p.get("photo_caption", p["name"]), "credit": p.get("photo_credit", ""),
        "license": "", "art_path": "main/img/art/portrait-frame.svg",
    }


def _featured():
    data = _people()
    groups = {g["id"]: g for g in data["groups"]}
    out = []
    for p in data["featured"]:
        p = dict(p)
        p["group_info"] = groups.get(p.get("group"))
        p["initial"] = p["name"].strip()[0]
        p["m"] = media(p.get("media")) or _person_photo(p)
        out.append(p)
    return out


def _roster():
    out = []
    featured_by_name = {p.get("roster_name", p["name"]): p["slug"] for p in _people()["featured"]}
    for i, r in enumerate(_people()["roster"], start=1):
        r = dict(r)
        r["n"] = i
        r["initial"] = r["name"].strip()[0]
        r["slug"] = featured_by_name.get(r["name"])
        out.append(r)
    return out


# ---------------------------------------------------------------- page contexts
def home_context():
    site = load("site")
    story = load("story")
    featured = _featured()
    return {
        "active": "home",
        "page": _page("home"),
        "hero": media("hero_masmak"),
        "stats": site["stats"],
        "journey": site["journey"],
        "night": story["night_scenes"],
        "featured_people": featured[:4],
        "principles": site["principles"],
    }


def old_riyadh_context():
    data = load("old_riyadh")
    return {
        "active": "old_riyadh",
        "page": _page("old_riyadh"),
        "data": data,
        "wall_history": data["wall_history"],
        "gates": _gates(data["gates"]),
        "landmarks": _with_media(data["landmarks"]),
        "architecture": data["architecture"],
        "compare_old": media("riyadh_old"),
        "compare_new": media("riyadh_today"),
        "gates_json": data["gates"],
        "sources": sources(data["sources"]),
    }


def king_context():
    data = load("king")
    return {
        "active": "king",
        "page": _page("king"),
        "data": data,
        "portrait": media("king_portrait"),
        "facts": data["facts"],
        "life": data["life"],
        "sections": data["sections"],
        "notes": data["notes"],
        "sources": sources(data["sources"]),
    }


def participants_context():
    data = _people()
    featured = _featured()
    roster = _roster()
    origins = sorted({r["origin"] for r in roster if r.get("origin")})
    return {
        "active": "participants",
        "page": _page("participants"),
        "intro": data["intro"],
        "groups": data["groups"],
        "king_photo": media("king_portrait"),
        "featured": featured,
        "roster": roster,
        "origins": origins,
        "roster_count": len(roster),
        "people_json": [
            {
                "slug": p["slug"],
                "name": p["name"],
                "role": p["role"],
                "years": p.get("years", ""),
                "group": p["group_info"]["title"] if p.get("group_info") else "",
                "summary": p["summary"],
                "initial": p["initial"],
            }
            for p in featured
        ],
        "sources": sources(data["sources"]),
    }


def person_context(slug):
    featured = _featured()
    index = next((i for i, p in enumerate(featured) if p["slug"] == slug), None)
    if index is None:
        raise KeyError(slug)
    person = featured[index]
    prev_p = featured[index - 1] if index > 0 else None
    next_p = featured[index + 1] if index + 1 < len(featured) else None
    page = _page("participants")
    page = dict(page, title=person["name"], description=person["summary"])
    return {
        "active": "participants",
        "page": page,
        "person": person,
        "prev_person": prev_p,
        "next_person": next_p,
        "others": [p for p in featured if p["slug"] != slug][:3],
        "sources": sources(person.get("sources", [])),
    }


def story_context():
    data = load("story")
    chapters = _with_media(data["chapters"])
    return {
        "active": "story",
        "page": _page("story"),
        "intro": data["intro"],
        "chapters": chapters,
        "route": data["route"],
        "versions": data["versions"],
        "historic_map": media("route_map"),
        "film": media("video_story"),
        "story_json": {
            "chapters": [
                {"slug": c["slug"], "title": c["title"], "date": c["date"], "place": c["place"], "point": c.get("point")}
                for c in data["chapters"]
            ],
            "route": data["route"],
        },
        "sources": sources(data["sources"]),
    }


def chapter_context(slug):
    data = load("story")
    chapters = _with_media(data["chapters"])
    index = next((i for i, c in enumerate(chapters) if c["slug"] == slug), None)
    if index is None:
        raise KeyError(slug)
    chapter = chapters[index]
    page = dict(_page("story"), title=chapter["title"], description=chapter["summary"])
    return {
        "active": "story",
        "page": page,
        "chapter": chapter,
        "number": index + 1,
        "total": len(chapters),
        "prev_chapter": chapters[index - 1] if index > 0 else None,
        "next_chapter": chapters[index + 1] if index + 1 < len(chapters) else None,
        "chapters": chapters,
        "sources": sources(chapter.get("sources", data["sources"])),
    }


def tour_context():
    data = load("tour")
    stops = _with_media(data["stops"])
    return {
        "active": "tour",
        "page": _page("tour"),
        "data": data,
        "stops": stops,
        "facts": data["facts"],
        "panorama": media("masmak_panorama"),
        "gallery": [media(mid) for mid in ("masmak_gate", "hero_masmak", "masmak_view_6", "masmak_view_4", "masmak_view_7", "masmak_tower",
                                        "masmak_view_8", "masmak_view_9", "masmak_view_2", "masmak_view_3")],
        "gate_media": media("masmak_gate"),
        "tour_json": [
            {
                "id": s["id"],
                "title": s["title"],
                "kicker": s["kicker"],
                "text": s["text"],
                "note": s.get("note", ""),
                "x": s["x"],
                "y": s["y"],
            }
            for s in data["stops"]
        ],
        "sources": sources(data["sources"]),
    }


def _pct(value):
    """نسبة مئوية كنص بنقطة عشرية دائماً: Django مع اللغة العربية يطبع الأعداد العشرية بفاصلة
    (45,2) فتصبح قيمة CSS غير صالحة وتتكدس النقاط في بداية الشريط."""
    return "%.2f" % value


def _segments(lo, hi):
    """أشرطة الحقب على المقياس الزمني (نسب مئوية من بدايته)."""
    bounds = [("roots", "الجذور", lo, 1891), ("recovery", "الاسترداد", 1891, 1902),
              ("unification", "التوحيد", 1902, 1932), ("memory", "الذاكرة", 1932, hi)]
    out = []
    for era, title, a, b in bounds:
        start = (a - lo) / (hi - lo) * 100
        out.append({"era": era, "title": title, "start": _pct(start),
                    "width": _pct((b - a) / (hi - lo) * 100), "range": f"{a}–{b}م"})
    return out


def timeline_context():
    data = load("timeline")
    years = [e["year"] for e in data["events"]]
    lo, hi = min(years), max(years)
    events = []
    for e in data["events"]:
        e = dict(e)
        e["pos"] = _pct((e["year"] - lo) / (hi - lo) * 100)
        events.append(e)
    span_start = (1902 - lo) / (hi - lo) * 100
    span_end = (1932 - lo) / (hi - lo) * 100
    return {
        "active": "timeline",
        "page": _page("timeline"),
        "eras": data["eras"],
        "events": events,
        "scale": {"from": lo, "to": hi, "span_start": _pct(span_start), "span_width": _pct(span_end - span_start),
                  "segments": _segments(lo, hi)},
        "results": data["results"],
        "sources": sources(data["sources"]),
    }


def museum_context():
    data = load("museum")
    all_media = load("media")["items"]
    media_status = [media(mid) for mid in all_media]
    missing = sum(1 for m in media_status if m["mode"] == "art")
    remote = sum(1 for m in media_status if m["mode"] == "remote")
    videos = []
    for v in data["videos"]:
        v = dict(v)
        v["m"] = media(v.get("media"))
        videos.append(v)
    all_sources = load("sources")["items"]
    return {
        "active": "museum",
        "page": _page("museum"),
        "data": data,
        "halls": data["halls"],
        "visit": data["visit"],
        "videos": videos,
        "method": data["method"],
        "media_status": media_status,
        "media_missing": missing,
        "media_remote": remote,
        "media_ok": len(media_status) - missing,
        "media_total": len(media_status),
        "media_pct": round((len(media_status) - missing) * 100 / max(1, len(media_status))),
        "all_sources": sources(list(all_sources.keys())),
        "archives": data["archives"],
    }


def quiz_context():
    data = load("quiz")
    return {
        "active": "quiz",
        "page": _page("quiz"),
        "intro": data["intro"],
        "quiz_json": data["questions"],
        "question_count": len(data["questions"]),
    }
