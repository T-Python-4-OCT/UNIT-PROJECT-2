"""
Content for the page "الأخضر في المونديال" (Saudi national team at the World Cup).
result: W = فوز, D = تعادل, L = خسارة
"""

TOURNAMENTS = [
    {"year": 1994, "host": "الولايات المتحدة", "stage": "دور الـ16", "best": True,
     "note": "أول مشاركة، وأفضل إنجاز في تاريخ المنتخب.",
     "matches": [
         {"vs": "هولندا", "score": "1-2", "result": "L"},
         {"vs": "المغرب", "score": "2-1", "result": "W"},
         {"vs": "بلجيكا", "score": "1-0", "result": "W"},
         {"vs": "السويد (دور الـ16)", "score": "1-3", "result": "L"},
     ]},
    {"year": 1998, "host": "فرنسا", "stage": "دور المجموعات", "best": False,
     "note": "تعادل مثير مع جنوب أفريقيا في المباراة الأخيرة.",
     "matches": [
         {"vs": "الدنمارك", "score": "0-1", "result": "L"},
         {"vs": "فرنسا", "score": "0-4", "result": "L"},
         {"vs": "جنوب أفريقيا", "score": "2-2", "result": "D"},
     ]},
    {"year": 2002, "host": "كوريا الجنوبية واليابان", "stage": "دور المجموعات", "best": False,
     "note": "مشاركة صعبة في مجموعة قوية.",
     "matches": [
         {"vs": "ألمانيا", "score": "0-8", "result": "L"},
         {"vs": "الكاميرون", "score": "0-1", "result": "L"},
         {"vs": "أيرلندا", "score": "0-3", "result": "L"},
     ]},
    {"year": 2006, "host": "ألمانيا", "stage": "دور المجموعات", "best": False,
     "note": "سامي الجابر يسجل في ثالث كأس عالم له.",
     "matches": [
         {"vs": "تونس", "score": "2-2", "result": "D"},
         {"vs": "أوكرانيا", "score": "0-4", "result": "L"},
         {"vs": "إسبانيا", "score": "0-1", "result": "L"},
     ]},
    {"year": 2018, "host": "روسيا", "stage": "دور المجموعات", "best": False,
     "note": "لعب مباراة الافتتاح، وختم بفوز على مصر.",
     "matches": [
         {"vs": "روسيا", "score": "0-5", "result": "L"},
         {"vs": "الأوروغواي", "score": "0-1", "result": "L"},
         {"vs": "مصر", "score": "2-1", "result": "W"},
     ]},
    {"year": 2022, "host": "قطر", "stage": "دور المجموعات", "best": False,
     "note": "الفوز التاريخي على الأرجنتين التي توّجت باللقب.",
     "matches": [
         {"vs": "الأرجنتين", "score": "2-1", "result": "W"},
         {"vs": "بولندا", "score": "0-2", "result": "L"},
         {"vs": "المكسيك", "score": "1-2", "result": "L"},
     ]},
    {"year": 2026, "host": "الولايات المتحدة وكندا والمكسيك", "stage": "دور المجموعات", "best": False,
     "note": "تعادلان وخسارة في أول نسخة بـ 48 منتخباً.",
     "matches": [
         {"vs": "الأوروغواي", "score": "1-1", "result": "D"},
         {"vs": "إسبانيا", "score": "0-4", "result": "L"},
         {"vs": "الرأس الأخضر", "score": "0-0", "result": "D"},
     ]},
]

MOMENTS = [
    {"year": "1994", "title": "هدف العويران", "image": "main/images/moment-owairan-1994.jpg",
     "text": "سعيد العويران يراوغ نصف لاعبي بلجيكا من منتصف الملعب، ويسجل أحد أجمل أهداف كأس العالم، ويقود المنتخب إلى دور الـ16."},
    {"year": "2022", "title": "إسقاط الأرجنتين", "image": "main/images/moment-argentina-2022.jpg",
     "text": "صالح الشهري وسالم الدوسري يقلبان التأخر إلى فوز 2-1 على الأرجنتين، في واحدة من أكبر مفاجآت تاريخ البطولة."},
    {"year": "2018", "title": "فوز في الوقت القاتل", "image": "main/images/moment-dawsari-2018.jpg",
     "text": "سالم الدوسري يسجل هدف الفوز على مصر في الدقائق الأخيرة، ويختم المنتخب مشاركته بانتصار."},
]

LEGENDS = [
    {"name": "سامي الجابر", "role": "مهاجم", "fact": "شارك في 4 نسخ من كأس العالم، وسجّل في 3 منها.", "icon": "bi-lightning-charge"},
    {"name": "محمد الدعيع", "role": "حارس مرمى", "fact": "حارس المنتخب في مونديالات 1994 و1998 و2002.", "icon": "bi-shield-check"},
    {"name": "سعيد العويران", "role": "مهاجم", "fact": "صاحب هدف بلجيكا الأسطوري في 1994.", "icon": "bi-stars"},
    {"name": "سالم الدوسري", "role": "جناح", "fact": "سجّل في مونديالي 2018 و2022، منها هدف الفوز على الأرجنتين.", "icon": "bi-fire"},
]


def summary():
    matches = [m for t in TOURNAMENTS for m in t["matches"]]
    return {
        "editions": len(TOURNAMENTS),
        "played": len(matches),
        "wins": sum(m["result"] == "W" for m in matches),
        "draws": sum(m["result"] == "D" for m in matches),
        "losses": sum(m["result"] == "L" for m in matches),
    }
