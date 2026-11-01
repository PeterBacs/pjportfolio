"""One-off: add the Awards page (nav, build, styles), remove awards from About, update Smart Helmet role."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def rw(p, f):
    path = ROOT / p
    path.write_text(f(path.read_text(encoding="utf-8")), encoding="utf-8", newline="\n")


# ---- build.py: nav item, data, page
def bld(s):
    if '"/awards/"' in s:
        return s
    s = s.replace('("About", "/about/", "about"), ("Contact"', '("About", "/about/", "about"), ("Awards", "/awards/", "awards"), ("Contact"', 1)
    s = s.replace('techstack = load("content/techstack.json")', 'techstack = load("content/techstack.json")\nawards = load("content/awards.json")', 1)
    s = s.replace("techstack=techstack,", "techstack=techstack, awards=awards,", 1)
    s = s.replace('    render("resume.html"', '    render("resume.html"', 1)
    s = s.replace('    render("contact.html"', '''    render("awards.html", "/awards/", page="awards", title="Awards and Recognition | Engr. Peter John R. Bacani",
           description="Silver Prize at the Seoul International Invention Fair 2024, SIBOL First Prize at NICE 2024, and National Science and Technology Fair recognition, with sources.",
           og_image="home", canonical="/awards/")
    render("contact.html"''', 1)
    return s


rw("tools/build.py", bld)

# ---- About: remove the awards section
rw("templates/about.html", lambda s: re.sub(r'\n  <section class="span-2" aria-labelledby="awards-h">.*?</section>\n', "\n", s, flags=re.S))

# ---- skills link to the new page
sk = json.loads((ROOT / "content/skills.json").read_text(encoding="utf-8"))
for sec in sk["sections"]:
    for c in sec["capabilities"]:
        for l in c.get("links", []):
            if l["url"] == "/about/#awards-h":
                l["url"] = "/awards/"
                l["label"] = "Winning Coach and other awards"
        if c.get("context"):
            c["context"] = c["context"].replace("mentored student team", "coached the student team").replace("mentored the student team", "coached the student team")
(ROOT / "content/skills.json").write_text(json.dumps(sk, indent=2, ensure_ascii=False), encoding="utf-8")

roles = (ROOT / "content/roles.json").read_text(encoding="utf-8")
roles = roles.replace("Smart Helmet: mentored the student team behind a wearable safety prototype that won the Silver Prize at SIIF 2024.", "Smart Helmet: coach and named inventor of a wearable safety prototype that won the Silver Prize at SIIF 2024 and the SIBOL First Prize at NICE 2024.")
(ROOT / "content/roles.json").write_text(roles, encoding="utf-8")

# ---- Smart Helmet: role grounded in the Embassy and DOST pages
d = json.loads((ROOT / "content/projects/smart-helmet.json").read_text(encoding="utf-8"))
d["role"] = "Coach and named inventor"
d["roleBasis"] = "documented"
d["involvement"] = "Student team, coached"
for s in d["sections"]:
    if s["id"] == "contribution":
        s["title"] = "My role"
        s["blocks"] = [{"type": "p", "text": "The Smart Helmet was developed by student researchers of Lanna National High School with their coaches, including me. I am named with a student co-inventor in the Seoul International Invention Fair 2024 entry, and DOST Region 02 lists me among the team's coaches."}]
    if s["id"] == "results":
        s["blocks"] = [
            {"type": "ul", "items": [
                "Silver Prize, Seoul International Invention Fair (SIIF) 2024, South Korea.",
                "First Prize, SIBOL Award (Creative Research, High School Level), National Invention Contest and Exhibits 2024, presented at the 2024 NICE Presidential Awards."]},
            {"type": "p", "text": "Photographs, articles and source links for each award are on the Awards page."},
        ]
(ROOT / "content/projects/smart-helmet.json").write_text(json.dumps(d, indent=2, ensure_ascii=False), encoding="utf-8")

# ---- CSS
css = """/* Awards page */
@keyframes rise { from { opacity: 0; transform: translateY(14px); } to { opacity: 1; transform: none; } }
.awards-hero { background: radial-gradient(120% 90% at 50% 0%, #1b2a30 0%, var(--dark) 60%); color: var(--on-dark); padding-block: var(--s-5) var(--s-4); overflow: hidden; }
.awards-hero .wrap > * { animation: rise 0.7s both; }
.awards-hero .wrap > :nth-child(2) { animation-delay: 0.08s; }
.awards-hero .wrap > :nth-child(3) { animation-delay: 0.16s; }
.awards-kicker { color: var(--accent-light); font-weight: 600; font-size: 0.85rem; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: var(--s-1); }
.awards-hero h1 { color: #fff; font-size: var(--step-3); max-width: 24ch; }
.awards-intro { color: var(--on-dark-muted); max-width: 40rem; font-size: var(--step-1); line-height: 1.5; }

.carousel { margin-top: var(--s-4); outline-offset: 6px; }
.stage { perspective: 1500px; height: clamp(21rem, 44vw, 29rem); position: relative; }
.deck { position: absolute; inset: 0; transform-style: preserve-3d; }
.slide { position: absolute; left: 50%; top: 50%; margin: 0; width: clamp(15rem, 30vw, 24rem); aspect-ratio: 1; border-radius: 14px; overflow: hidden; background: #000; border: 1px solid rgba(255, 255, 255, 0.14); box-shadow: 0 28px 60px rgba(0, 0, 0, 0.5); cursor: pointer; transform: translate(-50%, -50%) translateX(var(--x, 0)) translateZ(var(--z, 0)) rotateY(var(--ry, 0)) scale(var(--s, 1)); transition: transform 0.85s cubic-bezier(0.2, 0.7, 0.2, 1), opacity 0.6s ease, box-shadow 0.6s ease; will-change: transform; }
.slide img { width: 100%; height: 100%; object-fit: cover; object-position: var(--pos, 50% 40%); }
.slide::after { content: ""; position: absolute; inset: 0; background: linear-gradient(to top, rgba(10, 13, 15, 0.82) 0%, rgba(10, 13, 15, 0) 42%); pointer-events: none; }
.slide.is-active { cursor: default; box-shadow: 0 34px 70px rgba(0, 0, 0, 0.55), 0 0 0 1px rgba(124, 208, 217, 0.45); }
.slide-cap { position: absolute; left: 1rem; right: 1rem; bottom: 0.9rem; z-index: 2; display: grid; gap: 0.15rem; margin: 0; color: #fff; }
.slide-cap strong { font-size: 1.05rem; letter-spacing: -0.01em; }
.slide-level { color: var(--accent-light); font-size: 0.72rem; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; }
.carousel:not(.is-3d) .stage { height: auto; perspective: none; }
.carousel:not(.is-3d) .deck { position: static; display: grid; grid-template-columns: repeat(auto-fit, minmax(14rem, 1fr)); gap: var(--s-2); transform-style: flat; }
.carousel:not(.is-3d) .slide { position: relative; left: auto; top: auto; width: auto; transform: none; }
.carousel:not(.is-3d) .carousel-bar { display: none; }

.carousel-bar { display: flex; flex-wrap: wrap; justify-content: center; align-items: center; gap: 0.7rem; margin-top: var(--s-3); }
.cbtn { width: 2.75rem; height: 2.75rem; border-radius: 50%; border: 1px solid rgba(255, 255, 255, 0.35); background: transparent; color: #fff; font-size: 1.1rem; cursor: pointer; transition: background var(--ease), border-color var(--ease); }
.cbtn:hover { background: rgba(255, 255, 255, 0.12); border-color: #fff; }
.cbtn:focus-visible, .cdot:focus-visible, .cplay:focus-visible { outline: 2px solid var(--accent-light); outline-offset: 3px; }
.cdots { list-style: none; display: flex; flex-wrap: wrap; justify-content: center; gap: 0.4rem; }
.cdot { font: 600 0.8rem/1 var(--font-sans); color: var(--on-dark-muted); background: transparent; border: 1px solid rgba(255, 255, 255, 0.22); border-radius: 99px; padding: 0.55rem 0.9rem; cursor: pointer; transition: background var(--ease), color var(--ease), border-color var(--ease); }
.cdot:hover { color: #fff; border-color: rgba(255, 255, 255, 0.6); }
.cdot[aria-current="true"] { background: var(--accent-light); border-color: var(--accent-light); color: var(--dark); }
.cplay { font: 600 0.8rem/1 var(--font-sans); color: var(--on-dark-muted); background: transparent; border: 0; text-decoration: underline; text-underline-offset: 0.25em; cursor: pointer; padding: 0.55rem; }

.award-details { padding-block: var(--s-4) var(--s-3); }
.award-article[hidden] { display: none; }
.award-article.is-in { animation: rise 0.55s both; }
.award-article + .award-article { margin-top: var(--s-5); padding-top: var(--s-4); border-top: 1px solid var(--line); }
.award-meta { display: flex; flex-wrap: wrap; gap: 0.4rem 1rem; align-items: center; margin-bottom: var(--s-1); font-size: 0.88rem; color: var(--muted); }
.pill-level { background: var(--accent-soft); color: var(--accent-strong); font-weight: 600; font-size: 0.78rem; padding: 0.3rem 0.7rem; border-radius: 99px; }
.award-article h2 { font-size: var(--step-2); max-width: 32ch; }
.award-body { display: grid; grid-template-columns: minmax(0, 1.5fr) minmax(0, 1fr); gap: var(--s-4); align-items: start; margin-top: var(--s-2); }
.award-text p { max-width: 42rem; }
.award-actions { display: flex; flex-wrap: wrap; gap: 0.6rem; margin-top: var(--s-2); }
.award-sources { background: var(--bg-soft); border-radius: var(--radius); padding: var(--s-3); }
.award-sources h3 { font-size: 0.8rem; letter-spacing: 0.06em; text-transform: uppercase; color: var(--muted); margin-bottom: 0.8rem; }
.award-sources ul { list-style: none; display: grid; gap: 0.8rem; }
.award-sources a { font-weight: 600; font-size: 0.93rem; }
.src-note { display: block; font-size: 0.8rem; color: var(--muted); margin-top: 0.15rem; }
@media (max-width: 860px) { .award-body { grid-template-columns: 1fr; } }
.more-recognition { padding-top: var(--s-3); }
.more-recognition h2 { font-size: var(--step-2); }
.more-grid { list-style: none; display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 17rem), 1fr)); gap: var(--s-2); }
.more-grid li { display: grid; gap: 0.3rem; padding: var(--s-3); border: 1px solid var(--line); border-radius: var(--radius); }
.more-grid span { color: var(--muted); font-size: 0.93rem; }
@media (max-width: 640px) { .stage { height: 21rem; } .slide { width: clamp(14rem, 66vw, 20rem); } }
@media (prefers-reduced-motion: reduce) { .slide { transition: none; } .awards-hero .wrap > * { animation: none; } }

/* Project modal */"""
rw("static/css/style.css", lambda s: s if "Awards page" in s else s.replace("/* Project modal */", css, 1))
print("awards wired")
