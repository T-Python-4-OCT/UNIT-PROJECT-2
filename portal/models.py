from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Feedback(models.Model):
    "A message sent from the Share Your Feedback page."

    class Category(models.TextChoices):
        SUGGESTION = "suggestion", "Suggestion"
        QUESTION = "question", "Question"
        ISSUE = "issue", "Content issue"
        PRAISE = "praise", "Praise"

    # Each field becomes a column in the portal_feedback table (see migrations/0001_initial.py)
    name = models.CharField(max_length=60)
    email = models.EmailField()
    category = models.CharField(max_length=20, choices=Category.choices)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    message = models.TextField(max_length=1000)
    language = models.CharField(max_length=2, default="en")  # which language the visitor used
    created_at = models.DateTimeField(auto_now_add=True)  # set by Django when the row is created

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "feedback"

    def __str__(self):
        "How a row is named in the admin list."
        return f"{self.name} · {self.get_category_display()}"
