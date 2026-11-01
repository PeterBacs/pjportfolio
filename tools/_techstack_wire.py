"""One-off: wire the Tech stack strip into build.py, the Skills template and the stylesheet."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def rw(p, f):
    path = ROOT / p
    path.write_text(f(path.read_text(encoding="utf-8")), encoding="utf-8", newline="\n")


def bld(s):
    if "techstack" in s:
        return s
    s = s.replace('roles = load("content/roles.json")["roles"]', '''def _readable_text(hex_color):
    """Black or white text, whichever contrasts better with the badge colour."""
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    lin = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    lum = 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)
    return "#101316" if (lum + 0.05) / 0.05 > 1.05 / (lum + 0.05) else "#ffffff"


techstack = load("content/techstack.json")
for _t in techstack["items"]:
    _f = ROOT / "content" / "icons" / f"{_t['id']}.svg"
    _m = re.search(r'\\sd="([^"]+)"', _f.read_text(encoding="utf-8")) if _f.exists() else None
    _t["path"] = _m.group(1) if _m else None
    _t["fg"] = _readable_text(_t["color"])
roles = load("content/roles.json")["roles"]''', 1)
    s = s.replace("roles=roles, articles=articles,", "roles=roles, articles=articles, techstack=techstack,", 1)
    if "\nimport re\n" not in s:
        s = s.replace("import json\n", "import json\nimport re\n", 1)
    return s


rw("tools/build.py", bld)


def tpl(s):
    if "tech-stack" in s:
        return s
    return s.replace('''</section>

''', '''</section>

<section class="wrap tech-stack" aria-labelledby="stack-h">
  <h2 id="stack-h">{{ techstack.title }}</h2>
  <ul class="stack">
    {% for t in techstack["items"] %}
    <li class="badge{% if t.color|lower == '#ffffff' %} badge-light{% endif %}" style="--bg: {{ t.color }}; --fg: {{ t.fg }}">
      {% if t.path %}<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path fill="currentColor" d="{{ t.path }}"/></svg>{% endif %}<span>{{ t.name }}</span>
    </li>
    {% endfor %}
  </ul>
</section>

''', 1)


rw("templates/skills.html", tpl)


def css(s):
    if ".tech-stack" in s:
        return s
    return s.replace("/* Project modal */", """/* Tech stack badges */
.tech-stack { margin-top: var(--s-4); }
.tech-stack h2 { font-size: var(--step-1); margin-bottom: var(--s-2); }
.stack { list-style: none; display: flex; flex-wrap: wrap; gap: 0.5rem; }
.badge { display: inline-flex; align-items: center; gap: 0.55rem; padding: 0.6rem 0.9rem; background: var(--bg); color: var(--fg); border-radius: 3px; font: 500 0.74rem/1 var(--font-mono); letter-spacing: 0.07em; text-transform: uppercase; }
.badge svg { width: 1.05rem; height: 1.05rem; flex: none; }
.badge-light { border: 1px solid var(--line-strong); }

/* Project modal */""", 1)


rw("static/css/style.css", css)
print("tech stack wired")
