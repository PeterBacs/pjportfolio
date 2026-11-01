/* Site-wide behaviour: mobile nav, lightbox, copy-email, lazy PDF preview. No dependencies. */
(function () {
  "use strict";
  document.documentElement.classList.add("js");

  // Mobile navigation
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("site-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      toggle.setAttribute("aria-expanded", String(open));
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && nav.classList.contains("open")) {
        nav.classList.remove("open");
        toggle.setAttribute("aria-expanded", "false");
        toggle.focus();
      }
    });
  }

  // Lightbox for figures (native <dialog>: focus trap and Esc come built in)
  var dlg = document.getElementById("lightbox");
  if (dlg && typeof dlg.showModal === "function") {
    var img = document.getElementById("lb-img");
    var cap = document.getElementById("lb-cap");
    document.addEventListener("click", function (e) {
      var a = e.target.closest && e.target.closest("a.fig-open, a[data-lightbox]");
      if (!a) return;
      e.preventDefault();
      var thumb = a.querySelector("img");
      img.src = a.getAttribute("href");
      img.alt = thumb ? thumb.alt : "";
      cap.textContent = a.dataset.caption || "";
      dlg.showModal();
    });
    dlg.addEventListener("click", function (e) { if (e.target === dlg) dlg.close(); });
  }

  // Force a real download for links marked data-download (browsers otherwise open PDFs and videos inline)
  document.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest("a[data-download]");
    if (!a || e.ctrlKey || e.metaKey || e.shiftKey || e.button) return;
    e.preventDefault();
    fetch(a.href).then(function (r) {
      if (!r.ok) throw new Error(r.status);
      return r.blob();
    }).then(function (blob) {
      var url = URL.createObjectURL(blob);
      var t = document.createElement("a");
      t.href = url;
      t.download = a.getAttribute("data-download");
      document.body.appendChild(t);
      t.click();
      t.remove();
      setTimeout(function () { URL.revokeObjectURL(url); }, 4000);
    }).catch(function () { window.location.href = a.href; });
  });

  // Analytics events (only if Microsoft Clarity is loaded): contact clicks
  document.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest(".ct-soc, .ct-mail, .ct-mailcard .btn");
    if (!a || typeof window.clarity !== "function") return;
    var name = a.classList.contains("ct-soc") ? (a.querySelector("strong") || a).textContent.trim().toLowerCase() : "email";
    window.clarity("event", "contact_" + name);
  });

  // Copy email
  var copy = document.getElementById("copy-email");
  if (copy) {
    copy.addEventListener("click", function () {
      var status = document.getElementById("copy-status");
      var addr = copy.dataset.email;
      var done = function (msg) { if (status) status.textContent = msg; };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(addr).then(function () { done("Copied."); }, function () { done("Copy failed. Please select the address manually."); });
      } else { done("Copy is not available. Please select the address manually."); }
    });
  }

  // PDF preview loads only when opened
  var prev = document.querySelector("details.preview[data-src]");
  if (prev) {
    prev.addEventListener("toggle", function () {
      var box = prev.querySelector(".preview-box");
      if (prev.open && !box.querySelector("iframe")) {
        var f = document.createElement("iframe");
        f.src = prev.dataset.src;
        f.title = "Résumé PDF preview";
        f.loading = "lazy";
        box.insertBefore(f, box.firstChild);
      }
    });
  }

  // Project modal: "View project" opens the case study in a dialog (the full page URL still works on its own)
  var pm = document.getElementById("project-modal");
  if (pm && typeof pm.showModal === "function") {
    var pmBody = document.getElementById("pm-body");
    var pmOpen = document.getElementById("pm-open");
    var loadProject = function (href) {
      return fetch(href).then(function (r) {
        if (!r.ok) throw new Error(r.status);
        return r.text();
      }).then(function (html) {
        var art = new DOMParser().parseFromString(html, "text/html").querySelector("article.project");
        if (!art) throw new Error("no article");
        pmBody.replaceChildren(document.importNode(art, true));
        pmOpen.href = href;
        if (!pm.open) pm.showModal();
        pm.scrollTop = 0;
        var h = pmBody.querySelector("h1");
        if (h) { h.setAttribute("tabindex", "-1"); h.focus({ preventScroll: true }); }
      }).catch(function () { window.location.href = href; });
    };
    document.addEventListener("click", function (e) {
      if (e.defaultPrevented || e.ctrlKey || e.metaKey || e.shiftKey || e.button) return;
      var a = e.target.closest && e.target.closest("a");
      if (!a) return;
      var inModal = pm.contains(a);
      if (inModal && a.getAttribute("href").charAt(0) === "#") {
        e.preventDefault();
        var t = pmBody.querySelector(a.getAttribute("href"));
        if (t) t.scrollIntoView();
        return;
      }
      if (a.hasAttribute("data-modal") || (inModal && /\/projects\/[^/]+\/$/.test(a.getAttribute("href")))) {
        e.preventDefault();
        loadProject(a.getAttribute("href"));
      }
    });
    var closeProject = function () { pmBody.replaceChildren(); if (pm.open) pm.close(); };
    document.getElementById("pm-close").addEventListener("click", closeProject);
    pm.addEventListener("close", function () { pmBody.replaceChildren(); });
    pm.addEventListener("cancel", function () { pmBody.replaceChildren(); });
    pm.addEventListener("click", function (e) { if (e.target === pm) closeProject(); });
  }

  // View-only résumé: page images in a modal. No PDF is published, so there is nothing to download.
  var rm = document.getElementById("resume-modal");
  if (rm && typeof rm.showModal === "function") {
    document.addEventListener("click", function (e) {
      var b = e.target.closest && e.target.closest("[data-resume]");
      if (!b) return;
      rm.querySelectorAll("img[data-src]").forEach(function (im) { im.src = im.dataset.src; im.removeAttribute("data-src"); });
      rm.showModal();
      rm.scrollTop = 0;
    });
    document.getElementById("rm-close").addEventListener("click", function () { rm.close(); });
    rm.addEventListener("click", function (e) { if (e.target === rm) rm.close(); });
    rm.addEventListener("contextmenu", function (e) { if (e.target.tagName === "IMG") e.preventDefault(); });
  }

  // choosing something from the About list closes the phone menu
  document.addEventListener("click", function (e) {
    if (!(e.target.closest && e.target.closest(".subnav a, .subnav button"))) return;
    var nav = document.getElementById("site-nav"), tg = document.querySelector(".nav-toggle");
    if (nav && nav.classList.contains("open") && tg) tg.click();
  });

  // View-only Learning Delivery Modalities portfolio: page images in a modal with zoom. No PDF is published.
  var lm = document.getElementById("ldm-modal");
  if (lm && typeof lm.showModal === "function") {
    var lpages = document.getElementById("ldm-pages");
    var lshots = Array.prototype.slice.call(lpages.querySelectorAll("img"));
    var lcount = document.getElementById("ldm-page");
    var zoom = 1;
    var setZoom = function (z) {
      zoom = Math.max(0.6, Math.min(2.4, z));
      lpages.style.setProperty("--z", zoom);
    };
    var track = function () {
      var top = lm.getBoundingClientRect().top + 90, cur = 1;
      for (var i = 0; i < lshots.length; i++) { if (lshots[i].getBoundingClientRect().top <= top + lm.clientHeight * 0.3) cur = i + 1; else break; }
      lcount.textContent = "Page " + cur + " of " + lshots.length;
    };
    document.addEventListener("click", function (e) {
      var b = e.target.closest && e.target.closest("[data-ldm]");
      if (!b) return;
      lshots.forEach(function (im) { if (im.dataset.src) { im.src = im.dataset.src; im.removeAttribute("data-src"); } });
      setZoom(1);
      lm.showModal();
      lm.scrollTop = 0;
      track();
    });
    document.getElementById("ldm-close").addEventListener("click", function () { lm.close(); });
    document.getElementById("ldm-in").addEventListener("click", function () { setZoom(zoom + 0.25); });
    document.getElementById("ldm-out").addEventListener("click", function () { setZoom(zoom - 0.25); });
    lm.addEventListener("click", function (e) { if (e.target === lm) lm.close(); });
    lm.addEventListener("scroll", function () { window.requestAnimationFrame(track); }, { passive: true });
    lm.addEventListener("contextmenu", function (e) { if (e.target.tagName === "IMG") e.preventDefault(); });
    lm.addEventListener("keydown", function (e) {
      if (e.key === "+" || e.key === "=") setZoom(zoom + 0.25);
      else if (e.key === "-") setZoom(zoom - 0.25);
    });
  }


  // Skills: highlight the section currently being read in the side panel
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
})();
