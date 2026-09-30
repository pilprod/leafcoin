# Analytics setup

The website uses the existing **Leafcoin** GA4 property **556039415** in account **407006587**, web stream **15846666315**, measurement ID **G-SV3XY3N6NE**. These are public installation identifiers, not API credentials. No new Google property is required.

`analytics.js` implements [basic consent mode](https://developers.google.com/tag-platform/security/concepts/consent-mode#basic-vs-advanced): no Google script, event queue or measurement request is created before a visitor chooses **Allow Google Analytics**. The footer settings button lets visitors change that choice. Both approval and refusal expire after 180 days; blocked storage preserves the current decision and uses session storage when available. The two public origins have separate browser storage.

Only `https://leafcoin.org/` and `https://pilprod.github.io/leafcoin/` are measured. Their `index.html` routes are normalized to those URLs. All other routes and local previews are excluded. The controller sends one explicit `page_view` per activated visit, strips URL query strings and fragments, and reduces referrers to their origin. It does not send contact data, user IDs, custom click events, form content or filenames. Google may also generate its normal session and engagement events after consent; this is not anonymous analytics.

Advertising consent remains denied. Google signals and advertising personalization are disabled in the tag configuration. In the existing GA4 account, **Enhanced measurement was switched OFF and the saved state was verified**. Google signals and user-provided data collection were already disabled and remain disabled. Enhanced measurement must remain OFF to prevent automatic scroll, outbound-click and history events from bypassing the reviewed fields.

Existing account retention settings were preserved: event data retention **2 months**, user data retention **14 months**, and **Reset user data on new activity ON**. The 180-day browser consent choice is separate from these server-side retention settings. Code and account configuration checks do not establish that the new published site has delivered data; collection still requires verification after publication.

Withdrawal disables the property, deletes visible first-party `_ga` cookies at the current host and supported paths, and reloads to unload the Google tag. If a stale saved approval cannot be overwritten or overridden in session storage, the controller disables Google for the current page without reloading into that approval. Choices and withdrawals are synchronized across tabs on the same origin.

Withdrawal stops future collection from that browser; it does not delete previously collected data from Google Analytics.

Cloudflare Web Analytics is configured separately through Cloudflare. The existing automatic setup, **Enable, excluding visitor data in the EU**, is configured. [Cloudflare's automatic setup](https://developers.cloudflare.com/web-analytics/get-started/) injects its beacon into proxied site responses and excludes EU visitors in this mode. Beacon installation and delivery on the new published site still require a live check. No manual Cloudflare beacon has been added for the GitHub Pages preview.

The Cloudflare site tag is not its public beacon token. Do not add a guessed token or a manual beacon alongside automatic injection; only one installation should run on each public page. The Google consent controls do not control the separate Cloudflare beacon, which does not use analytics cookies.

Search Console is separate from analytics. The current Google account has delegated ownership, and an additional manual DNS TXT verification record has been added. Direct ownership verification is pending. Do not mark the Search Console migration complete until ownership verification and the canonical sitemap submission are confirmed.

Run the dependency-free checks from the repository root:

```sh
node scripts/check_analytics.cjs
```

The checks exercise fresh visits, refusal, approval, exact origins and routes, URL redaction, storage failures, expiry, withdrawal, duplicate execution and cross-tab changes without making network requests. After publication, verify one Cloudflare beacon, no Google requests before approval, one explicit Google pageview after approval, and dashboard receipt. A tag installed in source does not establish that data was received.
