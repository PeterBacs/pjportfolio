/* Teaching philosophy page: an auto-playing photo gallery that can also be scrolled.
   Crossfade with a slow zoom, a progress bar, a thumbnail rail, drag and swipe, sideways scroll and arrow keys. */
(function () {
  "use strict";
  var root = document.getElementById("pg");
  if (!root) return;

  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var stage = root.querySelector(".pg-stage");
  var slides = Array.prototype.slice.call(root.querySelectorAll(".pg-slide"));
  var thumbs = Array.prototype.slice.call(root.querySelectorAll(".pg-thumb"));
  var rail = root.querySelector(".pg-rail");
  var cap = root.querySelector(".pg-cap");
  var count = root.querySelector(".pg-count b");
  var playBtn = root.querySelector(".pg-play");
  var bar = root.querySelector(".pg-bar i");
  var n = slides.length;
  var INTERVAL = 1500;                  // milliseconds each photo stays on screen
  var FADE = Math.round(Math.min(1000, INTERVAL * 0.45));
  root.style.setProperty("--pg-ms", INTERVAL + "ms");
  root.style.setProperty("--pg-fade", FADE + "ms");
  var active = 0, timer = null, playing = !reduce, hovering = false, inView = true;

  function pad(k) { return (k < 10 ? "0" : "") + k; }

  /* pictures are fetched only when they are about to be shown */
  function load(k) {
    k = ((k % n) + n) % n;
    var s = slides[k];
    if (s.getAttribute("data-ready")) return;
    s.setAttribute("data-ready", "1");
    var bg = s.querySelector(".pg-bgd");
    if (bg && bg.getAttribute("data-bg")) bg.style.backgroundImage = "url(" + bg.getAttribute("data-bg") + ")";
    var im = s.querySelector("img[data-src]");
    if (im) {
      im.setAttribute("srcset", im.getAttribute("data-srcset"));
      im.setAttribute("src", im.getAttribute("data-src"));
      im.removeAttribute("data-src");
      im.removeAttribute("data-srcset");
    }
  }

  function restartBar() {
    if (!bar) return;
    bar.style.animation = "none";
    void bar.offsetWidth;
    bar.style.animation = "";
    bar.classList.toggle("run", playing && !reduce);
  }

  function centerThumb(k, smooth) {
    var t = thumbs[k];
    if (!t || !rail) return;
    var left = t.offsetLeft - (rail.clientWidth - t.offsetWidth) / 2;
    try { rail.scrollTo({ left: left, behavior: smooth && !reduce ? "smooth" : "auto" }); } catch (e) { rail.scrollLeft = left; }
  }

  function show(k, userMoved) {
    k = ((k % n) + n) % n;
    load(k); load(k + 1); load(k + 2); load(k + 3); load(k - 1);
    var prev = active;
    if (k !== prev) {
      slides[prev].classList.remove("is-active");
      slides[prev].classList.add("is-leaving");
      window.setTimeout(function (s) { return function () { s.classList.remove("is-leaving"); }; }(slides[prev]), FADE + 100);
    }
    active = k;
    slides[k].classList.remove("is-leaving");
    slides[k].classList.add("is-active");
    thumbs.forEach(function (t, i) {
      t.classList.toggle("is-active", i === k);
      if (i === k) t.setAttribute("aria-current", "true"); else t.removeAttribute("aria-current");
    });
    if (cap) {
      cap.textContent = slides[k].getAttribute("data-caption") || "";
      cap.classList.toggle("is-long", cap.textContent.length > 60);
    }
    if (count) count.textContent = pad(k + 1);
    centerThumb(k, true);
    restartBar();
    schedule();
  }

  function schedule() {
    window.clearTimeout(timer);
    if (!playing || hovering || !inView || document.hidden) return;
    timer = window.setTimeout(function () { show(active + 1); }, INTERVAL);
  }

  function setPlaying(on) {
    playing = on;
    if (playBtn) {
      playBtn.textContent = on ? "Pause" : "Play";
      playBtn.setAttribute("aria-pressed", on ? "false" : "true");
    }
    if (cap) cap.setAttribute("aria-live", on ? "off" : "polite");
    restartBar();
    schedule();
  }

  /* controls */
  root.querySelectorAll("[data-dir]").forEach(function (b) {
    b.addEventListener("click", function () { show(active + Number(b.getAttribute("data-dir"))); });
  });
  thumbs.forEach(function (t, i) { t.addEventListener("click", function () { if (!dragMoved) show(i); }); });
  if (playBtn) playBtn.addEventListener("click", function () { setPlaying(!playing); });

  stage.addEventListener("keydown", function (e) {
    if (e.key === "ArrowRight") { e.preventDefault(); show(active + 1); }
    else if (e.key === "ArrowLeft") { e.preventDefault(); show(active - 1); }
  });

  /* drag or swipe on the photo */
  var sx = null;
  stage.addEventListener("pointerdown", function (e) { if (e.target.closest(".pg-nav")) return; sx = e.clientX; });
  stage.addEventListener("pointerup", function (e) {
    if (sx === null) return;
    var dx = e.clientX - sx;
    sx = null;
    if (Math.abs(dx) > 45) show(active + (dx < 0 ? 1 : -1));
  });
  stage.addEventListener("pointercancel", function () { sx = null; });

  /* sideways scroll on a trackpad (or shift and the wheel); up and down still scrolls the page */
  var lock = 0;
  stage.addEventListener("wheel", function (e) {
    var dx = e.deltaX, dy = e.deltaY;
    if (e.shiftKey && !dx) { dx = dy; dy = 0; }
    if (Math.abs(dx) <= Math.abs(dy) || Math.abs(dx) < 12) return;
    e.preventDefault();
    var now = Date.now();
    if (now - lock < 450) return;
    lock = now;
    show(active + (dx > 0 ? 1 : -1));
  }, { passive: false });

  /* the thumbnail rail scrolls by touch and trackpad, and by dragging with a mouse */
  var dragging = false, dragMoved = false, startX = 0, startLeft = 0;
  rail.addEventListener("pointerdown", function (e) {
    if (e.pointerType !== "mouse") return;
    dragging = true; dragMoved = false; startX = e.clientX; startLeft = rail.scrollLeft;
  });
  window.addEventListener("pointermove", function (e) {
    if (!dragging) return;
    var dx = e.clientX - startX;
    if (Math.abs(dx) > 4) { dragMoved = true; rail.classList.add("is-dragging"); }
    rail.scrollLeft = startLeft - dx;
  });
  window.addEventListener("pointerup", function () {
    if (!dragging) return;
    dragging = false;
    rail.classList.remove("is-dragging");
    window.setTimeout(function () { dragMoved = false; }, 0);
  });

  /* pause while the pointer or keyboard focus is on the photo, while the tab is hidden, or when it is off screen */
  stage.addEventListener("mouseenter", function () { hovering = true; if (bar) bar.classList.add("hold"); schedule(); });
  stage.addEventListener("mouseleave", function () { hovering = false; if (bar) bar.classList.remove("hold"); restartBar(); schedule(); });
  document.addEventListener("visibilitychange", schedule);
  if ("IntersectionObserver" in window) {
    new IntersectionObserver(function (es) {
      inView = es[0].isIntersecting;
      if (bar) bar.classList.toggle("hold", !inView);
      schedule();
    }, { threshold: 0.25 }).observe(stage);
  }

  /* sections fade up as they arrive */
  var rvs = document.querySelectorAll(".pg-rv");
  if (document.documentElement.classList.contains("pgm") && "IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } });
    }, { threshold: 0.15 });
    rvs.forEach(function (el) { io.observe(el); });
  } else {
    rvs.forEach(function (el) { el.classList.add("in"); });
  }

  /* the contents list highlights the belief being read */
  var toc = Array.prototype.slice.call(document.querySelectorAll(".pg-toc a"));
  var items = toc.map(function (a) { return document.getElementById(a.getAttribute("href").slice(1)); });
  if (toc.length && "IntersectionObserver" in window) {
    var spy = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        toc.forEach(function (a) { a.classList.toggle("on", a.getAttribute("href") === "#" + e.target.id); });
      });
    }, { rootMargin: "-35% 0px -55% 0px" });
    items.forEach(function (el) { if (el) spy.observe(el); });
  }

  load(0); load(1); load(n - 1);
  centerThumb(0, false);
  setPlaying(playing);
  restartBar();
})();
