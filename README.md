# Leafcoin

A static concept site for verifiable agriculture: aeroponic farms, IoT telemetry, ML-assisted calibration and blockchain records. It reworks the [original Leafcoin concept](https://leafcoin.org/) as a full-width technical site. It shares local IBM Plex fonts and the dependency-free GitHub Pages approach of [Ilya Papou's CV](https://papou.work/).

Leafcoin is presented as a concept and personal R&D project. The linked controller code, sensor firmware and historical lab photographs document Home Aeroponics prototype work. The architecture and roadmap describe proposed research; implementation status beyond these materials is not established here. Besu with QBFT is being considered as a permissioned EVM option. Governance, data visibility, confidentiality and financial-integration feasibility would require evaluation.

The current canonical configuration targets the GitHub project preview. Domain, analytics-account and archive configuration are handled separately from the repository files.

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

The checker validates metadata and JSON-LD, local links and fragments, HTML IDs, assets, CSS resources, declared crawler rules, sitemap coverage and the complete concept companions. It can also verify a published copy:

```sh
python3 scripts/check_site.py --url https://pilprod.github.io/leafcoin/
```

External repository links are not fetched by the checker.

## GitHub Pages

The canonical URL used by this revision is [pilprod.github.io/leafcoin](https://pilprod.github.io/leafcoin/). The matching configuration is **Settings → Pages → Deploy from a branch → main → / (root)**. The `.nojekyll` file publishes the static files directly. GitHub Actions runs the separate validation workflow; it does not deploy the site.

Use relative asset links so the same files work both under `/leafcoin/` and at a custom domain. When moving to `leafcoin.org`, update the canonical, Open Graph and JSON-LD URLs in `index.html`, and the URLs in `robots.txt`, `sitemap.xml`, `llms.txt`, `index.md`, `llms-full.txt` and `concept.jsonld`. Configure the custom domain in GitHub Pages and the domain's DNS, then verify the published copy with `--url`. The preview configuration intentionally has no `CNAME`.

## Search and agent discovery

The sitemap lists the canonical homepage and its displayed content images. It omits section fragments and duplicate Markdown versions as separate search results. Keep `lastmod` tied to substantive content changes.

`llms.txt` is a concise resource index. `index.md` contains the complete visible concept, including architecture details, proposed ML irrigation/nutrient-solution calibration research, roadmap, prototype scope and image provenance. `llms-full.txt` is a convenience copy of that same Markdown. `concept.jsonld` relates the proposed concept and calibration research, creator, historical prototype, public repositories, AI concept illustrations and lab photographs. Keep the Markdown copy synchronized with the visible site and the graph synchronized with the displayed images and linked repositories.

During the GitHub project preview, `/leafcoin/robots.txt` is a published companion; effective crawler rules are read at `https://pilprod.github.io/robots.txt`, outside this repository's path. On a custom domain, this repository's `robots.txt` is served at the origin root. Submit the canonical sitemap in the verified Search Console property after publication and use URL Inspection for live crawl/index status. No verification token or account setup is implied by these files.

These resources aid discovery and interpretation; indexing, rich results and AI citations are determined by the services. References: [Google sitemap guidance](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap), [image sitemaps](https://developers.google.com/search/docs/crawling-indexing/sitemaps/image-sitemaps), [structured-data guidelines](https://developers.google.com/search/docs/appearance/structured-data/sd-policies), [OpenAI crawler controls](https://developers.openai.com/api/docs/bots) and the [llms.txt proposal](https://llmstxt.org/).

## Sources and scope

- [Leafcoin's original concept](https://leafcoin.org/): agricultural ecosystem and proposed blockchain direction.
- [Home Aeroponics project and lab photographs](https://papou.work/portfolio.html#home): prototype context and source photographs.
- [Controller code](https://github.com/pilprod/aeroponics-iot-control) and [sensor firmware](https://github.com/pilprod/aeroponics-sensor-firmware): the linked personal R&D repositories.

Keep proposed capabilities distinct from prototype evidence when editing the site. No project-wide license is declared here; bundled assets retain their accompanying license files.

The home-lab hero and four section illustrations are AI-generated concept visuals, distinct from prototype evidence. Their [prompt and provenance record](docs/generated-illustrations.md) explains their proposed subjects. A separate carousel contains nine historical lab images, with the electronics workbench first and root chamber last. Seven images carry the source portfolio's AI/privacy-retouching notes; the wiring diagram and root-chamber photograph have not been redrawn. The site owner's supplied SVG logo, favicon and touch icon are preserved as brand assets.

The footer links to the designated [original-version archive](https://old.leafcoin.org/). Its host and content configuration are handled separately; the link alone does not establish availability. The archive URL is not included in this site's sitemap.

The site's Google Analytics consent behaviour and account configuration notes are documented in [docs/analytics.md](docs/analytics.md). Verify account settings and the published behaviour independently of the static checks.
