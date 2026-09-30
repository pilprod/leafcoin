(() => {
  "use strict";

  document.querySelectorAll("[data-lab-gallery]").forEach((gallery) => {
    const track = gallery.querySelector("[data-gallery-track]");
    const slides = Array.from(gallery.querySelectorAll("[data-gallery-slide]"));
    const controls = gallery.querySelector("[data-gallery-controls]");
    const previous = gallery.querySelector("[data-gallery-previous]");
    const next = gallery.querySelector("[data-gallery-next]");
    const counter = gallery.querySelector("[data-gallery-counter]");
    if (!track || slides.length < 2 || !controls || !previous || !next) return;

    const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
    let animationFrame = 0;
    let announceTimer = 0;

    function positions() {
      const trackLeft = track.getBoundingClientRect().left + track.clientLeft;
      const maximum = Math.max(0, track.scrollWidth - track.clientWidth);
      return slides.map((slide) => Math.min(maximum,
        Math.max(0, slide.getBoundingClientRect().left - trackLeft + track.scrollLeft - 2)));
    }

    function currentIndex() {
      const offsets = positions();
      let closest = 0;
      offsets.forEach((offset, index) => {
        if (Math.abs(offset - track.scrollLeft) < Math.abs(offsets[closest] - track.scrollLeft)) {
          closest = index;
        }
      });
      return closest;
    }

    function updateControls() {
      const index = currentIndex();
      previous.disabled = index === 0;
      next.disabled = index === slides.length - 1;
      return index;
    }

    function updateCounter(index) {
      if (counter) counter.textContent = `${index + 1} / ${slides.length}`;
    }

    function scrollToSlide(index) {
      const destination = Math.max(0, Math.min(slides.length - 1, index));
      track.scrollTo({
        left: positions()[destination],
        behavior: reducedMotion.matches ? "auto" : "smooth",
      });
    }

    previous.addEventListener("click", () => scrollToSlide(currentIndex() - 1));
    next.addEventListener("click", () => scrollToSlide(currentIndex() + 1));

    track.addEventListener("keydown", (event) => {
      if (event.target !== track || event.altKey || event.ctrlKey || event.metaKey) return;
      let destination;
      if (event.key === "ArrowLeft") destination = currentIndex() - 1;
      if (event.key === "ArrowRight") destination = currentIndex() + 1;
      if (event.key === "Home") destination = 0;
      if (event.key === "End") destination = slides.length - 1;
      if (destination === undefined) return;
      event.preventDefault();
      scrollToSlide(destination);
    });

    track.addEventListener("scroll", () => {
      if (!animationFrame) {
        animationFrame = requestAnimationFrame(() => {
          updateControls();
          animationFrame = 0;
        });
      }
      window.clearTimeout(announceTimer);
      announceTimer = window.setTimeout(() => updateCounter(updateControls()), 150);
    }, { passive: true });

    if (typeof ResizeObserver === "function") {
      new ResizeObserver(() => updateCounter(updateControls())).observe(track);
    }

    controls.hidden = false;
    gallery.setAttribute("data-gallery-ready", "true");
    updateCounter(updateControls());
  });
})();
