from django.apps import AppConfig


class ProjectsConfig(AppConfig):
    name = "saudi_atlas.projects"
    label = "projects"

    def ready(self):
        from .content import debug_validate

        debug_validate()
