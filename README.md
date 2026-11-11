# 🇸🇦 Hikayat Watan | حكاية وطن

## About the Project

**Hikayat Watan** is an interactive educational website dedicated to exploring the history, heritage, culture, and cities of Saudi Arabia.

The website takes visitors on a journey through Saudi history, from the establishment of the first Saudi state to the modern Kingdom and its ongoing development.

It combines historical information, real photographs, visual galleries, and city-specific videos to provide an engaging experience.

## Website Pages

The website includes the following pages:

- **Home:** Introduces Saudi Arabia and highlights the main sections of the website.
- **History:** Explores the major historical periods of Saudi Arabia.
- **Historical Period Details:** Provides information about each historical period.
- **Cities:** Displays the featured Saudi cities.
- **City Details:** Provides information, photographs, galleries, and videos for each city.
- **About:** Introduces the purpose and goals of Hikayat Watan.

## Main Features

- Interactive homepage with visual content.
- Historical timeline covering major periods of Saudi history.
- Dedicated pages for Saudi cities.
- Real photographs and image galleries.
- Individual YouTube videos for each city, embedded directly into the website.
- Historical and cultural information.
- Previous and next city navigation.
- Arabic and English language support.
- Dark Mode and Light Mode.
- Responsive design for desktop, tablet, and mobile devices.
- Interactive navigation menus.

## Technologies Used

- Python
- Django
- HTML5
- CSS3
- JavaScript
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
│   ├── data/
│   │   └── content.json
│   ├── templates/
│   │   └── watan/
│   ├── static/
│   ├── templatetags/
│   ├── views.py
│   ├── urls.py
│   ├── apps.py
│   └── context_processors.py
│
├── manage.py
├── requirements.txt
├── PROJECT_REQUIREMENTS.md
└── README.md
```

## Content Management

Website content is stored in:

```text
watan/data/content.json
```

The JSON file contains the information displayed throughout the website, including cities, historical periods, and other content.

City information, images, and YouTube video IDs are managed through the project's content data.

The website does not require a database to store its main content.

## Theme Preferences

The website supports two display modes:

- Dark Mode
- Light Mode

The selected theme is saved in a browser cookie named:

```text
watan-theme
```

The preference is saved for one year and restored when the visitor returns to the website.

## Language Support

Hikayat Watan supports:

- Arabic
- English

Visitors can switch between languages using the language button in the navigation bar.

The selected language is saved in a browser cookie named:

```text
watan-language
```

Google Translate is used to provide translation functionality and requires an internet connection.

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

## Main Website URLs

| Page | URL |
|---|---|
| Home | `/` |
| History | `/history/` |
| Historical Period | `/history/<era_slug>/` |
| Cities | `/cities/` |
| City Details | `/city/<city_slug>/` |
| About | `/about/` |

## Project Vision

Hikayat Watan aims to preserve and present the story of Saudi Arabia through an engaging digital experience.

It highlights the Kingdom's rich history, cultural heritage, remarkable cities, and continuous development.

**A land with a story. A history worth remembering.** 🇸🇦