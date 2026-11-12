import json
import re
from pathlib import Path

from PIL import Image

DATA_DIR = Path(__file__).resolve().parent / "data"
IMAGE_DIR = Path(__file__).resolve().parent / "static" / "ministries" / "images"


def read_json(filename):
    with open(DATA_DIR / filename, encoding="utf-8") as file:
        return json.load(file)


def add_images(ministry):
    slug = ministry["slug"]
    ministry_dir = IMAGE_DIR / slug
    cover = ministry_dir / "cover.jpg"
    base = f"ministries/images/{slug}"
    ministry["cover"] = f"{base}/cover.jpg" if cover.is_file() else ""
    ministry["cover_webp"] = []
    ministry["gallery"] = []

    if ministry_dir.is_dir():
        def webp_variants(pattern):
            variants = []
            seen_widths = set()
            paths = sorted(
                (
                    path
                    for path in ministry_dir.glob(pattern)
                    if path.stem.rsplit("-", 1)[-1].isdigit()
                ),
                key=lambda path: int(path.stem.rsplit("-", 1)[1]),
            )
            for path in paths:
                with Image.open(path) as image:
                    width = image.width
                if width not in seen_widths:
                    variants.append({"url": f"{base}/{path.name}", "width": width})
                    seen_widths.add(width)
            return variants

        ministry["cover_webp"] = webp_variants("cover-*.webp")
        gallery = []
        gallery_paths = sorted(
            (
                path
                for path in ministry_dir.glob("*.jpg")
                if path.stem.isdigit()
            ),
            key=lambda path: int(path.stem),
        )
        for path in gallery_paths:
            variants = webp_variants(f"{path.stem}-*.webp")
            gallery.append({"url": f"{base}/{path.name}", "webp": variants})
        ministry["gallery"] = gallery

    if cover.is_file():
        if not ministry["gallery"]:
            ministry["gallery"] = [{"url": f"{base}/cover.jpg", "webp": []}]
        return ministry

    flat_image = IMAGE_DIR / f"{slug}.jpg"
    if flat_image.is_file():
        ministry["cover"] = f"ministries/images/{slug}.jpg"
        if not ministry["gallery"]:
            ministry["gallery"] = [{"url": ministry["cover"], "webp": []}]

    return ministry


def add_timeline(ministry):
    if ministry["timeline"]:
        return ministry

    match = re.search(r"(\d{4})م", ministry["founded"])
    if match:
        ministry["timeline"] = [
            {
                "year": int(match.group(1)),
                "title": "بداية الوزارة",
                "description": ministry["history"],
            }
        ]
    return ministry


def get_ministries():
    details = read_json("details.json")
    ministries = []
    for ministry in read_json("ministries.json"):
        combined = {**ministry, **details[ministry["slug"]]}
        ministries.append(add_images(add_timeline(combined)))
    return ministries


def get_ministry(slug):
    return next(
        (ministry for ministry in get_ministries() if ministry["slug"] == slug),
        None,
    )


def get_site_content():
    return read_json("site.json")


def get_home_features():
    return read_json("home_features.json")


def get_random_facts():
    ministries = {item["slug"]: item for item in get_ministries()}
    return [
        {
            "ministry": ministries[fact["slug"]],
            "text": ministries[fact["slug"]][fact["field"]],
        }
        for fact in read_json("facts.json")
    ]


def get_quiz_questions():
    ministries = {item["slug"]: item for item in get_ministries()}
    questions = []
    for question in read_json("quiz.json"):
        questions.append(
            {
                **question,
                "choices": [
                    {"slug": slug, "name": ministries[slug]["name"]}
                    for slug in question["choices"]
                ],
            }
        )
    return questions