
<div align="center">

# 🌿 ARDNA | أرضنا

### From Our Land, Stories Begin

**An Interactive Journey Through Agriculture in Saudi Arabia**

An Arabic-language web experience that brings together Saudi agricultural heritage, regional diversity, modern farming, and personal storytelling.

**Built with Django, Python, Tailwind CSS, and JavaScript.**

[Explore the Repository](https://github.com/Abdulmajeed-mo/UNIT-PROJECT-2)

</div>

---

## 📖 About the Project

**ARDNA (أرضنا)**, meaning *"Our Land"*, is an interactive educational website dedicated to exploring agriculture across the Kingdom of Saudi Arabia.

The project introduces visitors to the agricultural identity of five Saudi regions, highlighting their crops, farming traditions, natural environments, and local heritage.

Rather than presenting agricultural information through conventional pages, ARDNA combines visual storytelling, interactive experiences, and region-specific designs to make the journey more engaging.

The website also features a personal story inspired by my father's passion for farming and the agricultural transformation of our family's farm.

> **Language:** The entire website is developed in Arabic, featuring a Right-to-Left (RTL) interface designed specifically for Arabic-speaking visitors.

---

## 🎯 Project Objectives

- Highlight Saudi Arabia's agricultural diversity and heritage.
- Introduce visitors to major crops and farming practices across different regions.
- Create an engaging educational experience through interactive storytelling.
- Demonstrate Django development using dynamic data and reusable templates.
- Apply modern Front-End techniques while maintaining responsive and accessible layouts.
- Connect a personal farming story with the wider agricultural identity of Saudi Arabia.

---

## 🗺️ Explore Saudi Arabia's Agricultural Regions

ARDNA introduces five agricultural destinations, each featuring its own visual identity, regional information, crop journey, image galleries, and educational content.

| Region | Agricultural Identity | Featured Highlight |
|--------|----------------------|-------------------|
| Al-Ahsa (الأحساء) | Palm Oasis | Dates and traditional oasis farming |
| Taif (الطائف) | Rose Heritage | Taif roses and rosewater production |
| Al-Qassim (القصيم) | Land of Dates | Date cultivation, harvesting, and markets |
| Al-Jouf (الجوف) | Olive Region | Olive farming and olive oil production |
| Abha (أبها) | Jacaranda and Mountains | Jacaranda blossoms and Asir's agricultural landscapes |

Each region includes information about its agricultural history, farming methods, seasonal characteristics, and distinctive products.

---

## ❤️ Our Roots — A Personal Story

One of the most meaningful sections of ARDNA is **"Our Roots" (جذورنا)**.

This dedicated page tells the story of our family farm in **Unaikir Village, Al-Qunfudhah, Saudi Arabia**.

Inspired by my father, Mohammed Mustafa Al-Hassani, a retired teacher with a lifelong passion for farming, the page follows the transformation of a once-barren landscape into a thriving green space over approximately 25 years.

The farm reflects years of dedication, patience, and care, with mango trees, lemon trees, flowers, and natural surroundings becoming part of its identity.

This section uses visual storytelling, image galleries, and interactive elements to illustrate the journey.

**Our Roots represents the heart of ARDNA: the belief that every piece of land has a story worth telling.**

---

## 🖥️ Website Pages

The project contains **7 main pages**.

| Page | Description |
|------|-------------|
| Home | Introduces ARDNA through a cinematic hero section, agricultural stories, and interactive region cards |
| Our Roots | Shares the personal story and transformation of our family farm |
| Al-Ahsa | Explores oasis agriculture, palm trees, and date cultivation |
| Taif | Highlights Taif roses, harvesting, and traditional distillation |
| Al-Qassim | Introduces date farming, harvesting, processing, and agricultural markets |
| Al-Jouf | Explores olive farming, harvesting, and olive oil production |
| Abha | Highlights jacaranda trees, mountain environments, and agricultural diversity |

The five region pages share a reusable Django template while displaying their own content and visual themes.

---

## ✨ Key Features

### 🌿 Interactive Regional Experiences

Each region has a dedicated page with a distinct agricultural identity.

Features include:

- Region-specific color palettes.
- Full-screen animated introductions.
- Background videos and agricultural imagery.
- Educational content about regional crops.
- Agricultural history and heritage.
- Farming methods and seasonal information.
- Image galleries and related educational videos.

### 🌱 Interactive Crop Journeys

The **"From Land to Life"** section allows visitors to explore three stages of an agricultural journey.

Examples include:

- Palm care, pollination, and date harvesting in Al-Ahsa.
- Rose growth, harvesting, and distillation in Taif.
- Date production, harvesting, and processing in Al-Qassim.
- Olive growth, harvesting, and oil extraction in Al-Jouf.
- Jacaranda growth, blooming, and seasonal renewal in Abha.

Each stage includes:

- A dedicated image.
- An educational description.
- Interactive navigation buttons.
- A visual progress indicator.
- Dynamic content updates.

### 🎞️ Animated Storytelling

The website incorporates motion and visual effects to create a more immersive experience.

These include:

- Scroll-based animations.
- Animated page introductions.
- Smooth transitions.
- Interactive cards.
- Hover effects.
- Image galleries and sliders.

### 🌓 Dark and Light Modes

ARDNA supports both Dark Mode and Light Mode.

Theme preferences are handled through **Django cookies**, allowing the selected appearance to persist between page visits.

### 📱 Responsive Design

The website is designed to adapt to different screen sizes, including:

- Desktop computers.
- Tablets.
- Mobile devices.

The interface follows an Arabic **Right-to-Left (RTL)** layout.

### ☁️ Cloud-Based Media

The project uses **Cloudinary** to host and deliver its images and introductory videos.

This approach helps reduce the repository size and keeps large media files separate from the application's source code.

YouTube is also used for selected educational videos.

---

## 🛠️ Technologies Used

### Back-End

| Technology | Purpose |
|------------|---------|
| Python | Server-side programming |
| Django | Web framework, routing, views, and template rendering |
| JSON | Structured data for regional agricultural content |
| Django Templates | Dynamic HTML rendering and reusable layouts |
| Django Cookies | Theme preference management |

### Front-End

| Technology | Purpose |
|------------|---------|
| HTML5 | Semantic website structure |
| CSS3 | Custom styles, layouts, and visual effects |
| Tailwind CSS | Responsive utility-based styling |
| JavaScript | Interactive elements and dynamic behavior |
| GSAP | Animations and scroll-based effects |
| Swiper.js | Interactive image galleries and sliders |

### Media and Development Tools

| Tool | Purpose |
|------|---------|
| Cloudinary | Image and video hosting |
| YouTube | Embedded educational videos |
| Git | Version control |
| GitHub | Source code hosting and project submission |
| Visual Studio Code | Development environment |

---

## 🏗️ Project Architecture

ARDNA follows a Django-based structure with reusable templates, static assets, and data-driven regional pages.

```text
UNIT-PROJECT-2/
│
├── ARDNA/
│   ├── settings.py
│   ├── urls.py
│   └── ...
│
├── regions/
│   ├── data/
│   │   └── regions.json
│   │
│   ├── templates/
│   │   └── regions/
│   │       ├── base.html
│   │       ├── home.html
│   │       ├── our_roots.html
│   │       ├── region_detail.html
│   │       └── includes/
│   │           ├── agriculture_timeline.html
│   │           ├── crop_journey.html
│   │           ├── region_heritage.html
│   │           └── region_links.html
│   │
│   ├── static/
│   │   └── regions/
│   │       ├── css/
│   │       ├── js/
│   │       └── images/
│   │
│   ├── templatetags/
│   │   └── cloudinary_tags.py
│   │
│   ├── views.py
│   └── urls.py
│
└── manage.py
```

### Data-Driven Region Pages

The five region pages use a single reusable template:

`region_detail.html`

Their content is managed through:

`regions/data/regions.json`

This structure allows each region to have unique information, media, colors, crop journeys, and agricultural facts without creating a separate HTML template for every region.

---

## 🚀 Getting Started

Follow these steps to run ARDNA locally.

### 1. Clone the Repository

```bash
git clone https://github.com/Abdulmajeed-mo/UNIT-PROJECT-2.git
```

### 2. Navigate to the Project Directory

```bash
cd UNIT-PROJECT-2
```

### 3. Create a Virtual Environment

```bash
python -m venv .venv
```

### 4. Activate the Virtual Environment

**Windows PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
source .venv/bin/activate
```

### 5. Install Django

```bash
pip install django
```

### 6. Run Django System Checks

```bash
python manage.py check
```

### 7. Start the Development Server

```bash
python manage.py runserver
```

### 8. Open the Website

Visit:

http://127.0.0.1:8000/

**Note:** An internet connection is required to load Cloudinary-hosted media and external CDN resources.

For Front-End development, Tailwind CSS assets can be rebuilt using the project's existing Tailwind configuration and build scripts.

---

## 🎨 Design Philosophy

ARDNA was designed around the concept of **nature-driven visual storytelling**.

Its design combines:

- Earth-inspired colors.
- Natural green tones.
- Regional accent colors.
- Large editorial typography.
- Agricultural photography.
- Smooth and meaningful animations.
- Clean content organization.
- Arabic-first user experience.

Each region uses its own colors to reflect its agricultural character, while maintaining a consistent visual system across the entire website.

The goal is to create an experience that feels connected to the land, not simply a collection of informational pages.

---

## 📚 Educational Project

ARDNA was developed as **Unit Project 2** during the **Artificial Intelligence for Web Development using Python and Django Bootcamp** at **Tuwaiq Academy**.

The project demonstrates practical implementation of:

- Django project and application structure.
- Function-Based Views (FBVs).
- URL routing and dynamic URLs.
- Django Template Language (DTL).
- Template inheritance and reusable components.
- Static file management.
- JSON-based dynamic content.
- Responsive Front-End development.
- Third-party media integration.
- Interactive JavaScript functionality.

---

## 👨‍💻 Developer

**Abdulmajeed Mohammed Al-Hasani**

Computer Science Graduate | Software Developer

Passionate about combining software development, creative design, and meaningful digital experiences.

- **GitHub:** [Abdulmajeed-mo](https://github.com/Abdulmajeed-mo)
- **LinkedIn:** [Abdulmajeed Mohammed](https://www.linkedin.com/in/abdulmajeed-mohammed1)

---

<div align="center">

### 🌿 ARDNA | أرضنا

**From Our Land, Stories Begin.**

*Every Land Has a Story Worth Telling.*

Developed with 💚 in Saudi Arabia.

</div>
