# Sinaat Al-Ezz | Saudi Military Industries

A Django website about the military industries of Saudi Arabia and the Kingdom's journey from importing arms to manufacturing them locally under Vision 2030.

> **Made in Saudi Arabia… to protect Saudi Arabia**

---

## Pages

| URL | Page | Content |
|---|---|---|
| `/` | Home | Hero video, key numbers, about, entities, sectors |
| `/sector/<name>/` | Sector (`land`, `air`, `naval`) | Photo gallery, highlights, timeline, events |
| `/company/<name>/` | Entity (`sami`, `gami`) | About, photos, highlights, timeline |
| `/vision/` | Vision 2030 | The goal, progress in numbers, localization calculator, pillars |
| `/history/` | History | Timeline from the Al-Kharj factories to today |
| `/events/` | Events | Upcoming World Defense Show with a days countdown, and past editions |
| `/careers/` | Careers | Official training and job programs, and in-demand majors |

The sector and entity pages are **dynamic**: one template (`details.html`) shows any sector or entity based on the URL.

## Features

- **Two languages:** Arabic (right to left) and English (left to right). Your choice is saved.
- **Dark and light mode.**
- **Responsive** on phones, tablets and desktops.
- **Localization calculator:** enter a spending amount to see the local share today and the target for 2030.
- **Event countdown:** shows how many days are left until the next World Defense Show.
- **QR code:** opens the current page on your phone.
- **Image lightbox:** click any photo to view it full screen.

## Built With

- Python and Django
- Django templates with inheritance (`base.html`)
- Bootstrap 5 and Bootstrap Icons
- Cairo and IBM Plex Sans Arabic fonts
- JavaScript for dark mode, the calculator, the QR code and the lightbox

## Project Structure

```
SaudiDefense/
├── manage.py
├── IMAGE_CREDITS.md            # sources of all photos and video
├── SaudiDefense/               # project settings and main urls
└── main/
    ├── views.py                # one view per page
    ├── urls.py                 # routes, including dynamic ones
    ├── data.py                 # site content in Arabic and English
    ├── translations.py         # interface text in Arabic and English
    ├── context_processors.py   # sends language and texts to every page
    ├── templates/main/
    │   ├── base.html           # navbar, footer and shared layout
    │   ├── index.html          # home
    │   ├── details.html        # sector and entity pages
    │   ├── vision.html
    │   ├── history.html
    │   ├── events.html
    │   └── careers.html
    └── static/
        ├── css/style.css
        ├── js/                 # theme, effects, calculator, QR, lightbox
        ├── images/             # logo and photos
        └── videos/             # home page video
```

## Run Locally

```bash
pip install django
cd SaudiDefense
python manage.py runserver
```

Then open `http://127.0.0.1:8000`

## Image Credits

Photos and video are from the Saudi Press Agency, the General Authority for Military Industries (GAMI) and Saudi Arabian Military Industries (SAMI). Full details are in [IMAGE_CREDITS.md](SaudiDefense/IMAGE_CREDITS.md).

This is an educational project for a Python bootcamp. All images belong to their owners.

---

**Morad** · UNIT-PROJECT-2
