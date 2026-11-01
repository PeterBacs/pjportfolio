"""One-off: wire the new home page (data, build globals, styles)."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def rw(p, f):
    path = ROOT / p
    path.write_text(f(path.read_text(encoding="utf-8")), encoding="utf-8", newline="\n")


def bld(s):
    if "home_data" in s:
        return s
    s = s.replace('awards = load("content/awards.json")', '''awards = load("content/awards.json")
home_data = load("content/home.json")
for _st in home_data["stages"]:
    _st["project_list"] = [by_slug[x] for x in _st["projects"]]
_aw = {a["id"]: a for a in awards["awards"]}
home_data["recognition_items"] = [_aw[i] for i in home_data["recognition"]]''', 1)
    s = s.replace("techstack=techstack,", "techstack=techstack, home_data=home_data,", 1)
    return s


rw("tools/build.py", bld)

css = """
/* Home v2: sensor-to-decision pipeline, recognition strip, case-study rows */
.hm-hero { background: radial-gradient(110% 90% at 85% 10%, #1c2b31 0%, var(--dark) 58%); color: var(--on-dark); padding-block: var(--s-4); min-height: calc(100vh - 4rem); min-height: calc(100dvh - 4rem); display: flex; align-items: center; }
.hm-grid { display: grid; grid-template-columns: minmax(0, 1.05fr) minmax(0, 1fr); gap: var(--s-5); align-items: center; }
.hm-hero h1 { color: #fff; font-size: clamp(2.6rem, 1.6rem + 4.2vw, 5rem); line-height: 1.02; letter-spacing: -0.03em; margin-bottom: var(--s-2); max-width: 11ch; }
.hm-lede { font-size: var(--step-1); line-height: 1.5; color: var(--on-dark-muted); max-width: 32rem; margin-bottom: var(--s-3); }
.hm-byline { display: flex; align-items: center; gap: 0.85rem; margin-top: var(--s-4); }
.hm-byline img { inline-size: 3.4rem; block-size: 3.4rem; border-radius: 50%; object-fit: cover; object-position: 50% 14%; border: 2px solid rgba(124, 208, 217, 0.6); background: #e6e6e6; }
.hm-byline strong { display: block; color: #fff; font-size: 1rem; }
.hm-byline span { color: var(--on-dark-muted); font-size: 0.88rem; }
.hm-hero .btn { background: transparent; color: #fff; border-color: rgba(255, 255, 255, 0.35); }
.hm-hero .btn:hover { border-color: #fff; }
.hm-hero .btn-primary { background: var(--accent-light); border-color: var(--accent-light); color: var(--dark); }
.hm-hero .btn-primary:hover { background: #fff; border-color: #fff; color: var(--dark); }

.pipe { list-style: none; position: relative; display: grid; gap: 0.75rem; counter-reset: s; }
.pipe::before { content: ""; position: absolute; left: 1.45rem; top: 1.5rem; bottom: 1.5rem; inline-size: 2px; background: linear-gradient(to bottom, rgba(124, 208, 217, 0.15), rgba(124, 208, 217, 0.6), rgba(124, 208, 217, 0.15)); }
.pipe::after { content: ""; position: absolute; left: calc(1.45rem - 3px); top: 1.5rem; inline-size: 8px; block-size: 8px; border-radius: 50%; background: var(--accent-light); box-shadow: 0 0 0 4px rgba(124, 208, 217, 0.18); animation: pipe-pulse 6s ease-in-out infinite; }
@keyframes pipe-pulse { 0% { transform: translateY(0); opacity: 0; } 10% { opacity: 1; } 90% { opacity: 1; } 100% { transform: translateY(calc(100% * 0 + 17rem)); opacity: 0; } }
.pipe-step { position: relative; display: grid; grid-template-columns: 2.9rem minmax(0, 1fr); gap: 1rem; padding: 0.9rem 1rem 0.9rem 0; }
.pipe-n { z-index: 1; display: grid; place-items: center; inline-size: 2.9rem; block-size: 2.9rem; border-radius: 50%; background: #0f1417; border: 1px solid rgba(124, 208, 217, 0.55); color: var(--accent-light); font: 400 0.8rem var(--font-mono); }
.pipe-body { border: 1px solid rgba(255, 255, 255, 0.1); background: rgba(255, 255, 255, 0.03); border-radius: 12px; padding: 0.85rem 1rem; transition: border-color var(--ease), background var(--ease); }
.pipe-step:hover .pipe-body, .pipe-step:focus-within .pipe-body { border-color: rgba(124, 208, 217, 0.5); background: rgba(124, 208, 217, 0.06); }
.pipe-label { margin: 0; font-size: 1.15rem; color: #fff; letter-spacing: -0.01em; }
.pipe-text { margin: 0.15rem 0 0.5rem; font-size: 0.9rem; color: var(--on-dark-muted); }
.pipe-body .chips li { background: rgba(255, 255, 255, 0.08); color: var(--on-dark); font-size: 0.74rem; padding: 0.3rem 0.55rem; }
.pipe-links { display: flex; flex-wrap: wrap; gap: 0.3rem 0.9rem; margin-top: 0.55rem; font-size: 0.85rem; }
.pipe-links a { color: var(--accent-light); font-weight: 600; }
.pipe-links a:hover { color: #fff; }

.rec { background: var(--accent-soft); padding-block: var(--s-4); }
.rec-head { display: flex; justify-content: space-between; align-items: baseline; gap: var(--s-2); flex-wrap: wrap; margin-bottom: var(--s-3); }
.rec-head h2 { margin: 0; font-size: var(--step-2); }
.rec-grid { list-style: none; display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: var(--s-2); }
.rec-grid li { background: #fff; border-radius: var(--radius); padding: var(--s-2) var(--s-3); border-top: 3px solid var(--accent); }
.rec-level { font-size: 0.72rem; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; color: var(--accent-strong); }
.rec-grid strong { display: block; font-size: 1rem; line-height: 1.3; margin: 0.3rem 0; }
.rec-grid span.rec-when { font-size: 0.85rem; color: var(--muted); }

.cases { padding-block: var(--s-5); }
.cases-head { margin-bottom: var(--s-4); display: flex; justify-content: space-between; align-items: baseline; gap: var(--s-2); flex-wrap: wrap; }
.cases-head h2 { margin: 0; }
.case { display: grid; grid-template-columns: minmax(0, 1.1fr) minmax(0, 1fr); gap: var(--s-4); align-items: center; padding-block: var(--s-3); }
.case + .case { border-top: 1px solid var(--line); }
.case:nth-child(even) .case-img { order: 2; }
.case-img { display: block; background: #0b0b0c; border-radius: var(--radius); overflow: hidden; aspect-ratio: 3 / 2; }
.case-img img { inline-size: 100%; block-size: 100%; object-fit: contain; transition: transform 0.6s ease; }
.case:hover .case-img img { transform: scale(1.03); }
.case-n { font: 400 0.85rem var(--font-mono); color: var(--accent-strong); }
.case h3 { font-size: var(--step-2); margin: 0.2rem 0 0.6rem; }
.case h3 a { color: var(--ink); text-decoration: none; }
.case-sum { color: var(--ink-2); max-width: 34rem; }
.case-meta { margin: var(--s-2) 0; font-size: 0.92rem; color: var(--muted); }
.case-meta strong { color: var(--ink); }

.hm-roles { background: var(--bg-soft); padding-block: var(--s-5); }
.hm-roles h2 { margin-bottom: var(--s-3); }

@media (max-width: 960px) {
  .hm-grid { grid-template-columns: 1fr; gap: var(--s-4); }
  .hm-hero { min-height: 0; }
  .hm-hero h1 { max-width: none; }
  .rec-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .case { grid-template-columns: 1fr; gap: var(--s-2); }
  .case:nth-child(even) .case-img { order: 0; }
}
@media (max-width: 560px) { .rec-grid { grid-template-columns: 1fr; } .pipe-step { padding-right: 0; } }
@media (prefers-reduced-motion: reduce) { .pipe::after { animation: none; opacity: 0; } .case-img img { transition: none; } }
"""
rw("static/css/style.css", lambda s: s if "Home v2" in s else s + css)
print("home v2 data + css wired")
