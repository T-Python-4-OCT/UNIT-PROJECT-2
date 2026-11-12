# 🇸🇦 Hikayat Watan | حكاية وطن

## About the Project

**Hikayat Watan** is an interactive educational website that explores Saudi Arabia's history, heritage, culture, and destinations.

The website presents historical information, Saudi rulers, real photographs, galleries, and videos in an engaging digital experience.

## Website Pages

- **Home:** Introduction to Saudi Arabia.
- **History:** Historical periods and rulers of Saudi Arabia.
- **Cities:** Featured cities and regions.
- **City Details:** Attractions, galleries, information, and videos.
- **About:** Project goals and purpose.

## Main Features

- Interactive homepage.
- Historical timelines and rulers' profiles.
- Saudi cities and destinations.
- Special coverage of the Eastern Province and Al Ahsa.
- Real photographs and image galleries.
- Embedded YouTube videos.
- Arabic and English support.
- Dark Mode and Light Mode.
- Cookie-based preferences.
- Responsive design for all devices.
- Previous and next navigation.

## Technologies Used

- Python & Django
- HTML5, CSS3 & JavaScript
- Bootstrap 5
- JSON
- Google Translate
- YouTube Embed

## Project Structure

```text
UNIT-PROJECT-2/
│
├── hikayat_watan/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── watan/
│   ├── data/content.json
│   ├── templates/watan/
│   ├── static/watan/
│   │   ├── css/
│   │   ├── img/
│   │   ├── js/
│   │   └── video/
│   ├── templatetags/
│   ├── views.py
│   ├── urls.py
│   └── data_loader.py
│
├── manage.py
├── requirements.txt
├── PROJECT_REQUIREMENTS.md
└── README.md
```

## Content Management

Website content is stored in:

`watan/data/content.json`

It includes:
- Historical periods and rulers.
- Cities and destinations.
- Tourist attractions.
- Image galleries and YouTube videos.
- Historical events and descriptions.

The project uses JSON for content management without requiring a database.

## Images and Media

Images are stored locally in the static directory.

The website uses real photographs of Saudi landmarks and rulers where available. For historical figures without verified portraits, related historical landmarks are displayed instead.

YouTube videos are embedded directly into destination pages.

## Theme and Language

- Dark and Light modes are saved using the `watan-theme` cookie.
- Arabic and English language preferences are saved using the `watan-language` cookie.
- Google Translate requires an internet connection.

Both preferences are saved for one year.

## Installation

**1. Install dependencies:**

```bash
pip install -r requirements.txt
```

**2. Run the server:**

```bash
python manage.py runserver
```

**3. Open the website:**

`http://127.0.0.1:8000/`

## Main URLs

| Page | URL |
|---|---|
| Home | `/` |
| History | `/history/` |
| Historical Period | `/history/<era_slug>/` |
| Cities | `/cities/` |
| City Details | `/city/<city_slug>/` |
| About | `/about/` |

## Project Vision

Hikayat Watan aims to present Saudi Arabia's history, heritage, and destinations through an engaging digital experience.

**A land with a story. A history worth remembering.** 🇸🇦