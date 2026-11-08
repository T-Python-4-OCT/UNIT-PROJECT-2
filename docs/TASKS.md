# Implementation board

| Task | Owner | Files | Depends on | Acceptance and evidence | Status |
| --- | --- | --- | --- | --- | --- |
| Pin and integrate the toolchain | Faisal | `config/`, `requirements.txt`, `package.json`, `bun.lock`, `vite.config.js`, `frontend/main.js` | Official release and registry checks | Frozen install, manifest, compiled translations and static collection passed | Verified |
| Verify project records and image rights | Sara | `projects/data/projects.json`, `static/atlas/media/` photographs, `docs/SOURCES.md` | Official project sources and licensed photography | Six bilingual records, with verification dates and rights for each image | Verified |
| Build the Django routes and page templates | Omar | `projects/`, `templates/`, `locale/` | Shared data schema and asset tag | English and Arabic home and detail routes, localized errors and five backend tests | Verified |
| Style the atlas and fallback poster | Noura | `frontend/styles/`, `static/atlas/media/atlas-poster.svg`, `docs/DESIGN.md` | Template hooks and font files | Inspected both directions and themes at the required widths, and measured contrast | Verified |
| Build the progressive 3D view | Rayan | `frontend/scripts/atlas*.js`, `docs/SCENE.md` | Explorer hooks and poster composition | All six destinations, lazy loading, fallbacks and mobile DPR verified | Verified |
| Verify the production site | Sara and Faisal | `tests/`, `playwright.config.js`, `scripts/verify.ps1`, `docs/EVIDENCE.md` | Built and collected assets and full content | 44 browser tests and visual inspection. See [acceptance evidence](EVIDENCE.md). | Verified |

Each specialist owns their files through handoff. Faisal integrates shared settings, asset loading and test execution.
