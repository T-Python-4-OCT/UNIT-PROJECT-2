"""
Content for the page "عن الموقع".
"""

PROJECT = {
    "name": "الطريق إلى 2034",
    "course": "UNIT-PROJECT-2",
    "author": "سلطان الشهراني",   # change to your name if needed
    "idea": "موقع تعليمي يعرّف باستضافة المملكة العربية السعودية لكأس العالم 2034: المدن المستضيفة، والملاعب، ومشاركات المنتخب، ورحلة ملف الاستضافة.",
}

TECH = [
    {"name": "Django", "text": "إطار العمل، مع تطبيق main وملفات views وurls.", "icon": "bi-filetype-py"},
    {"name": "وراثة القوالب", "text": "قالب base.html واحد ترث منه كل الصفحات، وقوالب جزئية بـ include.", "icon": "bi-diagram-3"},
    {"name": "روابط ديناميكية", "text": "city/<slug>/ وstadium/<slug>/: قالب واحد لكل نوع من الصفحات.", "icon": "bi-link-45deg"},
    {"name": "Query Parameters", "text": "فلترة الملاعب حسب المدينة وترتيبها حسب السعة.", "icon": "bi-funnel"},
    {"name": "الملفات الثابتة", "text": "الصور والفيديوهات وCSS وJavaScript من مجلد static.", "icon": "bi-folder2-open"},
    {"name": "الكوكيز", "text": "حفظ اختيار الوضع الليلي أو النهاري في كوكي لمدة سنة.", "icon": "bi-cookie"},
    {"name": "Bootstrap RTL", "text": "تصميم متجاوب من اليمين لليسار، مع Carousel وAccordion.", "icon": "bi-bootstrap"},
    {"name": "Google Fonts", "text": "خط Reem Kufi للعناوين وTajawal للنصوص.", "icon": "bi-fonts"},
]
