"""One-off: (1) register the transparent portrait, (2) split each page template into a reusable section partial,
(3) turn the standalone pages into thin wrappers around those partials."""
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
T = ROOT / "templates"

# ---- 1. portrait cut-out
src = Path(r"C:\Users\client\AppData\Local\Temp\claude\C--Users-client-Desktop-Retinal\a6fd7b4c-e922-4dba-ac13-ad4c392c0709\images\50.png")
dst = ROOT / "Projects" / "Peter cutout.png"
if src.exists():
    shutil.copy2(src, dst)
m = json.loads((ROOT / "content/media.json").read_text(encoding="utf-8"))
m["images"]["peter-cutout"] = {
    "src": "Projects/Peter cutout.png", "widths": [320, 500], "alpha": True, "kind": "photo",
    "alt": "Portrait of Engr. Peter John R. Bacani in a dark suit, white shirt and navy tie.",
}
(ROOT / "content/media.json").write_text(json.dumps(m, indent=2, ensure_ascii=False), encoding="utf-8")

# keep the alpha channel for cut-outs
o = (ROOT / "tools/optimize_media.py")
s = o.read_text(encoding="utf-8")
if '"alpha"' not in s:
    s = s.replace('        im = Image.open(src)\n        im = im.convert("RGB")', '        im = Image.open(src)\n        im = im.convert("RGBA" if spec.get("alpha") else "RGB")')
    o.write_text(s, encoding="utf-8", newline="\n")

# ---- 2/3. partials
(T / "partials").mkdir(exist_ok=True)


def grab(t, name):
    mm = re.search(r"{%\s*block " + name + r"\s*%}(.*?){%\s*endblock\s*%}", t, re.S)
    return mm.group(1) if mm else ""


for name in ("about", "projects", "skills", "awards", "contact"):
    p = T / f"{name}.html"
    t = p.read_text(encoding="utf-8")
    if "{% include" in t:
        continue
    head, main, scripts = grab(t, "head"), grab(t, "main"), grab(t, "scripts")
    rest = t
    for blk in ("head", "main", "scripts"):
        rest = re.sub(r"{%\s*block " + blk + r"\s*%}.*?{%\s*endblock\s*%}", "", rest, flags=re.S)
    rest = re.sub(r'{%\s*extends\s+"base.html"\s*%}', "", rest).strip()
    body = (rest + "\n" + main).replace("<h1", "<{{ H }}").replace("</h1>", "</{{ H }}>")
    if name == "about":
        body = body.replace('<section class="abt-hero"', '<section class="abt-hero{% if H == \'h2\' %} abt-hero--flat{% endif %}"')
        body = re.sub(r'(\s*)<figure class="abt-portrait">.*?</figure>', r"\1{% if H == 'h1' %}<figure class=\"abt-portrait\">{{ img('peter', sizes='(min-width: 960px) 22rem, 60vw', loading='eager', fetchpriority='high') }}</figure>{% endif %}", body, flags=re.S)
    if name == "contact":
        body = body.replace("</div>\n", "</div>\n", 1)
    (T / "partials" / f"s_{name}.html").write_text(body, encoding="utf-8", newline="\n")
    wrapper = '{% extends "base.html" %}\n'
    if head.strip():
        wrapper += "{% block head %}" + head + "{% endblock %}\n"
    wrapper += "{% block main %}{% set H = 'h1' %}{% include \"partials/s_" + name + ".html\" %}{% endblock %}\n"
    if scripts.strip():
        wrapper += "{% block scripts %}" + scripts + "{% endblock %}\n"
    p.write_text(wrapper, encoding="utf-8", newline="\n")

# ---- heading selectors that target h1 also need to match the h2 used on the home page
css = ROOT / "static/css/style.css"
c = css.read_text(encoding="utf-8")
c = re.sub(r"(\.(?:page-head|projects-head|skills-head|awards-hero|abt-hero)) h1", r"\1 :is(h1, h2)", c)
css.write_text(c, encoding="utf-8", newline="\n")
print("prepped")
