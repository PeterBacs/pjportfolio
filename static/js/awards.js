/* Awards page: 3D cover-flow carousel. Clicking a photo opens its article in a modal.
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

  // ---- photos that alternate inside one award
  var reduceMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  function alternate(scope) {
    var phs = Array.prototype.slice.call(scope.querySelectorAll(".ph"));
    if (phs.length < 2) return null;
    var k = 0;
    return window.setInterval(function () {
      if (document.hidden) return;
      phs[k].classList.remove("on"); k = (k + 1) % phs.length; phs[k].classList.add("on");
    }, 3500);
  }
  slides.forEach(function (s) { alternate(s); });
  var modalTimer = null;

  // ---- article modal
  var swiped = false;
  function openArticle(i) {
    var tpl = document.getElementById("tpl-" + slides[i].getAttribute("data-id"));
    if (!tpl || !modal || typeof modal.showModal !== "function") return;
    active = i; layout(false);
    modalBody.replaceChildren(tpl.content.cloneNode(true));
    if (modalTimer) window.clearInterval(modalTimer);
    modalTimer = alternate(modalBody);
    var h = modalBody.querySelector("h2");
    if (h) modal.setAttribute("aria-labelledby", h.id);
    if (!modal.open) modal.showModal();
    modal.scrollTop = 0;
  }
  function closeArticle() { if (modalTimer) window.clearInterval(modalTimer); if (modal.open) modal.close(); modalBody.replaceChildren(); }
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

  // trackpad or mouse-wheel sideways scroll moves the carousel; up and down still scrolls the page
  var wheelLock = 0;
  stage.addEventListener("wheel", function (e) {
    var dx = e.deltaX, dy = e.deltaY;
    if (e.shiftKey && !dx) { dx = dy; dy = 0; }
    if (Math.abs(dx) <= Math.abs(dy) || Math.abs(dx) < 12) return;
    e.preventDefault();
    var now = Date.now();
    if (now - wheelLock < 420) return;
    wheelLock = now;
    step(dx > 0 ? 1 : -1);
    restartAuto();
  }, { passive: false });

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
