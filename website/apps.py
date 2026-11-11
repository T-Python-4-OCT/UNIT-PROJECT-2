# This file sets up the website app.
from django.apps import AppConfig


# Set the app name and default model ID.
class WebsiteConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "website"
