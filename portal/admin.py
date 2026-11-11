from django.contrib import admin

from .models import Feedback


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "rating", "language", "created_at")
    list_filter = ("category", "rating", "language")
    search_fields = ("name", "email", "message")
    readonly_fields = ("created_at",)
