# Leafcoin

A static concept site for verifiable agriculture: aeroponic farms, IoT telemetry, AI assistance and blockchain records. It reworks the [original Leafcoin concept](https://leafcoin.org/) using the typography and lightweight approach of [Ilya Papou's CV](https://papou.work/).

The proposed ecosystem is a concept. The linked controller code, sensor firmware and historical lab photographs document a separate Home Aeroponics personal R&D prototype. They do not establish that the Leafcoin ecosystem, a token, regulatory integrations or a production ledger have launched. GoQuorum is a candidate from the original concept; the final ledger has not been selected.

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

The checker validates metadata and JSON-LD, local links and fragments, HTML IDs, assets, CSS resources, crawler access and sitemap coverage. It can also verify a published copy:

```sh
python3 scripts/check_site.py --url https://pilprod.github.io/leafcoin/
```

External repository links are not fetched by the checker.

## GitHub Pages

The initial public URL is [pilprod.github.io/leafcoin](https://pilprod.github.io/leafcoin/). Configure **Settings → Pages → Deploy from a branch → main → / (root)**. The `.nojekyll` file publishes the static files directly. GitHub Actions runs the separate validation workflow; it does not deploy the site.

Use relative asset links so the same files work both under `/leafcoin/` and at a custom domain. When moving to `leafcoin.org`, update the canonical, Open Graph and JSON-LD URLs in `index.html`, and the URLs in `robots.txt`, `sitemap.xml` and `llms.txt`. Configure the custom domain in GitHub Pages and the domain's DNS, then verify the published copy with `--url`. The preview configuration intentionally has no `CNAME`.

## Sources and scope

- [Leafcoin's original concept](https://leafcoin.org/): agricultural ecosystem and proposed blockchain direction.
- [Home Aeroponics project and lab photographs](https://papou.work/portfolio.html#home): prototype context and source photographs.
- [Controller code](https://github.com/pilprod/aeroponics-iot-control) and [sensor firmware](https://github.com/pilprod/aeroponics-sensor-firmware): the linked personal R&D repositories.

Keep proposed capabilities distinct from prototype evidence when editing the site. No project-wide license is declared here; bundled assets retain their accompanying license files.
