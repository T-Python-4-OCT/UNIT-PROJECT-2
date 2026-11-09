# UNIT-PROJECT-2 — Project Requirements Checklist

## Project theme
**Hikayat Watan — Saudi Arabia's Cities, Heritage & Culture**

## Minimum requirements and implementation

| Requirement | Implementation | Status |
|---|---|---|
| Use Django | Django project with `saudi_heritage` configuration and `kingdom` app | Complete |
| Templates and template inheritance | Shared `templates/kingdom/base.html`; all pages extend the base template | Complete |
| Dynamic URLs where applicable | City and story detail routes use `<slug:slug>` | Complete |
| Static files | CSS, JavaScript and supporting graphics are in `static/` | Complete |
| Homepage + at least 6 pages | Homepage, six dynamic city detail pages, a dedicated Kingdom history page, stories and about pages | Complete |
| Coherent, uniform design | Shared navigation, footer, typography, spacing, colors and reusable components | Complete |
| Dark and light mode | Theme toggle saves the selection in the `saudi-heritage-theme` browser cookie | Complete |
| Arabic and English | Django language switch saves the selected language in the `saudi-heritage-language` cookie; all main pages and content have English translations | Complete |
| Responsive design | Bootstrap 5 RTL/LTR stylesheets plus responsive custom CSS breakpoints | Complete |
| City photos | Each city page has a photo gallery with image source credits | Complete |
| City video | Each city detail page embeds a related YouTube video | Complete |
| City attractions, history and events | Dynamic content is provided for all six cities | Complete |

## Pages

- `/` — Homepage and city directory.
- `/city/riyadh/` — Riyadh.
- `/city/abha/` — Abha.
- `/city/makkah/` — Makkah.
- `/city/alula/` — AlUla.
- `/city/jeddah/` — Jeddah.
- `/city/madinah/` — Madinah.
- `/history/` — Kingdom history timeline, kings, national occasions and image gallery.
- `/stories/` — Selected Quranic stories.
- `/stories/<slug>/` — Story detail.
- `/about/` — Project information and requirements checklist.

## Data and database

The project does not use a database. Django is configured with the Dummy Database Backend. City and story content is stored in `kingdom/data.py`; English translations are stored in `kingdom/localization.py`; Kingdom history, kings and national occasions are stored in `kingdom/history_data.py`. The views pass this content to Django templates. No migrations or database setup are required.

## Run locally

```bash
python -m venv .venv
```

Windows:

```powershell
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py runserver
```

macOS / Linux:

```bash
source .venv/bin/activate
pip install -r requirements.txt
python manage.py runserver
```

Open `http://127.0.0.1:8000/` in your browser.

## Image and video note

City and history photographs are referenced from Wikimedia Commons. Their source pages and credits are provided in the website and `IMAGE_CREDITS.md`. Please retain the visible image credit/source link when reusing the project. Embedded city videos are served by YouTube and require an internet connection.
