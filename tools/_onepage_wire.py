"""One-off: nav order and anchors, hero and chain styles, flat About variant, contact roles."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def rw(p, f):
    path = ROOT / p
    path.write_text(f(path.read_text(encoding="utf-8")), encoding="utf-8", newline="\n")


# ---- nav: Home, About, Projects, Skills, Awards, Contact (anchors on the one-page home)
def bld(s):
    old = re.search(r"    skills=skills, nav=\[.*?\],\n", s, re.S)
    if old and '"/#about"' not in s:
        new = '''    skills=skills, nav=[
        ("Home", "/#home", "home"), ("About", "/#about", "about"), ("Projects", "/#projects", "projects"),
        ("Skills", "/#skills", "skills"), ("Awards", "/#awards", "awards"), ("Contact", "/#contact", "contact"),
    ],
'''
        s = s.replace(old.group(0), new, 1)
    return s


rw("tools/build.py", bld)

# brand link goes to the top of the home page
rw("templates/base.html", lambda s: s.replace('<a class="brand" href="{{ u(\'/\') }}"', '<a class="brand" href="{{ u(\'/#home\') }}"'))

# contact: add role links
def contact(s):
    if "Hiring for a specific role" in s:
        return s
    add = """
<section class="wrap contact-roles" aria-labelledby="cr-h">
  <h2 id="cr-h">Hiring for a specific role?</h2>
  <ul class="role-grid">
    {% for r in roles %}<li><a class="role-link" href="{{ r.url }}"><strong>{{ r.nav }}</strong><span>{{ r.blurb }}</span><span class="role-go" aria-hidden="true">View →</span></a></li>{% endfor %}
  </ul>
</section>
"""
    return s.rstrip() + "\n" + add


rw("templates/partials/s_contact.html", contact)

css = """
/* One-page home: hero modelled on the supplied reference, in the portfolio palette */
.hx { position: relative; overflow: hidden; background: radial-gradient(60% 80% at 8% 0%, rgba(20, 120, 130, 0.5) 0%, rgba(20, 120, 130, 0) 62%), radial-gradient(50% 60% at 100% 100%, rgba(11, 102, 112, 0.18) 0%, rgba(11, 102, 112, 0) 70%), #05090a; color: var(--on-dark); min-height: calc(100vh - 4rem); min-height: calc(100dvh - 4rem); display: flex; align-items: stretch; }
.hx-grid { display: grid; grid-template-columns: minmax(0, 0.95fr) minmax(0, 1.05fr); gap: var(--s-4); align-items: end; }
.hx-photo { position: relative; margin: 0; align-self: end; line-height: 0; }
.hx-photo > img { display: block; inline-size: min(100%, 34rem); block-size: auto; margin-inline: auto 0; filter: contrast(1.05) brightness(0.94); -webkit-mask-image: linear-gradient(to bottom, #000 78%, transparent 100%); mask-image: linear-gradient(to bottom, #000 78%, transparent 100%); }
.hx-badge { position: absolute; left: 0; bottom: 2.2rem; inline-size: 8.5rem; block-size: 8.5rem; border-radius: 50%; background: radial-gradient(circle at 30% 25%, #0e2e30, #07191b); border: 1px solid rgba(124, 208, 217, 0.35); display: grid; place-items: center; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.45); }
.hx-badge svg { position: absolute; inset: 0; inline-size: 100%; block-size: 100%; }
.hx-ring { transform-origin: 80px 80px; animation: hx-spin 28s linear infinite; }
.hx-ring text { fill: rgba(190, 235, 240, 0.8); font: 500 9.2px var(--font-mono); letter-spacing: 0.12em; }
.hx-badge span { font: 400 1.15rem var(--font-mono); color: #fff; letter-spacing: 0.05em; }
@keyframes hx-spin { to { transform: rotate(360deg); } }
.hx-text { align-self: center; padding-block: var(--s-4); line-height: normal; }
.hx-eyebrow { color: var(--accent-light); font: 500 0.82rem var(--font-mono); letter-spacing: 0.14em; text-transform: uppercase; margin-bottom: var(--s-2); }
.hx h1 { color: #e6fbf4; font-size: clamp(2.8rem, 1.4rem + 5vw, 5.4rem); line-height: 1; letter-spacing: -0.03em; margin-bottom: var(--s-3); max-width: 10ch; font-weight: 600; }
.hx-lede { font-size: var(--step-1); line-height: 1.55; color: #b7c9c9; max-width: 33rem; margin-bottom: var(--s-4); }
.hx-pill { display: inline-flex; align-items: center; gap: 1.6rem; padding: 0.55rem 0.6rem 0.55rem 1.7rem; border-radius: 99px; border: 1px solid rgba(124, 208, 217, 0.28); background: linear-gradient(90deg, rgba(11, 102, 112, 0.55), rgba(11, 102, 112, 0.12)); color: #eafff9; text-decoration: none; font-size: 1.08rem; transition: border-color var(--ease), background var(--ease); }
.hx-pill:hover { border-color: var(--accent-light); background: linear-gradient(90deg, rgba(11, 102, 112, 0.75), rgba(11, 102, 112, 0.25)); color: #fff; }
.hx-pill-icon { display: grid; place-items: center; inline-size: 3.1rem; block-size: 3.1rem; border-radius: 50%; background: var(--accent-light); color: #05090a; font-size: 1.35rem; font-weight: 700; }
.hx-links { display: flex; flex-wrap: wrap; gap: 0.6rem; margin-top: var(--s-3); }
.hx .btn { background: transparent; color: #fff; border-color: rgba(255, 255, 255, 0.3); }
.hx .btn:hover { border-color: #fff; }

.chain { background: #05090a; color: var(--on-dark); padding-block: var(--s-4) var(--s-5); border-top: 1px solid rgba(255, 255, 255, 0.08); }
.chain-list { list-style: none; display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: var(--s-2); }
.chain-list li { position: relative; display: grid; gap: 0.5rem; align-content: start; padding: var(--s-3); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px; background: rgba(255, 255, 255, 0.03); }
.chain-list li + li::before { content: "→"; position: absolute; left: calc(-1 * var(--s-2) - 0.55rem); top: 1.2rem; color: var(--accent-light); font-family: var(--font-mono); background: #05090a; inline-size: 1.1rem; text-align: center; }
.chain-n { color: var(--accent-light); font: 400 0.78rem var(--font-mono); }
.chain-list h3 { margin: 0; color: #fff; font-size: 1.2rem; }
.chain-list p { margin: 0; color: #a9b9b9; font-size: 0.9rem; }
.chain-list .chips li { background: rgba(255, 255, 255, 0.08); color: var(--on-dark); font-size: 0.74rem; padding: 0.3rem 0.55rem; border: 0; }
.chain-list .chips li::before { content: none; }
.chain-links { display: flex; flex-wrap: wrap; gap: 0.3rem 0.9rem; margin-top: 0.3rem !important; }
.chain-links a { color: var(--accent-light); font-weight: 600; font-size: 0.85rem; }
.chain-links a:hover { color: #fff; }

.home-sec { scroll-margin-top: 4rem; }
.abt-hero--flat { background: #fff; color: var(--ink); padding-block: var(--s-5) var(--s-3); }
.abt-hero--flat .abt-hero-grid { grid-template-columns: 1fr; }
.abt-hero--flat .abt-kicker { color: var(--accent-strong); }
.abt-hero--flat :is(h1, h2) { color: var(--ink); }
.abt-hero--flat .abt-role { color: var(--accent-strong); }
.abt-hero--flat .abt-bio { color: var(--ink-2); }
.abt-hero--flat .btn { background: #fff; color: var(--ink); border-color: var(--line-strong); }
.abt-hero--flat .btn:hover { border-color: var(--ink); }
.abt-hero--flat .btn-primary { background: var(--accent); border-color: var(--accent); color: #fff; }
.abt-hero--flat .btn-primary:hover { background: var(--accent-strong); border-color: var(--accent-strong); color: #fff; }
.abt-hero--flat .abt-facts { border-top-color: var(--line-strong); }
.abt-hero--flat .abt-facts li + li { border-left-color: var(--line); }
.abt-hero--flat .abt-facts span { color: var(--muted); }
.abt-hero--flat .abt-facts strong { color: var(--ink); }
.contact-roles { padding-bottom: var(--s-5); }
.contact-roles h2 { font-size: var(--step-2); }
.home-sec .page-head { padding-block: var(--s-5) var(--s-3); }

@media (max-width: 960px) {
  .hx { min-height: 0; }
  .hx-grid { grid-template-columns: 1fr; gap: 0; align-items: start; }
  .hx-photo { order: 2; margin-top: var(--s-2); }
  .hx-photo > img { inline-size: min(78%, 24rem); margin-inline: auto; }
  .hx-badge { inline-size: 6.5rem; block-size: 6.5rem; left: 0.5rem; bottom: 1.2rem; }
  .hx-badge span { font-size: 0.95rem; }
  .hx-text { padding-block: var(--s-4) 0; }
  .hx h1 { max-width: none; }
  .chain-list { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .chain-list li + li::before { content: none; }
}
@media (max-width: 560px) { .chain-list { grid-template-columns: 1fr; } .hx-pill { gap: 1rem; font-size: 1rem; } }
@media (prefers-reduced-motion: reduce) { .hx-ring { animation: none; } }
"""
rw("static/css/style.css", lambda s: s if "One-page home: hero modelled" in s else s + css)
print("one-page wired")
