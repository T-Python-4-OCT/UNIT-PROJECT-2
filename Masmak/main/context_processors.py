"""سياق عام متاح في كل القوالب: بيانات الموقع وقائمة التنقل."""
from . import content


def site(request):
    data = content.load("site")
    return {
        "site": data["site"],
        "nav_items": data["nav"],
    }
