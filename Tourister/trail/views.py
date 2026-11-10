from django.http import Http404
from .data import CITIES, CITIES_BY_SLUG, TIPS, FAQS
from django.shortcuts import render, redirect
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

@require_POST
def toggle_theme(request):
    new = "light" if request.COOKIES.get("theme") == "dark" else "dark"
    next_url = request.POST.get("next", "/")
    if not url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        next_url = "/"
    response = redirect(next_url)
    response.set_cookie("theme", new, max_age=60 * 60 * 24 * 365, samesite="Lax")
    return response

def get_ordered_cities():
    return sorted(CITIES, key=lambda c: c["order"])


def home(request):
    return render(request, "trail/home.html", {
        "cities": get_ordered_cities(),
        "tips": TIPS,
        "faqs": FAQS,
    })


def city_detail(request, slug):
    city = CITIES_BY_SLUG.get(slug)
    if city is None:
        raise Http404("المدينة غير موجودة")

    ordered = get_ordered_cities()
    i = ordered.index(city)
    prev_city = ordered[i - 1] if i > 0 else None
    access_origin = CITIES_BY_SLUG.get(city.get("access_origin"), prev_city)

    return render(request, "trail/city_detail.html", {
        "city": city,
        "cities": ordered,
        "prev_city": prev_city,
        "access_origin": access_origin,
        "next_city": ordered[i + 1] if i < len(ordered) - 1 else None,
    })


def terms(request):
    return render(request, "trail/legal_page.html", {
        "page_title": "الشروط والأحكام",
        "page_intro": "باستخدامك هذا الموقع، فإنك توافق على الشروط التالية. هذا الموقع تجريبي وغير رسمي، ولا يمثل الهيئة السعودية للسياحة أو أي جهة حكومية.",
        "sections": [
            {
                "title": "طبيعة المحتوى",
                "text": "يُقدّم الموقع معلومات إرشادية عن مسار الشمال ووجهاته لأغراض التعريف والتخطيط الأولي. قد تتغير المسافات والطرق ومواعيد المواقع والخدمات؛ لذلك تحقّق من المعلومات لدى الجهات الرسمية ومقدمي الخدمة قبل السفر.",
            },
            {
                "title": "سلامة الرحلة",
                "text": "أنت مسؤول عن تخطيط رحلتك واتباع أنظمة المرور وتعليمات السلامة والتحقق من حالة الطقس والطرق. لا يعتمد الموقع بديلاً عن الإرشادات الرسمية أو خدمات الطوارئ.",
            },
            {
                "title": "الروابط الخارجية والملكية",
                "text": "قد يتضمن الموقع روابط لخدمات ووجهات خارجية مثل الخرائط. تخضع هذه المواقع لشروط وسياسات الجهات المشغلة لها، ولا يتحكم هذا الموقع في محتواها أو توفرها. تعود حقوق العلامات والصور والمحتوى لأصحابها.",
            },
            {
                "title": "تحديث الشروط",
                "text": "قد تُحدّث هذه الشروط عند الحاجة. استمرارك في استخدام الموقع بعد نشر التحديث يعني اطلاعك على النسخة المنشورة.",
            },
        ],
    })


def privacy(request):
    return render(request, "trail/legal_page.html", {
        "page_title": "سياسة الخصوصية",
        "page_intro": "نوضح هنا باختصار ما يتعامل معه هذا الموقع التجريبي من بيانات عند تصفحه.",
        "sections": [
            {
                "title": "المعلومات التي نجمعها",
                "text": "لا يطلب الموقع إنشاء حساب ولا يطلب بيانات شخصية لإتاحة محتواه. لا تُرسل بيانات النماذج إلى الموقع لأنه لا يحتوي على نماذج لجمعها.",
            },
            {
                "title": "ملفات تعريف الارتباط",
                "text": "يستخدم الموقع ملف ارتباط لحفظ اختيار الوضع الفاتح أو الداكن على جهازك لمدة تصل إلى سنة. يمكنك حذف ملفات الارتباط أو منعها من إعدادات المتصفح، وقد لا يُحفظ اختيارك بعد ذلك.",
            },
            {
                "title": "الخدمات الخارجية",
                "text": "عند فتح روابط الخرائط أو المواقع الخارجية، قد تتلقى تلك الجهات بيانات وفق سياساتها الخاصة. ننصح بمراجعة سياسات الخصوصية لدى مزودي الخدمات قبل استخدامها.",
            },
            {
                "title": "تغييرات السياسة",
                "text": "قد نحدّث هذه السياسة إذا تغيرت وظائف الموقع. ستُنشر النسخة الأحدث في هذه الصفحة.",
            },
        ],
    })