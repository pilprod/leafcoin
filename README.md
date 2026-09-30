# Leafcoin

A static concept site for verifiable agriculture: aeroponic farms, IoT telemetry, ML-assisted calibration and blockchain records. It reworks the [original Leafcoin concept](https://old.leafcoin.org/) as a full-width technical site. It shares local IBM Plex fonts and the dependency-free GitHub Pages approach of [Ilya Papou's CV](https://papou.work/).

Leafcoin is presented as a concept and personal R&D project. The linked controller code, sensor firmware and historical lab photographs document Home Aeroponics prototype work. The architecture and roadmap describe proposed research; implementation status beyond these materials is not established here. Besu with QBFT is being considered as a permissioned EVM option. Governance, data visibility, confidentiality and financial-integration feasibility would require evaluation.

The GitHub project preview has been published and checked. This revision prepares the production canonical URL, `https://leafcoin.org/`; the main-domain switch is being configured separately. The original-version archive redirect has been verified. Local validation does not establish that the production domain is live.

## Local preview

There is no build step or package installation. From the repository root:

```sh
python3 -m http.server 8000
```

Open `http://localhost:8000/`. The site uses local IBM Plex fonts and follows the device's light or dark appearance automatically.

Run the dependency-free checks before publishing:

```sh
python3 scripts/check_site.py
```

The checker validates metadata and JSON-LD, local links and fragments, HTML IDs, assets, CSS resources, declared crawler rules, sitemap coverage, the complete concept companions and the canonical hostname against `CNAME` when present. It can also verify a published copy:

```sh
python3 scripts/check_site.py --url https://leafcoin.org/
```

External repository links are not fetched by the checker.

## GitHub Pages

The canonical URL used by this revision is [leafcoin.org](https://leafcoin.org/). The matching configuration is **Settings → Pages → Deploy from a branch → main → / (root)**. The `.nojekyll` file publishes the static files directly. GitHub Actions runs the separate validation workflow; it does not deploy the site. The previously checked project preview is [pilprod.github.io/leafcoin](https://pilprod.github.io/leafcoin/).

Relative asset links work both under `/leafcoin/` and at the custom domain. `CNAME` contains `leafcoin.org`; the canonical, social-image and JSON-LD URLs in `index.html` and the discovery companions use that production origin. Configure the matching custom domain in GitHub Pages and the domain's DNS, then verify HTTPS, redirects and the published copy with `--url` after deployment. Keep these URLs and `CNAME` synchronized when changing the public origin.

## Search and agent discovery

The sitemap lists the canonical homepage and its displayed content images. It omits section fragments and duplicate Markdown versions as separate search results. Keep `lastmod` tied to substantive content changes.

`llms.txt` is a concise resource index. `index.md` contains the complete visible concept, including architecture details, proposed ML irrigation/nutrient-solution calibration research, roadmap, prototype scope and image provenance. `llms-full.txt` is a convenience copy of that same Markdown. `concept.jsonld` relates the proposed concept and calibration research, creator, historical prototype, public repositories, AI concept illustrations and lab photographs. Keep the Markdown copy synchronized with the visible site and the graph synchronized with the displayed images and linked repositories.

After the domain switch, this repository's `robots.txt` will be served at the `leafcoin.org` origin root. During the GitHub project preview, `/leafcoin/robots.txt` is only a companion; effective crawler rules are read at `https://pilprod.github.io/robots.txt`, outside this repository's path. Submit the canonical sitemap in the verified Search Console property after production publication and use URL Inspection for live crawl/index status. No verification token or account setup is implied by these files.

These resources aid discovery and interpretation; indexing, rich results and AI citations are determined by the services. References: [Google sitemap guidance](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap), [image sitemaps](https://developers.google.com/search/docs/crawling-indexing/sitemaps/image-sitemaps), [structured-data guidelines](https://developers.google.com/search/docs/appearance/structured-data/sd-policies), [OpenAI crawler controls](https://developers.openai.com/api/docs/bots) and the [llms.txt proposal](https://llmstxt.org/).

## Sources and scope

- [Leafcoin's original concept](https://old.leafcoin.org/): agricultural ecosystem and proposed blockchain direction, preserved through the archive redirect.
- [Home Aeroponics project and lab photographs](https://papou.work/portfolio.html#home): prototype context and source photographs.
- [Controller code](https://github.com/pilprod/aeroponics-iot-control) and [sensor firmware](https://github.com/pilprod/aeroponics-sensor-firmware): the linked personal R&D repositories.

Keep proposed capabilities distinct from prototype evidence when editing the site. No project-wide license is declared here; bundled assets retain their accompanying license files.

The home-lab hero and four section illustrations are AI-generated concept visuals, distinct from prototype evidence. Their [prompt and provenance record](docs/generated-illustrations.md) explains their proposed subjects. A separate carousel contains nine historical lab images, with the electronics workbench first and root chamber last. Seven images carry the source portfolio's AI/privacy-retouching notes; the wiring diagram and root-chamber photograph have not been redrawn. The site owner's supplied SVG logo, favicon and touch icon are preserved as brand assets.

The footer's [original-version archive](https://old.leafcoin.org/) uses a verified 302 redirect to the preserved public Gamma presentation. It is separate from this GitHub Pages site and is not included in this site's sitemap.

The site's Google Analytics consent behaviour and account configuration notes are documented in [docs/analytics.md](docs/analytics.md). Verify account settings and the published behaviour independently of the static checks.
