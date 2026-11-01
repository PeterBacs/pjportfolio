# Cinematic upgrade: what was added and how to change it

Built in place on the existing Python static generator (no Next.js rewrite). Rebuild with:

```
.venv\Scripts\python.exe tools/build.py
.venv\Scripts\python.exe tools/check.py
```

## What is new
| Piece | Files |
|---|---|
| Pinned scroll-driven hero (headline sits behind Peter, eased in both scroll directions) | `templates/partials/s_cinema.html`, `static/js/cinema.js`, `static/css/cinema.css` |
| Four hero scene objects (procedural Three.js) + a small corner companion that changes with each section: graduation cap (About, Contact), microchip (Skills), robotic arm (Projects, Videos), trophy (Awards, Gallery). Models generated with Higgsfield (Tripo text-to-3D), compressed GLBs in `static/models/`, originals in `_gen/glb/` | `static/js/cinema3d.js`, `static/js/vendor/` (three r170 + GLTFLoader, self-hosted) |
| All new copy | `content/cinema.json` (edit text, CTAs, scene statements, expertise cards here) |
| Dark teal-black palette matching the live site (#05090a, #101316, teal #0b6670, light teal #7cd0d9), IBM Plex Sans/Mono, Space Grotesk headline | `static/css/cinema.css`, `static/fonts/` |
| Hero images | `static/hero/*.webp`; sources in `_gen/` |

## Replacing assets
- **Hero scene / cutout**: replace `static/hero/hero-bg*.webp` (full scene) and `hero-person*.webp` (same canvas size, transparent background, subject at the same pixel position). Also regenerate `hero-depth.png` (distance transform of the cutout's alpha) and use a background with the person removed, or a ghost image appears when he turns.
- **Text**: `content/cinema.json`. Project text and results stay in `content/projects/*.json`.
- **External links**: LinkedIn / GitHub / Upwork are not set (no verified URLs were supplied). Add them in `content/profile.json` and `templates/partials/s_contact.html`.

## Hero (current): 1080p orbit from your real photo
The start and end frame is your real cutout (`static/hero/pj.webp`) composited on the studio background (`_gen/start-1080.png`). Higgsfield Seedance 1.5 Pro (free plan, 1080p, 12 s, same image as start and end frame so the orbit loops) generated `_gen/orbit1080.mp4`. It is exported to 121 WebP frames: `static/hero/orbit/` (1920x1080) and `static/hero/orbit-m/` (centre 720x1080 crop for phones). `cinema.js` scrubs them with scroll in both directions on `#cine-frames`.

To replace the clip, export new frames with the same naming (`f000.webp`...), update `data-count` in `templates/partials/s_cinema.html`, and rebuild.

## Honest limitations
- The first and last frames are your real photo pixels. During the turn (side and back views) the model redraws your face, so it is a close likeness, not your exact pixels. A true real-face orbit needs real footage.
- The studio background and holographic nodes are AI-generated.
- The headline sits in front of the video (the person is part of the video).
- Blender is not installed here. The Intelligence Core and scene objects are procedural Three.js geometry, not a Blender-authored GLB.
- GSAP/ScrollTrigger/Lenis were not used; scroll easing is a small custom loop (native scrolling is never hijacked).
- Reduced-motion and no-WebGL fallbacks are implemented but the reduced-motion path was not exercised in a browser.

## Responsive behaviour
- Checked for horizontal overflow on the home page and the About, Skills, Projects, Awards, Gallery, Contact, project, role and article pages at 320, 360, 768 and 1920 px wide: none.
- Hero statements sit beside the figure on laptops and desktops; they stack at the bottom on phones and on tablets held upright (`cinema.css` media queries, mirrored by `sideLayout()` in `cinema.js`); on phones held sideways (height 560 px or less) the type is sized by screen height and the intro line is hidden.
- Phones held upright use portrait-cropped orbit frames (`static/hero/orbit-m/`); every other screen uses the full frames.
- The corner model is sized and placed in pixels (52 to 120 px, 10 px from the corner) so it stays small on every device.
