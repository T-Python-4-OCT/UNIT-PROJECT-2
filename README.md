# SAUDI INDUSTRY 

A Django-powered educational website showcasing Saudi Arabia's industrial development, manufacturing companies, industrial cities, locally manufactured products, advanced technologies, and Vision 2030.

**Repository:** https://github.com/MMutairi/UNIT-PROJECT-2

> This is an independent educational project and is not affiliated with the Saudi government or the companies featured.

## Features

- Nine main pages with dynamic detail pages
- Search and filtering by industry, category, and location
- Responsive design using Bootstrap 5
- Light and dark mode
- Cinematic HTML5 video backgrounds
- Images and videos hosted locally or through Cloudinary
- JSON-based content management
- Automated Django tests

## Website Pages

| Page | URL |
|---|---|
| Home | `/` |
| Industries | `/industries/` |
| Companies | `/companies/` |
| Industrial Cities | `/industrial-cities/` |
| Made in Saudi | `/made-in-saudi/` |
| Technology | `/technology/` |
| Vision 2030 | `/vision-2030/` |
| Gallery | `/gallery/` |
| About | `/about/` |

Detail pages are also available, such as `/companies/sabic/`.

## Technology Stack

- Python 3.11
- Django 5.2.19
- HTML5, CSS3, JavaScript
- Bootstrap 5.3.3
- WhiteNoise
- python-dotenv
- Cloudinary CDN
- JSON files for website content
- SQLite for Django's built-in database features

## Project Structure

```text
UNIT-PROJECT-2/
├── README.md
└── SAUDI INDUSTRY/
    ├── manage.py
    ├── requirements.txt
    ├── saudi_industry/
    │   ├── settings.py
    │   ├── urls.py
    │   ├── asgi.py
    │   └── wsgi.py
    ├── apps/
    │   ├── core/
    │   └── catalog/
    ├── data/
    ├── templates/
    │   ├── base.html
    │   ├── includes/
    │   ├── core/
    │   └── catalog/
    └── static/
        ├── css/
        ├── js/
        ├── icons/
        └── images/
```

## Installation

### 1. Clone the repository

```powershell
git clone https://github.com/MMutairi/UNIT-PROJECT-2.git
cd "UNIT-PROJECT-2/SAUDI INDUSTRY"
```

### 2. Create a virtual environment

Python 3.11 is recommended.

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If your existing `.venv` references an unavailable Python interpreter, deactivate it and recreate the environment.

### 3. Install dependencies

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file inside `SAUDI INDUSTRY/`, alongside `manage.py`.

Generate a secret key:

```powershell
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Add the following to `.env`:

```dotenv
DJANGO_SECRET_KEY=YOUR_GENERATED_SECRET_KEY
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
DJANGO_HTTPS_ENABLED=False
```

**Important:** `DJANGO_SECRET_KEY` is required. Never commit `.env` or expose your actual secret key.

For production, the settings also support `DJANGO_CSRF_TRUSTED_ORIGINS` as a comma-separated list of trusted origins.

### 5. Initialize the database

```powershell
python manage.py migrate
```

### 6. Start the development server

```powershell
python manage.py runserver
```

Open http://127.0.0.1:8000/.

## Testing

Run the Django configuration checks:

```powershell
python manage.py check
```

Run the automated tests:

```powershell
python manage.py test
```

For detailed results:

```powershell
python manage.py test --verbosity 2
```

Tests are maintained in `apps/catalog/tests.py` and `apps/core/tests.py`.

## Content Management

Website content is maintained in JSON files under `SAUDI INDUSTRY/data/`.

| File | Content |
|---|---|
| `home.json` | Homepage |
| `industries.json` | Industrial sectors |
| `companies.json` | Industrial companies |
| `industrial_cities.json` | Industrial cities |
| `products.json` | Manufactured products |
| `technology.json` | Industrial technologies |
| `vision2030.json` | Vision 2030 |
| `gallery.json` | Gallery content |
| `about.json` | About page |

The project loads JSON using `apps/catalog/content_loader.py`.

When changing records, preserve existing keys and slug relationships, then rerun the tests.

## Media Management

The website uses local images and external Cloudinary media.

- Local images: `static/images/`
- Icons and branding: `static/icons/`
- Background video JavaScript: `static/js/background-video.js`
- External media: Cloudinary HTTPS URLs

The current shared background-video script handles video playback and pauses videos for visitors who request reduced motion.

### Media Usage

All external photographs, videos, logos, and trademarks remain the property of their respective owners.

Using Cloudinary for hosting does not automatically grant permission to reuse third-party content. Verify licenses and attribution requirements before public deployment.

## Deployment

This is a Django application. GitHub Pages cannot execute its Python backend.

Deploy the website using a service that supports Python and Django.

Before deploying:

1. Set `DJANGO_DEBUG=False`.
2. Configure a secure production `DJANGO_SECRET_KEY`.
3. Set `DJANGO_ALLOWED_HOSTS` to the actual production hostname.
4. Configure HTTPS before enabling `DJANGO_HTTPS_ENABLED=True`.
5. Configure a production WSGI or ASGI server.
6. Run migrations, collect static files, and check the deployment configuration.

Commands:

```powershell
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py check --deploy
```

WhiteNoise is configured to serve Django static files. Hosting infrastructure and TLS certificates must be configured separately.

## Future Improvements

- Optimize the navbar logo
- Improve background-video loading and poster images
- Complete Arabic translation and RTL support
- Review media attribution and licensing
- Deploy the website publicly

---

**SAUDI INDUSTRY**

UNIT-PROJECT-2 — An educational Django project exploring the future of Saudi manufacturing.
:::