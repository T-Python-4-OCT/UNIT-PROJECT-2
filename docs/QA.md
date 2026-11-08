# Browser and editorial review

The review covered both languages and themes for the home page and six details. It also covered the localized 404, keyboard path, 3D explorer and its fallback states. The tests run with the project's browser command against Django and the Vite production build.

- The production preview run passed all 39 checks in the acceptance suite. The 28 combinations of route, language and theme passed the 320, 390, 768 and 1440 CSS-pixel reflow checks, decoded-image checks, production asset checks and axe WCAG A/AA rules. The separate zoom and performance tests are part of the full verification command.
- Keyboard checks reached the skip link, main content, explorer, project links, language link and theme control. The theme remained set after reload, a language switch and next-project navigation. Chromium's accessibility tree exposed the pressed state and localized accessible name.
- JavaScript disabled, reduced motion, disabled WebGL 2 and an aborted scene chunk preserved the poster and project links. The on-demand scene opened by keyboard and removed its canvas on close. A separate Chromium pointer probe clicked the NEOM marker in English and Arabic and reached each localized detail route.
- The full desktop matrix and eight mobile home and Diriyah views were reviewed visually. Typography, shared controls, the project grid, images and captions, RTL order and both palettes were present. The first English light home capture missed three lazy tiles below the fold. The updated capture scrolls the last image into view, waits for paint and returns to the top. The recapture showed all six tiles.
- The bilingual summaries contain 22–34 words each. Every project has three sourced milestones. The six photograph files range from 56,370 to 168,866 bytes. Editorial and licensing evidence is in [SOURCES.md](SOURCES.md).

The verification harness saves full-page captures under the Playwright output directory. The accessibility check used keyboard interaction, browser accessibility-tree inspection and axe. A native screen-reader session was outside the verified coverage.
