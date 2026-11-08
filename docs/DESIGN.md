# Visual system

The atlas uses an editorial layout with limestone surfaces, palm green display type, and a small brass cue for labels and map details. The same header, grid rhythm, compass motif and text roles carry through the home and detail views. Photographs give each development an individual visual identity. The project index uses full-card links and repeats the explorer’s order.

The original terrain poster is `static/atlas/media/atlas-poster.svg`, a 1440 × 552 schematic with a north-up composition, hand-drawn contour strokes and a coast cut into an inset cartographic grid. Five approximate location symbols and a distributed dot motif distinguish projects with a representative location from ROSHN’s communities across the country. The graphic is illustrative and uses no external imagery, mapping tiles, or government branding. The surrounding HTML provides the caption and every project link in both languages. The artwork itself has no text.

IBM Plex Sans and IBM Plex Sans Arabic share the display and body hierarchy. Arabic headings have more leading and no tracking. The layout follows document direction and keeps the landscape north-up. The fonts are available under the SIL Open Font License 1.1. Ministry of Culture materials describe the Saudi and Masmak typefaces, and the associated download platforms returned HTTP 403 during research on 8 November 2026. With web embedding rights unverified for those files, the build uses Plex. [IBM Plex](https://github.com/IBM/plex) · [Saudi typeface initiative](https://www.moc.gov.sa/en/Modules/Pages/Initiative/SaudiandAwwal_Calligraphy) · [Masmak announcement](https://www.spa.gov.sa/w1873548?lang=en&newsid=2436438)

## Contrast measurements

Ratios use WCAG sRGB relative luminance with the opaque token values in `frontend/styles/atlas.css`. Text and control states are drawn on solid surfaces. The poster and photography contain no interface text overlays other than the card index, which has its own opaque backing.

| Pair | Light | Dark | Threshold |
| --- | ---: | ---: | ---: |
| Body on page | 15.51 | 15.51 | 4.5 |
| Secondary text on page | 6.89 | 9.56 | 4.5 |
| Secondary text on tinted surface | 6.25 | 6.70 | 4.5 |
| Accent text on page | 10.90 | 10.08 | 4.5 |
| Accent text on tinted surface | 9.88 | 7.06 | 4.5 |
| Eyebrow on page | 6.12 | 8.97 | 4.5 |
| Image index on its opaque backing | 6.67 | 7.84 | 4.5 |
| Filled control text on fill | 10.90 | 10.08 | 4.5 |
| Control outline on page | 3.66 | 4.75 | 3 |
| Control outline on tinted hover surface | 3.32 | 3.33 | 3 |
| Focus ring on page | 7.34 | 8.97 | 3 |
| Focus ring on tinted surface | 6.66 | 6.28 | 3 |
| Focus ring on card-index backing | 7.99 | 7.84 | 3 |

## Vertical-slice review

Inspected 1440px Chromium captures of the home page in English light and Arabic dark and the NEOM page in English dark and Arabic light. The shared alignment, atlas artwork, editorial hierarchy and mirrored layout were present in the captured slice. The first captures showed simultaneous theme glyphs and arrows pointing in the wrong direction. The CSS now switches glyphs by theme and maps forward and back arrows separately.

A follow-up Chromium probe with the updated working-tree styles checked both pages at 320px in English light, 390px in Arabic dark, 768px in Arabic light and 1440px in English dark. Each page had zero horizontal overflow and displayed one correct theme glyph. The 320px and 390px captures showed the header wrapping with all controls visible. This slice used the first project. The production-build browser suite covers the complete collection.
