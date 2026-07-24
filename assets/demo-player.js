(function () {
  document.querySelectorAll("[data-demo-video]").forEach(function (slot) {
    var video = slot.querySelector("video");
    var fallback = slot.querySelector("[data-demo-fallback]");
    if (!video || !fallback) return;

    function showFallback() {
      video.setAttribute("hidden", "");
      video.removeAttribute("src");
      fallback.removeAttribute("hidden");
      slot.classList.remove("has-video");
    }

    video.addEventListener("error", showFallback);

    var src = video.getAttribute("src");
    if (!src) {
      showFallback();
      return;
    }

    fetch(src, { method: "HEAD" })
      .then(function (res) {
        if (!res.ok) showFallback();
      })
      .catch(showFallback);
  });
})();
