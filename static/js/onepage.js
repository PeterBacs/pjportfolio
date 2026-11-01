/* Home as one scrolling page: each section is a full screen that snaps into place.
   This script adds the entrance animations, the side dots, the progress bar and the menu highlighting. */
(function () {
  "use strict";
  var root = document.documentElement;
  var sections = Array.prototype.slice.call(document.querySelectorAll(".onepage > .snap"));
  if (!sections.length) return;
  var animate = root.classList.contains("op");
  var byId = {};
  sections.forEach(function (s) { byId[s.id] = s; });

  /* header height, used for snap alignment */
  var header = document.querySelector(".site-header");
  function setHeader() { if (header) root.style.setProperty("--hdr", header.offsetHeight + "px"); }
  setHeader();
  window.addEventListener("resize", setHeader);

  /* items that fade and slide in one after another when a section arrives */
  var picks = {
    home: [".hx-photo", ".hx-text h1", ".hx-lede", ".hx-actions"],
    about: [".abt-portrait", ".abt-kicker", ".abt-hero h2", ".abt-bio", ".abt-actions", ".abt-facts li"],
    skills: [".mq-title", ".mq .carousel", ".mq-controls"],
    projects: [".mq-title", ".mq .carousel", ".mq-bar"],
    videos: [".mq-title", ".mq .carousel", ".mq-bar"],
    awards: ["#awards-title", ".carousel", ".award-details"],
    gallery: [".pg-stage", ".pg-controls"],
    contact: [".ct-kicker", ".ct h2", ".ct-lede", ".ct-card", ".ct-roles h2", ".rl-lede", ".rl"]
  };
  var fromLeft = [".hx-photo", ".abt-portrait"];
  if (animate) {
    sections.forEach(function (sec) {
      var i = 0, seen = [];
      (picks[sec.id] || []).forEach(function (sel) {
        sec.querySelectorAll(sel).forEach(function (el) {
          if (seen.indexOf(el) !== -1) return;
          seen.push(el);
          el.classList.add("rv");
          el.style.setProperty("--i", i++);
          fromLeft.forEach(function (k) { if (el.matches(k)) el.classList.add("rv-left"); });
        });
      });
    });
  }

  /* menu highlighting and side dots */
  var navLinks = {};
  document.querySelectorAll("#site-nav > ul > li > a").forEach(function (a) {
    var h = a.getAttribute("href") || "";
    var path = "";
    try { path = new URL(h, location.href).pathname; } catch (e) {}
    var id = h.indexOf("#") !== -1 ? h.split("#")[1] : (path === "/" ? "home" : "");
    if (id) navLinks[id] = a;
  });
  var dots = document.createElement("nav");
  dots.className = "op-dots";
  dots.setAttribute("aria-label", "Sections");
  var dotEls = {};
  sections.forEach(function (sec) {
    var b = document.createElement("button");
    b.type = "button";
    b.setAttribute("aria-label", sec.getAttribute("data-label"));
    b.innerHTML = "<span>" + sec.getAttribute("data-label") + "</span>";
    b.addEventListener("click", function () { go(sec.id); });
    dots.appendChild(b);
    dotEls[sec.id] = b;
  });
  document.body.appendChild(dots);
  var bar = document.createElement("div");
  bar.className = "op-progress";
  bar.setAttribute("aria-hidden", "true");
  document.body.appendChild(bar);

  /* sliding marker under the menu item of the section being read */
  var navList = document.querySelector("#site-nav ul");
  var marker = null;
  if (navList) {
    navList.style.position = "relative";
    marker = document.createElement("span");
    marker.className = "nav-ind";
    marker.setAttribute("aria-hidden", "true");
    navList.appendChild(marker);
  }
  function moveMarker(instant) {
    var a = navLinks[current];
    if (!marker || !a) return;
    if (instant) marker.style.transition = "none";
    marker.style.width = a.offsetWidth + "px";
    var ur = navList.getBoundingClientRect(), ar = a.getBoundingClientRect();
    marker.style.top = (ar.bottom - ur.top - 3) + "px";
    marker.style.transform = "translateX(" + (ar.left - ur.left) + "px)";
    if (instant) { void marker.offsetWidth; marker.style.transition = ""; }
    marker.classList.remove("nav-ind-pop");
    void marker.offsetWidth;
    marker.classList.add("nav-ind-pop");
  }
  window.addEventListener("resize", function () { moveMarker(true); });
  if (toggleRef()) toggleRef().addEventListener("click", function () { window.setTimeout(function () { moveMarker(true); }, 30); });
  function toggleRef() { return document.querySelector(".nav-toggle"); }

  var current = null;
  function setActive(id) {
    if (id === current) return;
    var first = current === null;
    current = id;
    var navId = id === "videos" ? "projects" : id;
    Object.keys(navLinks).forEach(function (k) {
      if (k === navId) navLinks[k].setAttribute("aria-current", "true"); else navLinks[k].removeAttribute("aria-current");
    });
    Object.keys(dotEls).forEach(function (k) {
      if (k === id) dotEls[k].setAttribute("aria-current", "true"); else dotEls[k].removeAttribute("aria-current");
    });
    moveMarker(first);
    var a = navLinks[id];
    if (a) { a.classList.remove("nav-pop"); void a.offsetWidth; a.classList.add("nav-pop"); }
    root.setAttribute("data-section", id);
    try { history.replaceState(null, "", id === "home" ? location.pathname + location.search : "#" + id); } catch (e) {}
  }

  function go(id) {
    var el = byId[id];
    if (!el) return;
    el.scrollIntoView({ behavior: animate ? "smooth" : "auto", block: "start" });
  }

  /* which section is on screen: the one covering the middle of the window */
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) setActive(e.target.id);
    });
  }, { rootMargin: "-45% 0px -50% 0px", threshold: 0 });
  sections.forEach(function (s) { io.observe(s); });

  /* entrance animation: plays each time a section arrives */
  if (animate) {
    var rv = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) e.target.classList.add("is-in");
        else if (e.intersectionRatio === 0) e.target.classList.remove("is-in");
      });
    }, { threshold: [0, 0.2] });
    sections.forEach(function (s) { rv.observe(s); });
  }

  /* progress bar */
  var tick = false;
  function progress() {
    tick = false;
    var max = root.scrollHeight - window.innerHeight;
    bar.style.transform = "scaleX(" + (max > 0 ? Math.min(1, window.scrollY / max) : 0) + ")";
  }
  window.addEventListener("scroll", function () {
    if (tick) return;
    tick = true;
    window.requestAnimationFrame(progress);
  }, { passive: true });
  progress();

  /* links that point at a section scroll to it instead of loading the stand-alone page */
  var pathToId = { "/": "home", "/about/": "about", "/skills/": "skills", "/projects/": "projects", "/awards/": "awards", "/gallery/": "gallery", "/contact/": "contact" };
  var toggle = document.querySelector(".nav-toggle");
  document.addEventListener("click", function (e) {
    if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    var a = e.target.closest && e.target.closest("a[href]");
    if (!a || a.hasAttribute("data-modal") || a.target === "_blank") return;
    var url;
    try { url = new URL(a.href, location.href); } catch (err) { return; }
    if (url.origin !== location.origin) return;
    var id = null;
    if (url.pathname === location.pathname && url.hash && byId[url.hash.slice(1)]) id = url.hash.slice(1);
    else if (!url.hash && pathToId[url.pathname]) id = pathToId[url.pathname];
    if (!id) return;
    e.preventDefault();
    go(id);
    if (toggle && toggle.getAttribute("aria-expanded") === "true") toggle.click();
  });

  /* opened with /#contact or similar */
  var start = location.hash && byId[location.hash.slice(1)] ? location.hash.slice(1) : "home";
  if (start !== "home") window.setTimeout(function () { byId[start].scrollIntoView({ block: "start" }); }, 60);
  setActive(start);
  window.addEventListener("hashchange", function () {
    var id = location.hash.slice(1);
    if (byId[id]) go(id);
  });
})();
