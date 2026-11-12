# Saudi Design

## About the project

Saudi Design is an Arabic website that introduces Saudi identity, heritage, architecture, and contemporary design. Its goal is to help visitors explore how local crafts, materials, and visual traditions shape design in Saudi Arabia.

## Main features

- Seven connected pages covering the main design topics.
- Responsive layout for desktop, tablet, and mobile.
- Light and dark themes.
- Event cards that can be filtered by category.
- Heritage and architecture content with images and a short Al Sadu video.

## User stories

- As a visitor, I want to explore Saudi heritage so I can learn about local crafts and visual identity.
- As a visitor, I want to browse architecture, products, fashion, and graphic design examples in one place.
- As a visitor, I want to filter contemporary events so I can find the topics I care about.
- As a mobile visitor, I want the pages to fit my screen and remain easy to navigate.
- As a visitor, I want to switch the page theme to make reading comfortable.

## Requirements

- Python 3.12 or newer.
- Django 6.1.3 (listed in `requirements.txt`).

## Installation and run

Open the project folder in VS Code. In the integrated PowerShell terminal, run:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Then open <http://127.0.0.1:8000/> in your browser. Stop the server with `Ctrl+C`.

## How to use

1. Open the homepage and choose a design topic from the navigation or topic cards.
2. Browse the page sections to read about each craft, style, or project.
3. On the contemporary page, select a category to filter the event cards.
4. Use the theme button in the header to switch between light and dark mode.
5. Follow the external heritage links in the footer to explore official resources.

## Project structure

- `manage.py` — runs Django commands.
- `config/` — project settings and top-level routes.
- `website/` — page views, templates, CSS, JavaScript, and images.
- `requirements.txt` — Python package dependencies.
