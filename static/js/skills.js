/* Skills page: auto-scrolling marquee of section cards. Read more opens the section full screen in a modal. */
(function () {
  "use strict";
  var root = document.getElementById("skills-carousel");
  if (!root) return;
  var cards = Array.prototype.slice.call(root.querySelectorAll(":scope > article"));
  var toggle = document.getElementById("mq-toggle");
  var modal = document.getElementById("skill-modal");
  var body = document.getElementById("sm-body");
  var n = cards.length, openIndex = 0, userPaused = false, pointerUsed = false;
  // the card's marquee animation (a hover transition can also be running on the card, so do not just take the first one)
  function marquee(c) {
    var list = c.getAnimations();
    for (var i = 0; i < list.length; i++) { if (list[i].animationName === "mq-marquee") return list[i]; }
    return null;
  }
  document.addEventListener("pointerdown", function () { pointerUsed = true; }, true);
  document.addEventListener("keydown", function () { pointerUsed = false; }, true);

  // ---- pause control (always available)
  function setPaused(p) {
    userPaused = p;
    root.classList.toggle("is-paused", p);
    if (toggle) { toggle.textContent = p ? "Play" : "Pause"; toggle.setAttribute("aria-pressed", p ? "true" : "false"); }
  }
  if (toggle) toggle.addEventListener("click", function () { setPaused(!userPaused); });
  // ---- arrows: pause the drift and move one card at a time
  var prevBtn = document.getElementById("mq-prev"), nextBtn = document.getElementById("mq-next");
  var reduceMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var moving = false;
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
    var D = anims[0].effect.getTiming().duration;
    var per = D / n;
    var start = anims.map(function (a) {
      var ct = Number(a.currentTime);
      // with a negative delay the animation only runs while currentTime >= 0, so keep it clear of 0 when going back
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

  // ---- drag, swipe and sideways scroll move the cards by hand; up and down still scroll the page
  if (!reduceMotion) {
    cards.forEach(function (c) { var im = c.querySelector("img"); if (im) im.draggable = false; });
    var gapPx = function () {
      var g = getComputedStyle(root).getPropertyValue("--carousel-item-gap").trim();
      var v = parseFloat(g) || 2;
      return /rem$/.test(g) ? v * parseFloat(getComputedStyle(document.documentElement).fontSize) : v;
    };
    // positive px moves the cards to the left
    var shiftPx = function (px) {
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
      var v = vel;
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
    var afterClose = function () {
      body.replaceChildren();
      root.classList.remove("is-open");
      // after a mouse/touch close, drop focus so the marquee resumes; keyboard users keep their place
      var drop = function () { if (pointerUsed && root.contains(document.activeElement)) document.activeElement.blur(); };
      drop(); window.setTimeout(drop, 0); window.setTimeout(drop, 120);
    };
    modal.addEventListener("close", afterClose);
    document.getElementById("sm-close").addEventListener("click", function () { window.setTimeout(afterClose, 0); });
    modal.addEventListener("keydown", function (e) {
      if (e.key === "ArrowRight") { e.preventDefault(); move(1); }
      else if (e.key === "ArrowLeft") { e.preventDefault(); move(-1); }
    });
  }
})();
