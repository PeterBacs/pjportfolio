"""One-off: move the Skills section navigation into a sticky side panel (desktop)."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def rw(p, f):
    path = ROOT / p
    path.write_text(f(path.read_text(encoding="utf-8")), encoding="utf-8", newline="\n")


# ---- template: nav and sections inside one two-column layout
def tpl(s):
    s = re.sub(r'\n<nav class="skill-nav".*?</nav>\n', "\n", s, flags=re.S)
    s = s.replace('<div class="wrap skills">', '''<div class="wrap skills-layout">
  <nav class="skill-nav" aria-label="Skill sections">
    <p class="nav-title">Sections</p>
    <ul>
      {% for s in skills.sections %}<li><a href="#{{ s.id }}"><span class="letter">{{ s.letter }}</span>{{ s.nav }}</a></li>{% endfor %}
    </ul>
  </nav>
  <div class="skills">''', 1)
    # close the extra wrapper just before the end of the main block
    s = s.replace("  {% endfor %}\n</div>\n{% endblock %}", "  {% endfor %}\n  </div>\n</div>\n{% endblock %}", 1)
    return s


rw("templates/skills.html", tpl)


# ---- CSS: replace the old full-width bar with bar (mobile) / side panel (desktop)
def css(s):
    s = re.sub(r"\.skill-nav \{ position: sticky; top: 4rem;.*?\n(?=\.skill-section \{)", "", s, flags=re.S)
    block = """.skills-layout { display: grid; grid-template-columns: 15rem minmax(0, 1fr); gap: var(--s-4); align-items: start; padding-top: var(--s-3); }
.skill-nav { position: sticky; top: 5.5rem; }
.skill-nav .nav-title { margin: 0 0 0.6rem; font-size: 0.72rem; font-weight: 600; letter-spacing: 0.06em; text-transform: uppercase; color: var(--muted); }
.skill-nav ul { list-style: none; display: grid; gap: 0.25rem; border-left: 1px solid var(--line); }
.skill-nav a { display: flex; align-items: center; gap: 0.6rem; text-decoration: none; color: var(--ink-2); font-size: 0.92rem; font-weight: 600; padding: 0.55rem 0.8rem; margin-left: -1px; border-left: 2px solid transparent; transition: color var(--ease), border-color var(--ease), background var(--ease); }
.skill-nav a:hover { color: var(--ink); border-left-color: var(--line-strong); }
.skill-nav a[aria-current="true"] { color: var(--ink); border-left-color: var(--accent); background: var(--accent-soft); }
.skill-nav .letter { display: grid; place-items: center; flex: none; width: 1.5rem; height: 1.5rem; border-radius: 50%; background: var(--accent-soft); color: var(--accent-strong); font: 600 0.72rem var(--font-mono); }
.skill-nav a[aria-current="true"] .letter { background: #fff; }
@media (max-width: 960px) {
  .skills-layout { grid-template-columns: 1fr; gap: 0; }
  .skill-nav { top: 4rem; z-index: 40; background: rgba(255, 255, 255, 0.96); backdrop-filter: blur(8px); border-bottom: 1px solid var(--line); margin-bottom: var(--s-3); }
  .skill-nav .nav-title { display: none; }
  .skill-nav ul { display: flex; gap: 0.5rem; overflow-x: auto; padding: 0.7rem 0; border-left: 0; scrollbar-width: thin; }
  .skill-nav a { white-space: nowrap; border: 1px solid var(--line-strong); border-radius: 99px; padding: 0.45rem 0.85rem; margin-left: 0; font-size: 0.88rem; }
  .skill-nav a[aria-current="true"] { border-color: var(--accent); }
}
"""
    s = s.replace(".skill-section { margin-bottom: var(--s-5);", block + ".skill-section { margin-bottom: var(--s-5);", 1)
    s = s.replace("@media (max-width: 860px) { .skill-nav { top: 4rem; } .skill-section { scroll-margin-top: 7.5rem; } }", "@media (max-width: 960px) { .skill-section { scroll-margin-top: 7.5rem; } }")
    s = s.replace(".skill-section { margin-bottom: var(--s-5); scroll-margin-top: 8rem; }", ".skill-section { margin-bottom: var(--s-5); scroll-margin-top: 6rem; }")
    return s


rw("static/css/style.css", css)

# ---- JS: highlight the section being read
def js(s):
    if "skill-nav" in s:
        return s
    add = """
  // Skills: highlight the section currently in view in the side panel
  var sNav = document.querySelector(".skill-nav");
  if (sNav && "IntersectionObserver" in window) {
    var links = {};
    sNav.querySelectorAll("a[href^='#']").forEach(function (a) { links[a.getAttribute("href").slice(1)] = a; });
    var current = null;
    var setCurrent = function (id) {
      if (current === id || !links[id]) return;
      if (current && links[current]) links[current].removeAttribute("aria-current");
      links[id].setAttribute("aria-current", "true");
      current = id;
    };
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) setCurrent(en.target.id); });
    }, { rootMargin: "-20% 0px -65% 0px" });
    document.querySelectorAll(".skill-section").forEach(function (sec) { io.observe(sec); });
  }
"""
    i = s.rstrip().rfind("})();")
    return s[:i] + add + s[i:]


rw("static/js/site.js", js)
print("side panel done")
