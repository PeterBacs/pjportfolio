"""One-off: the A-G section list becomes THE 3D carousel; each section opens its content full screen."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def w(p, text):
    (ROOT / p).write_text(text, encoding="utf-8", newline="\n")


def rw(p, f):
    path = ROOT / p
    path.write_text(f(path.read_text(encoding="utf-8")), encoding="utf-8", newline="\n")


w("templates/skills.html", """{% extends "base.html" %}
{% macro badges(items) %}<ul class="stack">{% for t in items %}<li class="badge{% if t.color|lower == '#ffffff' %} badge-light{% endif %}" style="--bg: {{ t.color }}; --fg: {{ t.fg }}">{% if t.path %}<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path fill="currentColor" d="{{ t.path }}"/></svg>{% endif %}<span>{{ t.name }}</span></li>{% endfor %}</ul>{% endmacro %}

{% macro capcard(c) %}
<article class="cap-card">
  <h4>{{ c.title }}</h4>
  <p class="cap-desc">{{ c.description }}</p>
  {% if c.tools %}<p class="cap-label">Tools and methods</p><ul class="chips">{% for t in c.tools %}<li>{{ t }}</li>{% endfor %}</ul>{% endif %}
  {% if c.byPurpose %}<p class="cap-label">By purpose</p><dl class="purpose">{% for b in c.byPurpose %}<div><dt>{{ b.purpose }}</dt><dd>{{ b.tools }}</dd></div>{% endfor %}</dl>{% endif %}
  {% if c.projects or c.links %}<p class="cap-label">Project evidence</p>
  <ul class="cap-evidence">
    {% for slug in c.projects %}<li><a href="{{ by_slug[slug].url }}" data-modal>{{ by_slug[slug].name }}</a> <span class="ev">{{ by_slug[slug].evidence }}</span></li>{% endfor %}
    {% for l in c.links %}<li><a href="{{ u(l.url) }}">{{ l.label }}</a></li>{% endfor %}
  </ul>{% endif %}
  {% if c.context %}<p class="cap-context"><strong>Experience</strong> {{ c.context }}</p>{% endif %}
</article>
{% endmacro %}

{% macro content(s) %}
<p class="section-summary">{{ s.summary }}</p>
{% if s.capabilities %}<div class="cap-grid">{% for c in s.capabilities %}{{ capcard(c) }}{% endfor %}</div>
{% else %}{% for g in techgroups %}<section class="stack-group"><h4>{{ g.title }}</h4><p class="cap-desc">{{ g.description }}</p>{{ badges(g["items"]) }}</section>{% endfor %}{% endif %}
{% endmacro %}

{% set stack_section = {"id": "stack", "letter": "G", "title": techstack.title, "nav": "Tech stack", "summary": "Languages, frameworks, databases, data tools and design software.", "capabilities": []} %}
{% set all_sections = skills.sections + [stack_section] %}

{% block main %}
<section class="page-head skills-head">
  <div class="wrap">
    <h1>{{ skills.title }}</h1>
    {% for t in skills.intro %}<p class="lede">{{ t }}</p>{% endfor %}
  </div>
</section>

<section class="wrap skills-stage" aria-label="Skill sections">
  <div class="scarousel" id="skills-carousel" role="group" aria-roledescription="carousel" aria-label="Skill sections">
    <div class="sstage"><div class="sdeck">
      {% for s in all_sections %}
      <article class="scard" data-index="{{ loop.index0 }}" data-id="{{ s.id }}" data-letter="{{ s.letter }}" data-title="{{ s.title }}">
        <div class="scard-face">
          <span class="scard-letter" aria-hidden="true">{{ s.letter }}</span>
          <h3>{{ s.title }}</h3>
          <p>{{ s.summary }}</p>
          {% if s.capabilities %}
          <ul class="chips">{% for c in s.capabilities[:3] %}<li>{{ c.title }}</li>{% endfor %}{% if s.capabilities|length > 3 %}<li>+{{ s.capabilities|length - 3 }}</li>{% endif %}</ul>
          <span class="scard-cta" aria-hidden="true">Open section · {{ s.capabilities|length }} capabilities →</span>
          {% else %}
          <ul class="chips">{% for g in techgroups[:3] %}<li>{{ g.title }}</li>{% endfor %}<li>+{{ techgroups|length - 3 }}</li></ul>
          <span class="scard-cta" aria-hidden="true">Open section · {{ techstack["items"]|length }} tools →</span>
          {% endif %}
        </div>
        <div class="scard-full">{{ content(s) }}</div>
        <button class="scard-open" type="button" aria-label="Open section {{ s.letter }}: {{ s.title }}"></button>
      </article>
      {% endfor %}
    </div></div>
    <div class="sbar">
      <button class="sbtn" type="button" data-dir="-1" aria-label="Previous section"><span aria-hidden="true">←</span></button>
      <ol class="sdots" aria-label="Choose a section">
        {% for s in all_sections %}<li><button type="button" class="sdot" data-go="{{ loop.index0 }}" aria-label="{{ s.nav }}"><span>{{ s.letter }}</span></button></li>{% endfor %}
      </ol>
      <button class="sbtn" type="button" data-dir="1" aria-label="Next section"><span aria-hidden="true">→</span></button>
    </div>
    <p class="scurrent" aria-live="polite"></p>
  </div>
</section>

<section class="wrap skills-fallback" aria-label="All skills">
  {% for s in all_sections %}
  <section class="skill-section" id="{{ s.id }}" aria-labelledby="{{ s.id }}-h">
    <header class="skill-section-head">
      <span class="section-letter" aria-hidden="true">{{ s.letter }}</span>
      <div><h2 id="{{ s.id }}-h">{{ s.title }}</h2></div>
    </header>
    {{ content(s) }}
  </section>
  {% endfor %}
</section>

<dialog id="skill-modal" aria-labelledby="sm-title">
  <div class="pm-bar">
    <span class="pm-label" id="sm-section"></span>
    <div class="sm-nav">
      <button class="sbtn sbtn-lite" type="button" id="sm-prev" aria-label="Previous section"><span aria-hidden="true">←</span></button>
      <span class="scount" id="sm-count"></span>
      <button class="sbtn sbtn-lite" type="button" id="sm-next" aria-label="Next section"><span aria-hidden="true">→</span></button>
      <button class="lb-close" type="button" id="sm-close" aria-label="Close section">Close ✕</button>
    </div>
  </div>
  <div class="sm-wrap"><div id="sm-body" class="sm-content"></div></div>
</dialog>
{% endblock %}
{% block scripts %}<script src="{{ u('/assets/js/skills.js') }}?v={{ asset_v }}" defer></script>{% endblock %}
""")

w("static/js/skills.js", """/* Skills page: the A-G section list is a 3D carousel; each section opens full-screen in a modal. */
(function () {
  "use strict";
  var root = document.getElementById("skills-carousel");
  if (!root) return;
  var modal = document.getElementById("skill-modal");
  var body = document.getElementById("sm-body");
  var cards = Array.prototype.slice.call(root.querySelectorAll(".scard"));
  var dots = Array.prototype.slice.call(root.querySelectorAll(".sdot"));
  var label = root.querySelector(".scurrent");
  var n = cards.length, active = 0, prevD = [], swiped = false, openIndex = 0;
  root.classList.add("is-3d");

  function offset(i) { var d = ((i - active) % n + n) % n; if (d > n / 2) d -= n; return d; }
  function layout(initial) {
    var w = cards[0].offsetWidth || 300;
    cards.forEach(function (c, i) {
      var d = offset(i), ad = Math.abs(d), sign = d < 0 ? -1 : 1;
      var x = ad === 0 ? 0 : sign * w * (ad === 1 ? 0.72 : 1.0);
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
    dots.forEach(function (b, i) { if (i === active) b.setAttribute("aria-current", "true"); else b.removeAttribute("aria-current"); });
    if (label) label.textContent = cards[active].getAttribute("data-letter") + " · " + cards[active].getAttribute("data-title");
  }
  function go(i) { active = ((i % n) + n) % n; layout(false); }

  root.querySelectorAll("[data-dir]").forEach(function (b) {
    b.addEventListener("click", function () { go(active + Number(b.getAttribute("data-dir"))); });
  });
  dots.forEach(function (b) { b.addEventListener("click", function () { go(Number(b.getAttribute("data-go"))); }); });
  cards.forEach(function (c, i) {
    c.querySelector(".scard-open").addEventListener("click", function () {
      if (swiped) { swiped = false; return; }
      if (i !== active) { go(i); return; }
      open(i);
    });
  });
  root.addEventListener("keydown", function (e) {
    if (e.key === "ArrowRight") { e.preventDefault(); go(active + 1); }
    else if (e.key === "ArrowLeft") { e.preventDefault(); go(active - 1); }
  });
  var sx = null, stage = root.querySelector(".sstage");
  stage.addEventListener("pointerdown", function (e) { sx = e.clientX; swiped = false; });
  stage.addEventListener("pointerup", function (e) {
    if (sx === null) return;
    var dx = e.clientX - sx; sx = null;
    if (Math.abs(dx) > 45) { swiped = true; go(active + (dx < 0 ? 1 : -1)); }
  });
  stage.addEventListener("pointercancel", function () { sx = null; });
  window.addEventListener("resize", function () { layout(true); });

  // ---- full-screen section modal
  function show() {
    var card = cards[openIndex];
    body.replaceChildren();
    var wrap = document.createElement("div");
    wrap.className = "sm-section";
    var head = document.createElement("header");
    head.className = "sm-head";
    var letter = document.createElement("span");
    letter.className = "section-letter";
    letter.textContent = card.getAttribute("data-letter");
    var h = document.createElement("h2");
    h.id = "sm-title";
    h.textContent = card.getAttribute("data-title");
    head.appendChild(letter); head.appendChild(h);
    wrap.appendChild(head);
    Array.prototype.forEach.call(card.querySelector(".scard-full").childNodes, function (nd) { wrap.appendChild(nd.cloneNode(true)); });
    body.appendChild(wrap);
    document.getElementById("sm-section").textContent = "Skills";
    document.getElementById("sm-count").textContent = (openIndex + 1) + " / " + n;
    active = openIndex; layout(false);
    var sc = modal.querySelector(".sm-wrap"); if (sc) sc.scrollTop = 0;
  }
  function open(i) { openIndex = i; show(); if (!modal.open) modal.showModal(); }
  function move(d) { openIndex = ((openIndex + d) % n + n) % n; show(); }
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

  // /skills/#ai (or any section id) brings that section to the centre
  var hash = (location.hash || "").replace("#", "");
  var found = cards.findIndex(function (c) { return c.getAttribute("data-id") === hash; });
  if (found > -1) active = found;
  layout(true);
})();
""")

css = """
/* Skills: the section list is the carousel */
.skills-stage { padding-bottom: var(--s-5); }
.skills-fallback { display: none; }
html:not(.js) .skills-fallback { display: block; padding-bottom: var(--s-5); }
html:not(.js) .skills-stage { display: none; }
.scarousel .sstage { height: clamp(21rem, 34vw, 24rem); }
.skills-stage .scard { width: clamp(17rem, 30vw, 23rem); min-height: 17rem; }
.skills-stage .scard-face { min-height: 17rem; }
.scard-letter { display: grid; place-items: center; width: 2.6rem; height: 2.6rem; border-radius: 9px; background: var(--dark); color: #fff; font: 400 1.05rem var(--font-mono); }
.skills-stage .scard h3 { font-size: 1.2rem; }
.skills-stage .scard-face p { -webkit-line-clamp: 3; }
.sdots { list-style: none; display: flex; gap: 0.35rem; }
.sdot { width: 2.1rem; height: 2.1rem; border-radius: 50%; border: 1px solid rgba(255, 255, 255, 0.28); background: transparent; color: var(--on-dark-muted); font: 500 0.8rem var(--font-mono); cursor: pointer; transition: background var(--ease), color var(--ease), border-color var(--ease); }
.sdot:hover { color: #fff; border-color: #fff; }
.sdot[aria-current="true"] { background: var(--accent-light); border-color: var(--accent-light); color: var(--dark); }
.sdot:focus-visible { outline: 2px solid var(--accent-light); outline-offset: 3px; }
.scurrent { text-align: center; color: var(--on-dark-muted); font-size: 0.85rem; margin: 0.3rem 0 0.4rem; min-height: 1.2em; }
.sm-head { display: flex; align-items: center; gap: var(--s-2); margin-bottom: var(--s-3); }
.sm-head h2 { margin: 0; font-size: var(--step-3); }
.sm-section .section-summary { font-size: var(--step-1); color: var(--ink-2); margin-bottom: var(--s-3); max-width: 46rem; }
.sm-section .cap-grid { grid-template-columns: repeat(auto-fit, minmax(min(100%, 22rem), 1fr)); }
.sm-section .cap-card h4 { margin: 0; font-size: 1.1rem; }
.stack-group { margin-bottom: var(--s-3); }
.stack-group h4 { margin: 0 0 0.3rem; font-size: 1.1rem; }
html:not(.js) .skills-fallback .cap-card h4 { margin: 0; font-size: 1.1rem; }
dialog#skill-modal .sm-content { width: min(100% - 2 * var(--gutter), 72rem); }
@media (max-width: 640px) {
  .scarousel .sstage { height: 20.5rem; }
  .skills-stage .scard { width: clamp(15rem, 76vw, 19rem); }
  .sdots { gap: 0.2rem; }
  .sdot { width: 1.85rem; height: 1.85rem; font-size: 0.72rem; }
  .sbar { gap: 0.45rem; }
  .sm-head h2 { font-size: var(--step-2); }
}
"""
rw("static/css/style.css", lambda s: s if "the section list is the carousel" in s else s + css)
print("section carousel written")
