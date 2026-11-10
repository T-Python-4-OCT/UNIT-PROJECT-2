import json
import re
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent / "data"
IMAGE_DIR = Path(__file__).resolve().parent / "static" / "ministries" / "images"


def read_json(filename):
    with open(DATA_DIR / filename, encoding="utf-8") as file:
        return json.load(file)


def add_images(ministry):
    slug = ministry["slug"]
    ministry_dir = IMAGE_DIR / slug
    cover = ministry_dir / "cover.jpg"

    if cover.is_file():
        base = f"ministries/images/{slug}"
        gallery = [
            f"{base}/{number}.jpg"
            for number in range(1, 4)
            if (ministry_dir / f"{number}.jpg").is_file()
        ]
        ministry["cover"] = f"{base}/cover.jpg"
        ministry["gallery"] = gallery or [ministry["cover"]]
        return ministry

    flat_image = IMAGE_DIR / f"{slug}.jpg"
    if flat_image.is_file():
        ministry["cover"] = f"ministries/images/{slug}.jpg"
        ministry["gallery"] = [ministry["cover"]]
    else:
        ministry["cover"] = ""
        ministry["gallery"] = []

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


def get_all_ministries():
    ministries = []
    for ministry in get_ministries():
        ministries.append(
            {
                **ministry,
                "summary": ministry["tagline"],
                "detail_slug": ministry["slug"],
            }
        )
    ministries.extend(read_json("additional_ministries.json"))
    return ministries


def get_ministry(slug):
    return next(
        (ministry for ministry in get_ministries() if ministry["slug"] == slug),
        None,
    )


def get_site_content():
    return read_json("site.json")


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