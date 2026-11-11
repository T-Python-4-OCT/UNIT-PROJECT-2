from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Feedback(models.Model):
    "A message sent from the Share Your Feedback page."

    class Category(models.TextChoices):
        SUGGESTION = "suggestion", "Suggestion"
        QUESTION = "question", "Question"
        ISSUE = "issue", "Content issue"
        PRAISE = "praise", "Praise"

    name = models.CharField(max_length=60)
    email = models.EmailField()
    category = models.CharField(max_length=20, choices=Category.choices)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    message = models.TextField(max_length=1000)
    language = models.CharField(max_length=2, default="en")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "feedback"

    def __str__(self):
        return f"{self.name} · {self.get_category_display()}"
