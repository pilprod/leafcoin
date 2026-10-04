# Analytics setup

The website uses the existing **Leafcoin** GA4 property **556039415** in account **407006587**, web stream **15846666315**, measurement ID **G-SV3XY3N6NE**. These are public installation identifiers, not API credentials. No new Google property is required.

`analytics.js` uses the same-origin Cloudflare `/cdn-cgi/trace` country response on `https://leafcoin.org`. Visitors in the 27 EU member countries and unknown regions use [basic consent mode](https://developers.google.com/tag-platform/security/concepts/consent-mode#basic-vs-advanced): no Google script, event queue or measurement request is created before **Allow Google Analytics**. Verified non-EU visitors start automatically unless they have a valid saved refusal. The country is not persisted or sent to Google; only the `loc` field is examined. Failed/redirected/non-text/invalid responses and a two-second timeout require consent. Language and timezone are never used as country evidence.

The footer settings button lets any visitor decline or allow analytics. Both approval and refusal expire after 180 days; blocked storage preserves the current decision and uses session storage when available. The two public origins have separate browser storage. The GitHub Pages preview remains opt-in because it does not provide Cloudflare country evidence. Keep Google Tag Gateway automatic insertion disabled to preserve the EU/unknown-region gate.

Only `https://leafcoin.org/` and `https://pilprod.github.io/leafcoin/` are measured. Their `index.html` routes are normalized to those URLs. All other routes and local previews are excluded. The controller sends one explicit `page_view` per activated visit, strips URL query strings and fragments, and reduces referrers to their origin. It does not send contact data, user IDs, custom click events, form content or filenames. Google may also generate its normal session and engagement events after consent; this is not anonymous analytics.

Advertising consent remains denied. Google signals and advertising personalization are disabled in the tag configuration. In the existing GA4 account, **Enhanced measurement was switched OFF and the saved state was verified**. Google signals and user-provided data collection were already disabled and remain disabled. Enhanced measurement must remain OFF to prevent automatic scroll, outbound-click and history events from bypassing the reviewed fields.

Existing account retention settings were preserved: event data retention **2 months**, user data retention **14 months**, and **Reset user data on new activity ON**. The 180-day browser consent choice is separate from these server-side retention settings.

Collection from the published site was verified after explicit Google Analytics approval in Chrome. GA4 Realtime displayed the exact new page title, **Leafcoin — A concept for verifiable agriculture**, with **11 views** at verification time. This confirms collection for the tested consented visits; it is a verification snapshot, not a measure of complete traffic coverage.

Withdrawal disables the property, deletes visible first-party `_ga` cookies at the current host and supported paths, and reloads to unload the Google tag. If a stale saved approval cannot be overwritten or overridden in session storage, the controller disables Google for the current page without reloading into that approval. Choices and withdrawals are synchronized across tabs on the same origin.

Withdrawal stops future collection from that browser; it does not delete previously collected data from Google Analytics.

Cloudflare Web Analytics is configured separately through Cloudflare. All four web A records, four AAAA records and the `www` record are proxied. The automatic setup, **Enable, excluding visitor data in the EU**, was saved and its persisted state verified. [Cloudflare's automatic setup](https://developers.cloudflare.com/web-analytics/get-started/) injects its beacon into proxied site responses and excludes EU visitors in this mode.

Automatic injection was verified in the full HTML returned by Cloudflare to a browser user agent: it contained a module beacon with subresource integrity and the public token `0f85ce25778449cf9ec15ab46a31f3e9`. No manual Cloudflare script is present in this repository or installed for the GitHub Pages preview.

The Cloudflare site tag is not its public beacon token. Do not add a guessed token or a manual beacon alongside automatic injection; only one installation should run on each public page. The separate Cloudflare beacon does not use analytics cookies and does not wait for Google Analytics consent. The site's **Allow Google Analytics** and **Decline Google Analytics** buttons control Google alone.

Search Console is separate from analytics. Ownership of the Leafcoin domain property is verified through DNS, and the property is linked to the existing Leafcoin GA4 property. The submitted canonical sitemap was processed with **Success**, confirmed in the current Search Console interface. Live URL Inspection confirmed that Google can access the published page and that it is eligible for indexing. The **Request indexing** action completed with an **Indexing requested** confirmation. Sitemap processing and an accepted request do not establish that every page or image has been indexed; use indexing reports to check those outcomes.

Run the dependency-free checks from the repository root:

```sh
node scripts/check_analytics.cjs
```

All 27 dependency-free checks pass. They exercise fresh visits, refusal, approval, exact origins and routes, URL redaction, storage failures, expiry, withdrawal, duplicate execution, cross-tab changes and the published HTML controls without making network requests. After future changes, verify one Cloudflare beacon on a visit outside the excluded traffic, no Google requests before approval for EU/unknown regions, automatic collection for verified non-EU visitors, no collection after refusal in any country, one explicit pageview per activated visit, and dashboard receipt. Keep the browser checks separate from static source validation.

On October 4, 2026, Cloudflare Google Tag Gateway **Set up tag** was switched off and the saved configuration was reopened to verify it. The gateway setting, measurement ID `G-SV3XY3N6NE` and `/o80a` path were retained. Only the site controller may install Google; Cloudflare Web Analytics remains separate. The regional controller passed 27 dependency-free checks before release, including an unsaved refusal made while country lookup is pending.
