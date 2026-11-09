"""The 4 kinds of reports a user can send."""

REPORT_TYPES = {
    "sms": {"title": "رسالة نصية", "icon": "bi-chat-dots", "contact_label": "رقم المرسل", "placeholder": "مثال: 0551234567 أو اسم المرسل"},
    "call": {"title": "مكالمة هاتفية", "icon": "bi-telephone", "contact_label": "رقم المتصل", "placeholder": "مثال: 0551234567"},
    "email": {"title": "بريد إلكتروني", "icon": "bi-envelope", "contact_label": "بريد المرسل", "placeholder": "مثال: support@fake-bank.com"},
    "social": {"title": "تواصل اجتماعي", "icon": "bi-at", "contact_label": "اسم الحساب ومنصته", "placeholder": "مثال: @offers_sa على إنستقرام"},
}
