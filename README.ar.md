<div dir="rtl" lang="ar">

[English README](README.md)

# أطلس المشاريع السعودية

دليل تفاعلي بالعربية والإنجليزية يستعرض سبعة من أبرز المشاريع والوجهات في المملكة: نيوم، والقدية، والدرعية، وروشن، والبحر الأحمر، وأمالا، والعُلا.

**[زيارة الموقع بالعربية](https://suliman-altwaijry.github.io/UNIT-PROJECT-2/ar/)**

## ما يقدّمه الأطلس

- **خريطة تفاعلية ثلاثية الأبعاد** تعرض تضاريس المملكة من بيانات الارتفاع وتحدّد مواقع المشاريع.
- **صفحة لكل مشروع** تضم نبذة، وحقائق أساسية، وأبرز المحطات، ومعرض صور، وأنشطة، وفيلمًا قصيرًا.
- **خط زمني موحّد** يجمع محطات المشاريع مع إمكانية تصفيتها حسب المشروع.
- **جدول مقارنة** يعرض المشاريع السبعة جنبًا إلى جنب.
- **بحث فوري باللغتين** يبرز الكلمات المطابقة في النتائج.
- **تصميم متجاوب** يدعم القراءة من اليمين إلى اليسار والوضعين الفاتح والداكن.

## التقنيات

| الجزء | الأدوات |
| --- | --- |
| الخادم | Django 6.1، وWhiteNoise، وGunicorn |
| الواجهة | Vite، وTailwind CSS، وthree.js |
| الوسائط | Cloudflare R2 لاستضافة الأفلام، وAVIF وWebP للصور |
| النشر | GitHub Pages وDocker على Render |

توجد بيانات المشاريع والخريطة والمصادر في `saudi_atlas/projects/data/`، وملفات الواجهة في `saudi_atlas/projects/frontend/`، والقوالب في `saudi_atlas/projects/templates/`، والترجمات في `saudi_atlas/projects/locale/`.

## التشغيل محليًا

المتطلبات هي Python 3.15 وBun 1.4.4. شغّل الأوامر التالية من مجلد المشروع على Windows.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
bun install --frozen-lockfile
bun run build
python manage.py compiletranslations
python manage.py runserver
```

افتح [الصفحة العربية](http://127.0.0.1:8000/ar/) أو [الصفحة الإنجليزية](http://127.0.0.1:8000/).

لتشغيل الاختبارات، استخدم الأمر `python manage.py test`.

## النشر

يُنشئ GitHub Actions نسخة ثابتة من صفحات Django وينشرها على GitHub Pages عند دفع تحديث إلى فرع `main`.

لنشر نسخة Django على Render، اختر **New > Blueprint**، واربط المستودع، ثم اختر **Deploy Blueprint**. يبني ملف `Dockerfile` الواجهة ويترجم ملفات اللغة ويجمع الملفات الثابتة ويشغّل Gunicorn. راجع [النسخة الإنجليزية من README](README.md#deploy) لمعرفة متغيّرات البيئة.

## المصادر والتراخيص

تضم [صفحة المصادر والتراخيص](https://suliman-altwaijry.github.io/UNIT-PROJECT-2/ar/credits/) اعتمادات الصور والأفلام وبيانات الخريطة والخطوط.

</div>
