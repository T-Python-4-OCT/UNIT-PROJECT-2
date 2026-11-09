# Upgrade plan and decisions (v2)

Branch: `upgrade/v2`. Baseline commit: `Checkpoint v1 working tree`. Started 9 November 2026 from `UPGRADE_PROMPT.md`.

## Decisions by area

| Area | Decision | Reason | Files |
| --- | --- | --- | --- |
| Data | Rebuild | Three files became one record per project with a validating loader. Map geometry stays in `atlas-map.json` because it is geometry, not editorial content. | `projects/data/projects/*.json`, `projects/content.py`, `projects/apps.py` |
| Routes and views | Refactor | Added `/timeline/`, `/compare/`, `sitemap.xml` and `robots.txt`. Views now share one context builder with absolute canonical and hreflang URLs. | `projects/views.py`, `projects/urls.py`, `config/urls.py` |
| Templates | Rebuild | New header with a Projects disclosure, compact menu and current-page state; new footer; home mosaic and editorial project list; project page with hero, at-a-glance facts, attractions, gallery viewer, film, timeline and pager. | `templates/` |
| Design system | Rebuild | One token layer (type scale, spacing, radii, elevation, motion), per-project accents and a Najdi parapet motif used in two places. | `frontend/styles/atlas.css` |
| Typography | Keep | IBM Plex Sans and Plex Sans Arabic. A display pairing could not be installed offline in this session, and the Ministry of Culture fonts still lack verified web-embedding terms. | `frontend/main.js` |
| Images | Rebuild | Responsive AVIF and WebP at 480, 960 and 1600 px through a `picture` tag. Stand-in photos of other places were removed. New lead and gallery images are stills from the official films the user cleared for hosting. | `projects/templatetags/atlas.py`, `scripts/build_media.mjs`, `scripts/media-jobs.json` |
| Films | Rebuild | Re-encoded to 720p H.264 with fast start. Total payload fell from 150 MB to 33 MB. Every film now has a poster frame. | `static/atlas/videos/` |
| Captions | Rebuild | Clean English captions for NEOM and Diriyah, a new Arabic track for NEOM, and on-page notes for music-only films. | `static/atlas/videos/*.vtt` |
| 3D map | Keep | Still illustrative. A real elevation model needs a download that this session could not make. Labels now carry project accents. | `frontend/scripts/` |
| Settings | Refactor | Environment-driven hosts and keys, CSRF and clickjacking middleware, and HTTPS hardening behind `ATLAS_HTTPS=1`. | `config/settings.py` |
| Tests | Rebuild | 12 Django tests, a 52-test browser acceptance suite covering nine routes in two languages and two themes, plus performance and zoom checks. | `projects/tests.py`, `tests/` |

## Audit findings status

| # | Finding | Status |
| --- | --- | --- |
| 1 | Repository missing current work | Fixed. Everything a fresh clone needs is committed, including films. |
| 2 | Oversized films without posters | Fixed. 2 to 10 MB each, 33 MB total, posters on all six. Qiddiya (7.9 MB) and AMAALA (10.3 MB) exceed the 6 MB target. |
| 3 | Raw auto-captions | Fixed for NEOM and Diriyah. ROSHN has speech but no transcript yet. Diriyah has Arabic subtitles burned into the picture. |
| 4 | Stand-in images | Fixed. ROSHN and AMAALA now show their own places. ROSHN's source film is 480p, so its images are soft. |
| 5 | Identical project pages | Fixed with accents, taglines, facts and new sections. |
| 6 | Navigation | Fixed. |
| 7 | Home hero, grid and em dash | Fixed. |
| 8 | Invented relief | Open. Needs a public-domain elevation download (for example NOAA ETOPO 2022). |
| 9 | Mixed Arabic digits | Fixed. Western digits everywhere, and inconsistent Arabic spellings of Six Flags, Aquarabia, Falcons Flight and Triple Bay were unified. |
| 10 | Unvalidated data | Fixed. |
| 11 | Single-size images | Fixed. |
| 12 | Metadata | Fixed. |
| 13 | Deploy warnings | Fixed when production variables are set. |
| 14 | Stale evidence | Replaced. See `EVIDENCE.md`. |

## Needs the user

- **Photo licenses.** The v1 register listed `diriyah.webp` as CC BY 2.0 and `the-red-sea.webp` as CC BY-SA 4.0. Both licenses require attribution, which `AGENTS.md` rules out. They now appear as `diriyah-turaif-panorama` and `red-sea-umluj-coast`. The other v1 gallery photos have no recorded license. Either allow a credits line or replace them.
- **ROSHN captions.** The SEDRA film has speech. A transcript is needed for English and Arabic tracks.
- **NEOM region photo.** `neom-wadi-al-disah` shows the Tabuk region rather than a NEOM site. It is captioned honestly but you may prefer to drop it.
