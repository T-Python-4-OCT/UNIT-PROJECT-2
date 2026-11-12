
import json
from functools import lru_cache
from pathlib import Path

from django.http import Http404
from django.shortcuts import render


DATA_DIR = Path(__file__).resolve().parent / "data"


# ==========================================
# تحميل البيانات التاريخية
# ==========================================

@lru_cache(maxsize=1)
def load_states():
    with (DATA_DIR / "states.json").open(
        "r", encoding="utf-8"
    ) as file:
        return json.load(file)


@lru_cache(maxsize=1)
def load_rulers():
    with (DATA_DIR / "rulers.json").open(
        "r", encoding="utf-8"
    ) as file:
        return json.load(file)


@lru_cache(maxsize=1)
def load_third_events():
    with (DATA_DIR / "third_events.json").open(
        "r", encoding="utf-8"
    ) as file:
        return json.load(file)


# ==========================================
# أدوات مساعدة للحكام
# ==========================================

def ruler_slug(ruler):
    return Path(ruler.get("image") or "").stem


def first_text(data, *keys):
    for key in keys:
        value = data.get(key)

        if isinstance(value, str) and value.strip():
            return value.strip()

    return ""


def normalize_highlights(ruler):
    """
    يدعم قائمة إنجازات نصية أو قائمة كائنات.
    لا يضيف معلومات تاريخية من عنده.
    """

    values = None

    for key in ("highlights", "achievements", "contributions"):
        if isinstance(ruler.get(key), list):
            values = ruler[key]
            break

    if values is None:
        return []

    result = []

    for item in values:
        if isinstance(item, str) and item.strip():
            result.append({
                "title": item.strip(),
                "description": "",
            })

        elif isinstance(item, dict):
            title = first_text(
                item, "title", "name", "label"
            )

            description = first_text(
                item, "description", "text", "details"
            )

            if title or description:
                result.append({
                    "title": title,
                    "description": description,
                })

    return result


def normalize_events(ruler):
    """
    توحيد شكل الأحداث الزمنية إن كانت موجودة.
    """

    values = None

    for key in ("timeline", "events", "milestones"):
        if isinstance(ruler.get(key), list):
            values = ruler[key]
            break

    if values is None:
        return []

    result = []

    for item in values:
        if isinstance(item, str) and item.strip():
            result.append({
                "year": "",
                "title": item.strip(),
                "description": "",
            })

        elif isinstance(item, dict):
            year = item.get("year") or item.get("date") or ""

            title = first_text(
                item, "title", "event", "label", "name"
            )

            description = first_text(
                item, "description", "details", "text"
            )

            if title or description:
                result.append({
                    "year": str(year),
                    "title": title,
                    "description": description,
                })

    return result


def normalize_sources(ruler):
    values = ruler.get("sources")

    if not isinstance(values, list):
        return []

    result = []

    for item in values:
        if not isinstance(item, dict):
            continue

        title = first_text(item, "title", "name")
        url = first_text(item, "url", "link")

        if url.startswith(("https://", "http://")):
            result.append({
                "title": title or "مصدر تاريخي",
                "url": url,
            })

    return result


# ==========================================
# الصفحة الرئيسية
# ==========================================

def home(request):
    return render(request, "history/home.html")

# About page
def about(request):
    return render(request, "history/about.html")
# ==========================================
# صفحات الدول الثلاث
# ==========================================

def state_detail(request, era):
    states = load_states()
    state = states.get(era)

    if state is None:
        raise Http404("الدولة المطلوبة غير موجودة")

    state_keys = list(states.keys())
    current_index = state_keys.index(era)

    previous_state = None
    next_state = None

    if current_index > 0:
        previous_slug = state_keys[current_index - 1]

        previous_state = {
            "slug": previous_slug,
            "title": states[previous_slug]["title"],
        }

    if current_index < len(state_keys) - 1:
        next_slug = state_keys[current_index + 1]

        next_state = {
            "slug": next_slug,
            "title": states[next_slug]["title"],
        }

    rulers = [
        {
            **ruler,
            "slug": ruler_slug(ruler),
        }
        for ruler in state.get("rulers", [])
    ]

    templates = {
        "first": "history/states/first.html",
        "second": "history/states/second.html",
        "third": "history/states/third.html",
    }

    template_name = templates.get(
        era, "history/state_detail.html"
    )

    context = {
        "state": state,
        "era": era,
        "rulers": rulers,
        "previous_state": previous_state,
        "next_state": next_state,
    }

    if era == "third":
        context["third_events"] = load_third_events()

    return render(request, template_name, context)


# ==========================================
# صفحة السيرة الذاتية للحاكم
# ==========================================

def ruler_detail(request, slug):
    rulers_data = load_rulers()
    states = load_states()

    ruler_data = rulers_data.get(slug)

    if not isinstance(ruler_data, dict):
        raise Http404("الحاكم المطلوب غير موجود")

    era = None
    state = None
    state_rulers = []
    ruler_index = None
    state_ruler_data = None

    # تحديد الدولة وترتيب الحاكم داخلها
    for state_key, state_info in states.items():
        items = state_info.get("rulers", [])

        for index, item in enumerate(items):
            if ruler_slug(item) == slug:
                era = state_key
                state = state_info
                state_rulers = items
                ruler_index = index
                state_ruler_data = item
                break

        if era is not None:
            break

    if era is None:
        raise Http404("الحاكم غير مرتبط بدولة موجودة")

    # دمج البيانات المختصرة والتفصيلية
    ruler = {
        **state_ruler_data,
        **ruler_data,
    }

    ruler["name"] = (
        ruler.get("name")
        or state_ruler_data.get("name", "")
    )

    ruler["image"] = (
        ruler.get("image")
        or state_ruler_data.get("image", "")
    )

    ruler["period"] = (
        ruler.get("period")
        or state_ruler_data.get("period", "")
    )

    story = first_text(
        ruler,
        "biography",
        "story",
        "bio",
        "overview",
        "description",
    )

    introduction = first_text(
        ruler, "introduction", "summary", "overview", "description"
    )

    legacy = first_text(
        ruler, "legacy", "impact", "historical_impact"
    )

    title = first_text(
        ruler, "title", "role", "subtitle", "nickname"
    )

    highlights = normalize_highlights(ruler)
    events = normalize_events(ruler)
    sources = normalize_sources(ruler)

    # الفصول السردية المخصصة لكل حاكم عند توفرها
    storyline = ruler.get("storyline", {})
    if not isinstance(storyline, dict):
        storyline = {}

    story_chapters = storyline.get("chapters", [])
    if not isinstance(story_chapters, list):
        story_chapters = []

    if storyline.get("timeline"):
        events = normalize_events({"timeline": storyline["timeline"]})

    facts = ruler.get("facts", {})
    if not isinstance(facts, dict):
        facts = {}
    fact_items = [
        {"label": key, "value": value}
        for key, value in facts.items()
        if value
    ]

    # تحديد الطابع البصري للصفحة
    is_founder = ruler_index == 0

    if era == "first":
        chapter_title = "الدولة السعودية الأولى"
        chapter_label = "الفصل الأول"
        ruler_kind = "الإمام"

    elif era == "second":
        chapter_title = "الدولة السعودية الثانية"
        chapter_label = "الفصل الثاني"
        ruler_kind = "الإمام"

    else:
        chapter_title = "الدولة السعودية الثالثة"
        chapter_label = "الفصل الثالث"
        ruler_kind = "الملك"

    if era == "third" and is_founder:
        hero_label = "مؤسس المملكة العربية السعودية"
    elif era == "first" and is_founder:
        hero_label = "مؤسس الدولة السعودية الأولى"
    elif era == "second" and is_founder:
        hero_label = "مؤسس الدولة السعودية الثانية"
    elif era == "third":
        hero_label = "من ملوك المملكة العربية السعودية"
    else:
        hero_label = "من أئمة الدولة السعودية"

    previous_ruler = None
    next_ruler = None

    if ruler_index > 0:
        item = state_rulers[ruler_index - 1]

        previous_ruler = {
            "name": item.get("name", ""),
            "slug": ruler_slug(item),
        }

    if ruler_index < len(state_rulers) - 1:
        item = state_rulers[ruler_index + 1]

        next_ruler = {
            "name": item.get("name", ""),
            "slug": ruler_slug(item),
        }

    context = {
        "ruler": ruler,
        "era": era,
        "state_title": state.get("title", chapter_title),
        "chapter_title": chapter_title,
        "chapter_label": chapter_label,
        "ruler_kind": ruler_kind,
        "hero_label": hero_label,
        "ruler_title": title,
        "introduction": introduction,
        "story": story,
        "storyline": storyline,
        "story_chapters": story_chapters,
        "fact_items": fact_items,
        "legacy": legacy,
        "highlights": highlights,
        "events": events,
        "sources": sources,
        "is_founder": is_founder,
        "previous_ruler": previous_ruler,
        "next_ruler": next_ruler,
        "ruler_number": ruler_index + 1,
        "ruler_count": len(state_rulers),
    }

    return render(
        request,
        "history/ruler_detail.html",
        context,
    )
