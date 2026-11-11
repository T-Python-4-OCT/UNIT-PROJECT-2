# بيانات الموقع بلغتين: "ar" عربي و "en" إنجليزي
# الـ views تختار اللغة المناسبة وترسلها للقالب
# ملاحظة: المعلومات والأرقام عامة وتقريبية، راجعها من المصادر الرسمية قبل التسليم
# video_id = رقم فيديو يوتيوب (الجزء اللي بعد v= في الرابط)، اتركه فاضي لو ما عندك فيديو


# القطاعات
SECTORS = {
    "ar": {
        "land": {
            "name": "الأنظمة البرية",
            "slogan": "قوة على الأرض… بأيدٍ سعودية",
            "about": "يشمل القطاع البري تصنيع العربات المدرعة والذخائر والأسلحة الخفيفة، "
                     "إضافة إلى صيانة وتطوير المعدات البرية. وهو من أقدم مجالات الصناعة "
                     "العسكرية في المملكة، إذ بدأت جذوره في مصانع الخرج.",
            "images": [
                ("photos/heet.webp", "مدرعات «هيت» من SAMI"),
                ("photos/sami-booth.webp", "جناح SAMI في معرض الدفاع العالمي"),
                ("photos/land-1.jpg", "دبابات القوات البرية الملكية السعودية"),
            ],
            "video_id": "",
            "highlights": [
                ("العربات المدرعة", "مدرعات «هيت» من SAMI بنسختي 4×4 و 8×8، وعربة «الدهناء».", "photos/heet.webp"),
                ("الدبابات", "تشغيل وتحديث دبابات القوات البرية الملكية السعودية.", "photos/land-1.jpg"),
                ("الصيانة والتطوير", "كفاءات سعودية تصون وتطوّر المعدات داخل المملكة.", "photos/sami-banner.webp"),
            ],
            "timeline": [
                ("1949", "بداية التصنيع العسكري في الخرج."),
                ("2017", "تأسيس الشركة السعودية للصناعات العسكرية SAMI."),
                ("2030", "الهدف: توطين أكثر من 50% من الإنفاق العسكري."),
            ],
            "events": [
                "عرض العربات المدرعة السعودية في معرض الدفاع العالمي.",
                "شراكات مع شركات عالمية لنقل التقنية.",
            ],
        },
        "air": {
            "name": "الطيران والأنظمة الجوية",
            "slogan": "سماء آمنة… وصناعة طموحة",
            "about": "يهتم القطاع الجوي بصيانة الطائرات الحربية والمروحيات وتطويرها، "
                     "وتصنيع الطائرات بدون طيار (المسيّرات)، وتوطين قطع الغيار "
                     "والإلكترونيات الخاصة بالطيران.",
            "images": [
                ("photos/air-1.jpg", "مقاتلة F-15SA للقوات الجوية الملكية السعودية"),
                ("photos/air-2.jpg", "تشكيل جوي بألوان اليوم الوطني 88"),
                ("photos/air-3.jpg", "فريق الصقور السعودية بالدخان الأخضر"),
                ("photos/air-4.jpg", "تشكيل الصقور السعودية"),
                ("photos/air-5.jpg", "مقاتلة يوروفايتر تايفون سعودية"),
            ],
            "video_id": "",
            "highlights": [
                ("المقاتلات الحديثة", "مقاتلات F-15SA ويوروفايتر تايفون في خدمة القوات الجوية الملكية السعودية.", "photos/air-1.jpg"),
                ("صيانة الطائرات", "شركة السلام للصناعات الجوية تصون وتطوّر طائرات القوات الجوية داخل المملكة.", "photos/air-5.jpg"),
                ("الصقور السعودية", "فريق الاستعراض الجوي الذي يمثّل المملكة في المناسبات والمعارض.", "photos/air-3.jpg"),
            ],
            "timeline": [
                ("1988", "تأسيس شركة السلام للصناعات الجوية."),
                ("2017", "انطلاق خطة توطين الصناعات العسكرية."),
                ("2022", "عرض المسيّرات السعودية في معرض الدفاع العالمي."),
            ],
            "events": [
                "عروض جوية ضمن معرض الدفاع العالمي في الرياض.",
                "اتفاقيات لتوطين صناعة قطع غيار الطائرات.",
            ],
        },
        "naval": {
            "name": "الأنظمة البحرية",
            "slogan": "حماية السواحل… من الخليج إلى البحر الأحمر",
            "about": "يشمل القطاع البحري بناء السفن الحربية والزوارق، وصيانتها، "
                     "وتوطين أنظمتها القتالية. وتعمل المملكة على بناء قدرات محلية "
                     "لحماية سواحلها الطويلة على الخليج العربي والبحر الأحمر.",
            "images": [
                ("photos/naval-corvette.jpg", "كورفيت للقوات البحرية الملكية السعودية"),
                ("photos/naval-makkah.jpg", "الفرقاطة مكة من فئة الرياض"),
                ("photos/naval-1.jpg", "الفرقاطة الدمام"),
                ("photos/naval-2.jpg", "زورق الصواريخ عقبة"),
            ],
            "video_id": "",
            "highlights": [
                ("الفرقاطات", "فرقاطات فئة الرياض مثل «مكة» لحماية المياه الإقليمية.", "photos/naval-makkah.jpg"),
                ("سفن الكورفيت", "سفن سريعة للقوات البحرية، ومشروع SAMI Navantia لتوطين أنظمتها.", "photos/naval-corvette.jpg"),
                ("زوارق الصواريخ", "زوارق هجومية سريعة مثل «عقبة» لحماية السواحل.", "photos/naval-2.jpg"),
            ],
            "timeline": [
                ("2020", "تأسيس SAMI Navantia للصناعات البحرية."),
                ("2020", "تدشين أول سفينة كورفيت من المشروع."),
                ("2030", "التوسع في بناء وصيانة السفن محلياً."),
            ],
            "events": [
                "تدشين سفن القوات البحرية الملكية السعودية الجديدة.",
                "معارض بحرية ضمن معرض الدفاع العالمي.",
            ],
        },
    },

    "en": {
        "land": {
            "name": "Land Systems",
            "slogan": "Strength on the ground… built by Saudi hands",
            "about": "The land sector covers armored vehicles, ammunition and light weapons, "
                     "as well as the maintenance and upgrade of ground equipment. It is one of "
                     "the oldest military industries in the Kingdom, with roots in the Al-Kharj factories.",
            "images": [
                ("photos/heet.webp", "SAMI HEET armored vehicles"),
                ("photos/sami-booth.webp", "SAMI pavilion at the World Defense Show"),
                ("photos/land-1.jpg", "Royal Saudi Land Forces tanks"),
            ],
            "video_id": "",
            "highlights": [
                ("Armored vehicles", "SAMI HEET vehicles in 4×4 and 8×8 versions, and the Al-Dahna vehicle.", "photos/heet.webp"),
                ("Tanks", "Operating and upgrading the tanks of the Royal Saudi Land Forces.", "photos/land-1.jpg"),
                ("Maintenance & upgrades", "Saudi talent maintaining and upgrading equipment inside the Kingdom.", "photos/sami-banner.webp"),
            ],
            "timeline": [
                ("1949", "Military manufacturing begins in Al-Kharj."),
                ("2017", "Saudi Arabian Military Industries (SAMI) is founded."),
                ("2030", "Goal: localize more than 50% of military spending."),
            ],
            "events": [
                "Saudi armored vehicles on display at the World Defense Show.",
                "Partnerships with global companies to transfer technology.",
            ],
        },
        "air": {
            "name": "Air Systems & Aviation",
            "slogan": "Safe skies… and an ambitious industry",
            "about": "The air sector focuses on maintaining and upgrading combat aircraft and helicopters, "
                     "building unmanned aerial vehicles (drones), and localizing spare parts "
                     "and aviation electronics.",
            "images": [
                ("photos/air-1.jpg", "Royal Saudi Air Force F-15SA"),
                ("photos/air-2.jpg", "Formation in 88th National Day livery"),
                ("photos/air-3.jpg", "Saudi Hawks with green smoke"),
                ("photos/air-4.jpg", "Saudi Hawks formation"),
                ("photos/air-5.jpg", "Saudi Eurofighter Typhoon"),
            ],
            "video_id": "",
            "highlights": [
                ("Modern fighters", "F-15SA and Eurofighter Typhoon jets serve the Royal Saudi Air Force.", "photos/air-1.jpg"),
                ("Aircraft maintenance", "Alsalam Aerospace Industries maintains and upgrades Air Force aircraft in the Kingdom.", "photos/air-5.jpg"),
                ("Saudi Hawks", "The aerobatic team that represents the Kingdom at events and air shows.", "photos/air-3.jpg"),
            ],
            "timeline": [
                ("1988", "Alsalam Aerospace Industries is founded."),
                ("2017", "The military industry localization plan begins."),
                ("2022", "Saudi drones shown at the World Defense Show."),
            ],
            "events": [
                "Air displays at the World Defense Show in Riyadh.",
                "Agreements to localize aircraft spare parts.",
            ],
        },
        "naval": {
            "name": "Naval Systems",
            "slogan": "Guarding the coasts… from the Gulf to the Red Sea",
            "about": "The naval sector covers building and maintaining warships and boats, "
                     "and localizing their combat systems. The Kingdom is building local "
                     "capabilities to protect its long coasts on the Arabian Gulf and the Red Sea.",
            "images": [
                ("photos/naval-corvette.jpg", "Royal Saudi Navy corvette"),
                ("photos/naval-makkah.jpg", "Al Riyadh-class frigate Makkah"),
                ("photos/naval-1.jpg", "Frigate Al Dammam"),
                ("photos/naval-2.jpg", "Missile boat Oqbah"),
            ],
            "video_id": "",
            "highlights": [
                ("Frigates", "Al Riyadh-class frigates such as Makkah protect territorial waters.", "photos/naval-makkah.jpg"),
                ("Corvettes", "Fast navy ships, and the SAMI Navantia project to localize their systems.", "photos/naval-corvette.jpg"),
                ("Missile boats", "Fast attack boats such as Oqbah guard the coastline.", "photos/naval-2.jpg"),
            ],
            "timeline": [
                ("2020", "SAMI Navantia Naval Industries is founded."),
                ("2020", "The project's first corvette is launched."),
                ("2030", "More shipbuilding and maintenance done locally."),
            ],
            "events": [
                "New Royal Saudi Navy ships are launched.",
                "Naval exhibits at the World Defense Show.",
            ],
        },
    },
}


# الجهات
COMPANIES = {
    "ar": {
        "sami": {
            "name": "الشركة السعودية للصناعات العسكرية SAMI",
            "slogan": "ذراع التصنيع العسكري الوطني",
            "logo": "photos/sami-logo.webp",
            "logo_style": "background-size: auto 260%;",
            "about": "شركة وطنية مملوكة لصندوق الاستثمارات العامة، تأسست عام 2017 "
                     "لتكون منصة مستدامة للصناعات العسكرية في المملكة، وتعمل في "
                     "المجالات البرية والجوية والبحرية والإلكترونيات الدفاعية.",
            "images": [
                ("photos/sami-banner.webp", "كفاءات SAMI في الطيران والبر والإلكترونيات"),
                ("photos/sami-electronics.webp", "شركة الإلكترونيات المتقدمة التابعة لـ SAMI"),
                ("photos/heet.webp", "مدرعات «هيت» 4×4 و 8×8"),
            ],
            "video_id": "",
            "highlights": [
                ("الأنظمة البرية", "تصنيع مدرعات «هيت» وصيانة العربات العسكرية.", "photos/heet.webp"),
                ("الإلكترونيات", "استحواذ على شركة الإلكترونيات المتقدمة AEC.", "photos/sami-electronics.webp"),
                ("الشراكات", "مشاريع مشتركة مع شركات عالمية مثل نافانتيا.", "photos/sami-booth.webp"),
            ],
            "timeline": [
                ("2017", "تأسيس SAMI من قبل صندوق الاستثمارات العامة."),
                ("2020", "الاستحواذ على شركة الإلكترونيات المتقدمة."),
                ("2020", "تأسيس SAMI Navantia للصناعات البحرية."),
            ],
            "events": [
                "مشاركة رئيسية في معرض الدفاع العالمي.",
                "برامج تدريب وتوظيف للشباب السعودي.",
            ],
        },
        "gami": {
            "name": "الهيئة العامة للصناعات العسكرية GAMI",
            "slogan": "المنظّم والممكّن للقطاع",
            "logo": "photos/gami-logo.png",
            "logo_style": "background-size: auto 105%;",
            "about": "جهة حكومية تأسست عام 2017، مسؤولة عن تنظيم قطاع الصناعات "
                     "العسكرية وتمكينه، وإصدار تراخيص الشركات، والإشراف على "
                     "مشتريات المملكة العسكرية لرفع نسبة التوطين.",
            "images": [
                ("photos/gami-booth.webp", "جناح الهيئة في معرض الدفاع العالمي"),
                ("photos/sami-booth.webp", "الشركات الوطنية في المعرض"),
                ("photos/sami-electronics.webp", "توطين الإلكترونيات الدفاعية"),
            ],
            "video_id": "",
            "highlights": [
                ("التراخيص", "إصدار تراخيص مزاولة أنشطة الصناعات العسكرية.", "photos/gami-booth.webp"),
                ("التوطين", "متابعة نسبة التوطين وتحقيق مستهدف رؤية 2030.", "photos/sami-banner.webp"),
                ("المعارض", "تنظيم معرض الدفاع العالمي في الرياض.", "photos/sami-booth.webp"),
            ],
            "timeline": [
                ("2017", "تأسيس الهيئة العامة للصناعات العسكرية."),
                ("2022", "النسخة الأولى من معرض الدفاع العالمي."),
                ("2024", "النسخة الثانية من معرض الدفاع العالمي."),
            ],
            "events": [
                "تنظيم معرض الدفاع العالمي كل سنتين.",
                "ورش عمل لتمكين المصانع المحلية.",
            ],
        },
    },

    "en": {
        "sami": {
            "name": "Saudi Arabian Military Industries (SAMI)",
            "slogan": "The national military manufacturing arm",
            "logo": "photos/sami-logo.webp",
            "logo_style": "background-size: auto 260%;",
            "about": "A national company owned by the Public Investment Fund, founded in 2017 "
                     "as a sustainable platform for military industries in the Kingdom. It works "
                     "in land, air, naval and defense electronics.",
            "images": [
                ("photos/sami-banner.webp", "SAMI talent in aerospace, land and electronics"),
                ("photos/sami-electronics.webp", "SAMI Advanced Electronics"),
                ("photos/heet.webp", "HEET 4×4 and 8×8 armored vehicles"),
            ],
            "video_id": "",
            "highlights": [
                ("Land systems", "Building HEET armored vehicles and maintaining military vehicles.", "photos/heet.webp"),
                ("Electronics", "Acquired Advanced Electronics Company (AEC).", "photos/sami-electronics.webp"),
                ("Partnerships", "Joint ventures with global companies such as Navantia.", "photos/sami-booth.webp"),
            ],
            "timeline": [
                ("2017", "SAMI is founded by the Public Investment Fund."),
                ("2020", "Acquisition of Advanced Electronics Company."),
                ("2020", "SAMI Navantia Naval Industries is founded."),
            ],
            "events": [
                "A main exhibitor at the World Defense Show.",
                "Training and hiring programs for young Saudis.",
            ],
        },
        "gami": {
            "name": "General Authority for Military Industries (GAMI)",
            "slogan": "The sector's regulator and enabler",
            "logo": "photos/gami-logo.png",
            "logo_style": "background-size: auto 105%;",
            "about": "A government authority founded in 2017. It regulates and enables the military "
                     "industries sector, issues company licenses, and oversees the Kingdom's "
                     "military procurement to raise localization.",
            "images": [
                ("photos/gami-booth.webp", "GAMI pavilion at the World Defense Show"),
                ("photos/sami-booth.webp", "National companies at the show"),
                ("photos/sami-electronics.webp", "Localizing defense electronics"),
            ],
            "video_id": "",
            "highlights": [
                ("Licensing", "Issuing licenses for military industry activities.", "photos/gami-booth.webp"),
                ("Localization", "Tracking localization toward the Vision 2030 target.", "photos/sami-banner.webp"),
                ("Exhibitions", "Organizing the World Defense Show in Riyadh.", "photos/sami-booth.webp"),
            ],
            "timeline": [
                ("2017", "The General Authority for Military Industries is founded."),
                ("2022", "First edition of the World Defense Show."),
                ("2024", "Second edition of the World Defense Show."),
            ],
            "events": [
                "Organizing the World Defense Show every two years.",
                "Workshops to enable local factories.",
            ],
        },
    },
}


# التاريخ
HISTORY = {
    "ar": [
        ("1949", "بداية التصنيع العسكري في مصانع الخرج لإنتاج الذخائر."),
        ("1988", "تأسيس شركة السلام للصناعات الجوية."),
        ("2016", "إطلاق رؤية المملكة 2030 وتوطين الصناعات العسكرية من أهدافها."),
        ("2017", "تأسيس الهيئة العامة للصناعات العسكرية GAMI، والشركة السعودية للصناعات العسكرية SAMI."),
        ("2020", "تأسيس SAMI Navantia، واستحواذ SAMI على شركة الإلكترونيات المتقدمة."),
        ("2022", "انطلاق النسخة الأولى من معرض الدفاع العالمي في الرياض."),
        ("2024", "النسخة الثانية من معرض الدفاع العالمي."),
        ("2030", "المستهدف: توطين أكثر من 50% من الإنفاق العسكري."),
    ],
    "en": [
        ("1949", "Military manufacturing begins in the Al-Kharj factories, producing ammunition."),
        ("1988", "Alsalam Aerospace Industries is founded."),
        ("2016", "Saudi Vision 2030 is launched, with military industry localization as a goal."),
        ("2017", "GAMI and Saudi Arabian Military Industries (SAMI) are founded."),
        ("2020", "SAMI Navantia is founded, and SAMI acquires Advanced Electronics Company."),
        ("2022", "First World Defense Show held in Riyadh."),
        ("2024", "Second edition of the World Defense Show."),
        ("2030", "Target: localize more than 50% of military spending."),
    ],
}


# المعارض التي أُقيمت (المصدر: صفحة الإنجازات في gami.gov.sa)
# achievements = (الرقم، الوصف)
EVENTS = {
    "ar": [
        {"name": "معرض الدفاع العالمي 2026", "date_text": "8 – 12 فبراير 2026", "place": "الرياض",
         "text": "النسخة الثالثة، وأكبر نسخة حتى الآن من حيث عدد العارضين والزوار والدول المشاركة.",
         "images": [("photos/wds/wds2026-1.jpg", "صورة جوية لموقع المعرض"),
                    ("photos/wds/wds2026-2.jpg", "العروض الخارجية للطائرات"),
                    ("photos/wds/wds2026-3.jpg", "أجنحة العارضين")],
         "achievements": [("1,468", "عارض من 89 دولة"),
                          ("137 ألف", "زائر"),
                          ("513", "وفد رسمي من 121 دولة"),
                          ("8.8 مليار $", "عقود شراء مسجّلة"),
                          ("272,800 م²", "المساحة الإجمالية")]},
        {"name": "معرض الدفاع العالمي 2024", "date_text": "4 – 8 فبراير 2024", "place": "الرياض",
         "text": "النسخة الثانية، اختُتمت بتوقيع قياسي لعقود الشراء على مدى خمسة أيام.",
         "images": [("photos/wds/wds2024-1.jpg", "جناح الهيئة العامة للصناعات العسكرية"),
                    ("photos/wds/wds2024-2.jpg", "فريق الهيئة في المعرض"),
                    ("photos/wds/wds2024-3.jpg", "زيارة الوفود للأجنحة")],
         "achievements": [("773", "عارض"),
                          ("106 ألف", "زائر"),
                          ("441", "وفد رسمي من 116 دولة"),
                          ("26 مليار ريال", "61 عقد شراء"),
                          ("73", "اتفاقية، منها 17 للمشاركة الصناعية")]},
        {"name": "معرض الدفاع العالمي 2022", "date_text": "6 – 9 مارس 2022", "place": "الرياض",
         "text": "النسخة الأولى من المعرض، وانطلاقة المملكة كمنصة عالمية لصناعة الدفاع.",
         "images": [("photos/wds/wds2022-1.jpg", "قاعة العرض الرئيسية"),
                    ("photos/wds/wds2022-2.jpg", "الطائرات والمعدات المعروضة"),
                    ("photos/wds/wds2022-3.jpg", "افتتاح المعرض")],
         "achievements": [("600", "عارض من 42 دولة"),
                          ("65 ألف", "زائر من 85 دولة"),
                          ("+82", "وفد عسكري ودفاعي"),
                          ("5.9 مليار $", "صفقات وعقود مسجّلة"),
                          ("22", "اتفاقية توطين بقيمة 2.13 مليار $")]},
    ],
    "en": [
        {"name": "World Defense Show 2026", "date_text": "8 – 12 February 2026", "place": "Riyadh",
         "text": "The third edition, and the largest so far in exhibitors, visitors and participating countries.",
         "images": [("photos/wds/wds2026-1.jpg", "Aerial view of the show venue"),
                    ("photos/wds/wds2026-2.jpg", "Outdoor aircraft displays"),
                    ("photos/wds/wds2026-3.jpg", "Exhibitor pavilions")],
         "achievements": [("1,468", "exhibitors from 89 countries"),
                          ("137K", "visitors"),
                          ("513", "official delegations from 121 countries"),
                          ("$8.8B", "recorded purchase contracts"),
                          ("272,800 m²", "total area")]},
        {"name": "World Defense Show 2024", "date_text": "4 – 8 February 2024", "place": "Riyadh",
         "text": "The second edition, closing with a record number of purchase contracts over five days.",
         "images": [("photos/wds/wds2024-1.jpg", "GAMI pavilion"),
                    ("photos/wds/wds2024-2.jpg", "The GAMI team at the show"),
                    ("photos/wds/wds2024-3.jpg", "Delegations touring the pavilions")],
         "achievements": [("773", "exhibitors"),
                          ("106K", "visitors"),
                          ("441", "official delegations from 116 countries"),
                          ("SAR 26B", "61 purchase contracts"),
                          ("73", "agreements, 17 for industrial participation")]},
        {"name": "World Defense Show 2022", "date_text": "6 – 9 March 2022", "place": "Riyadh",
         "text": "The first edition, launching the Kingdom as a global platform for the defense industry.",
         "images": [("photos/wds/wds2022-1.jpg", "The main exhibition hall"),
                    ("photos/wds/wds2022-2.jpg", "Aircraft and equipment on display"),
                    ("photos/wds/wds2022-3.jpg", "Opening of the show")],
         "achievements": [("600", "exhibitors from 42 countries"),
                          ("65K", "visitors from 85 countries"),
                          ("82+", "military and defense delegations"),
                          ("$5.9B", "recorded deals and contracts"),
                          ("22", "localization agreements worth $2.13B")]},
    ],
}




# المعارض القادمة (المصدر: الموقع الرسمي worlddefenseshow.com)
# start = تاريخ البداية (سنة، شهر، يوم) عشان نحسب كم يوم باقي
UPCOMING_EVENTS = {
    "ar": [
        {
            "name": "معرض الدفاع العالمي 2028",
            "date_text": "16 – 20 يناير 2028",
            "start": (2028, 1, 16),
            "place": "الرياض، المملكة العربية السعودية",
            "text": "النسخة الرابعة من المعرض، تنظّمه الهيئة العامة للصناعات العسكرية، "
                    "ويجمع شركات الدفاع السعودية والعالمية في البر والجو والبحر والفضاء والأمن.",
            "image": "photos/wds/wds2026-1.jpg",
            "visit_url": "https://www.worlddefenseshow.com/ar/about-the-show/what-to-expect",
            "exhibit_url": "https://www.worlddefenseshow.com/ar/exhibit/why-exhibit",
            "contact_url": "https://www.worlddefenseshow.com/ar/support/general-enquiry",
        },
    ],
    "en": [
        {
            "name": "World Defense Show 2028",
            "date_text": "16 – 20 January 2028",
            "start": (2028, 1, 16),
            "place": "Riyadh, Saudi Arabia",
            "text": "The fourth edition of the show, organized by GAMI, bringing together Saudi and "
                    "global defense companies across land, air, sea, space and security.",
            "image": "photos/wds/wds2026-1.jpg",
            "visit_url": "https://www.worlddefenseshow.com/en/about-the-show/what-to-expect",
            "exhibit_url": "https://www.worlddefenseshow.com/en/exhibit/why-exhibit",
            "contact_url": "https://www.worlddefenseshow.com/en/support/general-enquiry",
        },
    ],
}


# الوظائف والتدريب (روابط رسمية فقط)
CAREERS = {
    "ar": [
        {"icon": "bi-briefcase-fill",
         "title": "وظائف الشركة السعودية للصناعات العسكرية SAMI",
         "who": "الخريجين وأصحاب الخبرة",
         "text": "ابحث في الوظائف المتاحة وقدّم مباشرة، أو سجّل في برنامج التدريب، أو أرسل سيرتك الذاتية.",
         "url": "https://sami.jobs.hr.cloud.sap/search/?createNewAlert=false&q=",
         "button": "الوظائف المتاحة",
         "extra": [("برنامج التدريب", "https://www.sami.com.sa/en/join-internship-program/"),
                   ("أرسل سيرتك الذاتية", "https://www.sami.com.sa/en/submit-your-resume/")]},
        {"icon": "bi-mortarboard-fill",
         "title": "برنامج ابتعاث قطاع الصناعات العسكرية (MISP)",
         "who": "خريجي الثانوية والجامعة، وموظفي منشآت القطاع",
         "text": "أطلقته الهيئة العامة للصناعات العسكرية في أكتوبر 2022، لابتعاث الكفاءات السعودية للحصول على شهادات البكالوريوس والدراسات العليا، مع برامج تدريب خلال الدراسة.",
         "url": "https://www.gami.gov.sa/en/military-industries-scholarship-program-misp",
         "button": "صفحة البرنامج"},
        {"icon": "bi-people-fill",
         "title": "استراتيجية القوى البشرية للقطاع",
         "who": "كل المهتمين بالعمل في القطاع",
         "text": "مبادرات الهيئة لتأهيل الشباب السعودي للعمل في الصناعات العسكرية، ومنها برامج الأكاديمية الوطنية للصناعات العسكرية مثل التدريب المنتهي بالتوظيف.",
         "url": "https://www.gami.gov.sa/ar/human-capital-strategy",
         "button": "المبادرات والبرامج"},
    ],
    "en": [
        {"icon": "bi-briefcase-fill",
         "title": "Careers at Saudi Arabian Military Industries (SAMI)",
         "who": "Graduates and experienced professionals",
         "text": "Search open jobs and apply directly, join the internship program, or submit your resume.",
         "url": "https://sami.jobs.hr.cloud.sap/search/?createNewAlert=false&q=",
         "button": "Open positions",
         "extra": [("Internship program", "https://www.sami.com.sa/en/join-internship-program/"),
                   ("Submit your resume", "https://www.sami.com.sa/en/submit-your-resume/")]},
        {"icon": "bi-mortarboard-fill",
         "title": "Military Industries Scholarship Program (MISP)",
         "who": "High school and university graduates, and sector employees",
         "text": "Launched by GAMI in October 2022 to sponsor Saudi talent for bachelor's and postgraduate degrees, with training during their studies.",
         "url": "https://www.gami.gov.sa/en/military-industries-scholarship-program-misp",
         "button": "Program page"},
        {"icon": "bi-people-fill",
         "title": "The sector's human capital strategy",
         "who": "Anyone interested in working in the sector",
         "text": "GAMI's initiatives to prepare young Saudis for military industry jobs, including National Academy for Military Industries programs such as training that leads to employment.",
         "url": "https://www.gami.gov.sa/en/human-capital-strategy",
         "button": "Initiatives and programs"},
    ],
}

# التخصصات المطلوبة في القطاع (من إعلانات SAMI للخريجين)
CAREER_MAJORS = {
    "ar": ["الهندسة الكهربائية", "الهندسة الميكانيكية", "هندسة الميكاترونكس",
           "هندسة الحاسب", "علوم الحاسب", "هندسة البرمجيات"],
    "en": ["Electrical engineering", "Mechanical engineering", "Mechatronics engineering",
           "Computer engineering", "Computer science", "Software engineering"],
}
