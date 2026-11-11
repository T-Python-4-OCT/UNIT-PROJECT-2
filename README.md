# 🎮 Saudi Arena

### Discover the Future of Esports in Saudi Arabia 🇸🇦

**Saudi Arena** is a bilingual web platform developed using Python and Django. The website showcases Saudi Arabia's growing presence in the esports and gaming industry, highlighting local teams, professional players, tournaments, competitive games, and achievements.

The project reflects Saudi Arabia's ambition to become a global destination for esports, in alignment with **Saudi Vision 2030**.

---

## 🚀 Features

- **Home Page:** Interactive landing page with video backgrounds and a dedicated Saudi Vision 2030 section.
- **About Us:** Introduction to Saudi Arena and the development of esports in Saudi Arabia.
- **Tournaments:** Explore esports tournaments with filtering options.
- **Teams:** Discover Saudi esports organizations and search for teams.
- **Players:** Explore professional esports players.
- **Games:** Discover competitive games through interactive visuals and video content.
- **Achievements:** Highlight achievements in the Saudi esports industry.
- **Bilingual Support:** Arabic and English using Django's internationalization system.
- **Dark & Light Mode:** Switch between two visual themes.
- **Responsive Design:** Supports desktop, tablet, and mobile screens.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Django | Web framework |
| HTML5 | Website structure |
| CSS3 | Styling and responsive design |
| JavaScript | Interactive functionality |
| JSON | Website content storage |
| Django i18n | Arabic and English translations |
| Git & GitHub | Version control |

## 📁 Project Structure

```text
SaudiArena/
├── manage.py
├── esports/
│   ├── data/
│   │   └── content.json
│   ├── static/
│   │   └── esports/
│   │       ├── css/
│   │       ├── js/
│   │       ├── images/
│   │       └── videos/
│   ├── templates/
│   │   └── esports/
│   │       ├── base.html
│   │       ├── home.html
│   │       ├── about.html
│   │       ├── tournaments.html
│   │       ├── teams.html
│   │       ├── players.html
│   │       ├── games.html
│   │       └── achievements.html
│   ├── views.py
│   └── urls.py
└── locale/
    └── ar/
        └── LC_MESSAGES/
```

## ⚙️ Installation and Setup

**1. Clone the repository**

```bash
git clone YOUR_REPOSITORY_URL
cd SaudiArena
```

**2. Create a virtual environment**

```bash
python -m venv venv
```

**3. Activate the environment**

Windows (Git Bash):

```bash
source venv/Scripts/activate
```

**4. Install Django**

```bash
pip install django
```

**5. Run the development server**

```bash
python manage.py runserver
```

Open your browser and visit:

`http://127.0.0.1:8000/`

## 🌐 Languages and Themes

Saudi Arena supports:

- Arabic (RTL)
- English (LTR)
- Dark mode
- Light mode

The interface adapts to the selected language and theme.

## 🗂️ Data Management

The project uses a JSON-based content system instead of Django database models.

Website information is stored in `content.json`, while Django views handle data processing, filtering, and rendering.

This approach keeps the project lightweight and easy to maintain.

## 🇸🇦 Saudi Vision 2030

Saudi Arena highlights the Kingdom's growing esports ecosystem and its ambition to become a leading international hub for gaming and esports.

The platform showcases Saudi talent, esports organizations, competitive tournaments, and the industry's achievements.

*Saudi Arena is an independent educational project and is not an official Saudi government website.*

## 🎓 Project Information

**Project Name:** Saudi Arena  
**Project Type:** Django Web Development Project  
**Program:** Tuwaiq Academy Bootcamp  
**Focus:** Web Development with Python and Django  
**Purpose:** Educational and practical application

## 📌 Future Improvements

- Expanded esports content
- More advanced search and filtering
- Improved accessibility
- Additional interactive features
- Continued UI/UX enhancements

## 📄 License and Media

This project was developed for educational purposes. Third-party images, videos, logos, and trademarks belong to their respective owners and remain subject to their applicable licenses and usage permissions.

---

**Made with Python, Django, and a passion for Saudi esports. 🇸🇦🎮**