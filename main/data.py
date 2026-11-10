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


# Extra content for each city page (city/<slug>/). Merged into CITIES below.
CITY_DETAILS = {
    "riyadh": {
        "hero": "main/images/riyadh-kingdom-centre.jpg",
        "region": "منطقة الرياض",
        "intro": "عاصمة المملكة وقلبها النابض، ومدينة تكبر كل يوم. تستعد الرياض لاحتضان الحصة الأكبر من مباريات كأس العالم 2034 بثمانية ملاعب، بينها استاد الملك سلمان الدولي الذي يُخطط لأن يستضيف مباراتي الافتتاح والنهائي.",
        "gallery": [
            {"image": "main/images/riyadh-kingdom-centre.jpg", "caption": "برج المملكة وقت الغروب"},
            {"image": "main/images/riyadh-diriyah.jpg", "caption": "حي الطريف في الدرعية ليلاً"},
            {"image": "main/images/riyadh-masmak.jpg", "caption": "قصر المصمك"},
            {"image": "main/images/riyadh-boulevard.jpg", "caption": "بوليفارد سيتي"},
            {"image": "main/images/riyadh-faisaliah.jpg", "caption": "برج الفيصلية"},
        ],
        "video": "main/videos/riyadh.mp4",
        "video_poster": "main/videos/riyadh-poster.jpg",
        "stadiums": ["استاد الملك سلمان الدولي", "مدينة الملك فهد الرياضية", "ملعب الأمير محمد بن سلمان", "ملعب المربع الجديد", "ملعب روشن", "ملعب جامعة الملك سعود", "ملعب جنوب الرياض", "مدينة الأمير فيصل بن فهد الرياضية"],
        "attractions": [
            {"name": "الدرعية", "text": "مهد الدولة السعودية الأولى، وحي الطريف فيها مسجّل في قائمة التراث العالمي.", "icon": "bi-bank"},
            {"name": "قصر المصمك", "text": "الحصن الطيني الذي انطلق منه توحيد المملكة.", "icon": "bi-shield"},
            {"name": "برج المملكة", "text": "جسر المشاهدة في أعلاه يطل على المدينة كلها.", "icon": "bi-building"},
            {"name": "بوليفارد سيتي", "text": "وجهة ترفيهية تحتضن فعاليات موسم الرياض.", "icon": "bi-stars"},
        ],
        "timeline": [
            {"year": "1902", "text": "الملك عبدالعزيز يستعيد الرياض من قصر المصمك."},
            {"year": "1932", "text": "توحيد المملكة العربية السعودية والرياض عاصمتها."},
            {"year": "1987", "text": "افتتاح استاد الملك فهد الدولي."},
            {"year": "2019", "text": "انطلاق أول نسخة من موسم الرياض."},
            {"year": "2023", "text": "الرياض تفوز باستضافة إكسبو 2030."},
            {"year": "2034", "text": "مباريات كأس العالم في ثمانية ملاعب."},
        ],
        "events": [
            {"name": "موسم الرياض", "text": "حفلات وعروض وفعاليات عالمية كل شتاء.", "icon": "bi-calendar-event"},
            {"name": "إكسبو 2030", "text": "المعرض الدولي من أكتوبر 2030 إلى مارس 2031.", "icon": "bi-globe2"},
            {"name": "كأس العالم للرياضات الإلكترونية", "text": "أكبر بطولة للرياضات الإلكترونية في العالم.", "icon": "bi-controller"},
        ],
    },
    "jeddah": {
        "hero": "main/images/jeddah-corniche.jpg",
        "region": "منطقة مكة المكرمة",
        "intro": "عروس البحر الأحمر وبوابة الحرمين. تجمع جدة بين البلد التاريخي ورواشينه الخشبية، والكورنيش الممتد على البحر، وملعب الجوهرة الذي شهد أهم مباريات المنتخب والأندية.",
        "gallery": [
            {"image": "main/images/jeddah-corniche.jpg", "caption": "كورنيش جدة ومسجد الرحمة"},
            {"image": "main/images/jeddah-albalad.jpg", "caption": "رواشين جدة التاريخية"},
            {"image": "main/images/jeddah-fountain.jpg", "caption": "نافورة الملك فهد"},
            {"image": "main/images/hero-jawhara-tifo.jpg", "caption": "تيفو الجماهير في ملعب الجوهرة"},
            {"image": "main/images/jeddah-abdullah-alfaisal-stadium.jpg", "caption": "ملعب الأمير عبدالله الفيصل"},
            {"image": "main/images/jeddah-sign.jpg", "caption": "الواجهة البحرية"},
        ],
        "video": "main/videos/jeddah.mp4",
        "video_poster": "main/videos/jeddah-poster.jpg",
        "stadiums": ["ملعب مدينة الملك عبدالله الرياضية (الجوهرة)", "ملعب وسط جدة", "ملعب مدينة الملك عبدالله الاقتصادية", "ملعب ساحل القدية"],
        "attractions": [
            {"name": "جدة التاريخية (البلد)", "text": "بيوت الرواشين والأسواق القديمة، ومسجّلة في التراث العالمي.", "icon": "bi-house"},
            {"name": "نافورة الملك فهد", "text": "من أعلى النوافير في العالم، وتُرى من أغلب الكورنيش.", "icon": "bi-droplet"},
            {"name": "الكورنيش", "text": "واجهة بحرية طويلة للمشي والمطاعم والغروب.", "icon": "bi-water"},
            {"name": "مسجد الرحمة", "text": "المسجد العائم فوق مياه البحر الأحمر.", "icon": "bi-moon-stars"},
        ],
        "timeline": [
            {"year": "2014", "text": "افتتاح ملعب الجوهرة، وتسجيل جدة التاريخية في التراث العالمي."},
            {"year": "2021", "text": "أول جائزة كبرى للفورمولا 1 على حلبة كورنيش جدة."},
            {"year": "2023", "text": "جدة تستضيف كأس العالم للأندية."},
            {"year": "2034", "text": "مباريات كأس العالم في أربعة ملاعب."},
        ],
        "events": [
            {"name": "جائزة السعودية الكبرى (فورمولا 1)", "text": "سباق ليلي على حلبة كورنيش جدة.", "icon": "bi-flag"},
            {"name": "مهرجان البحر الأحمر السينمائي", "text": "مهرجان سينمائي دولي في جدة التاريخية.", "icon": "bi-film"},
            {"name": "موسم جدة", "text": "فعاليات وعروض في أنحاء المدينة.", "icon": "bi-calendar-event"},
        ],
    },
    "alkhobar": {
        "hero": "main/images/khobar-tower-sunset.jpg",
        "region": "المنطقة الشرقية",
        "intro": "مدينة ساحلية على الخليج العربي، جارة الدمام والظهران، وبوابة المملكة إلى البحرين عبر جسر الملك فهد. يحتضن ملعب أرامكو فيها مباريات كأس العالم 2034.",
        "gallery": [
            {"image": "main/images/khobar-tower-sunset.jpg", "caption": "برج الماء وقت الغروب"},
            {"image": "main/images/khobar-corniche-mosque.jpg", "caption": "كورنيش الخبر وقت الغروب"},
            {"image": "main/images/khobar-tower-dusk.jpg", "caption": "واجهة الخبر البحرية مساءً"},
            {"image": "main/images/khobar-night.jpg", "caption": "كورنيش الخبر ليلاً"},
        ],
        "video": "main/videos/khobar.mp4",
        "video_poster": "main/videos/khobar-poster.jpg",
        "stadiums": ["ملعب أرامكو"],
        "attractions": [
            {"name": "برج الماء", "text": "رمز الخبر على الكورنيش، وفيه مطل على الخليج.", "icon": "bi-droplet-half"},
            {"name": "كورنيش الخبر", "text": "حدائق وممشى على البحر.", "icon": "bi-water"},
            {"name": "جسر الملك فهد", "text": "يربط المملكة بالبحرين فوق البحر.", "icon": "bi-signpost-2"},
            {"name": "إثراء", "text": "مركز الملك عبدالعزيز الثقافي العالمي في الظهران المجاورة.", "icon": "bi-lightbulb"},
        ],
        "timeline": [
            {"year": "1938", "text": "اكتشاف النفط في بئر الدمام رقم 7 القريبة."},
            {"year": "1986", "text": "افتتاح جسر الملك فهد إلى البحرين."},
            {"year": "2018", "text": "افتتاح مركز إثراء في الظهران."},
            {"year": "2034", "text": "مباريات كأس العالم في ملعب أرامكو."},
        ],
        "events": [
            {"name": "كأس آسيا 2027", "text": "المملكة تستضيف البطولة القارية قبل المونديال.", "icon": "bi-trophy"},
            {"name": "فعاليات إثراء", "text": "معارض وعروض ثقافية على مدار العام.", "icon": "bi-easel"},
        ],
    },
    "abha": {
        "hero": "main/images/abha-clouds.jpg",
        "region": "منطقة عسير",
        "intro": "عاصمة عسير، مدينة الضباب والجبال الخضراء والطقس المعتدل. أبها تجعل كرة القدم في كأس العالم 2034 تُلعب حرفياً فوق السحاب.",
        "gallery": [
            {"image": "main/images/abha-clouds.jpg", "caption": "أبها فوق السحاب"},
            {"image": "main/images/abha-view.jpg", "caption": "إطلالة على المدينة"},
            {"image": "main/images/abha-cable-car.jpg", "caption": "تلفريك أبها"},
            {"image": "main/images/abha-statue.jpg", "caption": "مجسّم أبها بالخط العربي"},
        ],
        "video": "main/videos/abha.mp4",
        "video_poster": "main/videos/abha-poster.jpg",
        "stadiums": ["ملعب جامعة الملك خالد"],
        "attractions": [
            {"name": "السودة", "text": "أعلى قمة في المملكة، وغابات العرعر والضباب.", "icon": "bi-cloud-fog2"},
            {"name": "قرية رجال ألمع", "text": "قرية حجرية تراثية بين الجبال.", "icon": "bi-houses"},
            {"name": "التلفريك", "text": "رحلة معلقة بين الجبال والوديان.", "icon": "bi-geo-alt"},
            {"name": "القط العسيري", "text": "فن نسائي بالألوان على جدران البيوت.", "icon": "bi-palette"},
        ],
        "timeline": [
            {"year": "2017", "text": "اختيار أبها عاصمة للسياحة العربية، وتسجيل القط العسيري في التراث غير المادي."},
            {"year": "2034", "text": "مباريات كأس العالم في ملعب جامعة الملك خالد."},
        ],
        "events": [
            {"name": "موسم الصيف في عسير", "text": "فعاليات في الأجواء الباردة صيفاً.", "icon": "bi-sun"},
            {"name": "مهرجانات التراث", "text": "الفنون الشعبية والأسواق التقليدية.", "icon": "bi-music-note-beamed"},
        ],
    },
    "neom": {
        "hero": "main/images/neom-stadium.jpg",
        "region": "منطقة تبوك",
        "intro": "مشروع لمدن المستقبل في شمال غرب المملكة على البحر الأحمر. ملعب نيوم سيكون من أكثر ملاعب البطولة تميزاً، داخل مشروع ذا لاين.",
        "gallery": [
            {"image": "main/images/neom-stadium.jpg", "caption": "تصميم ملعب نيوم"},
            {"image": "main/images/neom-palms.jpg", "caption": "واحات النخيل والجبال"},
            {"image": "main/images/neom-canyon.jpg", "caption": "الأودية والصخور"},
            {"image": "main/images/neom-diving.jpg", "caption": "سواحل البحر الأحمر"},
            {"image": "main/images/neom-dune.jpg", "caption": "الكثبان الرملية"},
        ],
        "video": "main/videos/neom.mp4",
        "video_poster": "main/videos/neom-poster.jpg",
        "stadiums": ["ملعب نيوم"],
        "attractions": [
            {"name": "ذا لاين", "text": "مدينة خطية بلا سيارات، ويضم الملعب.", "icon": "bi-distribute-vertical"},
            {"name": "تروجينا", "text": "وجهة جبلية للأنشطة الشتوية.", "icon": "bi-snow"},
            {"name": "سندالة", "text": "جزيرة فاخرة في البحر الأحمر.", "icon": "bi-tsunami"},
            {"name": "الشعاب المرجانية", "text": "من أجمل مواقع الغوص في البحر الأحمر.", "icon": "bi-water"},
        ],
        "timeline": [
            {"year": "2017", "text": "الإعلان عن مشروع نيوم."},
            {"year": "2022", "text": "الكشف عن تصاميم ذا لاين."},
            {"year": "2034", "text": "مباريات كأس العالم في ملعب نيوم."},
        ],
        "events": [
            {"name": "مباريات المونديال", "text": "ملعب يطل على الجبال والبحر الأحمر.", "icon": "bi-trophy"},
        ],
    },
}

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

# The 15 World Cup 2034 stadiums (capacities from the bid book, gross seats).
# image: a real photo when we have one, otherwise None (the page shows a styled placeholder).
STADIUMS = [
    {"slug": "king-salman-international", "name": "استاد الملك سلمان الدولي", "city": "riyadh", "capacity": 92760,
     "status": "جديد", "completion": "2030", "image": None, "badge": "الافتتاح والنهائي",
     "description": "يُبنى شمال شرق الرياض قرب المطار، وسيكون الملعب الوطني للمملكة وأكبر ملاعب البطولة، ومقترح لاستضافة مباراتي الافتتاح والنهائي.",
     "features": ["أكبر ملاعب البطولة بأكثر من 92 ألف مقعد", "الملعب الوطني للمملكة بعد البطولة", "قريب من مطار الملك خالد الدولي"]},
    {"slug": "king-fahd-sports-city", "name": "مدينة الملك فهد الرياضية", "city": "riyadh", "capacity": 70200,
     "status": "قائم ويُطوَّر", "completion": "قائم منذ 1987", "image": "main/images/stadium-king-fahd-render.jpg", "badge": "",
     "description": "من أشهر ملاعب المملكة، وسقفه مستوحى من الخيمة العربية. يخضع لتطوير شامل يشمل إزالة مضمار ألعاب القوى لتقريب الجماهير من الملعب.",
     "features": ["سقف مستوحى من الخيمة العربية", "ملعب المنتخب السعودي", "إزالة مضمار ألعاب القوى في التطوير"]},
    {"slug": "prince-mohammed-bin-salman", "name": "ملعب الأمير محمد بن سلمان", "city": "riyadh", "capacity": 46979,
     "status": "جديد", "completion": "2029", "image": None, "badge": "",
     "description": "في قلب مشروع القدية جنوب غرب الرياض، بتصميم من ثلاثة جوانب مبني على حافة منحدر يطل على جبال طويق.",
     "features": ["مبني على حافة منحدر صخري", "إطلالة على جبال طويق", "مركز ترفيهي لمشروع القدية"]},
    {"slug": "new-murabba", "name": "ملعب المربع الجديد", "city": "riyadh", "capacity": 46010,
     "status": "جديد", "completion": "2029", "image": None, "badge": "",
     "description": "في شمال غرب الرياض داخل مشروع المربع الجديد، وسقفه مستوحى من لحاء شجرة الأكاسيا المنتشرة في وادي حنيفة.",
     "features": ["سقف مستوحى من شجرة الأكاسيا", "يندمج مع الحي المحيط", "ضمن مشروع المربع الجديد"]},
    {"slug": "roshn", "name": "ملعب روشن", "city": "riyadh", "capacity": 46000,
     "status": "جديد", "completion": "2032", "image": None, "badge": "",
     "description": "في جنوب غرب الرياض، بتصميم بلّوري يندمج مع الحي السكني المجاور ضمن مشاريع روشن.",
     "features": ["تصميم بلّوري لافت", "متصل بحي روشن السكني", "مساحة تتجاوز 450 ألف م²"]},
    {"slug": "south-riyadh", "name": "ملعب جنوب الرياض", "city": "riyadh", "capacity": 47060,
     "status": "جديد", "completion": "2032", "image": None, "badge": "",
     "description": "مستوحى من العمارة السلمانية، ويتصل بمنتزه وادي نمار ضمن مشروع الرياض الخضراء.",
     "features": ["طراز العمارة السلمانية", "متصل بمنتزه وادي نمار", "جزء من مشروع الرياض الخضراء"]},
    {"slug": "king-saud-university", "name": "ملعب جامعة الملك سعود", "city": "riyadh", "capacity": 46319,
     "status": "قائم ويُطوَّر", "completion": "قائم", "image": "main/images/stadium-ksu-alawwal.jpg", "badge": "",
     "description": "ملعب داخل الحرم الجامعي (الأول بارك)، يستضيف مباريات دوري روشن، وتُرفع سعته مؤقتاً مع تطوير مرافق الضيافة.",
     "features": ["يستضيف مباريات دوري روشن", "من ملاعب كأس آسيا 2027", "بجوار مجمع يو ووك"]},
    {"slug": "prince-faisal-bin-fahd", "name": "مدينة الأمير فيصل بن فهد الرياضية", "city": "riyadh", "capacity": 46865,
     "status": "قيد الإنشاء", "completion": "قبل 2027", "image": None, "badge": "",
     "description": "يُبنى ضمن مخطط رياضي وترفيهي أكبر، بمواد مصنّعة محلياً وألواح شمسية على السقف.",
     "features": ["ألواح شمسية على السقف", "مواد مصنّعة محلياً", "من ملاعب كأس آسيا 2027"]},
    {"slug": "king-abdullah-sports-city", "name": "ملعب مدينة الملك عبدالله الرياضية (الجوهرة)", "city": "jeddah", "capacity": 58432,
     "status": "قائم ويُطوَّر", "completion": "قائم منذ 2014", "image": "main/images/stadium-jawhara-fireworks.jpg", "badge": "",
     "description": "الجوهرة المشعة، ملعب الأهلي والاتحاد، واستضاف كأس العالم للأندية 2023 وأهم مباريات المنتخب.",
     "features": ["لقبه: الجوهرة المشعة", "استضاف كأس العالم للأندية 2023", "ملعب الأهلي والاتحاد"]},
    {"slug": "qiddiya-coast", "name": "ملعب ساحل القدية", "city": "jeddah", "capacity": 46096,
     "status": "جديد", "completion": "2032", "image": None, "badge": "",
     "description": "شمال جدة على ساحل البحر الأحمر، بأرضية ملعب قابلة للسحب، وتصميم بتدرجات ألوان مستوحى من موجة الجماهير.",
     "features": ["أرضية قابلة للسحب", "تصميم مستوحى من موجة الجماهير", "يتحول لمكان ترفيهي بعد البطولة"]},
    {"slug": "king-abdullah-economic-city", "name": "ملعب مدينة الملك عبدالله الاقتصادية", "city": "jeddah", "capacity": 45700,
     "status": "جديد", "completion": "2032", "image": None, "badge": "",
     "description": "على ساحل البحر الأحمر شمال جدة، بلمسات تصميم مستوحاة من الشعاب المرجانية.",
     "features": ["مستوحى من الشعاب المرجانية", "على ساحل البحر الأحمر", "يبدأ بناؤه في 2027"]},
    {"slug": "jeddah-central", "name": "ملعب وسط جدة", "city": "jeddah", "capacity": 45794,
     "status": "قيد الإنشاء", "completion": "قيد الإنشاء", "image": None, "badge": "",
     "description": "ضمن مشروع وسط جدة في جنوب غرب المدينة، بتصميم مستوحى من عمارة جدة التاريخية (البلد).",
     "features": ["مستوحى من عمارة البلد", "داخل حديقة رياضية", "ضمن مشروع وسط جدة"]},
    {"slug": "aramco", "name": "ملعب أرامكو", "city": "alkhobar", "capacity": 46096,
     "status": "قيد الإنشاء", "completion": "قبل 2027", "image": "main/images/stadium-aramco.jpg", "badge": "",
     "description": "شمال الخبر ضمن منطقة رياضية وترفيهية، ويستضيف كأس آسيا 2027 قبل كأس العالم.",
     "features": ["من ملاعب كأس آسيا 2027", "ملعب لنادٍ محترف بعد البطولة", "ضمن منطقة رياضية وترفيهية"]},
    {"slug": "king-khalid-university", "name": "ملعب جامعة الملك خالد", "city": "abha", "capacity": 45428,
     "status": "قائم ويُطوَّر", "completion": "قائم", "image": None, "badge": "",
     "description": "ملعب داخل الحرم الجامعي جنوب شرق أبها، تُضاف له مدرجات مؤقتة للبطولة مع الحفاظ على الملعب الأصلي بعدها.",
     "features": ["مدرجات مؤقتة فوق الملعب الحالي", "على ارتفاع أكثر من 2000 م", "الإرث بعد البطولة للجامعة"]},
    {"slug": "neom", "name": "ملعب نيوم", "city": "neom", "capacity": 46010,
     "status": "جديد", "completion": "2032", "image": "main/images/neom-stadium.jpg", "badge": "الأكثر تميزاً",
     "description": "داخل المنطقة الرياضية في المرحلة الأولى من ذا لاين، ويرتفع سقفه أكثر من 350 متراً فوق سطح الأرض.",
     "features": ["داخل مشروع ذا لاين", "سقف على ارتفاع 350 متراً", "محور المنطقة الرياضية"]},
]

for _s in STADIUMS:
    _s["capacity_display"] = f"{_s['capacity']:,}"


# Add the page details to each city
for _city in CITIES:
    _city.update(CITY_DETAILS[_city["slug"]])


def get_city(slug):
    return next((c for c in CITIES if c["slug"] == slug), None)


def get_stadium(slug):
    return next((s for s in STADIUMS if s["slug"] == slug), None)


def stadiums_in(city_slug):
    return [s for s in STADIUMS if s["city"] == city_slug]
