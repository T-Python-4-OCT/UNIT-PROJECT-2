
# TheKingdom 2.0 — Saudi History Interactive Website 🇸🇦

**Python · Django · HTML · CSS · JavaScript · Bootstrap · JSON**

An interactive, cinematic educational website exploring the history of Saudi Arabia across three major historical eras, from the founding of the First Saudi State in 1727 to the establishment of the modern Kingdom of Saudi Arabia and its ongoing development.

TheKingdom combines historical storytelling, interactive timelines, maps, ruler biographies, archival-inspired experiences, and cinematic media to make learning Saudi history more engaging and immersive.

---

## 📖 About the Project

TheKingdom 2.0 was developed as a web development project during the **Tuwaiq Academy Web Development Bootcamp**, in partnership with the **Saudi Ministry of Interior**.

The project presents Saudi history through three interactive chapters:

| Historical Era | Period | Capital |
|---|---|---|
| First Saudi State | 1727–1818 | Diriyah |
| Second Saudi State | 1824–1891 | Riyadh |
| Third Saudi State | 1902–Present | Riyadh |

Each chapter features its own visual identity, historical narrative, interactive elements, and ruler biographies.

---

## ✨ Key Features

### 🏛️ Three Interactive Historical Eras

- **First Saudi State:** The founding of the state by Imam Muhammad bin Saud, the rise of Diriyah, its rulers, and its historical legacy.
- **Second Saudi State:** The restoration of Saudi rule by Imam Turki bin Abdullah, Riyadh as the capital, historical challenges, and the state's development.
- **Third Saudi State:** The recapture of Riyadh by King Abdulaziz, the unification of Saudi Arabia, the establishment of the Kingdom in 1932, and modern national development.

### 🎬 Cinematic User Experience

- Full-screen historical hero sections
- Interactive video backgrounds
- Hover-triggered video playback
- Scroll-based storytelling
- Smooth transitions and animations
- Historical artwork and visual storytelling

### 📜 Interactive Historical Content

- Chronological historical timelines
- Interactive maps and image zoom
- Archival-inspired document presentation
- Interactive page-flipping book
- Historical milestones and key events

### 👑 Ruler and King Biographies

- Dedicated biography pages for Saudi rulers and kings
- Historical overviews and reign information
- Key achievements and milestones
- Illustrated historical storytelling chapters
- Navigation between rulers
- Historical references where available

### 🎨 Responsive Interface

- Arabic-first, right-to-left (RTL) layout
- Responsive desktop, tablet, and mobile design
- Light and dark modes
- Consistent olive, charcoal, and gold visual identity
- Arabic numeral presentation
- Accessible navigation and interactive controls

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Django | URL routing, views, and template rendering |
| HTML5 | Semantic page structure and video elements |
| CSS3 | Responsive layouts, animations, and visual design |
| JavaScript | Timelines, interactions, and dynamic behavior |
| Bootstrap 5 RTL | Responsive components and navigation |
| Bootstrap Icons | Interface icons |
| JSON | Historical content and ruler information |
| StPageFlip | Interactive historical book experience |
| Git & GitHub | Version control and project hosting |

---

## 📁 Project Structure

```text
TheKingdom/
│
├── manage.py
├── TheKingdom/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── history/
│   ├── data/
│   │   ├── states.json
│   │   ├── rulers.json
│   │   └── third_events.json
│   │
│   ├── templates/history/
│   │   ├── base.html
│   │   ├── home.html
│   │   ├── about.html
│   │   ├── ruler_detail.html
│   │   └── states/
│   │       ├── first.html
│   │       ├── second.html
│   │       └── third.html
│   │
│   ├── static/history/
│   │   ├── css/
│   │   │   ├── styles.css
│   │   │   ├── dark-theme.css
│   │   │   ├── states.css
│   │   │   ├── second.css
│   │   │   ├── second-map.css
│   │   │   ├── second-book.css
│   │   │   ├── third.css
│   │   │   └── rulers.css
│   │   │
│   │   ├── js/
│   │   │   ├── states.js
│   │   │   ├── second.js
│   │   │   ├── second-map.js
│   │   │   ├── third.js
│   │   │   └── rulers.js
│   │   │
│   │   ├── images/
│   │   │   ├── eras/
│   │   │   ├── first-state/
│   │   │   ├── second-state/
│   │   │   ├── third_saudi/
│   │   │   └── rulers/
│   │   │
│   │   └── videos/
│   │
│   ├── views.py
│   └── urls.py
│
└── README.md
```

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/AAQ224/UNIT-PROJECT-2.git
cd TheKingdom
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate the environment:

**Windows PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install django
```

If a `requirements.txt` file is available, you can use:

```bash
pip install -r requirements.txt
```

### 4. Run System Checks

```bash
python manage.py check
```

### 5. Start the Development Server

```bash
python manage.py runserver
```

Open the website at:

**http://127.0.0.1:8000/**

---

## 🧭 Website Navigation

| Page | Description |
|---|---|
| Home | Cinematic introduction and three historical eras |
| First Saudi State | Diriyah, founding, rulers, and historical timeline |
| Second Saudi State | Restoration, Riyadh, maps, and interactive documents |
| Third Saudi State | Unification milestones, historical storytelling, and kings |
| Ruler Biographies | Detailed pages for rulers and kings |
| About | Project concept, features, technologies, and developer information |

---

## 🗃️ Data Management

Historical content is stored in JSON files instead of being hardcoded into individual HTML pages.

- `states.json` — Saudi state details and ruler listings
- `rulers.json` — Ruler biographies, historical milestones, and related information
- `third_events.json` — Unification milestones and modern historical events

Django loads these files and passes the data to templates, allowing historical content to be maintained independently of the page layouts.

---

## 🎯 Learning Objectives

This project demonstrates practical experience with:

- Django URL routing and view functions
- Django template inheritance
- Dynamic rendering using JSON data
- Responsive frontend development
- DOM manipulation and event handling
- Interactive animations and user experience design
- Working with static images, CSS, JavaScript, and videos
- Code organization and version control

---

## 👨‍💻 Developer

**Abdulrahman Abdulaziz Al-Qahtani**

Computer Science Graduate — Jubail Industrial College

Web Developer | Python & Django

Developed as part of the Tuwaiq Academy Web Development Bootcamp in partnership with the Saudi Ministry of Interior.

**GitHub:** [AAQ224](https://github.com/AAQ224)

---

## 📚 Historical References

The project draws on historical resources, including:

- [Saudipedia](https://saudipedia.com/)
- [Saudi Founding Day](https://foundingday.sa/)
- Historical and educational references linked within relevant pages

Some illustrations and visual scenes are artistic representations created for educational storytelling and should not be interpreted as authentic historical photographs.

---

## ⚠️ Disclaimer

TheKingdom is an independent educational web development project.

It is not an official Saudi government website and is not affiliated with or endorsed by any government authority.

The project uses Saudi historical themes and national symbols for educational and illustrative purposes.

---

## 📄 License

This repository is intended for educational and portfolio purposes. No open-source license is specified. Third-party images, videos, and other assets remain subject to their respective licenses and usage rights.

---

**TheKingdom — Three Centuries. One Story. 🇸🇦**
