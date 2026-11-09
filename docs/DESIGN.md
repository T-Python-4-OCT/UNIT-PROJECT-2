# Visual system

The atlas opens with an introduction, then leads from the map to the project itinerary. Limestone surfaces, palm green display type and brass labels carry through the six project stories. The map and cards share the same stop numbers on desktop. 

The terrain poster is `static/atlas/media/atlas-poster.svg`, a 1440 × 552 north-up vector map with a Natural Earth boundary, shaded land and subdued regional context. Five location markers use leader lines to separate nearby projects. Dashed rings show examples of ROSHN’s communities across the country. The HTML overlays localized project links directly on the map and keeps the geography north-up in both languages.

IBM Plex Sans and IBM Plex Sans Arabic share the display and body hierarchy. Arabic headings have more leading and no tracking. The layout follows document direction and keeps the landscape north-up. The fonts are available under the SIL Open Font License 1.1. Ministry of Culture materials describe the Saudi and Masmak typefaces, and the associated download platforms returned HTTP 403 during research on 8 November 2026. With web embedding rights unverified for those files, the build uses Plex. [IBM Plex](https://github.com/IBM/plex) · [Saudi typeface initiative](https://www.moc.gov.sa/en/Modules/Pages/Initiative/SaudiandAwwal_Calligraphy) · [Masmak announcement](https://www.spa.gov.sa/w1873548?lang=en&newsid=2436438)

## Contrast measurements

Ratios below apply to the opaque tokens in `frontend/styles/atlas.css`. The home title and introduction sit over a dark gradient. Project photographs have separate captions, and the map markers use opaque labels.

| Pair | Light | Dark | Threshold |
| --- | ---: | ---: | ---: |
| Body on page | 15.51 | 15.51 | 4.5 |
| Secondary text on page | 6.89 | 9.56 | 4.5 |
| Secondary text on tinted surface | 6.25 | 6.70 | 4.5 |
| Accent text on page | 10.90 | 10.08 | 4.5 |
| Accent text on tinted surface | 9.88 | 7.06 | 4.5 |
| Eyebrow on page | 6.12 | 8.97 | 4.5 |
| Filled control text on fill | 10.90 | 10.08 | 4.5 |
| Focus ring on page | 7.34 | 8.97 | 3 |
| Focus ring on tinted surface | 6.66 | 6.28 | 3 |

## Vertical-slice review

Inspected 1440px Chromium captures of the home page in English light and Arabic dark and the NEOM page in English dark and Arabic light. The shared alignment, atlas artwork, editorial hierarchy and mirrored layout were present in the captured slice. The first captures showed simultaneous theme glyphs and arrows pointing in the wrong direction. The CSS now switches glyphs by theme and maps forward and back arrows separately.

A follow-up Chromium probe with the updated working-tree styles checked both pages at 320px in English light, 390px in Arabic dark, 768px in Arabic light and 1440px in English dark. Each page had zero horizontal overflow and displayed one correct theme glyph. The 320px and 390px captures showed the header wrapping with all controls visible. This slice used the first project. The production-build browser suite covers the complete collection.

## Version 2 system

Tokens live at the top of `frontend/styles/atlas.css`: a seven-step fluid type scale, a spacing scale, three radii, two elevations and motion durations. The Najdi parapet profile appears above section headings and along the footer edge. Each project record carries a light and dark accent. The accent colors rules, numbers, status dots, map labels and pager titles on that project's page, card and map label.

| Project | Light accent | On page | On tinted surface | Dark accent | On page | On tinted surface |
| --- | --- | ---: | ---: | --- | ---: | ---: |
| NEOM | `#1d5677` | 7.15 | 6.50 | `#9ccbe4` | 9.89 | 6.93 |
| Qiddiya | `#8a4512` | 6.44 | 5.85 | `#ecb37c` | 9.25 | 6.48 |
| Diriyah | `#8a5528` | 5.56 | 5.05 | `#e0b68c` | 9.20 | 6.45 |
| ROSHN | `#2c6a3a` | 5.87 | 5.33 | `#a2d6a9` | 10.42 | 7.30 |
| The Red Sea | `#0d6466` | 6.25 | 5.68 | `#86d8d1` | 10.44 | 7.32 |
| AMAALA | `#9c3f2c` | 6.00 | 5.45 | `#f2a895` | 8.85 | 6.20 |

Every accent clears 4.5:1 for normal text on both page and tinted surfaces.
