from pathlib import Path

import polib
from django.core.management.base import BaseCommand, CommandError

LOCALE_DIR = Path(__file__).resolve().parents[2] / "locale"


class Command(BaseCommand):
    help = "Compile the app's .po catalogs to .mo with polib (no GNU gettext needed)."

    def handle(self, *args, **options):
        catalogs = sorted(LOCALE_DIR.glob("*/LC_MESSAGES/django.po"))
        if not catalogs:
            raise CommandError("No translation catalogs found.")
        for path in catalogs:
            catalog = polib.pofile(str(path), check_for_duplicates=True)
            if not catalog.translated_entries() or catalog.untranslated_entries() or catalog.fuzzy_entries():
                raise CommandError(f"Incomplete catalog: {path}")
            catalog.save_as_mofile(str(path.with_suffix(".mo")))
            self.stdout.write(
                f"Compiled {path.parent.parent.name} ({len(catalog.translated_entries())} messages)"
            )
