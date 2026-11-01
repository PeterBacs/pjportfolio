/* Hero scroll stage: drives the pinned cinematic hero from scroll position, with eased (inertial) progress.
   Publishes window.cineState = { p, target, reduced } for the 3D layer. Scrolling is never locked or hijacked:
   the page scrolls natively and this only eases how far the hero has "played", in both directions. */
(function () {
  "use strict";
  var root = document.documentElement;
  var cine = document.getElementById("cine");
  if (!cine) return;
  var reduced = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  var state = (window.cineState = { p: 0, target: 0, reduced: reduced });
  root.classList.add("cx");

  var stage = cine.querySelector(".cine-stage");
  var bg = cine.querySelector(".cine-bg");
    var shade = cine.querySelector(".cine-shade");
  var copy = cine.querySelector(".cine-copy");
  var hint = cine.querySelector(".cine-hint");
  var meter = cine.querySelector(".cine-meter b");
  var scenes = Array.prototype.slice.call(cine.querySelectorAll(".cine-scene"));
  var header = document.querySelector(".site-header");

  /* text sits beside the figure on wide screens and on short landscape phones; stacked at the bottom on portrait phones */
  var sideLayout = function () {
    var w = window.innerWidth, h = window.innerHeight;
    if (h <= 560 && w > h) return true;
    return w > 700 && !(h > w && w <= 1100);
  };
  var clamp = function (v, a, b) { return Math.min(b, Math.max(a, v)); };
  var smooth = function (a, b, v) { var t = clamp((v - a) / (b - a), 0, 1); return t * t * (3 - 2 * t); };

  /* scenes play between SCENE_START and SCENE_END of the runway */
  var SCENE_START = 0.16, SCENE_END = 0.9;
  function sceneWeight(i, p) {
    var span = (SCENE_END - SCENE_START) / scenes.length;
    var a = SCENE_START + i * span, b = a + span, f = span * 0.22;
    return smooth(a, a + f, p) * (1 - smooth(b - f, b, p));
  }
  state.sceneWeight = sceneWeight;
  state.sceneCount = scenes.length;

  function targetProgress() {
    var r = cine.getBoundingClientRect();
    var run = r.height - window.innerHeight;
    return run > 0 ? clamp(-r.top / run, 0, 1) : 0;
  }

  function apply(p) {
    var ease = p;
    state.theta = 0;
    drawFrame(p);
    copy.style.opacity = (1 - smooth(0.0, 0.08, p)).toFixed(3);
    copy.style.transform = "translate3d(0," + (smooth(0.0, 0.08, p) * 6).toFixed(2) + "vh,0)";
    copy.style.pointerEvents = p > 0.06 ? "none" : "";
    copy.style.visibility = p > 0.1 ? "hidden" : "";
    hint.style.opacity = (1 - smooth(0.0, 0.04, p)).toFixed(3);
    var dim = smooth(0.1, 0.2, p) * 0.5 + smooth(0.86, 1, p) * 0.5;
    stage.style.setProperty("--dim", dim.toFixed(3));
    bg.style.filter = "brightness(" + (1 - dim * 0.55).toFixed(3) + ")";
    meter.style.transform = "scaleX(" + p.toFixed(4) + ")";
    for (var i = 0; i < scenes.length; i++) {
      var w = sceneWeight(i, p);
      scenes[i].style.opacity = w.toFixed(3);
      scenes[i].style.visibility = w < 0.01 ? "hidden" : "visible";
      var shift = (1 - w) * 24;
      scenes[i].style.transform = "translate3d(0," + (i % 2 ? shift : -shift).toFixed(1) + "px,0)" + (sideLayout() ? " translateY(-50%)" : "");
    }
  }

  /* scroll-scrubbed frame sequence (the orbit clip, exported as WebP frames) */
  var cv = document.getElementById("cine-frames"), ctx = cv && cv.getContext("2d");
  var FR = [], FN = parseInt(bg.getAttribute("data-count") || "0", 10), lastIdx = -1;
  var FB = (window.innerWidth <= 700 && window.innerHeight > window.innerWidth && bg.getAttribute("data-frames-m")) || bg.getAttribute("data-frames");
  function loadFrames() {
    if (!ctx || !FN) return;
    var order = [0], i;
    for (i = 8; i < FN; i += 8) order.push(i);
    for (i = 0; i < FN; i++) if (order.indexOf(i) === -1) order.push(i);
    var k = 0;
    (function next() {
      if (k >= order.length) return;
      var n = order[k++], im = new Image();
      im.onload = function () { FR[n] = im; if (n === 0) { sizeCanvas(); bg.classList.add("is-live"); lastIdx = -1; drawFrame(state.p); } setTimeout(next, 0); };
      im.onerror = function () { setTimeout(next, 0); };
      im.src = FB + ("00" + n).slice(-3) + ".webp";
    })();
  }
  function sizeCanvas() {
    var r = stage.getBoundingClientRect(), d = Math.min(window.devicePixelRatio || 1, 2);
    cv.width = Math.round(r.width * d); cv.height = Math.round(r.height * d); lastIdx = -1;
  }
  function drawFrame(p) {
    if (!ctx || !FN) return;
    var idx = Math.round(clamp(p, 0, 1) * (FN - 1));
    if (!FR[idx]) { var d; for (d = 1; d < FN; d++) { if (FR[idx - d]) { idx -= d; break; } if (FR[idx + d]) { idx += d; break; } } }
    var im = FR[idx]; if (!im || idx === lastIdx) return; lastIdx = idx;
    var cw = cv.width, ch = cv.height, s = Math.max(cw / im.naturalWidth, ch / im.naturalHeight);
    var w = im.naturalWidth * s, h = im.naturalHeight * s;
    ctx.drawImage(im, (cw - w) / 2, (ch - h) * 0.4, w, h);
  }
  window.addEventListener("resize", function () { if (ctx) { sizeCanvas(); drawFrame(state.p); } });

  var lastY = window.scrollY, away = false;
  function updateHeader(p) {
    if (!header) return;
    var y = window.scrollY, down = y > lastY + 1, up = y < lastY - 1;
    var inScenes = p > 0.04 && p < 0.97;
    if (inScenes && down) away = true;
    else if (up || !inScenes) away = false;
    header.classList.toggle("is-away", away);
    if (down || up) lastY = y;
  }

  loadFrames();
  if (reduced) {
    /* static hero, no pinning, no scroll scrubbing */
    root.classList.add("no-pin");
    state.p = 0; state.target = 0;
  } else {
    var last = performance.now(), running = false;
    function frame(now) {
      var dt = Math.min(0.1, (now - last) / 1000); last = now;
      state.target = targetProgress();
      /* hero off screen (anchor jump, reload far down the page): no easing, so its objects never linger over other sections */
      var rc = cine.getBoundingClientRect();
      if (rc.bottom < 0 || rc.top > window.innerHeight) state.p = state.target;
      /* time constant ~0.45s: settles in roughly 1.3s, in both scroll directions */
      var k = 1 - Math.exp(-dt / 0.45);
      state.p += (state.target - state.p) * k;
      if (Math.abs(state.target - state.p) < 0.004) state.p = state.target;
      apply(state.p);
      updateHeader(state.target);
      running = Math.abs(state.target - state.p) > 0.004;
      if (running) requestAnimationFrame(frame); else last = 0;
    }
    function kick() { if (!running) { running = true; last = performance.now(); requestAnimationFrame(frame); } }
    window.addEventListener("scroll", kick, { passive: true });
    window.addEventListener("resize", kick);
    apply(0);
    kick();
  }

})();
