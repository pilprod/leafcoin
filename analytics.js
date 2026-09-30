(() => {
  "use strict";

  const measurementId = "G-SV3XY3N6NE";
  const consentKey = "leafcoin.analytics-consent.v1";
  const consentLifetime = 180 * 24 * 60 * 60 * 1000;
  const disableKey = `ga-disable-${measurementId}`;
  const panel = document.getElementById("analytics-consent");
  const settings = document.getElementById("analytics-settings");
  const status = document.getElementById("analytics-status");
  const tools = document.getElementById("analytics-tools");
  const allow = document.getElementById("analytics-allow");
  const decline = document.getElementById("analytics-decline");
  if (!panel || !settings || !status || !tools || !allow || !decline) return;
  // A duplicate controller must not register another tag or pageview.
  if (window.__leafcoinAnalyticsLoaded) return;
  window.__leafcoinAnalyticsLoaded = true;

  // Only these reviewed public routes are measured. Never send the raw URL.
  const pages = new Map([
    ["https://leafcoin.org/", "https://leafcoin.org/"],
    ["https://leafcoin.org/index.html", "https://leafcoin.org/"],
    ["https://pilprod.github.io/leafcoin/", "https://pilprod.github.io/leafcoin/"],
    ["https://pilprod.github.io/leafcoin/index.html", "https://pilprod.github.io/leafcoin/"]
  ]);
  const url = new URL(window.location.href);
  const pageLocation = pages.get(url.origin + url.pathname);
  const cookiePath = url.origin === "https://pilprod.github.io" ? "/leafcoin/" : "/";
  const denied = {
    analytics_storage: "denied",
    ad_storage: "denied",
    ad_user_data: "denied",
    ad_personalization: "denied"
  };
  let active = false;
  let scriptAdded = false;
  let expiryTimer;
  window[disableKey] = true;

  function validChoice(saved) {
    return saved && ["granted", "denied"].includes(saved.value)
      && Number.isFinite(saved.expiresAt) && saved.expiresAt > Date.now()
      && saved.expiresAt <= Date.now() + consentLifetime;
  }

  function readStorage(storage) {
    try {
      const saved = JSON.parse(storage?.getItem(consentKey) || "null");
      if (validChoice(saved)) return { value: saved.value, expiresAt: saved.expiresAt };
      storage?.removeItem(consentKey);
    } catch { /* Blocked or malformed storage never grants consent. */ }
    return null;
  }

  function readChoice(skipSession = false) {
    // A session fallback overrides an unwritable permanent grant on reload.
    if (!skipSession) {
      try {
        const saved = readStorage(window.sessionStorage);
        if (saved) return { choice: saved, persisted: false };
      } catch { /* Access to the storage object itself may be blocked. */ }
    }
    try {
      const saved = readStorage(window.localStorage);
      if (saved) return { choice: saved, persisted: true };
    } catch { /* Analytics stays off until a choice is made. */ }
    return { choice: null, persisted: true };
  }

  let restored = readChoice();
  let choice = restored.choice;
  let choiceSaved = restored.persisted;

  function showPanel(show, restoreFocus = false) {
    panel.hidden = !show;
    settings.setAttribute("aria-expanded", String(show));
    if (restoreFocus) settings.focus({ preventScroll: true });
  }

  function render() {
    tools.hidden = false;
    status.textContent = !pageLocation ? "Analytics is disabled in this preview."
      : choice?.value === "granted" ? choiceSaved ? "Google Analytics is on."
        : "Google Analytics is on for this visit. Your browser could not save this choice."
      : choiceSaved ? "Google Analytics is off."
        : "Google Analytics is off for this visit. Your browser could not save this choice.";
    showPanel(Boolean(pageLocation) && !choice);
  }

  function safeReferrer() {
    try {
      const referrer = new URL(document.referrer);
      return ["https:", "http:"].includes(referrer.protocol) ? referrer.origin + "/" : "";
    } catch { return ""; }
  }

  function startAnalytics() {
    if (!pageLocation || active || choice?.value !== "granted" || choice.expiresAt <= Date.now()) return;
    active = true;
    window[disableKey] = false;
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    // Basic consent mode: neither the queue nor the Google script exists before opt-in.
    window.gtag("consent", "default", denied);
    window.gtag("consent", "update", { ...denied, analytics_storage: "granted" });
    window.gtag("set", "ads_data_redaction", true);
    window.gtag("set", "url_passthrough", false);
    window.gtag("js", new Date());
    window.gtag("config", measurementId, {
      allow_google_signals: false,
      allow_ad_personalization_signals: false,
      send_page_view: false,
      cookie_domain: window.location.hostname,
      cookie_path: cookiePath,
      cookie_expires: consentLifetime / 1000,
      cookie_update: false,
      cookie_flags: "SameSite=Lax;Secure",
      page_location: pageLocation,
      page_referrer: safeReferrer(),
      page_title: "Leafcoin — A concept for verifiable agriculture"
    });
    window.gtag("event", "page_view", { send_to: measurementId });
    if (!scriptAdded) {
      scriptAdded = true;
      const script = document.createElement("script");
      script.id = "leafcoin-google-analytics";
      script.async = true;
      script.referrerPolicy = "no-referrer";
      script.src = `https://www.googletagmanager.com/gtag/js?id=${measurementId}`;
      document.head.appendChild(script);
    }
  }

  function clearAnalyticsCookies() {
    for (const item of document.cookie.split(";")) {
      const name = item.trim().split("=")[0];
      if (!/^_ga(?:_|$)/.test(name)) continue;
      for (const path of new Set(["/", cookiePath])) {
        for (const domain of ["", window.location.hostname, "." + window.location.hostname]) {
          document.cookie = `${name}=; Max-Age=0; Path=${path}; SameSite=Lax; Secure${domain ? `; Domain=${domain}` : ""}`;
        }
      }
    }
  }

  function stopAnalytics(reload = true) {
    window[disableKey] = true;
    if (active) window.gtag("consent", "update", denied);
    if (pageLocation) clearAnalyticsCookies();
    if (active) {
      active = false;
      // A reload removes the loaded tag's listeners and timers.
      if (reload) window.location.reload();
    }
  }

  function checkExpiry() {
    window.clearTimeout(expiryTimer);
    if (!choice) return;
    const remaining = choice.expiresAt - Date.now();
    if (remaining <= 0) {
      choice = null;
      try { window.localStorage.removeItem(consentKey); } catch { /* Optional storage. */ }
      try { window.sessionStorage?.removeItem(consentKey); } catch { /* Optional storage. */ }
      stopAnalytics();
      render();
    } else {
      expiryTimer = window.setTimeout(checkExpiry, Math.min(remaining, 2147483647));
    }
  }

  function decide(value) {
    choice = { value, expiresAt: Date.now() + consentLifetime };
    choiceSaved = false;
    try {
      window.localStorage.setItem(consentKey, JSON.stringify(choice));
      choiceSaved = true;
    } catch { /* Keep the current decision even if persistence is blocked. */ }
    if (choiceSaved) {
      try { window.sessionStorage?.removeItem(consentKey); } catch { /* Optional storage. */ }
    } else {
      try { window.localStorage.removeItem(consentKey); } catch { /* May be read-only. */ }
      try { window.sessionStorage?.setItem(consentKey, JSON.stringify(choice)); } catch { /* The current-page choice still applies. */ }
    }
    if (value === "granted") startAnalytics();
    // Never reload into a stale grant when neither storage can save withdrawal.
    else stopAnalytics(readChoice().choice?.value !== "granted");
    checkExpiry();
    render();
    showPanel(false, true);
  }

  allow.addEventListener("click", () => decide("granted"));
  decline.addEventListener("click", () => decide("denied"));
  settings.addEventListener("click", () => {
    showPanel(panel.hidden);
    if (!panel.hidden) decline.focus({ preventScroll: true });
  });
  panel.addEventListener("keydown", event => {
    if (event.key === "Escape" && choice) showPanel(false, true);
  });
  window.addEventListener("storage", event => {
    if (event.key !== consentKey && event.key !== null) return;
    try { window.sessionStorage?.removeItem(consentKey); } catch { /* A cross-tab withdrawal still takes effect below. */ }
    restored = readChoice(true);
    choice = restored.choice;
    choiceSaved = restored.persisted;
    if (choice?.value === "granted") startAnalytics();
    else stopAnalytics(readChoice().choice?.value !== "granted");
    checkExpiry();
    render();
  });
  document.addEventListener("visibilitychange", () => {
    if (document.visibilityState === "visible") checkExpiry();
  });

  if (choice?.value === "granted") startAnalytics();
  else if (pageLocation) clearAnalyticsCookies();
  checkExpiry();
  render();
})();
