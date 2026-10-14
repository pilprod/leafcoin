(() => {
  "use strict";
  const key = "leafcoin.language.v1";
  const switcher = document.querySelector("[data-language-switch]");
  if (!switcher) return;
  const current = document.documentElement.lang === "es" ? "es" : "en";
  const other = current === "es" ? "en" : "es";
  function readChoice() {
    for (const type of ["sessionStorage", "localStorage"]) {
      try {
        const value = window[type].getItem(key);
        if (value === "en" || value === "es") return value;
      } catch { /* Language selection still works when storage is blocked. */ }
    }
    return null;
  }
  function saveChoice(value) {
    let saved = false;
    try { localStorage.setItem(key, value); saved = true; } catch { /* Session fallback. */ }
    try {
      if (saved) sessionStorage.removeItem(key);
      else sessionStorage.setItem(key, value);
    } catch { /* Navigation remains available without persistent storage. */ }
  }
  function navigate() {
    const target = new URL(switcher.href, location.href);
    if (target.origin !== location.origin) return;
    target.search = location.search;
    target.hash = location.hash;
    window.__leafcoinLanguageRedirect = true;
    location.replace(target.href);
  }
  switcher.addEventListener("click", event => {
    saveChoice(other);
    if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
    event.preventDefault();
    navigate();
  });
  // An explicitly opened Spanish URL stays Spanish. A saved choice overrides
  // automatic language detection; geographic location never triggers a redirect.
  if (current === "es") return;
  const choice = readChoice();
  const primaryLanguage = navigator.languages?.[0] || navigator.language || "";
  if (choice === "es" || (!choice && /^es(?:-|$)/i.test(primaryLanguage))) {
    navigate();
    return;
  }
  if (choice || typeof window.leafcoinVisitorCountry !== "function") return;
  const spanishRegions = new Set("AR BO CL CO CR CU DO EC ES GQ GT HN MX NI PA PE PR PY SV UY VE".split(" "));
  window.leafcoinVisitorCountry().then(country => {
    if (!spanishRegions.has(country) || readChoice()) return;
    const dialog = document.createElement("dialog");
    dialog.className = "language-dialog";
    dialog.setAttribute("aria-labelledby", "language-dialog-title");
    dialog.innerHTML = '<p class="eyebrow" lang="es">Leafcoin en español</p>'
      + '<h2 id="language-dialog-title" lang="es">¿Prefieres leer en español?</h2>'
      + '<p>Spanish is available for this page. We’ll remember your choice on this device.</p>'
      + '<div class="language-dialog-actions"><button type="button" data-language-accept lang="es">Cambiar a español</button>'
      + '<button type="button" data-language-stay>Keep English</button></div>';
    document.body.appendChild(dialog);
    dialog.querySelector("[data-language-accept]").addEventListener("click", () => {
      saveChoice("es");
      dialog.close();
      navigate();
    });
    function keepEnglish() {
      saveChoice("en");
      dialog.close();
      switcher.focus({ preventScroll: true });
    }
    dialog.querySelector("[data-language-stay]").addEventListener("click", keepEnglish);
    dialog.addEventListener("cancel", event => { event.preventDefault(); keepEnglish(); });
    if (typeof dialog.showModal === "function") dialog.showModal();
    else dialog.setAttribute("open", "");
  }).catch(() => { /* An unknown country leaves the current language in place. */ });
})();
