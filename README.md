# حكاية وطن — Django (بدون قاعدة بيانات)

## التشغيل
    pip install -r requirements.txt
    python manage.py runserver
ثم افتح http://127.0.0.1:8000/

## الروابط
/ · /history/ · /history/<era>/ · /cities/ · /city/<city>/ · /about/
(مثال: /city/riyadh/ ، /city/alula/ ، /history/first-state/)

## المحتوى
كل شيء في watan/data/content.json (يُعاد تحميله تلقائيًا عند تعديله).
لإضافة مدينة: أضف كائنًا جديدًا في cities. لفيديو يوتيوب: ضع youtube_id في video.
tools/make_assets.py هو المولّد الذي أنتج الصور (SVG) والفيديوهات.


## تفضيلات العرض واللغة
- الوضع الداكن/الفاتح يُحفظ في Cookie باسم `watan-theme` لمدة سنة، ولا يعتمد على localStorage.
- زر اللغة يبدّل بين العربية والإنجليزية باستخدام Google Translate، ويحفظ الاختيار في Cookie باسم `watan-language`. يلزم اتصال بالإنترنت لاستخدام خدمة الترجمة.
- سهم قائمتَي «التاريخ» و«المدن» يوضح إمكانية فتح القائمة وإغلاقها.
