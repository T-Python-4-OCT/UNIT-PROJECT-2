# Saudi Giga Atlas v2: upgrade prompt

Give this whole file to your coding agent, started at the repository root `C:\Users\DNC\Documents\python-camp\UNIT-PROJECT-2`.

---

## 1. Mission

You are the lead engineer and design director of Saudi Giga Atlas, a bilingual Django site about six Saudi developments. Version 1 works and passes its own tests. It is competent, safe and forgettable. Your job is version 2: the project a reviewer remembers. It must still meet every requirement in README.md, read like a native site in both English and Arabic, and hold up with a keyboard, a screen reader, a phone and a slow network.

You may refactor or rebuild any part of the site when that is the shorter path to the quality bar in section 6. Choose a rebuild over a third patch to the same problem. Every rebuild keeps the guarantees in section 3.

Read in this order before changing anything: `README.md`, `AGENTS.md`, this file, `MASTER_PROMPT.md`, `PROJECT_PLAN.md`, `SETUP.md`, `docs/*.md`, and any skill under `.agents/skills/` that fits the task at hand. Where this file conflicts with `MASTER_PROMPT.md` or `PROJECT_PLAN.md`, this file wins. `README.md` and `AGENTS.md` always win.

## 2. Current state (audited 9 November 2026)

**What exists:** Django 6.1.3 with one `projects` app. `i18n_patterns` serves English at `/` and Arabic at `/ar/`. Content lives in three JSON files under `projects/data/`. There is a home page, six project pages and a 404. The frontend uses Vite 8, Tailwind 4 and Three.js r187, built with Bun. The home page has a deferred 3D relief map with an SVG poster fallback, and the site has light and dark themes. Tests are Playwright with axe, driven by `scripts/verify.ps1`.

**Audit findings.** These come from reading the code and rendering every page at 390 and 1440 px in both languages and themes. Close each finding, or record why you are keeping it, in `docs/UPGRADE_PLAN.md`.

| # | Area | Finding | Severity |
| --- | --- | --- | --- |
| 1 | Repository | The last commit (`fabdcf0`) does not contain what the current code needs: `project-features.json`, `atlas-map.json`, `project-media.js`, the three new includes, 15 gallery images and all films are untracked. 25 tracked files have uncommitted changes. A fresh clone from GitHub renders an older, different site. | Critical |
| 2 | Films | Five of the excerpts are 1080p H.264 at 1.9 to 7.4 Mbps. AMAALA is 47 MB for 54 s, The Red Sea 34 MB, Qiddiya 34 MB and NEOM 25 MB. ROSHN is only 480p. No `<video>` has a `poster`, so every project page shows a large empty grey box until someone presses play. | High |
| 3 | Captions | Only NEOM and Diriyah have caption files. Both are English only and are raw YouTube auto-captions, with inline `<00:00:01.880><c>` timing tags and repeated rolling lines. No Arabic tracks exist. | High |
| 4 | Images | Several images are stand-ins for other places. ROSHN's lead image is "Green space and skyline in Riyadh, shown for city context", AMAALA's is "Tabuk coastline, shown for regional context", and ROSHN's gallery uses "Jeddah waterfront, shown for city context". NEOM's lead is an orbital photo with a magenta cast that looks like an error at card size. The Red Sea and AMAALA galleries have one photo each. | High |
| 5 | Project pages | All six pages use one identical template with nothing project-specific. They have no tagline, although README asks for a title "with a catchy phrase". "Project highlights" and "Milestones" use display-size headings over two or three short lines. The next-project link is small and easy to miss. | High |
| 6 | Navigation | The header has one link ("Projects"). You cannot move between projects from the header, and nothing marks the current page. The footer holds only the site name. At 390 px the header wraps onto two rows. | Medium |
| 7 | Home | The hero photo is dark and overcast, so the site opens on a heavy note. The project grid mixes aspect ratios, which leaves uneven gaps, and each card repeats its photo caption underneath. The index count `01 — 06` in `templates/home.html` uses an em dash, which breaks the project's own copy rule. | Medium |
| 8 | 3D map | The relief heights are invented, as `docs/SCENE.md` admits. The Hejaz and Asir mountains and the Tuwaiq escarpment, which the copy talks about, are not where they really are. The camera is fixed, and choosing a project does nothing in the scene except follow the link. | Medium |
| 9 | Arabic | The Arabic copy mixes digit systems: Arabic-Indic digits in 4 strings (for example `٢٬٦٠٠ متر`) and Western digits in others (`45 كيلومترًا`, `2012`). | Medium |
| 10 | Data | The plan calls for one validated source, but content is split across three files with no schema validation. A missing Arabic field or a wrong image size only fails at render time. | Medium |
| 11 | Images | Every image ships at one size. Phones download 1500 px card images. There is no `srcset` and no AVIF. | Medium |
| 12 | Metadata | There is no favicon and no canonical URL. `hreflang` uses relative paths. Open Graph and Twitter cards, `theme-color`, `sitemap.xml` and `robots.txt` are all missing. | Low |
| 13 | Settings | `SECRET_KEY` has an insecure default, `DEBUG` is on by default, and `ALLOWED_HOSTS` is hard-coded to localhost. `manage.py check --deploy` reports 5 security warnings (W002, W003, W004, W008, W009). | Low |
| 14 | Evidence | `docs/EVIDENCE.md` says its own results are historical and do not verify the current build. `collected-static/` holds a different bundle hash from `static/build/`. `verification/` holds 255 MB of probe output, including a full Edge browser profile. | Low |

**Deliberate decisions. Keep these unless the user says otherwise:**

- Detail pages do not show source lists, and `projects/tests.py` asserts this. Keep sources in the data and in `docs/SOURCES.md`.
- The user confirmed permission to self-host the six film excerpts (see `docs/SOURCES.md`, Films). Keep each film's source URL and excerpt range in the data.
- Pages carry no media credits (`AGENTS.md`).

## 3. Non-negotiables

- Meet every README minimum: Django, template inheritance, dynamic URLs, static files, a home page plus at least 6 pages, one coherent design, dark and light modes, and responsive layouts.
- Keep English at `/` and Arabic at `/ar/`. Existing URLs (`/projects/<slug>/`) keep working. Every new route exists in both languages. Switching language keeps the visitor on the same page.
- Follow the media rules in `AGENTS.md`: professional quality, no recognizable faces, no watermarks, real footage with verified terms, and only media that may be shown without credits.
- Facts: every number, date and status needs an official source and a verification date in the data. Label each item as operating, under construction or announced. Never invent figures, opening dates, renders or photos. Never present an illustration as the real project.
- The Red Sea and AMAALA are separate destinations under Red Sea Global. Never call the six "six PIF giga-projects".
- Progressive enhancement: all content and every link must work without JavaScript, without WebGL 2 and with reduced motion.
- Keep authored code free of explanatory comments. Keep third-party license notices.
- Copy: use sentence case. Headings are 2 to 7 words. The home introduction is at most 30 words and project summaries at most 45 words per language. Do not use em dashes, ellipses, repeated punctuation, hype or AI filler ("unlock", "seamless", "game-changing", "where tradition meets innovation").
- Do not push, deploy, publish or buy anything. Commit locally on a branch. Never change the assignment text in `README.md`.

## 4. Phase 0: secure the baseline (do this first)

1. Run `git switch -c upgrade/v2`. Confirm that `.gitignore` excludes `.media-archive/`, `verification/`, `node_modules/`, `.venv/`, `collected-static/` and `static/build/`. Then commit the current working tree, except the films, as `Checkpoint v1 working tree`. Section 5.4 covers the films.
2. Rebuild from scratch: `bun install --frozen-lockfile`, compile translations, `bun run --bun build`, then `collectstatic`. Run `.\scripts\verify.ps1` and record the pass and fail counts.
3. Capture baseline screenshots of all 7 routes, in English and Arabic, light and dark, at 390 and 1440 px. Save them in `verification/baseline/`. You will compare against these at the end.
4. Write `docs/UPGRADE_PLAN.md`. For each area in section 5, record Keep, Refactor or Rebuild with a one-line reason, the files you will touch and the acceptance check. Then start building.

## 5. Scope

### 5.1 Information architecture

- Keep the home page, the six project pages and the 404. Add two pages, built from existing data, that make the collection feel like an atlas rather than six brochures:
  - `/timeline/` shows every milestone from all six projects on one chronological timeline. Visitors can filter it by project using plain links, so filtering works without JavaScript.
  - `/compare/` shows the six projects at a glance: region, focus, developer, current status and first public opening, each linked to its page. Every cell needs a source in the data.
  - Name both routes, add both languages, and add them to the header, footer, sitemap and tests.
- Header: brand, a Projects menu (a disclosure button listing all six), Timeline, Compare, language and theme. It stays on one row from 320 px up and collapses into a menu button below about 48rem. Mark the active page with `aria-current`. Escape closes the menu and returns focus to its button.
- Footer: links to the six projects and the two new pages, the language and theme controls, one sentence on what the atlas covers and a note that map locations are approximate.
- Project pages: large, obvious previous and next links that mirror correctly in RTL.

### 5.2 Design system

- Keep the palette family (palm, limestone, sand, charcoal, brass) and rebuild the token layer in one place: semantic color tokens, a fluid type scale with 6 or 7 steps, a spacing scale, radii, elevation, and motion durations and easings.
- Give each project one accent drawn from its own landscape. Starting points: Diriyah mudbrick, The Red Sea lagoon turquoise, Qiddiya Tuwaiq ochre, NEOM Gulf of Aqaba blue, AMAALA coral, ROSHN garden green. Use the accent only on that project's page, card and map marker, for rules, eyebrows, timeline dots and focus details. Measure contrast in both themes and record the results in `docs/DESIGN.md`.
- Typography: try an OFL display pairing for h1 and h2 with matching Latin and Arabic cuts, to give the site more character than IBM Plex alone. Check again whether the Ministry of Culture's Saudi or Masmak fonts now allow web embedding, and use them only with a verified license. Keep Plex for body text unless the alternative reads better in both scripts. In Arabic, use no letter-spacing, generous leading, and check every line break. Preload only the critical display weight for the page's language. Font-related CLS must stay at or below 0.02.
- Size headings to the content they introduce. A section with two short lines gets a small heading.
- Use one or two Najdi details on purpose, such as the triangular parapet profile as a section divider or image mask. Do not use them as wallpaper.
- Motion: subtle reveals, image fade-in and card hover states. Turn all of it off under reduced motion. Never hijack scrolling or move text with parallax.
- Design the dark theme on its own terms rather than inverting the light one. Check photos, the map, the poster, the video frame and focus rings in both themes.

### 5.3 Pages

**Home**

- Hero: use a brighter, more striking lead image, or a short silent looping clip (at most 2 MB, poster first, a visible pause control, and a still image under reduced motion). Show the headline, an introduction of at most 30 words and two actions: the map and the projects.
- Map: see 5.5.
- Project index: use consistent aspect ratios and a deliberate rhythm. Each card shows a status chip (Operating, Under development or Phased), the region and a one-line hook. Remove the photo caption under each card and keep the alt text. Fix the em dash.
- Add a short teaser that links to the timeline and compare pages.

**Project page.** Rebuild it so it covers the README example sections, each one only where sources support it:

1. Hero: a full-bleed lead image with the project name, a concrete tagline of at most 8 words, the region and category, and a status chip.
2. At a glance: 3 to 5 sourced facts, such as location, developer, area, status and first opening.
3. Story: the three existing detail blocks.
4. Top attractions: the highlights as cards, with an image where a licensed one exists. Aim for 3 per project, all sourced.
5. Gallery: 4 to 6 licensed photos per project where they exist. Upgrade the existing dialog viewer with previous and next buttons, swipe, Escape to close, a "2 / 5" counter, captions, focus return and preloading of neighbouring images.
6. Film: a poster frame, a duration label, caption tracks and `preload="none"`.
7. Timeline: milestones on a vertical timeline. Include "Major events" (openings, hosted events) only when they are sourced.
8. Previous and next project.

**404:** on-brand, with links to all six projects.

### 5.4 Media pipeline

- **Images:** write `scripts/build_media.py`, with Pillow pinned in a dev requirements file, or a Bun script using sharp. It turns the master images into AVIF and WebP at 480, 960 and 1600 px wide, and writes each image's width, height and placeholder color into the data. Templates use `<picture>` with `srcset` and `sizes`. Keep large masters out of git.
- **Replace the stand-ins** with professional, project-specific photos that follow `AGENTS.md`. Search official media centres and press kits first, then credit-free libraries. Record each URL, license and date in `docs/SOURCES.md`. When no compliant photo of the actual project exists, use a designed alternative, such as a map crop or a typographic card, never a photo of a different place. Replace NEOM's magenta orbital lead image.
- **Films:** re-encode each one with ffmpeg to 1280×720 H.264 High at about CRF 26, with `-movflags +faststart` and AAC 96k audio, or no audio track if the film is silent. Aim for 6 MB or less per film and at most about 1.2 Mbps. For ROSHN, find a source of at least 720p if one exists. Extract a poster frame for each film in WebP and AVIF. Keep the total film payload at or below 40 MB so the films can be committed. If that is not possible, make the media base URL configurable with `ATLAS_MEDIA_URL` and document external hosting, as README suggests for large files.
- **Captions:** write clean WebVTT for every film with speech or on-screen text. Strip the inline timing tags, merge repeated rolling lines, use sentence case, and keep cues to 2 lines of about 42 characters. Add Arabic tracks (`srclang="ar"`) written as natural Arabic, and make the page language's track the default. For a film with no speech, put a short text description under the player and record that in the data.
- Commit every media file a fresh clone needs to render every page.

### 5.5 Map and 3D

- **Real terrain:** build a small heightmap from public-domain elevation data, such as NOAA ETOPO 2022, after confirming its license. Use a one-off script and commit only the processed file, at 300 KB or less. Drive both the 3D relief and a regenerated poster from it so the two views match.
- Store each project's latitude and longitude in the data and project them in code. Show ROSHN as a network of communities, never as one point.
- **Interaction:** hovering or focusing a project link highlights its marker and shows a small preview card with a photo, name, status and one line. Choosing a project in 3D eases the camera toward it before the link navigates, with no easing under reduced motion. Any drag or rotate is limited and optional. The map never captures page scroll, and keyboard users get the same functions as pointer users.
- **Keep:** the deferred import, the 1.5 pixel-ratio cap, rendering only on demand, cleanup on close and `pagehide`, the poster fallback for missing WebGL 2, errors and reduced motion, and the localized status messages.
- **Budget:** the deferred scene is at most 350 KB compressed, heightmap included. On the mobile profile in `tests/performance.spec.js`, the first interaction responds within 1 s.

### 5.6 Content and language

- Rewrite every user-facing string against the copy rules. Taglines must be specific. Good: "Mudbrick lanes above Wadi Hanifah". Bad: "Where heritage meets the future".
- Check every fact again against official sources and update the `verified` dates. Statuses change fast, especially for Qiddiya, AMAALA and The Red Sea openings.
- Write the Arabic as Arabic, not as a translation. Choose one digit system and use it everywhere, including dates formatted by Django. Read every Arabic page from top to bottom before you sign off.
- Fill the gaps so every project has 3 sourced highlights and at least 3 milestones.

### 5.7 Engineering

- **One data source:** merge the three files into `projects/data/projects/<slug>.json`, or one file, behind a loader that validates it with dataclasses or a small Python schema and no heavy dependencies. Run the validation at startup under DEBUG and in the tests. It checks that both languages exist for every localized field, the word limits, that every image exists with matching dimensions, that every video and caption file exists, ISO dates, `https` source URLs with verification dates, and unique slugs.
- Keep views thin and test their context helpers. Build every link with `{% url %}`.
- **Metadata:** absolute canonical and `hreflang` URLs, Open Graph and Twitter tags with each project's image, SVG and PNG favicons plus an Apple touch icon, `theme-color` for both schemes, JSON-LD (`WebSite`, plus `Place` or `TouristDestination` for each project), `sitemap.xml` with both languages and `robots.txt`.
- **Settings:** read `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS` from the environment, with safe production defaults. Turn on security headers when DEBUG is off. `manage.py check --deploy` must report no warnings with production variables set. Keep local development as simple as `SETUP.md` describes.
- **Performance budgets** on the mobile test profile: LCP at most 2.0 s, CLS at most 0.05, and core transfer at most 600 KB for the home page and 450 KB for a project page, films excluded. Only one image per page gets `fetchpriority="high"`. Lazy-load everything below the fold.
- **Hygiene:** probe browsers and screenshots write to a temp folder or the ignored `verification/` folder. Never commit generated files.

### 5.8 Tests and evidence

- Django tests: new routes in both languages, data validation, sitemap, metadata and the 404.
- Playwright: extend the route matrix to the new pages. Add tests for the header menu (keyboard, Escape, focus return), the gallery viewer, caption tracks and their default language, film posters, project accents, no horizontal overflow at 320, 390, 768, 1024 and 1440 px and at 200% zoom, zero axe violations, navigation with JavaScript disabled, the no-WebGL fallback and reduced motion.
- **Fresh-clone check:** clone the branch into a temp folder, follow `SETUP.md` word for word and run `verify.ps1`. Fix `SETUP.md` until this works.
- Rewrite `docs/EVIDENCE.md` from this run only: the commands, counts, measured performance, the screenshot folder and open issues. Never copy old numbers forward.

## 6. Quality bar

Score each dimension from 1 to 5 by looking at the screenshots, not by reading the code. Finish only when every dimension scores at least 4 and the average is at least 4.5. Record each score, with the screenshot that justifies it, in `docs/EVIDENCE.md`.

| Dimension | A 5 looks like |
| --- | --- |
| First impression | Within 5 seconds a visitor knows what the site is and wants to scroll |
| Hierarchy | Heading sizes match their content and the eye follows one clear path per page |
| Project identity | Each project page is recognizable before you read its name |
| Imagery | Every photo shows the actual project, is sharp, and plays its role in the layout |
| Map | The geography is real, and choosing a project feels direct in both 2D and 3D |
| Arabic and RTL | Reads as a native Arabic site, with correct mirroring, digits and line breaks |
| Dark mode | Designed in its own right, with photos, map and video all comfortable |
| Mobile | One-row header, thumb-friendly targets and no horizontal overflow from 320 px |
| Accessibility | Zero axe violations and full keyboard paths, with captions on every film with speech |
| Performance | Meets the 5.7 budgets on the mobile profile |
| Accuracy | Every fact is sourced and dated, with statuses current as of the run date |
| Code | One data source, validated, tested, no dead code, setup works from a fresh clone |

**Self-critique loop:** after each milestone, open the 390 and 1440 screenshots for English light and Arabic dark. Write down the 5 weakest things you see, fix the top 3 and capture again. Be specific: "card titles wrap to 3 lines at 768 px", not "spacing could improve". Repeat until the scores hold.

## 7. Way of working

- **Vertical slice first:** the new design system, header, footer, home page and the Diriyah page in both languages and themes, scoring at least 4 on every dimension, before you roll the design out to the other five projects and the new pages.
- **Roles**, if you can run sub-agents: Lead (integration, shared files, dependencies), Backend and i18n, Design and CSS, Map and 3D, Media, QA and Editorial. One owner per file at a time. If you cannot run sub-agents, do the roles as sequential passes, and never claim parallel work you did not do.
- Commit after each verified step with a clear message, and keep the build green between commits.
- If the same failure survives two attempts, change the approach. If an outside blocker appears (an unclear license, a source offline), use the documented fallback and log it in `docs/UPGRADE_PLAN.md`.
- Ask the user only before showing sources on pages, using a paid asset, deleting anything in `.media-archive/`, or pushing to GitHub. Make every other reversible decision yourself and record it.

## 8. Final report

Report back in this format:

1. **Summary:** the 5 most important changes.
2. **Before and after:** paths to paired screenshots from `verification/baseline/` and the final run.
3. **Scorecard:** the section 6 table with your scores.
4. **Verification:** the exact commands run, with pass and fail counts.
5. **README matrix:** each README requirement and the evidence that it is met.
6. **Open issues:** anything unresolved or unverified, stated plainly.
7. **For the user:** what they need to do next, such as review media choices, push the branch or merge.
