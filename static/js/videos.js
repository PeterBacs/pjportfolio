/* Project videos: the same card row as Projects. Choosing a card opens the video modal and plays it at once. */
(function () {
  "use strict";
  var m = window.PortfolioMarquee && window.PortfolioMarquee({ rootId: "videos-carousel", toggleId: "vd-toggle", prevId: "vd-prev", nextId: "vd-next" });
  if (!m) return;
  var modal = document.getElementById("video-modal");
  var video = document.getElementById("vm-video");
  if (!modal || !video || typeof modal.showModal !== "function") return;
  var title = document.getElementById("vm-title");
  var count = document.getElementById("vm-count");
  var cards = m.cards, n = cards.length, cur = 0;

  function play(i) {
    cur = ((i % n) + n) % n;
    var c = cards[cur];
    title.textContent = c.getAttribute("data-title");
    count.textContent = (cur + 1) + " / " + n;
    video.setAttribute("poster", c.getAttribute("data-poster") || "");
    video.src = c.getAttribute("data-src");
    video.currentTime = 0;
    var p = video.play();
    if (p && p.catch) p.catch(function () { /* the controls stay visible if the browser blocks autoplay */ });
  }
  function open(i) {
    m.root.classList.add("is-open");
    if (!modal.open) modal.showModal();
    play(i);
  }
  function stop() {
    video.pause();
    video.removeAttribute("src");
    video.load();
    m.root.classList.remove("is-open");
  }
  cards.forEach(function (c, i) {
    var b = c.querySelector(".mq-more");
    if (b) b.addEventListener("click", function () { open(i); });
  });
  function closeIt() { if (modal.open) modal.close(); stop(); }
  document.getElementById("vm-close").addEventListener("click", closeIt);
  document.getElementById("vm-prev").addEventListener("click", function () { play(cur - 1); });
  document.getElementById("vm-next").addEventListener("click", function () { play(cur + 1); });
  modal.addEventListener("close", stop);
  modal.addEventListener("click", function (e) { if (e.target === modal) closeIt(); });
  modal.addEventListener("contextmenu", function (e) { if (e.target === video) e.preventDefault(); });
})();
