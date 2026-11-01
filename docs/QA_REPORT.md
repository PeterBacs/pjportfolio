# QA report

Run on 2026-10-04 against a local build served at http://localhost:4173 (Windows, headless Chrome and the in-app browser). Nothing here was run against a public URL, because none exists yet. **No Lighthouse, axe or other scored audit was run**, so no performance or accessibility scores are claimed.

## Passed
| Check | Method | Result |
|---|---|---|
| Production build | `python tools/build.py` | 15 pages built; also built with `SITE_URL` set |
| Links and assets | `tools/check.py` crawled all pages | 514 internal references, 0 broken; all in-page anchors resolve; every `<img>` has `alt` |
| Project routes | Built and fetched | `/projects/<slug>/` exists for all 8 projects, plus Projects, Skills, About, Résumé, Contact, 404 |
| Thumbnail match | `check.py` + visual review of all 8 | Each page and card uses its own thumbnail; none cross-referenced. Illustrations are labelled. Images use `object-fit: contain` in a 16:9 frame, so no cropping or stretching |
| Search, filters, sort, reset | Scripted in browser | "u-net" → HYDRA only; "fractal" → RETINA only; no-match shows empty state and Reset restores all 8 and focuses the search box; MATLAB or CNN → 2 projects; adding status and text narrows correctly; Reset clears fields, chips and URL; A–Z and featured sorts reorder correctly; count text updates; deep links like `?q=zzzz` restore state |
| Year filter / newest sort | Inspected | Correctly absent (only one project has a year) |
| Downloads | HTTP HEAD for every PDF link | 200, `application/pdf` (résumé + 8 project descriptions) |
| PDF conversion | Rendered the two converted PDFs | One page each, text intact. A missing subscript glyph (SpO₂) was found and fixed |
| Video | Loaded metadata in browser | RETINA video loads (64 s, 1904 px wide); controls on, no autoplay, `preload="none"`, poster set |
| Lightbox | Scripted | Opens with full image and closes (native `<dialog>`, Esc works) |
| Mobile | Emulated 390 px, 9 pages | No horizontal overflow on any page; nav toggle opens and closes; home hero rendered and inspected |
| Desktop | Rendered 1360 px: home, projects, RETINA, HYSEIS, About, Skills, Résumé | Reviewed. Fixed during QA: orphaned 4th featured card (now 2×2), narrow search box, About timeline column, table wrapping |
| Console | Read console | Only error seen came from a test script calling a mis-named form method (`form.reset` shadowed by the Reset button). Fixed and retested; no other errors |
| Colour contrast | Computed WCAG ratios for the palette | Body ink 16.1:1, secondary text 10.1:1, muted text 5.1–5.6:1, teal links 6.0–8.2:1, white on teal buttons 6.7:1. All ≥ 4.5:1 |
| Social/SEO | Built with `SITE_URL` | Canonical, Open Graph and Twitter tags, 1200×630 per-project cards, sitemap.xml and robots.txt generated; JSON-LD parses |
| Videos | HTTP HEAD on all 5 | 200, `video/mp4`; each project page with a video shows it in a Video section near the top, and its card shows a Video tag |
| Résumé download | Scripted click | Handler fetches the PDF and saves it as `Peter-John-Bacani-Resume.pdf` instead of opening it |
| Content vs sources | Line-by-line against the papers, RETINA README and screenshots | See `SOURCE_INVENTORY.md`; ambiguous items were softened or flagged rather than asserted |

## Not verified
- Public URL, HTTPS, custom domain, and behaviour on the real host.
- Visible keyboard focus: styles are defined (`:focus-visible` 2 px teal outline, native controls, skip link) and the dialog uses the browser's own focus handling, but I did not tab through every page by hand.
- Screen-reader behaviour; real phones or Safari/Firefox (Chromium only).
- Video playback of the other two published videos beyond file presence (same markup as the RETINA one).
- Reduced-motion: implemented in CSS (`prefers-reduced-motion`), not observed.
- Page weight / speed. Images are lazy-loaded and served as sized WebP; videos load only on play. Total `dist/` is about 18 MB, mostly video; I did not measure load times.
- Contact: the mailto link is correct; copy-button clipboard access was not exercised because the browser pane restricts it.

## Content limits (by design)
The supplied project "papers" contain no metrics, so no accuracy, sample sizes or timings appear. See `OPEN_QUESTIONS.md`.
