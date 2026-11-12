import json

from django.conf import settings


def load_json(filename):
    file_path = settings.BASE_DIR / "data" / filename

    with file_path.open("r", encoding="utf-8") as file:
        return json.load(file)
