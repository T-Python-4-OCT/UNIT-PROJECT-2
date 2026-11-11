# Saudi Then & Now | السعودية بين الماضي والحاضر

A bilingual Django website that tells how Saudi Arabia changed, from mud houses and camel caravans to Vision 2030. Seven stories put the Kingdom's past and present side by side, and an interactive journey through time walks through 56 milestones from 1902 to 2034.

موقع بالعربي والإنجليزي مبني بـ Django، يحكي كيف تغيّرت المملكة العربية السعودية من بيوت الطين وقوافل الإبل إلى رؤية 2030. سبع قصص تضع الماضي والحاضر جنبًا إلى جنب، وتنقّل تفاعلي عبر الزمن يمر على 56 محطة من 1902 إلى 2034.

---

## Pages

| URL | Page | What it shows |
| --- | --- | --- |
| `/` | Home | "From Sand to Skyline" hero with a then-and-now time machine, the Kingdom in numbers, the seven story cards and the milestones that shaped the Kingdom |
| `/topic/<slug>/` | 7 story pages | A title with a catchy line, a then-and-now image slider, the story with four key numbers, key moments, a short video and what is coming next with a countdown |
| `/timeline/` | Travel Through Time | Opens with a short animated welcome, then 39 milestones and 17 future plans in an interactive slider, with story filters, eras, autoplay, keyboard and swipe support |
| `/about/` | About | The idea behind the project and the project in numbers |

The seven stories:

1. Riyadh & Urban Growth — `/topic/riyadh/`
2. Transport — `/topic/transport/`
3. Economy & Energy — `/topic/economy/`
4. Education — `/topic/education/`
5. Tourism — `/topic/tourism/`
6. Sports, Entertainment & Global Events — `/topic/events/`
7. Digital Government — `/topic/digital/`

## Features

- **Arabic and English** with full right-to-left support, saved in a cookie.
- **Dark and light mode**, saved in a cookie.
- **Responsive** on phones, tablets and desktops.
- **Interactive**: then-and-now image sliders, a time machine on the home page, a time-travel slider, countdowns, scroll animations and counting numbers.
- **Animated logo**: a mud fort and the Kingdom Centre; the tower grows as you scroll down the page.
- **Welcome intro** on Travel Through Time: two Najdi doors open on the page while the years count from 1902 to today. It plays each time the page opens, can be skipped, and is turned off for people who prefer reduced motion.
- **Custom design** inspired by Najdi architecture, written in plain CSS without a framework.

## Requirements checklist

| Requirement | How it is met |
| --- | --- |
| Use Django | Django 6.1 project with one app, `main` |
| Templates and template inheritance | Every page extends `base.html`, which holds the header, footer and theme |
| Dynamic URLs | `topic/<slug:slug>/` for the seven stories and `lang/<str:lang>/` for the language |
| Static files | CSS, JavaScript, images and videos loaded with `{% static %}` |
| Home page and at least 6 pages | Home page plus 9 pages: 7 stories, Travel Through Time and About |
| Coherent, uniform design | One design system shared by every page |
| Dark and light mode | Theme switch in the header |
| Responsive | Layouts adapt from 360px phones to wide screens |

## Built with

- Python and Django
- HTML, CSS and JavaScript
- Google Fonts (Readex Pro, Reem Kufi) and Material Symbols icons

## Project structure

```
UNIT-PROJECT-2/
├── README.md
├── requirements.txt
└── SaudiThenNow/
    ├── manage.py
    ├── SaudiThenNow/          project settings and main urls
    └── main/
        ├── views.py           page views
        ├── urls.py            app urls
        ├── translations.py    language helpers
        ├── data/
        │   ├── topics.json    data shared by several pages (stories and milestones)
        │   └── text.json      shared Arabic and English text (menu, footer, labels)
        ├── templates/main/
        │   ├── base.html
        │   ├── index.html
        │   ├── timeline.html
        │   ├── about.html
        │   └── topics/        one page for each story
        └── static/
            ├── css/style.css
            ├── js/main.js
            ├── images/
            └── video/
```

## Run it locally

```bash
git clone https://github.com/mohammedalnsaf10-design/UNIT-PROJECT-2.git
cd UNIT-PROJECT-2
python -m venv venv
venv\Scripts\activate          # on macOS or Linux: source venv/bin/activate
pip install -r requirements.txt
cd SaudiThenNow
python manage.py runserver
```

Then open http://127.0.0.1:8000

## Author

**Mohammed Alnsafi** 
