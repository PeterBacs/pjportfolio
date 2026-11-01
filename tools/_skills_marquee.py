"""One-off: Skills carousel becomes the auto-scrolling marquee design supplied by the user, in a matte black theme."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def rw(p, f):
    path = ROOT / p
    path.write_text(f(path.read_text(encoding="utf-8")), encoding="utf-8", newline="\n")


def tpl(s):
    start = s.index('<section class="hcarousel"')
    end = s.index('<section class="wrap skills-fallback"')
    new = '''<section class="mq" aria-labelledby="sc-h">
  <h2 id="sc-h" class="sr-only">Skill sections</h2>
  <div class="carousel" mask id="skills-carousel" style="--items: {{ all_sections|length }}">
    {% for s in all_sections %}
    <article data-index="{{ loop.index0 }}" data-id="{{ s.id }}" data-letter="{{ s.letter }}" data-title="{{ s.title }}" style="--i: {{ loop.index0 }}">
      {{ img(visuals[s.id].image, sizes="300px", loading=('eager' if loop.index0 < 3 else 'lazy'), max_w=800) }}
      <span class="mq-letter" aria-hidden="true">{{ s.letter }}</span>
      <h3>{{ s.title }}</h3>
      <div>
        <p>{{ s.summary }}</p>
        <button class="mq-more" type="button" aria-label="Read more: section {{ s.letter }}, {{ s.title }}">Read more <span class="mq-n">{% if s.capabilities %}{{ s.capabilities|length }} capabilities{% else %}{{ techstack["items"]|length }} tools{% endif %}</span></button>
      </div>
      <div class="scard-full">{{ content(s) }}</div>
    </article>
    {% endfor %}
  </div>
  <div class="mq-bar">
    <button class="mq-toggle" type="button" id="mq-toggle" aria-pressed="false">Pause</button>
    <span class="mq-hint">Hover or focus to pause. Select Read more to open a section.</span>
  </div>
</section>

'''
    return s[:start] + new + s[end:]


rw("templates/skills.html", tpl)

js = r"""/* Skills page: auto-scrolling marquee of section cards. Read more opens the section full screen in a modal. */
(function () {
  "use strict";
  var root = document.getElementById("skills-carousel");
  if (!root) return;
  var cards = Array.prototype.slice.call(root.querySelectorAll("article"));
  var toggle = document.getElementById("mq-toggle");
  var modal = document.getElementById("skill-modal");
  var body = document.getElementById("sm-body");
  var n = cards.length, openIndex = 0, userPaused = false;

  // ---- pause control (always available)
  function setPaused(p) {
    userPaused = p;
    root.classList.toggle("is-paused", p);
    if (toggle) { toggle.textContent = p ? "Play" : "Pause"; toggle.setAttribute("aria-pressed", p ? "true" : "false"); }
  }
  if (toggle) toggle.addEventListener("click", function () { setPaused(!userPaused); });
  // touch: pause while a finger is down; focus: pause while any card has focus
  root.addEventListener("touchstart", function () { root.classList.add("is-touch"); }, { passive: true });
  root.addEventListener("touchend", function () { window.setTimeout(function () { root.classList.remove("is-touch"); }, 1500); }, { passive: true });

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
  function open(i) { openIndex = i; root.classList.add("is-open"); show(); if (!modal.open) modal.showModal(); }
  function move(d) { openIndex = ((openIndex + d) % n + n) % n; show(); }
  cards.forEach(function (c, i) {
    c.querySelector(".mq-more").addEventListener("click", function () { open(i); });
    c.querySelector("img").addEventListener("click", function () { open(i); });
  });
  if (modal) {
    document.getElementById("sm-close").addEventListener("click", function () { modal.close(); });
    document.getElementById("sm-prev").addEventListener("click", function () { move(-1); });
    document.getElementById("sm-next").addEventListener("click", function () { move(1); });
    modal.addEventListener("close", function () { body.replaceChildren(); root.classList.remove("is-open"); });
    modal.addEventListener("keydown", function (e) {
      if (e.key === "ArrowRight") { e.preventDefault(); move(1); }
      else if (e.key === "ArrowLeft") { e.preventDefault(); move(-1); }
    });
  }
})();
"""
(ROOT / "static/js/skills.js").write_text(js, encoding="utf-8", newline="\n")

css = """
/* Skills: auto-scrolling marquee carousel (design supplied by the user), matte black theme */
.mq { background: #0b0b0c; color: #e9e9ea; padding-block: var(--s-4) var(--s-3); margin-bottom: var(--s-5); border-block: 1px solid #1c1c1e; }
.carousel { --carousel-duration: 42s; --carousel-item-width: 300px; --carousel-item-height: 470px; --carousel-item-gap: 2rem;
  --carousel-width: min(100%, 1600px);
  position: relative; width: var(--carousel-width); height: var(--carousel-item-height); margin-inline: auto; overflow: clip; }
.carousel[mask] { mask-image: linear-gradient(to right, transparent, #000 7% 93%, transparent); -webkit-mask-image: linear-gradient(to right, transparent, #000 7% 93%, transparent); }
.carousel > article { position: absolute; top: 0; left: calc(100% + var(--carousel-item-gap)); width: var(--carousel-item-width); height: var(--carousel-item-height);
  display: grid; grid-template-rows: 200px auto 1fr; gap: 0.25rem; border: 1px solid #26262a; border-radius: 12px; background: #141416; color: #e9e9ea; padding-block-end: 1rem;
  will-change: transform; animation: mq-marquee var(--carousel-duration) linear infinite; animation-delay: calc(var(--carousel-duration) / var(--items) * var(--i) * -1); }
.carousel:hover > article, .carousel:focus-within > article, .carousel.is-paused > article, .carousel.is-touch > article, .carousel.is-open > article { animation-play-state: paused; }
.carousel > article:hover { border-color: #3a3a40; }
.carousel img { width: 100%; height: 100%; object-fit: cover; border-radius: 11px 11px 0 0; background: #000; filter: saturate(0.85) contrast(1.02); }
.mq-letter { position: absolute; left: 0.7rem; top: 0.7rem; display: grid; place-items: center; width: 2rem; height: 2rem; border-radius: 7px; background: #0b0b0c; color: #fff; border: 1px solid #2c2c30; font: 400 0.9rem var(--font-mono); }
.carousel > article > :not(img):not(.mq-letter) { padding: 0 1rem; }
.carousel > article h3 { font-size: 1.1rem; font-weight: 600; line-height: 1.25; padding-block: 0.75rem 0.25rem; margin: 0; color: #fff; letter-spacing: -0.01em; }
.carousel > article > div:not(.scard-full) { display: grid; grid-template-rows: 1fr auto; gap: 0.6rem; font-size: 0.88rem; }
.carousel > article p { margin: 0; color: #a7a7ad; display: -webkit-box; -webkit-line-clamp: 5; -webkit-box-orient: vertical; overflow: hidden; }
.mq-more { place-self: start; display: inline-flex; align-items: center; gap: 0.6rem; background: transparent; color: var(--accent-light); border: 1px solid var(--accent-light); border-radius: 4px; padding: 0.4rem 0.7rem; font: 600 0.82rem var(--font-sans); cursor: pointer; transition: background 150ms ease-in-out, color 150ms ease-in-out; }
.mq-more:hover, .mq-more:focus-visible { background: var(--accent-light); color: #0b0b0c; outline: none; }
.mq-more:focus-visible { box-shadow: 0 0 0 3px rgba(124, 208, 217, 0.4); }
.mq-n { font: 400 0.7rem var(--font-mono); opacity: 0.8; }
.carousel .scard-full { display: none; }
.mq-bar { display: flex; align-items: center; gap: var(--s-2); justify-content: center; padding: var(--s-2) var(--gutter) 0; flex-wrap: wrap; }
.mq-toggle { font: 600 0.82rem var(--font-sans); color: #e9e9ea; background: transparent; border: 1px solid #3a3a40; border-radius: 99px; padding: 0.45rem 1rem; cursor: pointer; transition: border-color var(--ease), background var(--ease); }
.mq-toggle:hover { border-color: #fff; background: #1a1a1c; }
.mq-toggle:focus-visible { outline: 2px solid var(--accent-light); outline-offset: 3px; }
.mq-hint { color: #8d8d93; font-size: 0.82rem; }
@keyframes mq-marquee { 100% { transform: translateX(calc((var(--items) * (var(--carousel-item-width) + var(--carousel-item-gap))) * -1)); } }
html:not(.js) .mq { display: none; }
@media (max-width: 640px) { .carousel { --carousel-item-width: 260px; --carousel-item-height: 455px; --carousel-duration: 48s; } .carousel[mask] { mask-image: linear-gradient(to right, transparent, #000 4% 96%, transparent); -webkit-mask-image: linear-gradient(to right, transparent, #000 4% 96%, transparent); } }
@media (prefers-reduced-motion: reduce) {
  .carousel { display: flex; gap: var(--carousel-item-gap); height: auto; overflow-x: auto; mask-image: none; -webkit-mask-image: none; padding: 0 var(--gutter) var(--s-2); scroll-snap-type: x mandatory; scrollbar-width: thin; }
  .carousel > article { position: static; animation: none; flex: none; height: var(--carousel-item-height); scroll-snap-align: start; }
  .mq-toggle { display: none; }
  .mq-hint { display: none; }
}
"""
rw("static/css/style.css", lambda s: s if "auto-scrolling marquee carousel" in s else s + css)
print("marquee written")
