"""One-off: Awards page v2 (article modal, centred title, Global Excellence award, persistent auto-play)."""
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def w(p, text):
    (ROOT / p).write_text(text, encoding="utf-8", newline="\n")


# ---- photo
src = Path(r"C:\Users\client\AppData\Local\Temp\claude\C--Users-client-Desktop-Retinal\a6fd7b4c-e922-4dba-ac13-ad4c392c0709\images\30.jpg")
dst = ROOT / "Projects" / "Awards" / "Global Excellence Awards.jpg"
if src.exists():
    shutil.copy2(src, dst)

# ---- media registry
m = json.loads((ROOT / "content/media.json").read_text(encoding="utf-8"))
m["images"]["award-global"] = {
    "src": "Projects/Awards/Global Excellence Awards.jpg", "widths": [600, 1000, 1500], "kind": "photo",
    "alt": "Seven officials and educators standing on a decorated stage, one holding a certificate, in front of a screen reading Global Excellence Awards: Honoring International Achievements.",
    "caption": "The Global Excellence Awards ceremony, honouring international achievements."}
(ROOT / "content/media.json").write_text(json.dumps(m, indent=2, ensure_ascii=False), encoding="utf-8")

# ---- awards data: add the new award as the second slide
a = json.loads((ROOT / "content/awards.json").read_text(encoding="utf-8"))
a["awards"] = [x for x in a["awards"] if x["id"] != "global"]
new = {
    "id": "global", "short": "Global Excellence", "title": "International Awardee for Coaching, Global Excellence Awards",
    "level": "International", "date": "", "place": "", "image": "award-global", "position": "50% 38%", "credit": "",
    "paragraphs": [
        "I was recognised as an International Awardee for Coaching at the Global Excellence Awards, a ceremony honouring international achievements. The certificate recognises my international achievement as a coach of student inventors and researchers.",
        "My international coaching results include the Silver Prize that the Smart Helmet team won at the Seoul International Invention Fair 2024."],
    "sources": [{"label": "Facebook post on the Global Excellence Awards", "url": "https://www.facebook.com/share/p/1c6u2JD54v/", "note": "Social media post"}],
    "project": "smart-helmet"}
a["awards"].insert(1, new)
(ROOT / "content/awards.json").write_text(json.dumps(a, indent=2, ensure_ascii=False), encoding="utf-8")

# ---- template
w("templates/awards.html", """{% extends "base.html" %}
{% block head %}
<script type="application/ld+json">{{ {
  "@context": "https://schema.org", "@type": "Person", "name": profile.name,
  "award": awards.awards|map(attribute="title")|list
}|tojson }}</script>
{% endblock %}

{% macro article(a, tid) %}
<header>
  <p class="award-meta"><span class="pill-level">{{ a.level }}</span>{% if a.date %}<span>{{ a.date }}</span>{% endif %}{% if a.place %}<span>{{ a.place }}</span>{% endif %}</p>
  <h2 id="{{ tid }}">{{ a.title }}</h2>
</header>
<div class="award-body">
  <div class="award-text">
    {% for para in a.paragraphs %}<p>{{ para }}</p>{% endfor %}
    <p class="award-actions">
      <a class="btn btn-small" data-lightbox href="{{ full_url(a.image) }}" data-caption="{{ registry.images[a.image].caption }}" aria-label="View the full photo: {{ a.short }}">View full photo</a>
      {% if a.project %}<a class="btn btn-small" href="{{ by_slug[a.project].url }}" data-modal>View the {{ by_slug[a.project].name }} project</a>{% endif %}
    </p>
    {% if a.credit %}<p class="small muted">{{ a.credit }}</p>{% endif %}
  </div>
  <aside class="award-sources" aria-label="Sources">
    <h3>Sources</h3>
    <ul>
      {% for s in a.sources %}
      <li><a href="{{ s.url }}" target="_blank" rel="noopener noreferrer">{{ s.label }} <span aria-hidden="true">↗</span></a>{% if s.note %}<span class="src-note">{{ s.note }}</span>{% endif %}</li>
      {% endfor %}
    </ul>
  </aside>
</div>
{% endmacro %}

{% block main %}
<section class="awards-hero" aria-labelledby="awards-title">
  <div class="wrap">
    <h1 id="awards-title">{{ awards.title }}</h1>
  </div>

  <div class="carousel" id="carousel" role="group" aria-roledescription="carousel" aria-label="Award photographs">
    <div class="stage">
      <div class="deck">
        {% for a in awards.awards %}
        <figure class="slide" data-index="{{ loop.index0 }}" data-id="{{ a.id }}" style="--pos: {{ a.position }}">
          {{ img(a.image, sizes="(min-width: 960px) 26rem, 78vw", loading=('eager' if loop.index0 < 3 else 'lazy'), max_w=1400) }}
          <figcaption class="slide-cap"><span class="slide-level">{{ a.level }}</span><strong>{{ a.short }}</strong></figcaption>
          <button class="slide-open" type="button" aria-label="Read the article: {{ a.title }}"></button>
        </figure>
        {% endfor %}
      </div>
    </div>

    <div class="carousel-bar">
      <button class="cbtn" type="button" data-dir="-1" aria-label="Previous award"><span aria-hidden="true">←</span></button>
      <ol class="cdots" aria-label="Choose an award">
        {% for a in awards.awards %}
        <li><button type="button" class="cdot" data-go="{{ loop.index0 }}">{{ a.short }}</button></li>
        {% endfor %}
      </ol>
      <button class="cbtn" type="button" data-dir="1" aria-label="Next award"><span aria-hidden="true">→</span></button>
      <button class="cplay" type="button" id="cplay" aria-pressed="false" hidden>Pause</button>
    </div>
  </div>
</section>

<section class="section award-details" aria-label="Award articles" id="details">
  <div class="wrap">
    {% for a in awards.awards %}
    <article class="award-article" id="award-{{ a.id }}" aria-labelledby="t-{{ a.id }}">
      {{ article(a, 't-' ~ a.id) }}
    </article>
    {% endfor %}
  </div>
</section>

<section class="section more-recognition" aria-labelledby="more-h">
  <div class="wrap">
    <h2 id="more-h">More recognition</h2>
    <ul class="more-grid">
      {% for m in awards.more %}<li><strong>{{ m.title }}</strong><span>{{ m.detail }}</span></li>{% endfor %}
    </ul>
  </div>
</section>

<dialog id="award-modal" aria-label="Award article">
  <div class="pm-bar">
    <span class="pm-label">Award</span>
    <button class="lb-close" type="button" id="am-close" aria-label="Close article">Close ✕</button>
  </div>
  <div id="am-body" class="am-body"></div>
</dialog>

{% for a in awards.awards %}
<template id="tpl-{{ a.id }}">
  <figure class="am-figure" style="--pos: {{ a.position }}">
    {{ img(a.image, sizes="(min-width: 960px) 900px, 92vw", max_w=1400) }}
  </figure>
  <div class="am-article">{{ article(a, 'am-title') }}</div>
</template>
{% endfor %}
{% endblock %}
{% block scripts %}<script src="{{ u('/assets/js/awards.js') }}?v={{ asset_v }}" defer></script>{% endblock %}
""")

# ---- script
w("static/js/awards.js", """/* Awards page: 3D cover-flow carousel. Clicking a photo opens its article in a modal.
   Auto-plays by default (pause button always available), pauses while the pointer is over the photos or an article is open. */
(function () {
  "use strict";
  var root = document.getElementById("carousel");
  if (!root) return;

  var slides = Array.prototype.slice.call(root.querySelectorAll(".slide"));
  var dots = Array.prototype.slice.call(root.querySelectorAll(".cdot"));
  var playBtn = document.getElementById("cplay");
  var modal = document.getElementById("award-modal");
  var modalBody = document.getElementById("am-body");
  var n = slides.length;
  var active = 0;
  var prevD = [];
  root.classList.add("is-3d");

  function offset(i) {
    var d = ((i - active) % n + n) % n;
    if (d > n / 2) d -= n;
    return d;
  }

  function layout(initial) {
    var w = slides[0].offsetWidth || 320;
    slides.forEach(function (s, i) {
      var d = offset(i), ad = Math.abs(d), sign = d < 0 ? -1 : 1;
      var x = ad === 0 ? 0 : sign * w * (ad === 1 ? 0.74 : 1.0);
      var z = ad === 0 ? 0 : -(ad === 1 ? 170 : 360);
      var ry = ad === 0 ? 0 : -sign * (ad === 1 ? 36 : 48);
      var sc = ad === 0 ? 1 : (ad === 1 ? 0.84 : 0.66);
      var op = ad === 0 ? 1 : (ad === 1 ? 0.8 : (ad === 2 ? 0.42 : 0));
      var jumped = !initial && prevD[i] !== undefined && Math.abs(d - prevD[i]) > n / 2;
      if (jumped) s.style.transition = "none";
      s.style.setProperty("--x", x + "px");
      s.style.setProperty("--z", z + "px");
      s.style.setProperty("--ry", ry + "deg");
      s.style.setProperty("--s", sc);
      s.style.opacity = op;
      s.style.zIndex = String(10 - ad);
      s.style.pointerEvents = ad > 2 ? "none" : "auto";
      s.classList.toggle("is-active", ad === 0);
      var btn = s.querySelector(".slide-open");
      if (btn) btn.tabIndex = ad > 1 ? -1 : 0;
      if (jumped) { void s.offsetWidth; s.style.transition = ""; }
      prevD[i] = d;
    });
    dots.forEach(function (b, i) {
      if (i === active) b.setAttribute("aria-current", "true"); else b.removeAttribute("aria-current");
    });
  }

  function go(i) { active = ((i % n) + n) % n; layout(false); }
  function step(dir) { go(active + dir); }

  // ---- article modal
  var swiped = false;
  function openArticle(i) {
    var tpl = document.getElementById("tpl-" + slides[i].getAttribute("data-id"));
    if (!tpl || !modal || typeof modal.showModal !== "function") return;
    active = i; layout(false);
    modalBody.replaceChildren(tpl.content.cloneNode(true));
    var h = modalBody.querySelector("h2");
    if (h) modal.setAttribute("aria-labelledby", h.id);
    if (!modal.open) modal.showModal();
    modal.scrollTop = 0;
  }
  function closeArticle() { if (modal.open) modal.close(); modalBody.replaceChildren(); }
  if (modal) {
    document.getElementById("am-close").addEventListener("click", closeArticle);
    modal.addEventListener("close", function () { modalBody.replaceChildren(); restartAuto(); });
    modal.addEventListener("cancel", function () { modalBody.replaceChildren(); });
    modal.addEventListener("click", function (e) { if (e.target === modal) closeArticle(); });
  }
  slides.forEach(function (s, i) {
    s.querySelector(".slide-open").addEventListener("click", function () {
      if (swiped) { swiped = false; return; }
      openArticle(i);
    });
  });

  // ---- controls
  root.querySelectorAll("[data-dir]").forEach(function (b) {
    b.addEventListener("click", function () { step(Number(b.getAttribute("data-dir"))); restartAuto(); });
  });
  dots.forEach(function (b) {
    b.addEventListener("click", function () { go(Number(b.getAttribute("data-go"))); restartAuto(); });
  });
  root.addEventListener("keydown", function (e) {
    if (e.target.closest && e.target.closest("input, textarea")) return;
    if (e.key === "ArrowRight") { e.preventDefault(); step(1); restartAuto(); }
    else if (e.key === "ArrowLeft") { e.preventDefault(); step(-1); restartAuto(); }
  });

  // swipe
  var startX = null;
  var stage = root.querySelector(".stage");
  stage.addEventListener("pointerdown", function (e) { startX = e.clientX; swiped = false; });
  stage.addEventListener("pointerup", function (e) {
    if (startX === null) return;
    var dx = e.clientX - startX;
    startX = null;
    if (Math.abs(dx) > 45) { swiped = true; step(dx < 0 ? 1 : -1); restartAuto(); }
  });
  stage.addEventListener("pointercancel", function () { startX = null; });

  // ---- auto-play (on by default)
  var INTERVAL = 6000;
  var timer = null, hovering = false, userPaused = false;
  function tick() {
    if (hovering || document.hidden || (modal && modal.open) || userPaused) return;
    step(1);
  }
  function startAuto() { if (!timer && !userPaused) timer = window.setInterval(tick, INTERVAL); }
  function stopAuto() { if (timer) { window.clearInterval(timer); timer = null; } }
  function restartAuto() { stopAuto(); startAuto(); }
  stage.addEventListener("mouseenter", function () { hovering = true; });
  stage.addEventListener("mouseleave", function () { hovering = false; });
  if (playBtn) {
    playBtn.hidden = false;
    playBtn.addEventListener("click", function () {
      userPaused = !userPaused;
      playBtn.textContent = userPaused ? "Play" : "Pause";
      playBtn.setAttribute("aria-pressed", userPaused ? "true" : "false");
      if (userPaused) stopAuto(); else startAuto();
    });
  }

  window.addEventListener("resize", function () { layout(true); });
  layout(true);
  var hash = (location.hash || "").replace("#", "");
  var found = slides.findIndex(function (s) { return s.getAttribute("data-id") === hash; });
  if (found > -1) { active = found; layout(true); }
  startAuto();
})();
""")

# ---- CSS
css = (ROOT / "static/css/style.css").read_text(encoding="utf-8")
if "slide-open" not in css:
    css = css.replace("/* Project modal */", """/* Awards v2: article modal, centred title */
.awards-hero .wrap { text-align: center; }
.awards-hero h1 { max-width: none; margin: 0 auto; }
.slide-open { position: absolute; inset: 0; z-index: 3; width: 100%; height: 100%; padding: 0; border: 0; background: transparent; cursor: pointer; border-radius: inherit; }
.slide-open:focus-visible { outline: 3px solid var(--accent-light); outline-offset: -3px; }
html.js .award-details { display: none; }
dialog#award-modal { border: 0; border-radius: var(--radius); padding: 0; width: min(96vw, 960px); max-width: none; max-height: 92vh; background: #fff; color: var(--ink); overflow: auto; }
dialog#award-modal::backdrop { background: rgba(16, 19, 22, 0.85); }
dialog#award-modal[open] { animation: rise 0.35s both; }
.pm-label { font-weight: 600; font-size: 0.9rem; color: var(--muted); }
.am-figure { margin: 0; aspect-ratio: 16 / 8; background: var(--dark); }
.am-figure img { width: 100%; height: 100%; object-fit: cover; object-position: var(--pos, 50% 40%); }
.am-article { padding: var(--s-3) var(--s-3) var(--s-4); }
.am-article .award-body { margin-top: var(--s-2); }
@media (max-width: 640px) { .am-figure { aspect-ratio: 4 / 3; } }
@media (prefers-reduced-motion: reduce) { dialog#award-modal[open] { animation: none; } }

/* Project modal */""", 1)
    (ROOT / "static/css/style.css").write_text(css, encoding="utf-8", newline="\n")
print("awards v2 written")
