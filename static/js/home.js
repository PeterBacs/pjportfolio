/* Home hero: "Hi! I'm Peter" is typed, shakes slowly, is erased and typed again, in a loop. Static text when reduced motion is preferred. */
(function () {
  "use strict";
  var h1 = document.getElementById("hero-title");
  var live = h1 && h1.querySelector(".type-live");
  var ghost = h1 && h1.querySelector(".type-ghost");
  if (!live || !ghost) return;
  var text = ghost.textContent;
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (reduce) { live.textContent = text; h1.classList.add("typed"); return; }

  var i = 0;
  var timer = null;
  function later(fn, ms) { timer = window.setTimeout(fn, ms); }
  function jolt() {
    live.classList.remove("jolt");
    void live.offsetWidth;
    live.classList.add("jolt");
  }
  function typeNext() {
    live.classList.remove("shake");
    if (i === 0) h1.classList.remove("typed");
    i += 1;
    live.textContent = text.slice(0, i);
    jolt();
    if (i < text.length) {
      later(typeNext, 130 + Math.random() * 90);
    } else {
      h1.classList.add("typed");
      live.classList.add("shake");
      later(function () { live.classList.remove("shake"); later(eraseNext, 600); }, 3600);
    }
  }
  function eraseNext() {
    live.classList.remove("shake");
    h1.classList.remove("typed");
    i -= 1;
    live.textContent = text.slice(0, i);
    if (i > 0) {
      later(eraseNext, 45);
    } else {
      later(typeNext, 450);
    }
  }
  document.addEventListener("visibilitychange", function () {
    if (document.hidden) { window.clearTimeout(timer); }
    else { window.clearTimeout(timer); later(i < text.length ? typeNext : eraseNext, 300); }
  });
  later(typeNext, 650);
})();
