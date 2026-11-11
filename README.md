# 🇸🇦 Hikayat Watan | حكاية وطن

## About the Project

**Hikayat Watan** is an interactive educational website dedicated to exploring the history, heritage, culture, and destinations of Saudi Arabia.

The website takes visitors on a journey through Saudi history, from ancient civilizations and the early Islamic era to the establishment and unification of the Kingdom and its modern development.

It combines historical information, real photographs, visual galleries, interactive timelines, and YouTube videos to provide an engaging digital experience.

The project also highlights the diversity of Saudi destinations, including major cities and regions such as Riyadh, Makkah, Madinah, Jeddah, AlUla, Abha, and the Eastern Province, with a special focus on Al Ahsa.

---

## Website Pages

The website includes the following pages:

- **Home:** Introduces Saudi Arabia and highlights the main sections and destinations.
- **History:** Explores the major historical periods of Saudi Arabia.
- **Historical Period Details:** Provides detailed information about each historical period.
- **Cities & Destinations:** Displays the featured Saudi cities and regions.
- **City Details:** Provides information, photographs, galleries, attractions, and videos for each destination.
- **About:** Introduces the purpose and goals of Hikayat Watan.

---

## Main Features

- Interactive homepage with visual content.
- Historical timeline covering major periods of Saudi history.
- Dedicated pages for Saudi cities and regions.
- Eastern Province destination featuring Al Ahsa and its historical landmarks.
- Real photographs and historical image collections.
- Individual YouTube videos embedded directly into destination pages.
- Historical and cultural information.
- Tourist attractions and important landmarks.
- Previous and next destination navigation.
- Arabic and English language support.
- Dark Mode and Light Mode.
- Cookie-based theme and language preferences.
- Interactive navigation menus.
- Responsive design for desktop, tablet, and mobile devices.

---

## Technologies Used

- Python
- Django
- HTML5
- CSS3
- JavaScript
- Bootstrap 5
- JSON
- Google Translate
- YouTube Embedded Player

---

## Project Structure

```text
UNIT-PROJECT-2/
│
├── hikayat_watan/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── watan/
│   ├── data/
│   │   └── content.json
│   │
│   ├── templates/
│   │   └── watan/
│   │
│   ├── static/
│   │   └── watan/
│   │       ├── css/
│   │       ├── images/
│   │       ├── js/
│   │       └── video/
│   │
│   ├── templatetags/
│   ├── __init__.py
│   ├── apps.py
│   ├── context_processors.py
│   ├── data_loader.py
│   ├── urls.py
│   └── views.py
│
├── manage.py
├── requirements.txt
├── PROJECT_REQUIREMENTS.md
└── README.md
```

---

## Content Management

Website content is stored in:

```text
watan/data/content.json
```

The JSON file contains the information displayed throughout the website, including:

- Saudi cities and destinations.
- Historical periods.
- Destination descriptions.
- Tourist attractions.
- Image gallery information.
- YouTube video IDs.
- Historical timelines and events.

The Eastern Province has been added as an additional destination, highlighting Al Ahsa and its historical and natural attractions.

The destination includes information about:

- Al Ahsa Oasis.
- Qara Mountain.
- Ibrahim Palace.
- Qaisariya Market.
- Jawatha Mosque.
- Yellow Lake.
- Ithra.
- Al Khobar Corniche.

Content is managed through JSON files without requiring a database.

---

## Images and Media

Images and media files are stored locally within the project's static directory.

The website uses real photographs to represent Saudi cities, historical landmarks, and cultural heritage.

The historical homepage cards feature dedicated images for:

- Pre-Islamic Civilizations.
- The Early Islamic Era.
- Historic Hejaz.
- The First Saudi State.
- The Second Saudi State.
- The Founding and Unification of Saudi Arabia.

Additional destination images are used throughout the website.

YouTube videos are embedded directly into the website, allowing visitors to watch videos without leaving the destination pages.

---

## Theme Preferences

The website supports two display modes:

- Dark Mode.
- Light Mode.

The selected theme is saved in a browser cookie named:

```text
watan-theme
```

The preference is saved for one year and automatically restored when the visitor returns to the website.

Theme preferences are managed through cookies without relying on Local Storage.

---

## Language Support

Hikayat Watan supports:

- Arabic.
- English.

Visitors can switch between languages using the language button in the navigation bar.

The selected language is saved in a browser cookie named:

```text
watan-language
```

Google Translate provides the translation functionality and requires an internet connection.

---

## Installation and Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Development Server

```bash
python manage.py runserver
```

### 3. Open the Website

Visit:

```text
http://127.0.0.1:8000/
```

---

## Main Website URLs

| Page | URL |
|---|---|
| Home | `/` |
| History | `/history/` |
| Historical Period | `/history/<era_slug>/` |
| Cities & Destinations | `/cities/` |
| Destination Details | `/city/<city_slug>/` |
| Eastern Province | `/city/eastern-province/` |
| About | `/about/` |

---

## Project Vision

Hikayat Watan aims to preserve and present the story of Saudi Arabia through an engaging digital experience.

It highlights the Kingdom's rich history, cultural heritage, remarkable cities, diverse regions, and continuous development.

The project brings together the past and present, allowing visitors to discover the stories, landmarks, and traditions that make Saudi Arabia unique.

**A land with a story. A history worth remembering.** 🇸🇦