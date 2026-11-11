# Vision Atlas 🇸🇦

🌐 **Live Demo:** https://vision-atlas.onrender.com

A bilingual (English / Arabic) Django website that takes you on a visual journey through the giga-projects of **Saudi Vision 2030**.

Built as **UNIT-PROJECT-2** for the Tuwaiq Academy bootcamp.

> ⏳ The site is hosted on Render's free plan, so the first visit after a period of inactivity may take up to a minute to load.

---

## ✨ Features

### Core
- **8 pages**: Home, About Vision 2030, and 6 project pages
- **Dynamic URLs**: one route `project/<slug>/` serves every project
- **Template inheritance**: `base.html` → `project_base.html` → one template per project
- **Dark / Light mode** saved with **cookies** and **URL parameters**
- **English / Arabic** with a full **RTL** layout, also saved with cookies
- **Responsive design** with Bootstrap 5 (desktop, tablet and mobile)
- Project content stored in a **JSON** file with English and Arabic versions
- Custom **404 page** in the site's design

### Experience
- 🗺️ **Interactive 3D map** of the Kingdom: click a project and the camera flies to it, showing a card with its image, numbers and a link to its page
- **Map / Grid toggle** to switch between the map and project cards
- Full-screen **video hero** with a transparent navbar that turns to glass on scroll
- **Scrollytelling** story sections where images change as you scroll
- Attractions in a **zigzag layout** on desktop and a **swipe slider** on mobile
- **About page** with Vision 2030 targets, real **achievements** from the 2025 annual report, and a live **countdown to 2030**
- **Animated counters**, scroll progress bar and reveal-on-scroll effects
- Navbar with a **projects dropdown** and a footer with each project's **official accounts**

### Performance & Deployment
- Hero videos hosted on **Cloudinary CDN** with automatic compression
- Images compressed and lazy-loaded
- **Deployed on Render** with Gunicorn and WhiteNoise, auto-deploys on every push

## 📄 Pages

| Page | URL |
|---|---|
| Home | `/` |
| About Vision 2030 | `/about/` |
| NEOM | `/project/neom/` |
| The Red Sea | `/project/red-sea/` |
| Qiddiya | `/project/qiddiya/` |
| Diriyah | `/project/diriyah/` |
| ROSHN | `/project/roshn/` |
| AlUla | `/project/alula/` |

Each project page includes: a title and catchy phrase, a video, the project story, top attractions, an image gallery, a timeline, major events, and the project's official accounts.

## 🍪 How Theme and Language Work

Both settings work **without JavaScript**, using Django views, URL parameters and cookies:

1. Clicking the toggle opens a link like `/theme/?theme=dark&next=/about/`
2. The view reads the URL parameter, saves it in a cookie, and redirects back to the page
3. Every template reads the cookie with `request.COOKIES` and renders the right theme or language

## 🧱 Code Organization

The code follows **separation of concerns**:

| Layer | Where | Role |
|---|---|---|
| Data | `projects.json` | Content only (EN + AR) |
| Logic | Helper functions in `views.py` (`localize`, `build_map_data`, `safe_redirect`) | Shape the data |
| Views | `home`, `project_detail`, `about`, `set_theme`, `set_language` | Read the request, call helpers, render |
| Templates | `templates/main/` | Presentation only |

## 🛠️ Built With

- Python 3 & Django 5.2
- Bootstrap 5.3 (LTR and RTL) & Bootstrap Icons
- MapLibre GL JS & OpenFreeMap for the 3D map
- HTML, CSS, JavaScript (design effects only)
- Google Fonts: Space Grotesk, Inter, IBM Plex Sans Arabic
- Cloudinary for video hosting
- Gunicorn & WhiteNoise for production
- Render for hosting

## 🚀 Run Locally

```bash
git clone https://github.com/JZL9/UNIT-PROJECT-2.git
cd UNIT-PROJECT-2

python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS / Linux

pip install -r vision_atlas/requirements.txt

cd vision_atlas
python manage.py runserver
```

Then open `http://127.0.0.1:8000/`

## ☁️ Deployment (Render)

| Setting | Value |
|---|---|
| Root Directory | `vision_atlas` |
| Build Command | `pip install -r requirements.txt && python manage.py collectstatic --no-input` |
| Start Command | `gunicorn vision_atlas.wsgi:application` |

Environment variables: `SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS=.onrender.com`

## 📁 Project Structure

```
vision_atlas/
├── manage.py
├── requirements.txt
├── vision_atlas/              # project settings and main urls
└── main/                      # the app
    ├── data/projects.json     # projects content (EN + AR) and map coordinates
    ├── views.py               # helpers and views
    ├── urls.py
    ├── static/main/
    │   ├── css/style.css
    │   ├── js/design.js       # design effects, countdown and map
    │   └── images/            # images per project and favicon
    └── templates/
        ├── 404.html
        └── main/
            ├── base.html          # navbar, footer, theme and language
            ├── home.html          # hero, map, projects and pillars
            ├── about.html         # targets, achievements and countdown
            ├── project_base.html  # shared layout for project pages
            └── projects/          # one template per project with its story
```

## 🙏 Credits

Information, images and videos belong to their official owners: Saudi Vision 2030, NEOM, Red Sea Global, Qiddiya, Diriyah Company, ROSHN and the Royal Commission for AlUla. Map data © OpenStreetMap contributors, map tiles by OpenFreeMap. Used for educational purposes only.

---

Made by **Fahad Al-Otaibi**