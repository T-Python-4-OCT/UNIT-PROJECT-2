import 'vite/modulepreload-polyfill';
import '@fontsource/ibm-plex-sans/latin-400.css';
import '@fontsource/ibm-plex-sans/latin-600.css';
import '@fontsource/ibm-plex-sans-arabic/arabic-400.css';
import '@fontsource/ibm-plex-sans-arabic/arabic-600.css';
import '@fontsource/instrument-serif/400.css';
import '@fontsource/instrument-serif/400-italic.css';
import '@fontsource/amiri/400.css';
import './styles/atlas.css';
import './scripts/theme.js';
import './scripts/navigation.js';
import './scripts/expedition.js';
import './scripts/locator-loader.js';
import './scripts/relief-shade.js';
import './scripts/project-media.js';
import './scripts/motion.js';

if (document.querySelector('[data-scrubber]')) import('./scripts/timeline-scrubber.js');
if (document.querySelector('[data-live-search]')) import('./scripts/search-live.js');
if (document.querySelector('[data-compare-scroll]')) import('./scripts/compare-scroll.js');
if (
  document.querySelector('[data-gallery-strip]') &&
  matchMedia('(hover: hover) and (pointer: fine) and (prefers-reduced-motion: no-preference)').matches
) {
  import('./scripts/view-cursor.js');
}
