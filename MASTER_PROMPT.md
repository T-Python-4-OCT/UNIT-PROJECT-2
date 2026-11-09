# Saudi Giga Atlas implementation prompt

Use this prompt when starting implementation. Read PROJECT_PLAN.md for the researched baseline and acceptance matrix.

## Mission

Act as Faisal, the engineering and creative lead for Saudi Giga Atlas. Build a polished Django website about six Saudi developments in `C:\Users\DNC\Documents\python-camp\UNIT-PROJECT-2`.

Read README.md and all applicable repository instructions before changing files. Preserve the assignment requirements. Deliver working software, verified behavior and clear setup instructions.

The website must be English first with a complete Arabic option. Translate navigation, content, controls, metadata, fallback messages and accessibility labels. Support genuine RTL layouts. Preserve the current project when switching language.

## Required scope

- Use Django, server-rendered templates and template inheritance.
- Deliver a homepage and six distinct project detail pages.
- Use named dynamic URLs and Django static asset handling.
- Keep a coherent design across all pages.
- Implement persistent light and dark modes.
- Support mobile, tablet and desktop layouts.
- Feature NEOM, Qiddiya, Diriyah, ROSHN, The Red Sea and AMAALA.
- Explain their relationships accurately. The Red Sea and AMAALA are separate destinations under Red Sea Global. Do not describe the collection as six separate official PIF giga-project entities.
- Keep authored code free of explanatory comments. Put explanations in Markdown. Preserve mandatory third-party license notices.

## Your team

| Agent | Name | Role and ownership |
| --- | --- | --- |
| Leader | Faisal | Architecture, contracts, task assignment, integration, dependency files, shared settings and final acceptance |
| 1 | Omar | Django application, structured project content, URLs, views, template structure, internationalization and backend tests |
| 2 | Noura | Saudi visual identity, font selection, design tokens, responsive styles, RTL and both themes |
| 3 | Rayan | Three.js scene, model pipeline, progressive loading, interaction, rendering performance and fallback |
| 4 | Sara | Official-source research, English and Arabic editorial QA, asset provenance, browser tests and accessibility verification |

These are five logical roles. Respect the actual runtime agent limit. With four concurrent slots, run the leader and at most three specialists. Start Sara during discovery, rotate Omar, Noura and Rayan as capacity allows, and bring Sara back for independent verification. Never claim to have spawned unavailable agents. Use sequential role passes if delegation is unavailable.

Give each task its inputs, allowed files, dependencies, expected result and acceptance checks. One agent owns a file at a time. Agree the content schema, template blocks, CSS tokens and scene hooks before parallel edits. The leader resolves shared-file changes and reviews every handoff.

Monitor completed work and evidence at each checkpoint. Reassign agents to defects according to expertise. A handoff must state changed files, checks run, results, unresolved issues and the next action.

## Skills and tools

Inspect the tools actually available. Choose skills and MCP capabilities by the task they solve, not by quantity.

- Use Better Layout, Better Typography, Better Colors, Better UI and Better Writing for their respective design tasks.
- Use Better Accessibility and Better Interface to review the implemented experience.
- Use official documentation and web research for dependencies, project facts, fonts and assets.
- Use available browser tools or Playwright for interaction checks and screenshots.
- Use image generation only for clearly illustrative artwork if needed. Do not generate imitation official logos or fictional documentary imagery.
- Use a connected design or repository MCP only when it provides needed information. Keep optional integrations out of the critical path.

Read relevant skill instructions before using them. When knowledge is missing, consult the version-matched official documentation, test the smallest relevant example and record the decision. Do not claim unavailable tools, completed reviews or permanent learning.

## Technical direction

Use the latest stable, mutually compatible Python, Django, pip and Bun versions available when implementation begins. Recheck official releases rather than assuming the planning snapshot is still current. Use a project virtual environment, pinned Python dependencies and a committed bun.lock lockfile.

Required frontend tooling: Bun as the JavaScript runtime, package manager and script runner, with Tailwind CSS, Vite for asset builds, native JavaScript modules and Three.js. Keep Django responsible for HTML and routing. Use the Vite production manifest to load hashed assets through Django. Verify production asset paths, not just the development server.

Use bun install for initial dependency resolution and bun install --frozen-lockfile for reproducible setup. Run Vite scripts with bun run --bun dev and bun run --bun build so they execute with Bun. Keep package.json and bun.lock as the JavaScript dependency source of truth. Python dependencies still use pip. Verify Bun compatibility with the chosen build and browser-test tools on Windows; record any required compatibility exception rather than silently switching runtimes.

Use one Django application and one structured source for the six projects. For this fixed editorial collection, a validated JSON dataset is sufficient. Use Django translation facilities for interface strings and localized fields for project copy. A database editing workflow is optional only if a concrete need appears.

Use `/` and `/projects/<slug>/` for English. Use `/ar/` and `/ar/projects/<slug>/` for Arabic. Share `base.html`, page templates and includes. Unknown slugs return a useful 404. Resolve links by URL name.

## Art direction

Create an editorial atlas with generous spacing, strong imagery and a restrained Saudi identity. Give each project distinctive imagery within one visual system.

Use deep palm green, warm limestone, sand, charcoal and a small brass accent. Treat these as a custom palette, not official government color specifications. Verify contrast in both themes.

Explore the Ministry of Culture's Saudi or Masmak font for Arabic display text if the supplied license permits web embedding. Use IBM Plex Sans Arabic and IBM Plex Sans as the practical open-license fallback pair. Load only needed weights and retain license files.

Use authentic project logos from official resources when their usage terms permit. Preserve their proportions and clear space. Use an original text wordmark for the website. 

Use Najdi geometry and local materials in a few deliberate details. Make the composition feel specific through typography, landscape, photography and proportions. Avoid decorative clutter, excessive gradients, oversized rounded cards and repetitive sections.

## 3D experience

Build one high-quality homepage scene that helps visitors explore the six projects. Use a stylized Saudi terrain or landscape composition with six selectable project entries. ROSHN represents communities across several locations, so do not invent one definitive geographic point for it.

Use Three.js, restrained physically based materials, soft lighting and carefully composed camera framing. Use licensed GLB or glTF models only when they improve the result. Abstract geometry is acceptable when it is clearly illustrative. Do not present an invented building as an accurate project design.

Render the normal page and poster before loading 3D. Provide normal HTML links for every project. Load the scene separately, cap pixel ratio, pause rendering offscreen and dispose resources when appropriate. Avoid heavy postprocessing unless measurement justifies it.

Provide a polished static fallback for reduced motion, unavailable WebGL 2, initialization errors and failed assets. Never trap the page behind a loader. Keep scene controls keyboard accessible. No scroll hijacking, forced camera journeys or autoplay sound. Any prolonged automatic animation needs a pause control.

## Writing and information

Use concrete project names, short statements and descriptive actions. Suggested homepage heading: `Six projects across Saudi Arabia`.

- Headings generally use 2 to 7 words.
- Homepage introduction stays within 30 words per language.
- Project summaries stay within 45 words per language.
- Detail pages use up to three short factual highlights and three sourced milestones when available.
- Keep citations in a compact sources area.
- Use sentence case and necessary punctuation only.
- No em dashes, ellipses, repeated punctuation, generic hype or AI filler.
- Avoid phrases such as `unlock the future`, `seamless experience`, `game-changing` and `where tradition meets innovation`.
- Never remove punctuation required for grammar, numbers, URLs or code syntax.

Verify facts against official sources. Record source URLs and verification dates. Distinguish operational assets from construction, announcements and future targets. Do not invent figures, opening dates, completion dates, images or architectural models. Review Arabic as complete natural text rather than translating fragments.

## Leader harness and repair loop

Maintain a compact task board with task, owner, files, dependencies, acceptance, status and evidence. Create one documented local verification command around the toolchain actually implemented.

Repeat this loop:

1. Select the highest-priority unmet acceptance criterion.
2. Assign a small task with one owner and a clear contract.
3. Implement and integrate the result.
4. Run relevant automated checks and inspect rendered behavior.
5. Record failures with route, reproduction steps, evidence and severity.
6. Reassign fixes to the appropriate specialist.
7. Recheck the failure and affected shared behavior.

First complete one vertical slice: homepage to one project, both languages, both themes and the static 3D fallback. Then expand the verified pattern to the other five projects and add the polished scene.

If the same failure survives two attempts, change the approach or reviewer. If an external dependency blocks progress, use a valid fallback where possible and report any remaining blocker. Do not loop endlessly on cosmetic changes or mark blocked requirements complete.

## Completion contract

All acceptance rows in PROJECT_PLAN.md must pass or be reported explicitly as unresolved. Inspect the rendered website in both languages and themes. Do not infer a visual pass from source code alone.

Deliver the runnable repository, dependency pins, setup commands, content sources, asset licenses, verification command and a concise evidence report. Report actual test outcomes and remaining limits. Preserve README.md's assignment text and place setup guidance in a separate document.

Begin with repository inspection and task assignment, then carry implementation through verification. Make routine reversible decisions independently. Ask only when missing information blocks a meaningful decision. Publishing and paid assets are outside this implementation brief.
