# حكاية وطن | UNIT-PROJECT-2

موقع سياحي وثقافي عن المملكة العربية السعودية، مبني باستخدام **Django**. يستعرض ست مدن سعودية، ويقدم لكل مدينة نبذة ومعالم ومحطات تاريخية وفعاليات ومعرض صور وفيديو تعريفي، بالإضافة إلى صفحة مستقلة لتاريخ المملكة وملوكها ومناسباتها الوطنية.

## متطلبات المشروع

- Django framework.
- Django templates مع template inheritance.
- Dynamic URLs لصفحات المدن والقصص.
- Static files: CSS وJavaScript والصور المساندة.
- الصفحة الرئيسية + ست صفحات مدن على الأقل.
- تصميم موحد ومتناسق.
- الوضع الليلي والنهاري مع حفظ الاختيار في Cookie لمدة سنة.
- واجهة عربية وإنجليزية مع حفظ اللغة المختارة في Cookie عبر Django LocaleMiddleware.
- تصميم Responsive للجوال واللوحي والكمبيوتر.
- معرض صور وفيديو لكل مدينة.

تمت إضافة قائمة تحقق مفصلة في `PROJECT_REQUIREMENTS.md`، كما تظهر داخل صفحة «عن المشروع».

## صفحات الموقع

| الرابط | الصفحة |
|---|---|
| `/` | الرئيسية ودليل المدن |
| `/city/riyadh/` | الرياض |
| `/city/abha/` | أبها |
| `/city/makkah/` | مكة المكرمة |
| `/city/alula/` | العلا |
| `/city/jeddah/` | جدة |
| `/city/madinah/` | المدينة المنورة |
| `/history/` | تاريخ المملكة العربية السعودية |
| `/stories/` | قصص من القرآن الكريم |
| `/stories/<slug>/` | تفاصيل القصة |
| `/about/` | عن المشروع ومتطلبات الوحدة |

## تشغيل المشروع على Windows

افتح Terminal داخل المجلد الذي يحتوي على `manage.py` ثم نفّذ:

```powershell
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
py manage.py runserver
```

ثم افتح `http://127.0.0.1:8000/` في المتصفح. استخدم زر `EN` أو `العربية` في شريط التنقل لتغيير لغة الموقع؛ سيبقى اختيارك محفوظًا عند التنقل بين الصفحات والعودة لاحقًا.

إذا لم يعمل الأمر `py` استخدم `python` بدلًا منه.

## تشغيل المشروع على macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py runserver
```

## بنية المشروع

```text
UNIT-PROJECT-2/
├── manage.py
├── requirements.txt
├── saudi_heritage/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── kingdom/
│   ├── data.py              # City and story content (no content database)
│   ├── history_data.py      # Kingdom milestones, kings, and national occasions
│   ├── localization.py      # English content for cities, stories, and history
│   ├── templatetags/
│   │   ├── __init__.py
│   │   └── translations.py  # Fixed interface translations
│   ├── urls.py              # Dynamic routes
│   └── views.py             # Passes content to templates
├── templates/
│   └── kingdom/
│       ├── base.html        # Shared base template
│       ├── home.html
│       ├── city_detail.html
│       ├── history.html
│       ├── stories.html
│       ├── story_detail.html
│       └── about.html
├── static/
│   ├── css/style.css
│   ├── js/theme.js
│   └── images/
└── PROJECT_REQUIREMENTS.md
```

## تخزين البيانات

المشروع لا يستخدم قاعدة بيانات إطلاقًا؛ تم تفعيل Django Dummy Database Backend. اختيار اللغة العربية أو الإنجليزية يُحفظ في Cookie باسم `saudi-heritage-language`، واختيار المظهر يُحفظ في Cookie باسم `saudi-heritage-theme`. بيانات المدن والقصص محفوظة في `kingdom/data.py`، ومحطات تاريخ المملكة والملوك والمناسبات الوطنية محفوظة في `kingdom/history_data.py`، وتُعرض جميعها باستخدام Django Views وTemplates.

## الصور والفيديو

- صور المدن وتاريخ المملكة وصور الملوك مرتبطة بملفاتها في Wikimedia Commons، وتظهر إحالات المصدر واسم المصور أو الجهة الناشرة ضمن الصفحة.
- فيديوهات المدن مضمّنة من YouTube.
- يلزم اتصال بالإنترنت لتحميل الصور والفيديو والخطوط وBootstrap CDN.
- احتفظ بروابط المصدر ونسب الصور إلى أصحابها عند إعادة استخدام المشروع. راجع `IMAGE_CREDITS.md`.

## مصادر المحتوى

- [Visit Saudi](https://www.visitsaudi.com/)
- [هيئة التراث](https://heritage.moc.gov.sa/)
- [الهيئة الملكية لمحافظة العلا](https://www.rcu.gov.sa/)
- [UNESCO — Hegra](https://whc.unesco.org/en/list/1293/)

المعلومات التاريخية موجزة لأغراض تعليمية، وينبغي مراجعة المصادر الرسمية عند التوسع في المحتوى.
