<div align="center">

# 🇸🇦 Saudi Then & Now

### السعودية بين الماضي والحاضر

[![Typing SVG](https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&pause=1000&color=E3A52A&center=true&vCenter=true&width=560&lines=From+mud+houses+to+Vision+2030+🏙️;7+stories+•+56+milestones+•+1902+to+2034+⏳;Arabic+%26+English+•+Dark+%26+Light+🌗)](https://git.io/typing-svg)

![Python](https://img.shields.io/badge/Python-3.14-blue?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-6.1.3-092E20?logo=django&logoColor=white)
![Languages](https://img.shields.io/badge/languages-AR%20%7C%20EN-c49a6c)
![Theme](https://img.shields.io/badge/theme-dark%20%7C%20light-4a2e1a)
![Status](https://img.shields.io/badge/status-complete-success)

### 👨‍💻 Developed by **Mohammed Alnsafi**

</div>

## 📖 Overview
A bilingual **Django** website that tells how Saudi Arabia changed, from mud houses and camel caravans to Vision 2030. Seven stories put the Kingdom's past and present side by side, and an interactive journey through time walks through **56 milestones** from 1902 to 2034. 🎓

موقع بالعربي والإنجليزي مبني بـ Django، يحكي كيف تغيّرت المملكة العربية السعودية من بيوت الطين وقوافل الإبل إلى رؤية 2030. سبع قصص تضع الماضي والحاضر جنبًا إلى جنب، وتنقّل تفاعلي عبر الزمن يمر على 56 محطة من 1902 إلى 2034.

## 🗺️ Pages

| URL | Page | What it shows |
|---|---|---|
| `/` | 🏠 Home | "From Sand to Skyline" hero with a then-and-now time machine, the Kingdom in numbers, the seven story cards and the milestones that shaped the Kingdom |
| `/topic/<slug>/` | 📚 7 story pages | A then-and-now image slider, the story with four key numbers, key moments, a short video and what is coming next with a countdown |
| `/timeline/` | ⏳ Travel Through Time | A short animated welcome, then 39 milestones and 17 future plans in an interactive slider |
| `/about/` | ℹ️ About | The idea behind the project and the project in numbers |

## 📚 The Seven Stories

| # | Story | URL |
|---|---|---|
| 1 | 🏙️ Riyadh & Urban Growth | `/topic/riyadh/` |
| 2 | 🚆 Transport | `/topic/transport/` |
| 3 | 🛢️ Economy & Energy | `/topic/economy/` |
| 4 | 🎓 Education | `/topic/education/` |
| 5 | 🏝️ Tourism | `/topic/tourism/` |
| 6 | 🏟️ Sports, Entertainment & Global Events | `/topic/events/` |
| 7 | 📱 Digital Government | `/topic/digital/` |

## ✨ Features

| 🎨 Design | ⚡ Interaction |
|---|---|
| 🌐 Arabic and English with full right-to-left support | ↔️ Then-and-now image sliders you can drag |
| 🌗 Dark and light mode, saved in a cookie | 🕰️ Time machine on the home page |
| 📱 Responsive on phones, tablets and desktops | ⏳ Time-travel slider with story filters, eras and autoplay |
| 🏰 Animated logo: a mud fort and the Kingdom Centre that grows as you scroll | 🚪 Welcome intro: two Najdi doors open while the years count from 1902 to today |
| 🧱 Custom design inspired by Najdi architecture, plain CSS | ⏱️ Countdowns to the coming projects |
| 🎞️ A short video in every story | 🔢 Scroll animations and counting numbers |

## 📝 User Stories

**As a visitor, I can:**
- 🌐 switch between Arabic and English, and the site remembers my choice
- 🌗 switch between dark and light mode
- 🕰️ pick a year in the time machine and see how the Kingdom looked
- 📚 open any of the seven stories and drag the slider to compare then and now
- 🎞️ watch a short video and read the key moments of each story
- ⏱️ see how many days are left for the coming projects
- ⏳ travel through 56 milestones, filter them by story, and let them play on their own

## 🚀 Run

```bash
git clone https://github.com/mohammedalnsaf10-design/UNIT-PROJECT-2.git
cd UNIT-PROJECT-2
python -m venv venv
source venv/Scripts/activate      # Windows (Git Bash)
python -m pip install -r requirements.txt
cd SaudiThenNow
python manage.py runserver
```

🌍 Then open http://127.0.0.1:8000

## 🎮 Usage

| Control | Action |
|---|---|
| 🌐 | Switch the language (header) |
| 🌗 | Switch dark / light mode (header) |
| ↔️ | Drag the line on any image to compare then and now |
| ⬅️ ➡️ | Move between milestones on Travel Through Time |
| ▶️ | Play the milestones on their own |
| ⏭️ | Skip the welcome intro (or press `Esc`) |

## ✅ Requirements Checklist

| Requirement | How it is met |
|---|---|
| ✅ Use Django | Django 6.1 project with one app, `main` |
| ✅ Templates and template inheritance | Every page extends `base.html`, which holds the header, footer and theme |
| ✅ Dynamic URLs | `topic/<slug:slug>/` for the seven stories and `lang/<str:lang>/` for the language |
| ✅ Static files | CSS, JavaScript, images and videos loaded with `{% static %}` |
| ✅ Home page and at least 6 pages | Home page plus 9 pages: 7 stories, Travel Through Time and About |
| ✅ Coherent, uniform design | One design shared by every page |
| ✅ Dark and light mode | Theme switch in the header |
| ✅ Responsive | Layouts adapt from 360px phones to wide screens |

## 🗂️ Structure

```text
UNIT-PROJECT-2/
├── README.md
├── requirements.txt
└── SaudiThenNow/
    ├── manage.py            ▶️ entry point
    ├── SaudiThenNow/        ⚙️ settings and main urls
    └── main/
        ├── views.py         🧠 page views
        ├── urls.py          🔗 app urls
        ├── translations.py  🌐 language helpers
        ├── data/            💾 topics.json (stories and milestones) · text.json (shared text)
        ├── templates/main/  🖥️ base, home, timeline, about + topics/ (one page per story)
        └── static/          🎨 css · js · images · video
```

## 📚 Built With
`Python` 🐍 · `Django` 🌐 · `HTML` · `CSS` 🎨 · `JavaScript` ⚡ · Google Fonts (Readex Pro, Reem Kufi) · Material Symbols icons

## 👨‍💻 Developer
**Mohammed Alnsafi** 🚀  
Django course unit project: Saudi Then & Now 🇸🇦
