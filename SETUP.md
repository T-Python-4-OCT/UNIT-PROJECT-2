# Run Saudi Giga Atlas

Use PowerShell from the repository root on Windows. The verified runtime versions are Python 3.15.2, pip 26.3 and Bun 1.4.4. Django and its Python dependencies are pinned in `requirements.txt`. Frontend versions are pinned in `package.json` and `bun.lock`.

Install [Python](https://www.python.org/downloads/release/python-3152/) and [Bun](https://bun.sh/docs/installation) first. Open a new shell so `py` and `bun` are available on `PATH`.

```powershell
py -3.15 -m venv .venv
$python = '.\.venv\Scripts\python.exe'
& $python -m pip install pip==26.3
& $python -m pip install -r requirements.txt
bun install --frozen-lockfile
& $python scripts/compile_translations.py
bun run --bun build
& $python manage.py collectstatic --noinput
& $python manage.py runserver
```

Open [English](http://127.0.0.1:8000/) or [Arabic](http://127.0.0.1:8000/ar/). The project uses an editorial dataset and needs no database setup.

The compiler uses pinned `polib` to write Django's gettext `.mo` catalog on Windows. Changes to the Arabic `.po` require recompilation and a server restart. Changes to `projects/data/projects.json` also require a restart.

## Work on the frontend

In a separate shell run `bun run --bun dev`. In the Django shell set `$env:ATLAS_VITE_DEV = '1'` before running `manage.py runserver`. Django serves pages at port 8000 and Vite serves development assets at port 5173. Remove that variable to use the production build.

Django resolves hashed scripts and styles from `static/build/.vite/manifest.json`. The local production-mode verification server serves collected files with WhiteNoise. To run it manually, set `$env:ATLAS_DEBUG = '0'` after building and collecting the assets.

## Verify

Install the pinned Playwright Chromium binary once, then run the verification harness. The browser zoom check uses Microsoft Edge in a temporary test profile with a 200% zoom preference.

```powershell
bun run --bun playwright install chromium
.\scripts\verify.ps1
```

The harness checks Python dependencies, Django, translations, the production build and collection, then runs the browser suite against collected assets on port 8765. Use `-Port 8766` if that port is occupied. Browser captures and logs are written to `verification/`.

See `docs/SOURCES.md` for project and media provenance, `docs/licenses/` for bundled font and library notices, and `docs/EVIDENCE.md` for verification results.

## Version checks

Stable releases were checked on 8 November 2026. Django 6.1.3 adds Python 3.15 compatibility. Vite 8.3.6, Tailwind CSS 4.3.5 and Three.js r187 are pinned. Bun 1.4.4 resolved the lockfile and ran Vite and Playwright on Windows. No dependency lifecycle scripts required additional trust. [Python](https://www.python.org/downloads/) · [Django](https://docs.djangoproject.com/en/6.1/releases/6.1.3/) · [pip](https://pip.pypa.io/en/stable/news/) · [Bun](https://bun.sh/docs/installation) · [Vite](https://github.com/vitejs/vite/releases/tag/v8.3.6) · [Tailwind CSS](https://github.com/tailwindlabs/tailwindcss/releases/tag/v4.3.5) · [Three.js](https://github.com/mrdoob/three.js/releases/tag/r187)
