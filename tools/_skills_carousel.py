"""One-off: turn every Skills section into a 3D carousel whose cards open full-screen modals."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def w(p, text):
    (ROOT / p).write_text(text, encoding="utf-8", newline="\n")


def rw(p, f):
    path = ROOT / p
    path.write_text(f(path.read_text(encoding="utf-8")), encoding="utf-8", newline="\n")


# ---- tech stack groups (section G becomes a carousel too)
ts = json.loads((ROOT / "content/techstack.json").read_text(encoding="utf-8"))
ts["groups"] = [
    {"title": "Languages and markup", "description": "Languages used for firmware, analysis, interfaces and data work.", "ids": ["cpp", "dart", "html5", "java", "css3", "javascript", "markdown", "php", "python", "cuda"]},
    {"title": "Frameworks and servers", "description": "Web frameworks, servers and workflow engines.", "ids": ["django", "flutter", "flask", "joomla", "apache", "airflow"]},
    {"title": "Databases", "description": "Relational and document databases.", "ids": ["mysql", "mongodb", "sqlite"]},
    {"title": "Data science and machine learning", "description": "Numerical, plotting and deep-learning libraries, and business intelligence.", "ids": ["numpy", "pandas", "scipy", "matplotlib", "plotly", "sklearn", "keras", "tensorflow", "pytorch", "powerbi"]},
    {"title": "Design and productivity", "description": "Graphics, video, interface design and documentation tools.", "ids": ["adobe", "illustrator", "photoshop", "premiere", "figma", "canva", "notion"]},
]
(ROOT / "content/techstack.json").write_text(json.dumps(ts, indent=2, ensure_ascii=False), encoding="utf-8")


def bld(s):
    if "techgroups" in s:
        return s
    s = s.replace('awards = load("content/awards.json")', '''awards = load("content/awards.json")
_by_id = {t["id"]: t for t in techstack["items"]}
techgroups = [{**g, "items": [_by_id[i] for i in g["ids"]]} for g in techstack["groups"]]''', 1)
    s = s.replace("techstack=techstack,", "techstack=techstack, techgroups=techgroups,", 1)
    return s


rw("tools/build.py", bld)

# ---- template
w("templates/skills.html", """{% extends "base.html" %}
{% macro badges(items) %}<ul class="stack">{% for t in items %}<li class="badge{% if t.color|lower == '#ffffff' %} badge-light{% endif %}" style="--bg: {{ t.color }}; --fg: {{ t.fg }}">{% if t.path %}<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path fill="currentColor" d="{{ t.path }}"/></svg>{% endif %}<span>{{ t.name }}</span></li>{% endfor %}</ul>{% endmacro %}

{% macro capfull(c) %}
<h3>{{ c.title }}</h3>
<p class="cap-desc">{{ c.description }}</p>
{% if c.tools %}<p class="cap-label">Tools and methods</p><ul class="chips">{% for t in c.tools %}<li>{{ t }}</li>{% endfor %}</ul>{% endif %}
{% if c.byPurpose %}<p class="cap-label">By purpose</p><dl class="purpose">{% for b in c.byPurpose %}<div><dt>{{ b.purpose }}</dt><dd>{{ b.tools }}</dd></div>{% endfor %}</dl>{% endif %}
{% if c.projects or c.links %}<p class="cap-label">Project evidence</p>
<ul class="cap-evidence">
  {% for slug in c.projects %}<li><a href="{{ by_slug[slug].url }}" data-modal>{{ by_slug[slug].name }}</a> <span class="ev">{{ by_slug[slug].evidence }}</span></li>{% endfor %}
  {% for l in c.links %}<li><a href="{{ u(l.url) }}">{{ l.label }}</a></li>{% endfor %}
</ul>{% endif %}
{% if c.context %}<p class="cap-context"><strong>Experience</strong> {{ c.context }}</p>{% endif %}
{% endmacro %}

{% block main %}
<section class="page-head skills-head">
  <div class="wrap">
    <h1>{{ skills.title }}</h1>
    {% for t in skills.intro %}<p class="lede">{{ t }}</p>{% endfor %}
  </div>
</section>

<div class="wrap skills-layout">
  <nav class="skill-nav" aria-label="Skill sections">
    <p class="nav-title">Sections</p>
    <ul>
      {% for s in skills.sections %}<li><a href="#{{ s.id }}"><span class="letter">{{ s.letter }}</span>{{ s.nav }}</a></li>{% endfor %}
      <li><a href="#stack"><span class="letter">G</span>Tech stack</a></li>
    </ul>
  </nav>

  <div class="skills">
    {% for s in skills.sections %}
    <section class="skill-section" id="{{ s.id }}" aria-labelledby="{{ s.id }}-h" data-letter="{{ s.letter }}" data-title="{{ s.title }}">
      <header class="skill-section-head">
        <span class="section-letter" aria-hidden="true">{{ s.letter }}</span>
        <div><h2 id="{{ s.id }}-h">{{ s.title }}</h2><p class="section-summary">{{ s.summary }}</p></div>
      </header>
      <div class="scarousel" role="group" aria-roledescription="carousel" aria-label="{{ s.title }}">
        <div class="sstage"><div class="sdeck">
          {% for c in s.capabilities %}
          <article class="scard" data-index="{{ loop.index0 }}">
            <div class="scard-face">
              <span class="scard-n">{{ '%02d'|format(loop.index) }}</span>
              <h3>{{ c.title }}</h3>
              <p>{{ c.description }}</p>
              {% if c.tools %}<ul class="chips">{% for t in c.tools[:3] %}<li>{{ t }}</li>{% endfor %}{% if c.tools|length > 3 %}<li>+{{ c.tools|length - 3 }}</li>{% endif %}</ul>{% endif %}
              <span class="scard-cta" aria-hidden="true">View details →</span>
            </div>
            <div class="scard-full">{{ capfull(c) }}</div>
            <button class="scard-open" type="button" aria-label="Open details: {{ c.title }}"></button>
          </article>
          {% endfor %}
        </div></div>
        <div class="sbar">
          <button class="sbtn" type="button" data-dir="-1" aria-label="Previous card"><span aria-hidden="true">←</span></button>
          <span class="scount" aria-live="polite"><b>1</b> / {{ s.capabilities|length }}</span>
          <button class="sbtn" type="button" data-dir="1" aria-label="Next card"><span aria-hidden="true">→</span></button>
        </div>
      </div>
    </section>
    {% endfor %}

    <section class="skill-section" id="stack" aria-labelledby="stack-h" data-letter="G" data-title="{{ techstack.title }}">
      <header class="skill-section-head">
        <span class="section-letter" aria-hidden="true">G</span>
        <div><h2 id="stack-h">{{ techstack.title }}</h2><p class="section-summary">Languages, frameworks, databases, data tools and design software.</p></div>
      </header>
      <div class="scarousel" role="group" aria-roledescription="carousel" aria-label="{{ techstack.title }}">
        <div class="sstage"><div class="sdeck">
          {% for g in techgroups %}
          <article class="scard" data-index="{{ loop.index0 }}">
            <div class="scard-face">
              <span class="scard-n">{{ '%02d'|format(loop.index) }}</span>
              <h3>{{ g.title }}</h3>
              <p>{{ g.description }}</p>
              <ul class="chips">{% for t in g["items"][:3] %}<li>{{ t.name }}</li>{% endfor %}<li>+{{ g["items"]|length - 3 }}</li></ul>
              <span class="scard-cta" aria-hidden="true">View all →</span>
            </div>
            <div class="scard-full"><h3>{{ g.title }}</h3><p class="cap-desc">{{ g.description }}</p>{{ badges(g["items"]) }}</div>
            <button class="scard-open" type="button" aria-label="Open details: {{ g.title }}"></button>
          </article>
          {% endfor %}
        </div></div>
        <div class="sbar">
          <button class="sbtn" type="button" data-dir="-1" aria-label="Previous card"><span aria-hidden="true">←</span></button>
          <span class="scount" aria-live="polite"><b>1</b> / {{ techgroups|length }}</span>
          <button class="sbtn" type="button" data-dir="1" aria-label="Next card"><span aria-hidden="true">→</span></button>
        </div>
      </div>
    </section>
  </div>
</div>

<dialog id="skill-modal" aria-labelledby="sm-title">
  <div class="pm-bar">
    <span class="pm-label" id="sm-section"></span>
    <div class="sm-nav">
      <button class="sbtn sbtn-lite" type="button" id="sm-prev" aria-label="Previous card"><span aria-hidden="true">←</span></button>
      <span class="scount" id="sm-count"></span>
      <button class="sbtn sbtn-lite" type="button" id="sm-next" aria-label="Next card"><span aria-hidden="true">→</span></button>
      <button class="lb-close" type="button" id="sm-close" aria-label="Close details">Close ✕</button>
    </div>
  </div>
  <div class="sm-wrap"><div id="sm-body" class="sm-content"></div></div>
</dialog>
{% endblock %}
{% block scripts %}<script src="{{ u('/assets/js/skills.js') }}?v={{ asset_v }}" defer></script>{% endblock %}
""")

# ---- script
w("static/js/skills.js", """/* Skills page: a 3D carousel per section; each card opens full-screen details in a modal. */
(function () {
  "use strict";
  var carousels = Array.prototype.slice.call(document.querySelectorAll(".scarousel"));
  if (!carousels.length) return;
  var modal = document.getElementById("skill-modal");
  var body = document.getElementById("sm-body");
  var cur = null; // {cards, index, title, letter}

  function setup(root) {
    var cards = Array.prototype.slice.call(root.querySelectorAll(".scard"));
    var n = cards.length, active = 0, prevD = [];
    var count = root.querySelector(".scount b");
    root.classList.add("is-3d");
    var api = { cards: cards, root: root, get active() { return active; } };

    function offset(i) { var d = ((i - active) % n + n) % n; if (d > n / 2) d -= n; return d; }
    function layout(initial) {
      var w = cards[0].offsetWidth || 300;
      cards.forEach(function (c, i) {
        var d = offset(i), ad = Math.abs(d), sign = d < 0 ? -1 : 1;
        var x = ad === 0 ? 0 : sign * w * (ad === 1 ? 0.72 : 1.02);
        var z = ad === 0 ? 0 : -(ad === 1 ? 150 : 320);
        var ry = ad === 0 ? 0 : -sign * (ad === 1 ? 34 : 46);
        var sc = ad === 0 ? 1 : (ad === 1 ? 0.86 : 0.7);
        var op = ad === 0 ? 1 : (ad === 1 ? 0.85 : (ad === 2 ? 0.4 : 0));
        var jumped = !initial && prevD[i] !== undefined && Math.abs(d - prevD[i]) > n / 2;
        if (jumped) c.style.transition = "none";
        c.style.setProperty("--x", x + "px"); c.style.setProperty("--z", z + "px");
        c.style.setProperty("--ry", ry + "deg"); c.style.setProperty("--s", sc);
        c.style.opacity = op; c.style.zIndex = String(10 - ad);
        c.style.pointerEvents = ad > 2 ? "none" : "auto";
        c.classList.toggle("is-active", ad === 0);
        var b = c.querySelector(".scard-open"); if (b) b.tabIndex = ad > 1 ? -1 : 0;
        if (jumped) { void c.offsetWidth; c.style.transition = ""; }
        prevD[i] = d;
      });
      if (count) count.textContent = String(active + 1);
    }
    api.go = function (i) { active = ((i % n) + n) % n; layout(false); };
    api.layout = layout;

    root.querySelectorAll("[data-dir]").forEach(function (b) {
      b.addEventListener("click", function () { api.go(active + Number(b.getAttribute("data-dir"))); });
    });
    cards.forEach(function (c, i) {
      c.querySelector(".scard-open").addEventListener("click", function () {
        if (swiped) { swiped = false; return; }
        if (i !== active) { api.go(i); return; }
        openModal(api, i, root.closest(".skill-section"));
      });
    });
    root.addEventListener("keydown", function (e) {
      if (e.key === "ArrowRight") { e.preventDefault(); api.go(active + 1); }
      else if (e.key === "ArrowLeft") { e.preventDefault(); api.go(active - 1); }
    });
    var sx = null, stage = root.querySelector(".sstage");
    stage.addEventListener("pointerdown", function (e) { sx = e.clientX; swiped = false; });
    stage.addEventListener("pointerup", function (e) {
      if (sx === null) return;
      var dx = e.clientX - sx; sx = null;
      if (Math.abs(dx) > 45) { swiped = true; api.go(active + (dx < 0 ? 1 : -1)); }
    });
    stage.addEventListener("pointercancel", function () { sx = null; });
    layout(true);
    return api;
  }
  var swiped = false;
  var apis = carousels.map(setup);
  window.addEventListener("resize", function () { apis.forEach(function (a) { a.layout(true); }); });

  // ---- modal
  function show() {
    var card = cur.api.cards[cur.index];
    body.replaceChildren();
    var full = card.querySelector(".scard-full");
    var wrap = document.createElement("div");
    wrap.className = "sm-card";
    var num = document.createElement("span");
    num.className = "sm-n";
    num.textContent = String(cur.index + 1).padStart(2, "0");
    wrap.appendChild(num);
    Array.prototype.forEach.call(full.childNodes, function (n) { wrap.appendChild(n.cloneNode(true)); });
    var h = wrap.querySelector("h3");
    if (h) { h.id = "sm-title"; }
    body.appendChild(wrap);
    document.getElementById("sm-section").textContent = cur.letter + " · " + cur.title;
    document.getElementById("sm-count").textContent = (cur.index + 1) + " / " + cur.api.cards.length;
    cur.api.go(cur.index);
    modal.scrollTop = 0;
    var sc = modal.querySelector(".sm-wrap"); if (sc) sc.scrollTop = 0;
  }
  function openModal(api, i, section) {
    cur = { api: api, index: i, title: section.getAttribute("data-title"), letter: section.getAttribute("data-letter") };
    show();
    if (!modal.open) modal.showModal();
  }
  function move(d) { var n = cur.api.cards.length; cur.index = ((cur.index + d) % n + n) % n; show(); }
  if (modal) {
    document.getElementById("sm-close").addEventListener("click", function () { modal.close(); });
    document.getElementById("sm-prev").addEventListener("click", function () { move(-1); });
    document.getElementById("sm-next").addEventListener("click", function () { move(1); });
    modal.addEventListener("close", function () { body.replaceChildren(); });
    modal.addEventListener("keydown", function (e) {
      if (e.key === "ArrowRight") { e.preventDefault(); move(1); }
      else if (e.key === "ArrowLeft") { e.preventDefault(); move(-1); }
    });
  }
})();
""")

# ---- CSS
css = """
/* Skills: 3D carousels + full-screen details */
.js .scard-full { display: none; }
.scarousel { background: radial-gradient(120% 100% at 50% 0%, #1d2d33 0%, var(--dark) 62%); border-radius: var(--radius); padding: var(--s-3) var(--s-2) var(--s-2); overflow: hidden; }
.sstage { perspective: 1400px; height: clamp(19rem, 30vw, 21rem); position: relative; }
.sdeck { position: absolute; inset: 0; transform-style: preserve-3d; }
.scard { position: absolute; left: 50%; top: 50%; width: clamp(16rem, 28vw, 21rem); min-height: 15rem; background: #fff; color: var(--ink); border-radius: 14px; border: 1px solid rgba(255, 255, 255, 0.2); box-shadow: 0 26px 54px rgba(0, 0, 0, 0.5); transform: translate(-50%, -50%) translateX(var(--x, 0)) translateZ(var(--z, 0)) rotateY(var(--ry, 0)) scale(var(--s, 1)); transition: transform 0.8s cubic-bezier(0.2, 0.7, 0.2, 1), opacity 0.55s ease, box-shadow 0.5s ease; will-change: transform; }
.scard.is-active { box-shadow: 0 32px 64px rgba(0, 0, 0, 0.55), 0 0 0 2px var(--accent-light); }
.scard-face { display: flex; flex-direction: column; gap: 0.6rem; padding: var(--s-3); height: 100%; min-height: 15rem; }
.scard-n { font: 400 0.75rem var(--font-mono); color: var(--accent-strong); }
.scard h3 { margin: 0; font-size: 1.12rem; line-height: 1.2; }
.scard-face p { margin: 0; font-size: 0.9rem; color: var(--ink-2); display: -webkit-box; -webkit-line-clamp: 4; -webkit-box-orient: vertical; overflow: hidden; }
.scard-face .chips { margin-top: auto; }
.scard-cta { font-weight: 600; font-size: 0.88rem; color: var(--accent-strong); }
.scard-open { position: absolute; inset: 0; z-index: 3; width: 100%; height: 100%; padding: 0; border: 0; background: transparent; cursor: pointer; border-radius: inherit; }
.scard-open:focus-visible { outline: 3px solid var(--accent-light); outline-offset: -3px; }
.sbar { display: flex; justify-content: center; align-items: center; gap: 1rem; padding: var(--s-2) 0 0.3rem; }
.sbtn { width: 2.6rem; height: 2.6rem; border-radius: 50%; border: 1px solid rgba(255, 255, 255, 0.35); background: transparent; color: #fff; font-size: 1.05rem; cursor: pointer; transition: background var(--ease), border-color var(--ease); }
.sbtn:hover { background: rgba(255, 255, 255, 0.12); border-color: #fff; }
.sbtn:focus-visible { outline: 2px solid var(--accent-light); outline-offset: 3px; }
.scount { color: var(--on-dark-muted); font: 500 0.85rem var(--font-mono); min-width: 4rem; text-align: center; }
.scount b { color: #fff; font-weight: 500; }
html:not(.js) .scarousel { background: none; padding: 0; }
html:not(.js) .sdeck { position: static; display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 22rem), 1fr)); gap: var(--s-3); }
html:not(.js) .sstage { height: auto; perspective: none; }
html:not(.js) .scard { position: static; width: auto; transform: none; padding: var(--s-3); }
html:not(.js) .scard-face, html:not(.js) .scard-open, html:not(.js) .sbar { display: none; }
.purpose { margin: 0; display: grid; gap: 0.6rem; }
.purpose dt { font-weight: 600; }
.purpose dd { margin: 0; color: var(--ink-2); }

dialog#skill-modal { position: fixed; inset: 0; margin: 0; padding: 0; border: 0; border-radius: 0; width: 100vw; max-width: 100vw; height: 100vh; height: 100dvh; max-height: 100dvh; background: #fff; color: var(--ink); overflow: hidden; }
dialog#skill-modal[open] { display: grid; grid-template-rows: auto minmax(0, 1fr); animation: rise 0.3s both; }
dialog#skill-modal::backdrop { background: #101316; }
dialog#skill-modal .pm-bar { position: static; padding: 0.7rem var(--gutter); }
.sm-nav { display: flex; align-items: center; gap: 0.6rem; }
.sm-nav .scount { color: var(--muted); min-width: 3.5rem; }
.sbtn-lite { width: 2.4rem; height: 2.4rem; border-color: var(--line-strong); color: var(--ink); }
.sbtn-lite:hover { background: var(--bg-soft); border-color: var(--ink); }
.sm-wrap { overflow-y: auto; min-height: 0; overscroll-behavior: contain; -webkit-overflow-scrolling: touch; }
.sm-content { width: min(100% - 2 * var(--gutter), 52rem); margin: 0 auto; padding: var(--s-4) 0 var(--s-5); }
.sm-card { display: grid; gap: 0.8rem; }
.sm-n { font: 400 0.85rem var(--font-mono); color: var(--accent-strong); }
.sm-card h3 { font-size: var(--step-3); margin: 0; }
.sm-card .cap-desc { font-size: var(--step-1); color: var(--ink-2); }
.sm-card .chips li { font-size: 0.85rem; padding: 0.5rem 0.8rem; }
.sm-card .stack { margin-top: 0.4rem; }
@media (max-width: 640px) {
  .sstage { height: 19.5rem; }
  .scard { width: clamp(14.5rem, 74vw, 19rem); }
  .scarousel { padding-inline: 0.4rem; }
  .sm-card h3 { font-size: var(--step-2); }
  .sm-nav { gap: 0.35rem; }
  .sm-nav .scount { min-width: 2.8rem; font-size: 0.78rem; }
  dialog#skill-modal .pm-label { display: none; }
}
@media (prefers-reduced-motion: reduce) { .scard { transition: none; } dialog#skill-modal[open] { animation: none; } }
"""
rw("static/css/style.css", lambda s: s if "Skills: 3D carousels" in s else s + css)
print("skills carousels written")
