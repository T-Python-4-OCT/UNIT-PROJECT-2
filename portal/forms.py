import re

from django import forms

from .models import Feedback

# Arabic letters (U+0621-U+064A) and English letters, plus spaces, hyphens and apostrophes.
NAME_PATTERN = re.compile(r"^[A-Za-zء-ي\s'\-]+$")
LINK_PATTERN = re.compile(r"https?://|www\.", re.IGNORECASE)
LETTER_PATTERN = re.compile(r"[A-Za-zء-ي]")

MAX_LINKS = 2


class FeedbackForm(forms.Form):
    """
    Server-side validation for the feedback page.

    All error messages come from feedback.json, so the same form
    shows its errors in Arabic or English depending on the language.
    """

    name = forms.CharField(min_length=2, max_length=60)
    email = forms.EmailField(max_length=254)
    category = forms.ChoiceField()
    rating = forms.TypedChoiceField(coerce=int, widget=forms.RadioSelect)
    message = forms.CharField(min_length=20, max_length=1000, widget=forms.Textarea)

    # Honeypot: hidden from people with CSS, bots tend to fill every field.
    website = forms.CharField(required=False)

    def __init__(self, *args, text, **kwargs):
        super().__init__(*args, **kwargs)
        errors = text["errors"]

        for field in self.fields.values():
            field.error_messages["required"] = errors["required"]

        self.fields["name"].error_messages.update(
            min_length=errors["name_min"], max_length=errors["name_max"]
        )
        self.fields["email"].error_messages.update(
            invalid=errors["email_invalid"], max_length=errors["email_invalid"]
        )
        self.fields["message"].error_messages.update(
            min_length=errors["message_min"], max_length=errors["message_max"]
        )

        # Values come from the model, labels from the language file.
        self.fields["category"].choices = [("", text["category_placeholder"])] + [
            (value, text["categories"][value]) for value in Feedback.Category.values
        ]
        self.fields["category"].error_messages["invalid_choice"] = errors["category_invalid"]

        self.fields["rating"].choices = [
            (number, label) for number, label in enumerate(text["rating_labels"], start=1)
        ]
        self.fields["rating"].error_messages["invalid_choice"] = errors["rating_invalid"]

        self.errors_text = errors

    def clean_name(self):
        name = " ".join(self.cleaned_data["name"].split())

        if not NAME_PATTERN.match(name):
            raise forms.ValidationError(self.errors_text["name_invalid"])

        return name

    def clean_email(self):
        return self.cleaned_data["email"].lower()

    def clean_message(self):
        message = self.cleaned_data["message"]

        if not LETTER_PATTERN.search(message):
            raise forms.ValidationError(self.errors_text["message_meaningless"])

        if len(LINK_PATTERN.findall(message)) > MAX_LINKS:
            raise forms.ValidationError(self.errors_text["message_links"])

        return message

    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data.get("website"):
            raise forms.ValidationError(self.errors_text["spam"])

        return cleaned_data

    def save(self, language):
        data = self.cleaned_data
        return Feedback.objects.create(
            name=data["name"],
            email=data["email"],
            category=data["category"],
            rating=data["rating"],
            message=data["message"],
            language=language,
        )
