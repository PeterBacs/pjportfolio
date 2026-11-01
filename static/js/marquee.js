/* Shared card row (Projects and Project videos): it drifts by itself and pauses on hover or focus.
   Drag, swipe or scroll sideways to move it by hand, or use the arrows and the Pause button.
   Clicking a card presses its ".mq-more" button or link. */
window.PortfolioMarquee = function (opts) {
  "use strict";
  var root = document.getElementById(opts.rootId);
  if (!root) return null;
  var cards = Array.prototype.slice.call(root.querySelectorAll(":scope > article"));
  var toggle = document.getElementById(opts.toggleId);
  var prevBtn = document.getElementById(opts.prevId), nextBtn = document.getElementById(opts.nextId);
  var n = cards.length, userPaused = false, moving = false;
  var reduceMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // the card's marquee animation (a hover transition can also be running on the card)
  function marquee(c) {
    var list = c.getAnimations();
    for (var i = 0; i < list.length; i++) { if (list[i].animationName === "mq-marquee") return list[i]; }
    return null;
  }

  function setPaused(p) {
    userPaused = p;
    root.classList.toggle("is-paused", p);
    if (toggle) { toggle.textContent = p ? "Play" : "Pause"; toggle.setAttribute("aria-pressed", p ? "true" : "false"); }
  }
  if (toggle) toggle.addEventListener("click", function () { setPaused(!userPaused); });

  // arrows: pause the drift and move one card at a time
  function stepCards(dir) {
    if (reduceMotion) {
      var w = (cards[0].getBoundingClientRect().width || 300) + 32;
      root.scrollBy({ left: dir * w, behavior: "auto" });
      return;
    }
    if (moving) return;
    var anims = cards.map(marquee).filter(Boolean);
    if (!anims.length) return;
    setPaused(true);
    var D = anims[0].effect.getTiming().duration, per = D / n;
    var start = anims.map(function (a) {
      var ct = Number(a.currentTime);
      if (ct < per * 1.5) ct += D;
      return ct;
    });
    var t0 = Date.now(), dur = 520;
    moving = true;
    var timer = window.setInterval(function () {
      var k = Math.min(1, (Date.now() - t0) / dur);
      var e = 1 - Math.pow(1 - k, 3);
      anims.forEach(function (a, i) { a.currentTime = start[i] + dir * per * e; });
      if (k >= 1) { window.clearInterval(timer); moving = false; }
    }, 16);
  }
  if (prevBtn) prevBtn.addEventListener("click", function () { stepCards(-1); });
  if (nextBtn) nextBtn.addEventListener("click", function () { stepCards(1); });

  root.addEventListener("touchstart", function () { root.classList.add("is-touch"); }, { passive: true });
  root.addEventListener("touchend", function () { window.setTimeout(function () { root.classList.remove("is-touch"); }, 1500); }, { passive: true });

  // drag, swipe and sideways scroll move the cards by hand; up and down still scroll the page
  if (!reduceMotion) {
    cards.forEach(function (c) { var im = c.querySelector("img"); if (im) im.draggable = false; });
    var gapPx = function () {
      var g = getComputedStyle(root).getPropertyValue("--carousel-item-gap").trim();
      var v = parseFloat(g) || 2;
      return /rem$/.test(g) ? v * parseFloat(getComputedStyle(document.documentElement).fontSize) : v;
    };
    var shiftPx = function (px) {   // positive px moves the cards to the left
      var anims = cards.map(marquee).filter(Boolean);
      if (!anims.length) return;
      var D = anims[0].effect.getTiming().duration, per = D / n;
      var dt = px / ((cards[0].offsetWidth || 300) + gapPx()) * per;
      anims.forEach(function (a) {
        var ct = Number(a.currentTime);
        if (ct < per * 1.5) ct += D;
        a.currentTime = ct + dt;
      });
    };
    var down = false, dragged = false, suppress = false, pid = null, startX = 0, lastX = 0, lastT = 0, vel = 0, glide = null;
    root.addEventListener("pointerdown", function (e) {
      if (e.pointerType === "mouse" && e.button !== 0) return;
      window.clearInterval(glide);
      down = true; dragged = false; pid = e.pointerId; startX = lastX = e.clientX; lastT = e.timeStamp; vel = 0;
    });
    root.addEventListener("pointermove", function (e) {
      if (!down || e.pointerId !== pid) return;
      if (!dragged && Math.abs(e.clientX - startX) > 6) {
        dragged = true;
        root.classList.add("is-dragging");
        try { root.setPointerCapture(pid); } catch (err) {}
      }
      if (!dragged) return;
      var dx = e.clientX - lastX, dt = Math.max(1, e.timeStamp - lastT);
      shiftPx(-dx);
      vel = 0.8 * vel + 0.2 * (-dx / dt);
      lastX = e.clientX; lastT = e.timeStamp;
    });
    var release = function () {
      if (!down) return;
      down = false;
      if (!dragged) return;
      suppress = true;
      window.setTimeout(function () { suppress = false; }, 0);
      root.classList.remove("is-dragging");
      var v = Math.max(-1.6, Math.min(1.6, vel));
      glide = window.setInterval(function () {
        shiftPx(v * 16);
        v *= 0.93;
        if (Math.abs(v) < 0.02) window.clearInterval(glide);
      }, 16);
    };
    root.addEventListener("pointerup", release);
    root.addEventListener("pointercancel", release);
    root.addEventListener("click", function (e) { if (suppress) { e.stopPropagation(); e.preventDefault(); } }, true);
    root.addEventListener("wheel", function (e) {
      var dx = e.deltaX, dy = e.deltaY;
      if (e.shiftKey && !dx) { dx = dy; dy = 0; }
      if (Math.abs(dx) <= Math.abs(dy) || Math.abs(dx) < 2) return;
      e.preventDefault();
      shiftPx(dx);
    }, { passive: false });
  }

  // the whole card presses its button or link
  cards.forEach(function (c) {
    c.addEventListener("click", function (e) {
      if (e.target.closest("a, button")) return;
      var a = c.querySelector(".mq-more");
      if (a) a.click();
    });
  });

  return { root: root, cards: cards, pause: function () { setPaused(true); } };
};
