// Enhance the mobile navigation without hiding links when JavaScript is unavailable.
(() => {
  const toolbar = document.querySelector(".site-toolbar");
  const toggle = toolbar?.querySelector(".menu-toggle");
  const menu = toolbar?.querySelector("#site-menu");
  const label = toggle?.querySelector(".menu-toggle-label");
  if (!toolbar || !toggle || !menu || !label) return;

  const mobile = window.matchMedia("(max-width: 1000px)");
  function setOpen(open) {
    toolbar.classList.toggle("is-menu-open", open);
    toggle.setAttribute("aria-expanded", String(open));
    toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    label.textContent = open ? "Close" : "Menu";
  }
  function isOpen() {
    return toggle.getAttribute("aria-expanded") === "true";
  }

  toggle.addEventListener("click", () => setOpen(!isOpen()));
  menu.addEventListener("click", event => {
    if (event.target.closest("a")) setOpen(false);
  });
  document.addEventListener("click", event => {
    if (isOpen() && !toolbar.contains(event.target)) setOpen(false);
  });
  document.addEventListener("keydown", event => {
    if (event.key === "Escape" && isOpen()) {
      setOpen(false);
      toggle.focus();
    }
  });
  mobile.addEventListener("change", () => setOpen(false));
  toolbar.setAttribute("data-menu-ready", "true");
})();

// Include the full architecture when printing, then restore the reader's view.
let printDisclosureState;
window.addEventListener("beforeprint", () => {
  if (printDisclosureState) return;
  printDisclosureState = [...document.querySelectorAll("details")]
    .map(detail => ({ detail, open: detail.open }));
  printDisclosureState.forEach(({ detail }) => { detail.open = true; });
});
window.addEventListener("afterprint", () => {
  printDisclosureState?.forEach(({ detail, open }) => { detail.open = open; });
  printDisclosureState = undefined;
});
