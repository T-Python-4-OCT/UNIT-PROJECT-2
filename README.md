# Tawjeeh — A Guide to Saudi Ministries

**Tawjeeh** (توجيه) is an interactive Arabic website that introduces the ministries of the Kingdom of Saudi Arabia in a simple, engaging way: what each ministry does, when it was founded, who leads it, and how it connects to Saudi Vision 2030.

## The Idea

We hear ministry names every day, but few of us know their story or what they actually do. Tawjeeh brings that information together in one place and presents it visually, so visitors explore instead of reading dry lists.

This is an independent educational project, not an official government website.

## Visitor Experience

- **A walk through Riyadh:** The home page opens with an illustrated Riyadh skyline: Kingdom Centre, Al Faisaliah, the TV Tower, and a Najdi-style mud fort. As you scroll, the landmarks draw closer, as if you were walking into the city.
- **Day and night:** The whole site switches between light and dark mode. By day there is sun and drifting sand; by night, a moon, stars and lit windows.
- **Instant search:** The search button at the top shows results as you type. You can search by ministry name, field, responsibilities or minister.
- **Tawjeeh Assistant:** A small chat assistant answers questions such as "What does the Ministry of Health do?" using the guide's own information.

## What's on the Site

| Page | What it offers |
|---|---|
| Home | The interactive scene, quick stats, ministry cards, a timeline preview, a "Did you know?" fact, and the Vision 2030 pillars |
| All Ministries | The full directory with search, filtering by field, and links to official websites |
| Ministry page | Overview, history, responsibilities, minister, founding year, headquarters, and a photo gallery |
| Timeline | Ministries ordered by founding year, from oldest to newest |
| Compare | Two ministries side by side |
| Quiz | A short quiz to test your knowledge of the ministries |

## Ministries in the Guide

The guide covers 13 ministries across four fields:

- **Sovereign:** Foreign Affairs, Interior, Defense, Finance.
- **Services:** Health, Education, Justice, Hajj and Umrah.
- **Economic:** Commerce, Energy, Communications and Information Technology.
- **Quality of Life:** Tourism, Sports.

## Link to Vision 2030

The site presents the three Vision 2030 pillars, **A Vibrant Society**, **A Thriving Economy** and **An Ambitious Nation**, and links each ministry to the pillars closest to its work. This mapping is an exploratory classification for learning purposes, not an official one.

## A Note on the Information

The information is for educational purposes and may change over time, for example ministers' names. For official, up-to-date information, please refer to each ministry's official website; the links are included in the guide.

## Running and Testing the Project

Requires Python 3.12 or newer.

**1. Run the site** from inside the `wizarat` folder:

```bash
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Then open `http://127.0.0.1:8000/` in your browser.

**2. Automated tests** from inside the `wizarat` folder:

```bash
python manage.py test ministries
```

Expected result: 13 tests pass (`OK`). The tests check that every page loads, that each ministry has its page and images, that search returns the right results, and that the quiz and "Did you know?" data are valid.

**3. Quick manual check:**

- [ ] Scroll slowly down the home page and watch the Riyadh landmarks draw closer.
- [ ] Switch between light and dark mode with the button at the top and confirm the whole site changes.
- [ ] Click the search button and type «الصحة» (Health) or «الميزانية» (Budget); results should appear instantly.
- [ ] Open any ministry page and try the photo gallery and the "Share page" button.
- [ ] On the Compare page, pick two ministries and view the comparison.
- [ ] Complete the Quiz until your score appears.
- [ ] Ask the Tawjeeh Assistant: «ما مهام وزارة التعليم؟» (What does the Ministry of Education do?)
- [ ] Open the site on a phone, or narrow the browser window, and confirm the layout adapts.

> Note: the website itself is in Arabic, so search terms and assistant questions work best in Arabic.
