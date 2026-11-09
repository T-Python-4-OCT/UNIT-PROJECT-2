# Acceptance evidence

The results below describe the 8 November build, before the subsequent media and caption changes. They are historical and do not verify the current build or embedded film playback.

Verified on 8 November 2026 on Windows with `./scripts/verify.ps1` in PowerShell. The harness served the Vite production build from Django's collected static directory with `ATLAS_DEBUG=0`. It compiled 28 Arabic messages, passed five Django tests and passed 44 browser tests. The frozen Bun install reproduced the locked dependencies.

| Requirement | Result | Evidence |
| --- | --- | --- |
| Django | Pass | `manage.py check` and five tests passed. |
| Template inheritance | Pass | Home, project and 404 templates use `base.html`. |
| Seven core pages | Pass | The homepage and six details rendered with distinct headings and content in both languages. |
| Dynamic URLs | Pass | Django reversed the named routes and returned 404 for unknown slugs. Chromium exercised the localized recovery links. |
| Static assets | Pass | Vite built hashed assets and Django collected them. Browser checks loaded the CSS, JavaScript, fonts, poster, all six WebPs and the deferred scene from `/static/`. |
| Uniform design | Pass | Inspected 28 full-page captures and mobile samples for shared navigation, spacing, typography, and image treatment. |
| Light and dark modes | Pass | Both themes rendered on every route. Keyboard tests changed the theme and confirmed persistence through reload, locale switch and next-project navigation. |
| Responsive layout | Pass | Checked each of the 28 page states at 320, 390, 768 and 1440 px. Edge verified all 14 routes at actual 200% browser zoom in an isolated profile. |
| English and Arabic | Pass | English stayed the root default with Arabic browser preferences. Arabic metadata, copy, captions, navigation, fallback messages and control names rendered with `lang="ar"` and RTL. Alternate links preserved the current project. |
| Keyboard access | Pass | Verified the skip link, focus order and rings, native project links, language navigation, theme toggle and 3D toggle. Chromium exposed the theme button's name and pressed state in its accessibility tree. |
| Contrast | Pass | The lowest measured text pair was 6.12:1 and the lowest control boundary was 3.32:1. The WCAG A/AA axe runs returned zero violations across the 28 page states and the open scene. See [design measurements](DESIGN.md). |
| Motion and fallback | Pass | Verified reduced motion, blocked scene import, unavailable WebGL 2, context loss, and JavaScript-disabled navigation. Clicked all six canvas badges, and verified scene canvas release on close. |
| Content accuracy | Pass | Each record includes primary sources and verification dates. The editorial register records the evidence for milestones and separates the two Red Sea Global destinations. See [sources](SOURCES.md). |
| Clean copy and code | Pass | Reviewed the English and Arabic templates, catalog and project copy. Dataset tests check the editorial limits, and authored source contains no explanatory comments. |
| Performance | Pass | Cold-load measurements below meet the transfer, LCP, CLS and mobile pixel-ratio targets. |

## Measured browser performance

Headless Chromium used a 390 × 844 CSS-pixel viewport, emulated 3× device pixel ratio, disabled network cache, 80 ms latency, 10 Mbps download, 5 Mbps upload and 4× CPU throttling. The server was on localhost. Each route had three cold navigations with trace capture disabled. The suite applies the 2.5 s LCP target to the median and checks the worst observed CLS and transfer. Core transfer counts the document and initially requested resources. Deferred transfer counts resources fetched after enabling 3D.

| Route | Median LCP and samples in ms | Maximum CLS | Maximum core transfer | Deferred scene |
| --- | ---: | ---: | ---: | ---: |
| `/` | 916 (496, 916, 1,340) | 0.0234 | 571,648 B | 138,997 B |
| `/ar/` | 1,008 (816, 1,008, 3,264) | 0.0163 | 614,253 B | 138,997 B |
| `/projects/neom/` | 920 (848, 920, 1,600) | 0.0010 | 266,008 B | — |
| `/ar/projects/diriyah/` | 612 (548, 612, 1,812) | 0.0012 | 337,774 B | — |

Both homepages capped scene pixel ratio at 1.50. Vite emits its generic 500 kB warning for the deferred 559 kB minified chunk. The compressed browser transfer is about 139 kB against a 3 MB deferred budget. Individual paint times varied. An earlier trace-enabled Arabic Diriyah sample measured 5,412 ms, and one Arabic homepage sample in the final run measured 3,264 ms.

## Interface review

Reviewed the homepage, six detail pages, localized 404 and map failure states. The layout follows the conventions in `PROJECT_PLAN.md` and `docs/DESIGN.md`. Django renders shared templates, and Tailwind and CSS tokens provide the shared styles.

| Domain | Evidence inspected | Result |
| --- | --- | --- |
| Accessibility | Keyboard paths, accessible names and state, visible focus, axe and reduced-motion behavior | Clear |
| Layout | Desktop captures, 390 px mobile captures, four responsive widths and Edge 200% zoom | Clear |
| Writing | Both catalogs and datasets, navigation labels and failure messages | Clear |
| Typography | Plex families, Arabic heading leading, line wrapping and delayed font arrival | Clear |
| Colors | Light and dark foreground pairs, outlines and focus token | Clear |
| UI | Theme states, directional arrows, interactive map, poster and failure state | Clear |

No actionable interface findings remain in the reviewed scope. The visual review used Chromium and Edge. Accessibility checks used the browser accessibility tree and axe, with no native screen-reader session.

| Reproduction | Severity | Owner | Verified repair |
| --- | --- | --- | --- |
| In the first homepage and NEOM captures, inspect the theme glyph and follow the back or next arrows in both directions. | Medium | Noura | One theme glyph renders at a time. Directional icons now match the link action in LTR and RTL. |
| Load Arabic Diriyah at 390 px under the mobile profile and delay font downloads. The header could switch rows twice and reached 0.6601 CLS. | High | Noura | The two-row grid keeps a stable order and height. Deliberately delaying fonts left the header and main positions unchanged. The cold production run passed the CLS budget. |
| Open the desktop scene and inspect badge 01 near the top of the stage. | Medium | Rayan | Updated camera framing kept every badge visible at 320 and 1440 px. |
| Inspect the empty scene status region before forcing a failed import. | Medium | Faisal | The live region remains in the accessibility tree before a failure and displays the localized fallback when populated. |

**Approve** for the inspected interface scope. Browser evidence is generated under `verification/test-results/`, the run log is `verification/final-run.log`, and manual scene captures are under `verification/scene/`.
