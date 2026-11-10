"""
Site content (no database needed).
Images are relative to the static folder.
"""

# The official dates of the tournament are not announced yet,
# so the countdown counts down to the start of the year 2034.
COUNTDOWN_TARGET = "2034-01-01T00:00:00+03:00"

STATS = [
    {"value": 5, "label": "مدن مستضيفة", "icon": "bi-geo-alt"},
    {"value": 15, "label": "ملعباً", "icon": "bi-building"},
    {"value": 48, "label": "منتخباً", "icon": "bi-flag"},
    {"value": 104, "label": "مباراة", "icon": "bi-trophy"},
]


CITIES = [
    {
        "slug": "riyadh",
        "name": "الرياض",
        "name_en": "Riyadh",
        "tagline": "العاصمة التي تحتضن الافتتاح",
        "image": "main/images/riyadh-kingdom-centre.jpg",
        "stadiums_count": 8,
    },
    {
        "slug": "jeddah",
        "name": "جدة",
        "name_en": "Jeddah",
        "tagline": "عروس البحر الأحمر",
        "image": "main/images/jeddah-corniche.jpg",
        "stadiums_count": 4,
    },
    {
        "slug": "alkhobar",
        "name": "الخبر",
        "name_en": "Al Khobar",
        "tagline": "بوابة الشرقية على الخليج",
        "image": "main/images/khobar-tower-sunset.jpg",
        "stadiums_count": 1,
    },
    {
        "slug": "abha",
        "name": "أبها",
        "name_en": "Abha",
        "tagline": "كرة القدم فوق السحاب",
        "image": "main/images/abha-clouds.jpg",
        "stadiums_count": 1,
    },
    {
        "slug": "neom",
        "name": "نيوم",
        "name_en": "NEOM",
        "tagline": "ملعب من المستقبل",
        "image": "main/images/neom-stadium.jpg",
        "stadiums_count": 1,
    },
]

# Links to the other sections, shown on the home page
EXPLORE = [
    {"url_name": "main:stadiums", "title": "الملاعب", "text": "تعرّف على الملاعب الخمسة عشر التي ستحتضن المباريات.", "image": "main/images/card-stadium-jawhara.jpg", "icon": "bi-building"},
    {"url_name": "main:history", "title": "الأخضر في المونديال", "text": "مشاركات المنتخب السعودي في كأس العالم منذ 1994.", "image": "main/images/card-green-worldcup.jpg", "icon": "bi-star"},
    {"url_name": "main:journey", "title": "رحلة الاستضافة", "text": "من تقديم الملف إلى إعلان المملكة دولةً مستضيفة.", "image": "main/images/card-journey-flag.jpg", "icon": "bi-signpost-split"},
]

def get_city(slug):
    return next((c for c in CITIES if c["slug"] == slug), None)
