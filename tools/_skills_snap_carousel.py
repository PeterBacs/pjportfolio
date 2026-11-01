"""One-off: replace the 3D skills carousel with the scroll-snap card carousel supplied by the user,
using the portfolio's own palette, self-hosted assets and its own project illustrations (no CDN or hotlinked images)."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def rw(p, f):
    path = ROOT / p
    path.write_text(f(path.read_text(encoding="utf-8")), encoding="utf-8", newline="\n")


def tpl(s):
    start = s.index('<section class="wrap skills-stage"')
    end = s.index('<section class="wrap skills-fallback"')
    new = '''<section class="hcarousel" id="skills-carousel" aria-labelledby="sc-h">
  <div class="wrap">
    <h2 id="sc-h" class="sr-only">Skill sections</h2>
    <ul class="hcards" tabindex="0" aria-label="Skill sections, scroll sideways">
      {% for s in all_sections %}
      <li class="hcard" data-index="{{ loop.index0 }}" data-id="{{ s.id }}" data-letter="{{ s.letter }}" data-title="{{ s.title }}">
        <div class="hvisual">
          {{ img(visuals[s.id].image, sizes="(min-width: 700px) 22rem, 80vw", loading=('eager' if loop.index0 < 2 else 'lazy'), max_w=800) }}
          <span class="hletter" aria-hidden="true">{{ s.letter }}</span>
        </div>
        <div class="hcontent">
          <div class="hwrap">
            <h3 class="htitle">{{ s.title }}</h3>
            <p class="hdesc">{{ s.summary }}</p>
            {% if s.capabilities %}
            <ul class="chips">{% for c in s.capabilities[:3] %}<li>{{ c.title }}</li>{% endfor %}{% if s.capabilities|length > 3 %}<li>+{{ s.capabilities|length - 3 }}</li>{% endif %}</ul>
            {% else %}
            <ul class="chips">{% for g in techgroups[:3] %}<li>{{ g.title }}</li>{% endfor %}<li>+{{ techgroups|length - 3 }}</li></ul>
            {% endif %}
          </div>
          <button class="hlink" type="button" aria-label="Open section {{ s.letter }}: {{ s.title }}">Open section <span class="hcount">{% if s.capabilities %}{{ s.capabilities|length }} capabilities{% else %}{{ techstack["items"]|length }} tools{% endif %}</span></button>
        </div>
        <div class="scard-full">{{ content(s) }}</div>
      </li>
      {% endfor %}
    </ul>
    <div class="hbar">
      <button class="hbtn" type="button" data-dir="-1" aria-label="Scroll back"><span aria-hidden="true">←</span></button>
      <button class="hbtn" type="button" data-dir="1" aria-label="Scroll forward"><span aria-hidden="true">→</span></button>
      <ol class="hdots" aria-label="Jump to a section">
        {% for s in all_sections %}<li><button type="button" class="hdot" data-go="{{ loop.index0 }}" aria-label="{{ s.nav }}"><span>{{ s.letter }}</span></button></li>{% endfor %}
      </ol>
    </div>
  </div>
</section>

'''
    s = s[:start] + new + s[end:]
    s = s.replace('{% set all_sections = skills.sections + [stack_section] %}', '''{% set all_sections = skills.sections + [stack_section] %}
{% set visuals = {
  "embedded": {"image": "thumb-smart-helmet"},
  "robotics": {"image": "thumb-hydra"},
  "ai": {"image": "thumb-vision"},
  "design": {"image": "thumb-skin"},
  "software": {"image": "thumb-school-system"},
  "research": {"image": "thumb-retina"},
  "stack": {"image": "thumb-hyseis"}
} %}''', 1)
    return s


rw("templates/skills.html", tpl)

js = r"""/* Skills page: scroll-snap card carousel (native horizontal scrolling). Each card opens its section full screen. */
(function () {
  "use strict";
  var root = document.getElementById("skills-carousel");
  if (!root) return;
  var list = root.querySelector(".hcards");
  var cards = Array.prototype.slice.call(root.querySelectorAll(".hcard"));
  var dots = Array.prototype.slice.call(root.querySelectorAll(".hdot"));
  var prev = root.querySelector('[data-dir="-1"]');
  var next = root.querySelector('[data-dir="1"]');
  var modal = document.getElementById("skill-modal");
  var body = document.getElementById("sm-body");
  var n = cards.length, openIndex = 0;
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var behavior = reduce ? "auto" : "smooth";

  function step() {
    var gap = parseFloat(getComputedStyle(list).columnGap) || 16;
    return cards[0].getBoundingClientRect().width + gap;
  }
  function current() {
    var left = list.getBoundingClientRect().left + (parseFloat(getComputedStyle(list).paddingLeft) || 0);
    var best = 0, bd = Infinity;
    cards.forEach(function (c, i) { var d = Math.abs(c.getBoundingClientRect().left - left); if (d < bd) { bd = d; best = i; } });
    return best;
  }
  function update() {
    var max = list.scrollWidth - list.clientWidth - 2;
    prev.disabled = list.scrollLeft <= 2;
    next.disabled = list.scrollLeft >= max;
    var cur = (list.scrollLeft >= max) ? n - 1 : current();
    dots.forEach(function (b, i) { if (i === cur) b.setAttribute("aria-current", "true"); else b.removeAttribute("aria-current"); });
  }
  function goTo(i) {
    var c = cards[Math.max(0, Math.min(n - 1, i))];
    list.scrollTo({ left: c.offsetLeft - list.offsetLeft - (parseFloat(getComputedStyle(list).paddingLeft) || 0), behavior: behavior });
  }
  prev.addEventListener("click", function () { list.scrollBy({ left: -step(), behavior: behavior }); });
  next.addEventListener("click", function () { list.scrollBy({ left: step(), behavior: behavior }); });
  dots.forEach(function (b) { b.addEventListener("click", function () { goTo(Number(b.getAttribute("data-go"))); }); });
  var tick = false;
  list.addEventListener("scroll", function () {
    if (tick) return; tick = true;
    window.requestAnimationFrame(function () { tick = false; update(); });
  }, { passive: true });
  window.addEventListener("resize", update);
  list.addEventListener("keydown", function (e) {
    if (e.target !== list) return;
    if (e.key === "ArrowRight") { e.preventDefault(); next.click(); }
    else if (e.key === "ArrowLeft") { e.preventDefault(); prev.click(); }
  });

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
    var sc = modal.querySelector(".sm-wrap"); if (sc) sc.scrollTop = 0;
  }
  function open(i) { openIndex = i; show(); if (!modal.open) modal.showModal(); }
  function move(d) { openIndex = ((openIndex + d) % n + n) % n; show(); goTo(openIndex); }
  cards.forEach(function (c, i) {
    c.querySelector(".hlink").addEventListener("click", function () { open(i); });
    c.querySelector(".hvisual").addEventListener("click", function () { open(i); });
  });
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

  var hash = (location.hash || "").replace("#", "");
  var found = cards.findIndex(function (c) { return c.getAttribute("data-id") === hash; });
  if (found > -1) goTo(found);
  update();
})();
"""
(ROOT / "static/js/skills.js").write_text(js, encoding="utf-8", newline="\n")

css = """
/* Skills: scroll-snap card carousel (design supplied by the user, rendered in the portfolio palette) */
.hcarousel { background: radial-gradient(120% 100% at 50% 0%, #1d2d33 0%, var(--dark) 62%); color: var(--on-dark); padding-block: var(--s-4) var(--s-3); margin-bottom: var(--s-5); container-type: inline-size; }
.hcards { --pad: var(--gutter); list-style: none; display: grid; grid-auto-flow: column; grid-template-rows: auto 1fr; gap: var(--s-3); overflow-x: auto; overscroll-behavior-inline: contain; padding: var(--s-2) var(--pad) var(--s-3); margin-inline: calc(var(--pad) * -1); scroll-padding-inline: var(--pad); scroll-snap-type: x mandatory; scroll-behavior: smooth; scrollbar-width: thin; scrollbar-color: rgba(255, 255, 255, 0.3) transparent; }
.hcards:focus-visible { outline: 2px solid var(--accent-light); outline-offset: -2px; }
.hcard { scroll-snap-align: start; display: grid; grid-row: 1 / -1; grid-template-rows: subgrid; background: #1b2227; border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 18px; box-shadow: 0 18px 40px rgba(0, 0, 0, 0.35); padding: var(--s-1); inline-size: min(80cqi, 23rem); transition: border-color var(--ease), transform var(--ease); }
.hcard:hover { border-color: rgba(124, 208, 217, 0.55); }
.hvisual { position: relative; border-radius: 12px; overflow: clip; background: #0b0e10; aspect-ratio: 16 / 9; cursor: pointer; }
.hvisual img { display: block; inline-size: 100%; block-size: 100%; object-fit: cover; }
.hletter { position: absolute; left: 0.7rem; top: 0.7rem; display: grid; place-items: center; width: 2.2rem; height: 2.2rem; border-radius: 8px; background: rgba(16, 19, 22, 0.88); color: #fff; font: 400 0.95rem var(--font-mono); border: 1px solid rgba(255, 255, 255, 0.2); }
.hcontent { display: grid; align-content: space-between; gap: var(--s-3); padding: var(--s-2) var(--s-2) var(--s-2); }
.hwrap { display: grid; gap: var(--s-1); align-content: start; }
.htitle { font-size: 1.25rem; line-height: 1.2; color: #fff; text-wrap: pretty; margin: 0; }
.hdesc { margin: 0; color: var(--on-dark-muted); font-size: 0.95rem; text-wrap: pretty; }
.hcard .chips li { background: rgba(255, 255, 255, 0.08); color: var(--on-dark); }
.hlink { display: flex; align-items: center; gap: 0.7rem; width: 100%; padding: 0; border: 0; background: transparent; color: var(--accent-light); font: 600 0.95rem var(--font-sans); cursor: pointer; text-align: left; }
.hlink::before { content: "→"; display: grid; place-items: center; flex: none; inline-size: 2.2rem; block-size: 2.2rem; border-radius: 8px; background: var(--accent-light); color: var(--dark); font-size: 1rem; transition: background var(--ease); }
.hlink:hover::before { background: #fff; }
.hlink:focus-visible { outline: 2px solid var(--accent-light); outline-offset: 4px; border-radius: 8px; }
.hcount { margin-left: auto; font: 400 0.75rem var(--font-mono); color: var(--on-dark-muted); }
.hbar { display: flex; align-items: center; gap: 0.6rem; flex-wrap: wrap; padding-top: var(--s-1); }
.hbtn { inline-size: 2.75rem; block-size: 2.75rem; border-radius: 12px; border: 1px solid var(--accent-light); background: transparent; color: var(--accent-light); font-size: 1.15rem; cursor: pointer; transition: background var(--ease); }
.hbtn:hover:not(:disabled) { background: rgba(124, 208, 217, 0.14); }
.hbtn:disabled { opacity: 0.4; cursor: not-allowed; }
.hbtn:focus-visible { outline: 2px dashed var(--accent-light); outline-offset: 3px; }
.hdots { list-style: none; display: flex; gap: 0.35rem; margin-left: auto; }
.hdot { inline-size: 2.1rem; block-size: 2.1rem; border-radius: 50%; border: 1px solid rgba(255, 255, 255, 0.28); background: transparent; color: var(--on-dark-muted); font: 500 0.8rem var(--font-mono); cursor: pointer; transition: background var(--ease), color var(--ease), border-color var(--ease); }
.hdot:hover { color: #fff; border-color: #fff; }
.hdot[aria-current="true"] { background: var(--accent-light); border-color: var(--accent-light); color: var(--dark); }
.hdot:focus-visible { outline: 2px solid var(--accent-light); outline-offset: 3px; }
.hcard .scard-full { display: none; }
html:not(.js) .hcarousel { display: none; }
@media (max-width: 640px) { .hcard { inline-size: min(84cqi, 21rem); } .hdots { margin-left: 0; width: 100%; } .hdot { inline-size: 1.95rem; block-size: 1.95rem; } }
@media (prefers-reduced-motion: reduce) { .hcards { scroll-behavior: auto; } .hcard { transition: none; } }
"""
rw("static/css/style.css", lambda s: s if "scroll-snap card carousel" in s else s + css)
print("snap carousel written")
