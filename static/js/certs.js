/* Awards: the three "More recognition" cards open a window with that group's certificates in the auto-scrolling row. */
(function () {
  "use strict";
  var modal = document.getElementById("cert-modal");
  var cards = document.querySelectorAll(".more-card");
  if (!modal || !cards.length || typeof modal.showModal !== "function" || !window.PortfolioMarquee) return;
  var title = document.getElementById("cm-title");
  var groups = Array.prototype.slice.call(modal.querySelectorAll(".mq-certs"));
  groups.forEach(function (g) {
    var k = g.getAttribute("data-group");
    window.PortfolioMarquee({ rootId: "certs-carousel-" + k, toggleId: "cm-toggle-" + k, prevId: "cm-prev-" + k, nextId: "cm-next-" + k });
  });
  function open(k) {
    groups.forEach(function (g) { g.hidden = g.getAttribute("data-group") !== String(k); });
    var g = modal.querySelector('.mq-certs[data-group="' + k + '"]');
    title.textContent = g ? g.getAttribute("data-heading") : "Certificates";
    if (!modal.open) modal.showModal();
  }
  Array.prototype.forEach.call(cards, function (c) {
    c.addEventListener("click", function () { open(c.getAttribute("data-certs")); });
  });
  document.getElementById("cm-close").addEventListener("click", function () { modal.close(); });
  modal.addEventListener("click", function (e) { if (e.target === modal) modal.close(); });
})();
