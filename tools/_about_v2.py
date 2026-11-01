"""One-off: About page redesign data + styles."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

p = ROOT / "content/profile.json"
d = json.loads(p.read_text(encoding="utf-8"))
d["aboutFacts"] = [
    {"k": "Licence", "v": "PRC-registered Electronics Engineer"},
    {"k": "Teaching", "v": "10+ years, secondary and higher education"},
    {"k": "Degrees", "v": "MS Engineering · MS Teaching (Mathematics)"},
    {"k": "Based in", "v": d["location"]},
]
p.write_text(json.dumps(d, indent=2, ensure_ascii=False), encoding="utf-8")

css = """
/* About page: profile header + consistent two-column sections */
.abt-hero { background: var(--dark); color: var(--on-dark); padding-block: var(--s-5) var(--s-4); }
.abt-hero-grid { display: grid; grid-template-columns: minmax(0, 20rem) minmax(0, 1fr); gap: var(--s-5); align-items: center; }
.abt-portrait { margin: 0; }
.abt-portrait img { inline-size: 100%; aspect-ratio: 4 / 5; object-fit: cover; object-position: 50% 14%; border-radius: var(--radius); background: #e6e6e6; }
.abt-kicker { color: var(--accent-light); font-weight: 600; font-size: 0.85rem; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: var(--s-1); }
.abt-hero h1 { color: #fff; font-size: var(--step-3); margin-bottom: 0.4rem; max-width: none; }
.abt-role { color: var(--accent-light); font-size: var(--step-1); font-weight: 600; margin-bottom: var(--s-3); }
.abt-bio { color: var(--on-dark-muted); max-width: 44rem; }
.abt-hero .btn { background: transparent; color: #fff; border-color: rgba(255, 255, 255, 0.35); }
.abt-hero .btn:hover { border-color: #fff; }
.abt-hero .btn-primary { background: var(--accent-light); border-color: var(--accent-light); color: var(--dark); }
.abt-hero .btn-primary:hover { background: #fff; border-color: #fff; color: var(--dark); }
.abt-facts { list-style: none; display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); margin-top: var(--s-4); border-top: 1px solid rgba(255, 255, 255, 0.16); }
.abt-facts li { display: grid; gap: 0.3rem; padding: var(--s-2) var(--s-2) 0 0; }
.abt-facts li + li { padding-left: var(--s-2); border-left: 1px solid rgba(255, 255, 255, 0.12); }
.abt-facts span { font-size: 0.72rem; letter-spacing: 0.08em; text-transform: uppercase; color: var(--on-dark-muted); }
.abt-facts strong { font-weight: 600; font-size: 0.95rem; color: #fff; }
.abt-body { padding-block: var(--s-4) var(--s-5); }
.abt-row { display: grid; grid-template-columns: 15rem minmax(0, 1fr); gap: var(--s-4); padding-block: var(--s-4); border-top: 1px solid var(--line); }
.abt-row:first-child { border-top: 0; }
.abt-row > h2 { font-size: var(--step-1); margin: 0; position: sticky; top: 5.5rem; align-self: start; }
.abt-timeline { list-style: none; display: grid; gap: var(--s-4); }
.abt-timeline li { display: grid; grid-template-columns: 9.5rem minmax(0, 1fr); gap: var(--s-3); }
.abt-timeline li + li { padding-top: var(--s-4); border-top: 1px solid var(--line); }
.abt-when { color: var(--accent-strong); font-weight: 600; font-size: 0.9rem; padding-top: 0.25rem; }
.abt-timeline h3 { margin: 0 0 0.2rem; font-size: 1.15rem; }
.abt-org { color: var(--muted); margin-bottom: var(--s-2); }
.abt-list { list-style: none; display: grid; }
.abt-list li { display: grid; gap: 0.15rem; padding-block: 0.9rem; border-bottom: 1px solid var(--line); }
.abt-list li:first-child { padding-top: 0; }
.abt-list li:last-child { border-bottom: 0; }
.abt-list span { color: var(--muted); font-size: 0.93rem; }
.abt-strengths { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: var(--s-2); }
.abt-strengths > div { padding: var(--s-3); background: var(--bg-soft); border-radius: var(--radius); }
.abt-strengths h3 { font-size: 1.05rem; margin-bottom: 0.4rem; }
.abt-strengths p { margin: 0; color: var(--ink-2); font-size: 0.95rem; }
.abt-next { background: var(--accent-soft); padding-block: var(--s-4); }
.abt-next-in { display: flex; justify-content: space-between; align-items: center; gap: var(--s-3); flex-wrap: wrap; }
.abt-next p { margin: 0; font-size: var(--step-1); font-weight: 600; }
.abt-next .cta-row { margin: 0; }
@media (max-width: 900px) {
  .abt-hero-grid { grid-template-columns: 1fr; gap: var(--s-3); }
  .abt-portrait { inline-size: min(55%, 14rem); }
  .abt-facts { grid-template-columns: 1fr 1fr; }
  .abt-facts li:nth-child(odd) { padding-left: 0; border-left: 0; }
  .abt-facts li:nth-child(n+3) { border-top: 1px solid rgba(255, 255, 255, 0.12); margin-top: var(--s-2); }
  .abt-row { grid-template-columns: 1fr; gap: var(--s-2); }
  .abt-row > h2 { position: static; }
}
@media (max-width: 560px) {
  .abt-timeline li { grid-template-columns: 1fr; gap: 0.3rem; }
  .abt-strengths { grid-template-columns: 1fr; }
  .abt-facts { grid-template-columns: 1fr; }
  .abt-facts li, .abt-facts li + li { padding-left: 0; border-left: 0; }
  .abt-facts li + li { border-top: 1px solid rgba(255, 255, 255, 0.12); margin-top: var(--s-2); }
}
"""
cp = ROOT / "static/css/style.css"
s = cp.read_text(encoding="utf-8")
if "About page: profile header" not in s:
    cp.write_text(s + css, encoding="utf-8", newline="\n")
print("about v2 written")
