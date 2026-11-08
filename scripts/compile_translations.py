from pathlib import Path

import polib


root = Path(__file__).resolve().parent.parent
catalogs = sorted((root / "locale").glob("*/LC_MESSAGES/django.po"))
if not catalogs:
    raise SystemExit("No project translation catalogs found.")

for path in catalogs:
    catalog = polib.pofile(str(path), check_for_duplicates=True)
    if not catalog.translated_entries() or catalog.untranslated_entries() or catalog.fuzzy_entries():
        raise SystemExit(f"Incomplete catalog: {path.relative_to(root)}")
    catalog.save_as_mofile(str(path.with_suffix(".mo")))
    print(f"Compiled {path.relative_to(root)} ({len(catalog.translated_entries())} messages)")
