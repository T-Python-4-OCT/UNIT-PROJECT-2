"""Fraud signs the local scanner looks for.

Every rule has: a short title, an explanation for the user, a weight (how risky it is),
and regex patterns. Patterns are written on NORMALIZED Arabic text
(أ إ آ -> ا , ة -> ه , ى -> ي , no tashkeel), see analyzer.normalize().
"""

OFFICIAL_NAMES = (
    "absher|alrajhi|rajhi|alahli|ncb|snb|riyadbank|sabb|alinma|albilad|stc|mobily|zain|"
    "sama|moi|najiz|tawakkalna|spl|saudipost|aramex|smsa|mada|zatca|gosi|qiwa|muqeem"
)

RULES = [
    {
        "key": "credentials",
        "title": "يطلب رمز تحقق أو بيانات سرية",
        "explain": "الجهات الرسمية والبنوك لا تطلب منك رمز التحقق أو كلمة المرور أو بيانات البطاقة أبداً.",
        "weight": 40,
        "patterns": [
            r"رمز (ال)?(تحقق|تفعيل|التاكيد|السري)", r"\bكود\b", r"\botp\b", r"كلمه (ال)?(مرور|سر)",
            r"(ال)?رقم (ال)?سري", r"\bpin\b", r"\bcvv\b", r"رقم (ال)?بطاق", r"بيانات (ال)?بطاق",
            r"تاريخ (ال)?انتهاء", r"بياناتك (ال)?بنكيه", r"password", r"verification code",
        ],
    },
    {
        "key": "personal_data",
        "title": "يطلب تحديث بياناتك الشخصية",
        "explain": "طلب رقم الهوية أو تحديث البيانات عبر رابط في رسالة من أشهر طرق سرقة الهوية.",
        "weight": 25,
        "patterns": [
            r"رقم (ال)?(هويه|اقامه)", r"(ال)?هويه (ال)?وطنيه", r"تحديث (ال)?بيانات", r"بياناتك (ال)?شخصيه",
            r"صوره (ال)?هويه", r"تاكيد (ال)?بيانات", r"update your (details|information)", r"\bverify (your|now)\b",
        ],
    },
    {
        "key": "short_link",
        "title": "رابط مختصر يخفي وجهته",
        "explain": "الروابط المختصرة تخفي الموقع الحقيقي، والمحتالون يستخدمونها حتى لا تنتبه لعنوان الموقع المزيف.",
        "weight": 25,
        "patterns": [r"\b(bit\.ly|tinyurl\.com|t\.co|cutt\.ly|goo\.gl|is\.gd|rb\.gy|shorturl\.at|t\.ly)/\S*"],
    },
    {
        "key": "fake_domain",
        "title": "رابط يقلّد اسم جهة رسمية",
        "explain": "عنوان الموقع فيه اسم جهة معروفة لكنه ليس موقعها الرسمي. المواقع الحكومية تنتهي بـ gov.sa.",
        "weight": 30,
        "patterns": [
            rf"\b(?:https?://)?(?:www\.)?[\w-]*(?:{OFFICIAL_NAMES})[\w-]*\.(?!gov\.sa\b|com\.sa\b|sa\b)[a-z]{{2,}}\S*",
            rf"\b(?:https?://)?[\w-]*(?:{OFFICIAL_NAMES})-[\w-]+\.\S+",
        ],
    },
    {
        "key": "link",
        "title": "يحتوي على رابط",
        "explain": "لا تفتح الروابط في الرسائل غير المتوقعة. ادخل للموقع الرسمي بكتابة عنوانه بنفسك.",
        "weight": 15,
        "patterns": [
            r"https?://\S+", r"\bwww\.\S+",
            r"\b[\w-]+\.(com|net|org|xyz|top|info|link|live|online|site|click|shop|vip|io|me|ly|cc)\b(/\S*)?",
        ],
    },
    {
        "key": "threat",
        "title": "تهديد بإيقاف أو عقوبة",
        "explain": "التخويف بإيقاف الحساب أو غرامة هدفه يخليك تتصرف بسرعة بدون تفكير.",
        "weight": 20,
        "patterns": [
            r"(ايقاف|تعليق|تجميد|اغلاق|حظر|الغاء) (حسابك|الحساب|بطاقتك|البطاقه|الخدمه|خدماتك|رقمك|اشتراكك)",
            r"سيتم (ايقاف|تعليق|تجميد|اغلاق|حظر|الغاء)", r"(مخالفه|غرامه|قضيه|محكمه)( (مروريه|ماليه))?",
            r"(suspended|blocked|locked)",
        ],
    },
    {
        "key": "urgency",
        "title": "يستعجلك",
        "explain": "الاستعجال من أقوى علامات الاحتيال. الجهة الحقيقية تعطيك وقت للتحقق.",
        "weight": 15,
        "patterns": [
            r"\bفورا\b", r"\bحالا\b", r"\bعاجل\b", r"خلال \d+ (ساعه|ساعات|دقيقه|دقائق)", r"خلال (ساعه|يوم)",
            r"(اخر|اخير) فرصه", r"اليوم فقط", r"قبل فوات", r"\bسارع\b", r"\bبادر\b", r"\burgent\b", r"immediately",
        ],
    },
    {
        "key": "prize",
        "title": "جائزة أو هدية مفاجئة",
        "explain": "ما فيه جائزة تجيك من سحب ما دخلته. الهدف إنك تدفع رسوم أو تعطي بياناتك.",
        "weight": 25,
        "patterns": [
            r"\bمبروك\b", r"\bفزت\b", r"\bربحت\b", r"\bكسبت\b", r"جائز", r"(ال)?سحب (ال)?(شهري|اسبوعي|على)",
            r"هديه مجانيه", r"\bرابح\b", r"congratulations", r"\bwinner\b", r"\bprize\b",
        ],
    },
    {
        "key": "money",
        "title": "يطلب دفع أو تحويل مال",
        "explain": "طلب رسوم بسيطة أو تحويل مبلغ مقابل خدمة أو جائزة نمط احتيال معروف.",
        "weight": 15,
        "patterns": [
            r"(حول|حولي|ارسل) (مبلغ|المبلغ)", r"\bحول(ي)? لي\b", r"رسوم (ال)?(شحن|توصيل|تفعيل|استلام|جمركيه|اداريه)",
            r"\bادفع\b", r"(سداد|دفع) (ال)?(رسوم|مبلغ|المبلغ)", r"\bعربون\b",
        ],
    },
    {
        "key": "relative",
        "title": "يدّعي إنه قريبك برقم جديد",
        "explain": "حيلة «أنا ولدك أو أخوك، هذا رقمي الجديد» منتشرة. اتصل على رقمه القديم قبل أي تحويل.",
        "weight": 30,
        "patterns": [
            r"(هذا|هذي) رقمي (ال)?جديد", r"رقمي (ال)?جديد", r"(جوالي|تلفوني) (خرب|ضاع|انكسر|انسرق)",
            r"(ضاع|خرب|انكسر|انسرق) (جوالي|تلفوني)", r"انا (اخوك|ولدك|بنتك|اختك|ابوك|امك)",
        ],
    },
    {
        "key": "too_good",
        "title": "عرض أحلى من الحقيقة",
        "explain": "الأرباح المضمونة والدخل اليومي العالي بدون خبرة وعود لا تتحقق.",
        "weight": 20,
        "patterns": [
            r"ارباح مضمونه", r"ربح (مضمون|يومي)", r"دخل يومي", r"عمل من (ال)?(منزل|بيت)", r"بدون خبره",
            r"(تداول|عملات رقميه|بيتكوين|كريبتو)", r"ضاعف (فلوسك|راس مالك|مبلغك)", r"استثمار (مضمون|بسيط)",
        ],
    },
    {
        "key": "impersonation",
        "title": "يذكر جهة رسمية أو بنك",
        "explain": "المحتالون ينتحلون أسماء البنوك والجهات الحكومية. تأكد من الجهة من قنواتها الرسمية فقط.",
        "weight": 10,
        "patterns": [
            r"\bبنك\b", r"\bمصرف\b", r"(ال)?راجحي", r"البنك (ال)?(الاهلي|المركزي)", r"بنك (ال)?رياض",
            r"\bابشر\b", r"\bساما\b", r"وزاره", r"(ال)?جوازات", r"\bالمرور\b", r"\bناجز\b", r"توكلنا",
            r"البريد (ال)?سعودي", r"\bسبل\b", r"ارامكس", r"سمسا", r"هيئه (ال)?زكاه", r"\bمدى\b",
        ],
    },
    {
        "key": "off_channel",
        "title": "يطلب التواصل خارج القنوات الرسمية",
        "explain": "طلب التواصل على واتساب أو رقم جوال شخصي بدل الرقم الرسمي للجهة علامة خطر.",
        "weight": 10,
        "patterns": [r"واتس(اب)?", r"تيليجرام|تلجرام", r"\b05\d{8}\b", r"\+?9665\d{8}\b", r"wa\.me/\S*"],
    },
]

# Rules that, together, are the classic scam signature (they lower the safety a lot)
DANGEROUS_PAIRS = [
    ("credentials", "link"),
    ("credentials", "short_link"),
    ("credentials", "fake_domain"),
    ("personal_data", "link"),
    ("personal_data", "fake_domain"),
    ("prize", "money"),
    ("impersonation", "fake_domain"),
    ("threat", "link"),
    ("too_good", "off_channel"),
    ("relative", "money"),
    ("relative", "urgency"),
]

# Words that mean the message is only WARNING you (like a real OTP message: "do not share this code")
SAFE_HINTS = [r"لا (ت)?شارك", r"لا تعطي", r"لا تفصح", r"لن (نطلب|يطلب)", r"do not share", r"never share"]

# Colors of the highlighted words inside the message:
# a rule with weight 25 or more is DANGEROUS (red), a lighter rule is SUSPICIOUS (yellow),
# and the SAFE_HINTS words are green (only when the whole message is safe).
# The same red keys are listed in main/css/style.css (mark.flag-...) and detector/css/detector.css (.flag-item...).
DANGER_WEIGHT = 25
