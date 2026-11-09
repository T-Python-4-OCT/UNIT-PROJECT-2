# Acceptance evidence (v2)

Run on 9 November 2026 in a Linux preview environment, against the `upgrade/v2` working tree. This is not the Windows harness. The preview used Django 6.1.3 from the project's virtual environment, Python 3.13, Playwright 1.63 Chromium, axe-core from the project's `node_modules`, and an esbuild preview bundle in place of Vite because the registry was unreachable. Run `.\scripts\verify.ps1` on Windows to confirm these results with the pinned toolchain.

## Results

| Check | Result |
| --- | --- |
| `manage.py check` | No issues |
| `manage.py test` | 12 of 12 passed |
| Content validation | All six records pass, including every image rendition, poster and caption file |
| Browser acceptance suite | 51 of 51 passed. The film playback test was excluded because the preview held placeholder video files. It needs the Windows run. |
| Route matrix | 9 routes × 2 languages × 2 themes, with no horizontal overflow and a one-row header at 320, 390, 768, 1024 and 1440 px |
| Accessibility | Zero axe WCAG 2.2 A and AA violations on all 36 page states and the open 3D scene |
| Keyboard | Skip link, mosaic, Projects menu with Escape and focus return, compact menu, theme persistence across reload and language switch, photo viewer stepping and focus return |
| Fallbacks | JavaScript disabled, reduced motion, missing WebGL 2 and a failed scene import all keep the poster and links |
| `check --deploy` | With `ATLAS_DEBUG=0` and `ATLAS_HTTPS=1`, no warnings |

## Performance (preview server, WhiteNoise, mobile profile)

390 × 844 viewport at 3× DPR, 80 ms latency, 10 Mbps down, 4× CPU throttling, three cold loads each.

| Route | Median LCP | Max CLS | Max core transfer | Deferred scene |
| --- | ---: | ---: | ---: | ---: |
| `/` | 444 ms | 0.0006 | 357,892 B | 237,771 B |
| `/ar/` | 440 ms | 0.0023 | 402,341 B | 237,771 B |
| `/projects/neom/` | 356 ms | 0.0003 | 259,575 B | n/a |
| `/ar/projects/diriyah/` | 384 ms | 0.0034 | 317,810 B | n/a |
| `/timeline/` | 308 ms | 0.0201 | 144,121 B | n/a |

All are within the budgets: LCP at most 2.0 s, CLS at most 0.05, 600 KB for the home page, 450 KB for a project page and 350 KB for the deferred scene.

## Quality scorecard

Scored from 1440 px and 390 px captures in English light and Arabic dark.

| Dimension | Score | Note |
| --- | ---: | --- |
| First impression | 4 | A bright mosaic of all six projects beside the headline replaces the dark hero |
| Hierarchy | 4 | Small sections now use small headings |
| Project identity | 4 | Accents, taglines and each project's own imagery |
| Imagery | 3 | ROSHN stills are 480p, and two photos have unresolved attribution terms |
| Map | 3 | The 2D map and labels work well, but the relief is still invented |
| Arabic and RTL | 4 | Mirrored layouts, one digit system and unified names |
| Dark mode | 4 | Designed surfaces and accents with measured contrast |
| Mobile | 4 | One-row header and compact menu |
| Accessibility | 4 | Zero axe violations, but ROSHN captions are missing |
| Performance | 5 | Well inside every budget |
| Accuracy | 4 | Every fact is sourced. Statuses were not re-checked online in this run. |
| Code | 4 | One validated source, but the Windows harness has not yet been rerun |

The average is 3.9. The bar in `UPGRADE_PROMPT.md` is not yet met, mainly because of the open items in `UPGRADE_PLAN.md`.
