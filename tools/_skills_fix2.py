import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def rw(p, f):
    path = ROOT / p
    path.write_text(f(path.read_text(encoding="utf-8")), encoding="utf-8", newline="\n")


def css(s):
    s = s.replace(".skills-layout { display: grid; grid-template-columns: 15rem minmax(0, 1fr);", ".skills-layout { display: grid; grid-template-columns: 15rem minmax(0, 1fr);")
    s = s.replace("  .skills-layout { grid-template-columns: 1fr; gap: 0; }", "  .skills-layout { grid-template-columns: minmax(0, 1fr); gap: 0; }")
    s = s.replace(".skill-nav { position: sticky; top: 5.5rem; }", ".skills-layout > * { min-width: 0; }\n.skill-nav { position: sticky; top: 5.5rem; }", 1)
    return s


rw("static/css/style.css", css)


def js(s):
    start = s.index("  // Skills: highlight the section currently in view in the side panel")
    end = s.rindex("})();")
    new = """  // Skills: highlight the section currently being read in the side panel
  var sNav = document.querySelector(".skill-nav");
  if (sNav) {
    var sections = Array.prototype.slice.call(document.querySelectorAll(".skill-section"));
    var navLinks = {};
    sNav.querySelectorAll("a[href^='#']").forEach(function (a) { navLinks[a.getAttribute("href").slice(1)] = a; });
    var current = null;
    var update = function () {
      var line = (window.innerHeight || document.documentElement.clientHeight || 0) * 0.3 + 96;
      var active = null;
      sections.forEach(function (sec) { if (sec.getBoundingClientRect().top <= line) active = sec.id; });
      if (active === current) return;
      if (current && navLinks[current]) navLinks[current].removeAttribute("aria-current");
      if (active && navLinks[active]) navLinks[active].setAttribute("aria-current", "true");
      current = active;
    };
    var ticking = false;
    window.addEventListener("scroll", function () {
      if (ticking) return;
      ticking = true;
      window.requestAnimationFrame(function () { ticking = false; update(); });
    }, { passive: true });
    window.addEventListener("resize", update);
    update();
  }
"""
    return s[:start] + new + s[end:]


rw("static/js/site.js", js)
print("fixed")
