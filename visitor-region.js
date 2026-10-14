// Share one country lookup between language suggestions and analytics.
// The full Cloudflare trace is discarded and is never stored or sent to Google.
(() => {
  let lookup;
  window.leafcoinVisitorCountry = () => {
    if (lookup) return lookup;
    lookup = (async () => {
      if (location.origin !== "https://leafcoin.org" || typeof fetch !== "function") return null;
      const controller = new AbortController();
      const timer = setTimeout(() => controller.abort(), 2000);
      try {
        const response = await fetch("/cdn-cgi/trace", {
          cache: "no-store", credentials: "omit", redirect: "error", signal: controller.signal
        });
        if (!response.ok || !response.headers.get("content-type")?.startsWith("text/plain")) return null;
        const text = await response.text();
        const countries = text.length <= 4096 ? [...text.matchAll(/^loc=([A-Z]{2})\r?$/gm)] : [];
        return countries.length === 1 ? countries[0][1] : null;
      } catch {
        return null;
      } finally {
        clearTimeout(timer);
      }
    })();
    return lookup;
  };
})();
