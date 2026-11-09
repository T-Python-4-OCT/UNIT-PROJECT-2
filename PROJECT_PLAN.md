# Saudi Giga Atlas project plan

Planning date: 8 November 2026

This plan maps README.md to an English-first Django website with a complete Arabic option. The implementation prompt is in MASTER_PROMPT.md. This document describes proposed work, not completed software or passed tests.

## 1. Scope and pages

Build seven core pages in each language, using shared templates.

| Page | English route | Editorial focus | Official source |
| --- | --- | --- | --- |
| Home | `/` | Six-project overview and visual explorer | [PIF](https://www.pif.gov.sa/en/our-investments/giga-projects/) |
| NEOM | `/projects/neom/` | Regional development and industry | [NEOM](https://www.neom.com/en-us) |
| Qiddiya | `/projects/qiddiya/` | Entertainment, sport and culture | [Qiddiya](https://qiddiya.com/en/) |
| Diriyah | `/projects/diriyah/` | Najdi heritage and urban development | [Diriyah Company](https://www.diriyahcompany.sa/en) |
| ROSHN | `/projects/roshn/` | Communities across Saudi Arabia | [ROSHN](https://www.roshn.sa/) |
| The Red Sea | `/projects/the-red-sea/` | Coastal tourism and conservation | [Red Sea Global](https://www.redseaglobal.com/en/portfolio/the-red-sea/) |
| AMAALA | `/projects/amaala/` | Wellness, art and marine discovery | [AMAALA](https://www.redseaglobal.com/en/portfolio/amaala/) |

Arabic routes add `/ar/`. Language switching preserves the project and works on direct page visits. English remains the default on `/`.

PIF lists five giga-project entities. Red Sea Global includes The Red Sea and AMAALA, allowing six distinct featured developments without inventing a sixth PIF entity. Use the headline `Six projects across Saudi Arabia`. [PIF classification](https://www.pif.gov.sa/en/our-investments/giga-projects/)

Homepage composition: compact navigation, short title, scene with poster fallback, six project entries and a restrained footer. Detail composition: project identity, strong hero image, short summary, up to three highlights, a small sourced milestone section and next-project navigation. Add content only when it helps explain the project.

## 2. Team and ownership

| Role | Name | Primary deliverables |
| --- | --- | --- |
| Leader | Faisal | Architecture, task board, shared-file ownership, dependency choices, integration and evidence |
| Agent 1 | Omar | Django routes, views, templates, structured data, translations and backend tests |
| Agent 2 | Noura | Saudi identity, tokens, typography, responsive styling, RTL and themes |
| Agent 3 | Rayan | Three.js scene, assets, controls, performance and fallback |
| Agent 4 | Sara | Source verification, English and Arabic copy review, browser QA and accessibility checks |

With four available runtime slots, the leader runs at most three workers at once. Discovery starts with Sara, Omar and Noura. Rayan enters when a slot opens. Sara returns for QA and Omar returns for defects as needed. Workers never edit the same file concurrently. Shared templates and dependency changes require an explicit ownership handoff.

## 3. Stack baseline

These releases were checked against official sources on the planning date. Recheck stable releases and compatibility when implementation starts, then record the versions actually installed. Package installation and build compatibility have not yet been tested in this repository.

| Component | Planning baseline | Purpose and source |
| --- | --- | --- |
| Python | 3.15.2 | Runtime, [official downloads](https://www.python.org/downloads/) |
| Django | 6.1.3 | Templates and routing, [official downloads](https://www.djangoproject.com/download/) |
| pip | 26.3 | Virtual-environment package installation, [changelog](https://pip.pypa.io/en/stable/news/) |
| Bun | 1.4.4 | JavaScript runtime, package manager and script runner, [official installation](https://bun.sh/docs/installation) |
| Tailwind CSS | 4.3.5 | Compiled styling, [releases](https://github.com/tailwindlabs/tailwindcss/releases) |
| Vite | 8.3.6 | Asset bundling, [releases](https://github.com/vitejs/vite/releases) |
| Three.js | r187 | Optional 3D explorer, [releases](https://github.com/mrdoob/three.js/releases) |

Django 6.1.3 explicitly adds Python 3.15 compatibility. If another required tool does not support that runtime, select the newest fully compatible stable combination and document the reason. [Django release notes](https://docs.djangoproject.com/en/6.1/releases/6.1.3/)

Keep the backend small: one Django app and a validated JSON content file. Store stable slugs, localized names and summaries, highlights, milestones, images, source URLs, verification dates and asset references. A database content editor is unnecessary for six fixed entries.

Use Django internationalization for interface strings and localized fields for editorial content. Compile translation catalogs during setup and document any required gettext tooling on Windows.

Bun replaces Node.js and npm in the frontend workflow. Keep Python and pip for Django. Record the installed Bun version and verify the selected tools on Windows. Use package.json scripts with bun run --bun dev and bun run --bun build to run Vite through Bun. Check browser-test tooling separately and document any proven runtime compatibility exception. Review required dependency lifecycle scripts and trust only the packages that need them. [Bun with Vite](https://bun.sh/guides/ecosystem/vite), [Bun package installation](https://bun.sh/docs/pm/cli/install)

Vite owns asset builds. Django owns HTML. Resolve hashed files through the production manifest, configure the static base path and verify nested chunks, fonts and model textures after collection. Tailwind must scan Django templates and use complete class names. [Vite backend integration](https://vite.dev/guide/backend-integration.html), [Tailwind source detection](https://tailwindcss.com/docs/detecting-classes-in-source-files), [Django static files](https://docs.djangoproject.com/en/6.1/howto/static-files/)

## 4. Visual and content specification

Proposed custom palette:

| Token | Starting value | Intended use |
| --- | --- | --- |
| Palm | `#123D32` | Primary brand color and light-theme actions |
| Limestone | `#F5F1E8` | Light background and dark-theme text |
| Sand | `#D9C9AA` | Secondary surfaces and restrained accents |
| Charcoal | `#151D19` | Dark background and light-theme text |
| Brass | `#B4935A` | Small decorative accents |

These are design proposals, not official Saudi tokens. Noura must measure actual foreground and background pairs before use. Brass is not approved for small text by default.

Use Saudi or Masmak display typography only after checking the downloaded font's web-use license. IBM Plex Sans and IBM Plex Sans Arabic provide an open-license fallback. Use correct language metadata, natural Arabic line breaks and logical CSS properties. Do not apply tracking that breaks Arabic joining. [Ministry of Culture font initiative](https://www.moc.gov.sa/modules/pages/initiative/saudiandawwal_calligraphy), [official Masmak announcement](https://www.spa.gov.sa/w1873548?lang=en&newsid=2436438), [IBM Plex](https://github.com/IBM/plex)

Use official logos where permitted, original site branding and licensed imagery. Use media that permits credit-free presentation. If an asset cannot be used, replace it with a licensed alternative or text identity. Keep factual content separate from promotional claims.

Limit page copy rather than shrinking it. Use short headings, a 30-word homepage introduction and 45-word project summaries as editorial targets. Keep necessary grammar. Reject em dashes, repeated punctuation and generic slogans in user-facing copy.

## 5. Implementation sequence

| Phase | Work | Exit evidence |
| --- | --- | --- |
| 1. Inspect | Faisal reads repository instructions, checks tools and verifies compatible releases | Requirement matrix, dependency decision and task ownership |
| 2. Research and design | Sara verifies six project records and assets; Noura defines English and Arabic layouts, tokens and type | Source register, content schema and a concrete home/detail design |
| 3. Build a vertical slice | Omar builds the shell, home and one detail page; Noura styles both themes and directions | Working navigation, locale switch, theme persistence and static poster |
| 4. Extend and enhance | Omar adds five records; Rayan builds the scene against agreed hooks | All seven page types available in both languages with scene fallback |
| 5. Review and repair | Sara runs browser checks; Faisal assigns defects to their owners | Passed acceptance rows with screenshots and command outcomes |
| 6. Deliver | Faisal verifies setup from pinned dependencies and documents operation | Runnable project, setup guide, source register and final evidence report |

Agree file boundaries before phase 3. Suggested areas are `config/`, `projects/`, `templates/`, `frontend/styles/`, `frontend/scripts/`, `static/`, `locale/`, `tests/`, `docs/` and `scripts/`. Faisal owns dependency files and global configuration. Omar owns template structure; Noura requests explicit handoffs when markup needs design changes.

## 6. 3D and performance targets

Create one polished scene rather than six heavy viewers. Use a stylized landscape and project selection that has equivalent HTML links. Distinguish representative geography from exact project boundaries. Keep Three.js and its addons on the same version. Package any model decoders and textures needed by the production build. [Three.js installation](https://threejs.org/manual/pages/installation.html), [model loading](https://threejs.org/manual/pages/loading-3d-models.html)

The scene is progressive enhancement. Render content first and defer 3D until idle or deliberate interaction. Provide a static poster for reduced motion, unavailable WebGL 2 or load failure. Pause the renderer while hidden and provide pause control for sustained animation. [Renderer requirements](https://threejs.org/docs/pages/WebGLRenderer.html)

Initial project budgets: core page assets at or below 1 MB transferred, deferred scene payload at or below 3 MB, and capped device pixel ratio of 1.5 on mobile. Measure LCP with a target of 2.5 seconds and CLS of 0.1 or less under a documented test profile. These are targets, not measured results. If the scene misses its budget, simplify textures, geometry and effects before increasing the budget.

## 7. Acceptance matrix

| Requirement | Passing evidence | Owner |
| --- | --- | --- |
| Django | Django checks and backend tests pass | Omar |
| Template inheritance | Home and detail templates extend the shared base | Omar |
| Seven core pages | Home and all six distinct slugs return expected content in both languages | Omar |
| Dynamic URLs | Named URL reversal works and unknown slugs return 404 | Omar |
| Static assets | Production build and static collection succeed; no missing assets in browser | Faisal |
| Uniform design | Shared navigation, type, spacing and tokens inspected across all pages | Noura |
| Light and dark modes | Every page works in both themes; saved choice survives reload and navigation | Noura |
| Responsive layout | No lost content or horizontal overflow at 320, 390, 768 and 1440 px or 200 percent zoom | Sara |
| English and Arabic | Complete localized content, correct `lang` and `dir`, current-page language switching | Omar and Sara |
| Keyboard access | Skip link, logical focus, visible focus and named native controls work | Sara |
| Contrast | Measured 4.5:1 normal text and 3:1 large text and meaningful UI boundaries in both themes | Noura |
| Motion and fallback | Reduced motion, disabled WebGL and failed scene assets all leave a usable page | Rayan |
| Content accuracy | Every numerical claim, status and milestone has an official source and verification date | Sara |
| Asset provenance | Used fonts, images, logos and models have recorded usage rights | Sara |
| Clean copy and code | Copy reviewed in both languages; no explanatory comments in authored code | Sara and Faisal |
| Performance | Transfer budgets and documented browser measurements meet targets | Rayan |

Check the complete route matrix: seven core pages in two languages and two themes. Automate route coverage and inspect full-page captures for layout. Exercise keyboard navigation, theme persistence, language switching and failure states directly. Automated accessibility checks supplement manual inspection.

## 8. Harness and completion

Create `scripts/verify.ps1` as a small Windows-friendly verification entry point. Make it fail on nonzero command exits and summarize each stage. Keep dependency installation separate from routine verification.

The implemented harness should cover:

- `python -m pip check`
- `python manage.py check`
- `python manage.py test`
- Translation compilation and completeness checks
- `bun run --bun build`
- `python manage.py collectstatic --noinput`
- The project's configured browser-test command against built assets

Add migration consistency checks only if application models are introduced. Use `bun install` for initial resolution and commit `bun.lock`. Use `bun install --frozen-lockfile` during clean setup to reproduce it. Do not invent a passing command before its script exists. [Django testing guidance](https://docs.djangoproject.com/en/6.1/topics/testing/overview/)

Track defects as open, assigned, fixed and verified. Include affected route, language, theme, reproduction steps and evidence. Fix blocked navigation, unreadable text and failed fallbacks before visual polish. After two unsuccessful fixes, change the approach or reviewer.

Completion requires passing mandatory acceptance rows and a final visual inspection. Document any unresolved item as failed or not verified. Deliver setup instructions in `SETUP.md`, sources and licenses under `docs/`, and an evidence report. Preserve the original README assignment. Keep hosting, paid assets and unrelated features outside this scope.
