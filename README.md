# Engr. Peter John R. Bacani: engineering portfolio

A static portfolio site: home, one searchable project collection, eight case studies, skills, about, résumé and research, and contact. It needs no database, login or paid service.

**Stack.** A small Python generator (`tools/build.py`, Jinja2) turns JSON content and HTML templates into plain HTML, CSS and a little JavaScript in `dist/`. I used Python instead of Next.js because Node.js is not installed on this computer. The output is ordinary static files, so any host works.

## Folder map
```
content/      profile.json, skills.json, media.json, projects/*.json   <- you edit these
templates/    page layouts (Jinja2 HTML)
static/       CSS, JavaScript, fonts (IBM Plex, self-hosted), icon
media/        optimised images, videos, PDFs + manifest.json (generated)
tools/        build.py, optimize_media.py, check.py
dist/         the finished website (generated, not committed)
docs/         SOURCE_INVENTORY.md, OPEN_QUESTIONS.md, QA_REPORT.md
Projects/, Peter.jpg, Resume.pdf   your untouched originals
```

## Run it locally
Needs Python 3.10+. In PowerShell, from this folder:

```bash
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements-tools.txt
.venv\Scripts\python.exe tools/optimize_media.py
.venv\Scripts\python.exe tools/build.py
.venv\Scripts\python.exe tools/check.py
.venv\Scripts\python.exe -m http.server 4173 --directory dist
```
Open http://localhost:4173. (`.venv` already exists on this machine, so only the last four lines are needed.)

`optimize_media.py` needs your originals and only has to run when media changes. `build.py` needs only `jinja2` and the committed `media/` folder, which is what the hosts use.

## Deployment
**Nothing is online yet.** I cannot create accounts or publish for you, so there is no public URL. Choose one route:

### A. Netlify with drag-and-drop (fastest, no account linking)
1. Set your final address if you know it, then build: `$env:SITE_URL="https://your-name.netlify.app"; .venv\Scripts\python.exe tools/build.py`
2. Go to app.netlify.com/drop and drag the `dist` folder onto the page.
3. Netlify gives you an HTTPS link. Rename it under Site configuration → Change site name, then rebuild with the exact `SITE_URL` and drop again so social previews and the sitemap use the right address.

### B. Netlify or Vercel from GitHub (updates on every push)
1. Create a GitHub repository and push this folder. `.gitignore` already excludes your large originals, so the optimised `media/` folder is what gets published.
2. Netlify: Add new site → Import from Git. `netlify.toml` supplies the build settings.
   Vercel: Import project. `vercel.json` supplies the build settings.
3. Add the environment variable `SITE_URL` (your final address) in the host's settings. The sitemap and social cards need it. Netlify also provides it automatically. There are no secrets.

### Custom domain
Buy the domain from any registrar. In Netlify: Domain management → Add a domain. In Vercel: Settings → Domains. Follow the DNS records shown. HTTPS certificates are issued automatically. Then set `SITE_URL=https://yourdomain` and redeploy.

### Before you publish
Read `docs/OPEN_QUESTIONS.md`. Two items matter most: your résumé PDF contains your phone number and licence numbers, and two videos (school system, news feature) may need consent or permission.

## Maintenance
**Edit your profile, experience, education, awards.** `content/profile.json`.
**Edit skills.** `content/skills.json`. Each skill names its basis and the project slugs that support it.
**Replace the résumé.** Overwrite `Resume.pdf`, run `optimize_media.py`, then `build.py`. The résumé is shown only as page images in a modal; the PDF itself is never published.
**Replace your portrait.** Overwrite `Peter.jpg` and rerun the same two commands. It is cropped by CSS (4:5 frame, face kept in view), never stretched.

### Add a project
1. Put the files in `Projects/<Name>/`.
2. Add each image, video or PDF to `content/media.json`. Thumbnails must be keyed `thumb-<name>`, with a descriptive `alt`.
3. Copy `content/projects/hydra.json` to `content/projects/<slug>.json` and edit. Key fields: `name`, `summary`, `status`, `statusGroup` (drives the status filter), `role`, `tech` (drives the technology filter and search), `featuredOrder`, `thumbnail`, `docs`, `videos`, and `sections`.
4. Section blocks: `p`, `ul`, `table`, `flow` (diagram), `figure`, `gallery`, `video`, `note`.
5. Add `"year": 2025` to enable the Year filter and "Newest first" sort. They appear once at least two projects have years.
6. Run `optimize_media.py`, `build.py`, `check.py`.

### Replace a thumbnail
Overwrite the original image (keep the path in `media.json`, or edit the path), then run `optimize_media.py` and `build.py`. The same file feeds the card, the featured card, the case-study header and the social card. Social cards are letterboxed to 1200×630, never cropped.

### Hide or show a video
In `content/media.json` set `"publish": false` (hide) or `true` (show) for that video, then run `optimize_media.py` and `build.py`.

## Search engines
The site tells search engines not to list it (a `noindex` tag on every page, plus an `X-Robots-Tag` header in `static_root/_headers`, `netlify.toml` and `vercel.json`). It is meant to be shared by link. To allow Google to list it, build with `ALLOW_INDEXING=1` and delete the `X-Robots-Tag` lines from those three files.

## Contact handling
The contact page uses a `mailto:` link and a copy-address button. There is no form, so there is nothing to spam-protect and no service to pay for.

## Environment variables
See `.env.example`. Both are optional and neither is secret: `SITE_URL` (absolute address for sitemap, canonical and social images) and `BASE_PATH` (sub-folder hosting).
