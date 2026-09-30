#!/usr/bin/env python3
"""Validate the static site locally, or fetch its published files with --url."""

import argparse
import datetime as dt
from html.parser import HTMLParser
import json
from pathlib import Path, PurePosixPath
import re
import sys
from urllib.parse import quote, unquote, urljoin, urlsplit
from urllib.request import Request, urlopen
from urllib.robotparser import RobotFileParser
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRECTORIES = {".git", ".github", "scripts", "work", "__pycache__"}
SITEMAP_NS = "http://www.sitemaps.org/schemas/sitemap/0.9"


def require(condition, message):
    if not condition:
        raise ValueError(message)


class Page(HTMLParser):
    def __init__(self, source, path):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.lang = ""
        self.title = []
        self.title_count = 0
        self.meta = {}
        self.canonicals = []
        self.ids = set()
        self.references = []
        self.idrefs = []
        self.jsonld = []
        self._title = False
        self._json = None
        self.feed(source)
        self.close()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "html":
            self.lang = attrs.get("lang", "")
        if tag == "title":
            self._title = True
            self.title_count += 1
        if "id" in attrs:
            identifier = attrs["id"]
            require(identifier and identifier not in self.ids,
                    f"{self.path}: empty or duplicate ID {identifier!r}")
            self.ids.add(identifier)
        for attribute in ("aria-labelledby", "aria-describedby", "aria-controls", "for"):
            if attrs.get(attribute):
                self.idrefs.extend(attrs[attribute].split())
        if tag == "meta":
            key = attrs.get("name", attrs.get("property", "")).lower()
            if key:
                self.meta.setdefault(key, []).append(attrs.get("content", ""))
        if tag == "link" and "canonical" in attrs.get("rel", "").split():
            self.canonicals.append(attrs.get("href", ""))
        for attribute in ("href", "src", "poster"):
            if attrs.get(attribute):
                self.references.append(attrs[attribute])
        if attrs.get("srcset"):
            # Inline data URLs may contain commas; they are not local resources.
            if not attrs["srcset"].lstrip().startswith("data:"):
                self.references.extend(item.strip().split()[0]
                                       for item in attrs["srcset"].split(",") if item.strip())
        if tag == "img":
            require("alt" in attrs, f"{self.path}: image has no alt attribute")
        if tag == "script" and attrs.get("type", "").lower() == "application/ld+json":
            self._json = []

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)

    def handle_endtag(self, tag):
        if tag == "title":
            self._title = False
        if tag == "script" and self._json is not None:
            try:
                self.jsonld.append(json.loads("".join(self._json)))
            except json.JSONDecodeError as error:
                raise ValueError(f"{self.path}: invalid JSON-LD: {error}") from error
            self._json = None

    def handle_data(self, value):
        if self._title:
            self.title.append(value)
        if self._json is not None:
            self._json.append(value)

    def metadata(self, name):
        values = self.meta.get(name, [])
        require(len(values) == 1 and values[0].strip(),
                f"{self.path}: expected one nonempty {name} metadata value")
        return values[0]


class Site:
    def __init__(self, published_url=None):
        self.published_url = published_url
        self.resources = {}
        self.pages = {}
        self.canonical = ""

    def resource(self, path):
        path = path or "index.html"
        if path not in self.resources:
            local = (ROOT / path).resolve()
            require(local.is_relative_to(ROOT), f"Resource escapes the site root: {path}")
            require(local.is_file(), f"Missing local resource: {path}")
            if self.published_url:
                url = urljoin(self.published_url, "" if path == "index.html" else quote(path))
                request = Request(url, headers={"User-Agent": "Leafcoin-site-check/1.0"})
                with urlopen(request, timeout=20) as response:
                    self.resources[path] = response.read()
            else:
                self.resources[path] = local.read_bytes()
            require(self.resources[path], f"Empty resource: {path}")
        return self.resources[path]

    def page(self, path):
        path = path or "index.html"
        if path not in self.pages:
            self.pages[path] = Page(self.resource(path).decode("utf-8"), path)
        return self.pages[path]

    def local_target(self, reference, source="index.html"):
        """Map same-site URLs under the canonical base to repository paths."""
        parsed_reference = urlsplit(reference)
        if parsed_reference.scheme and parsed_reference.scheme not in ("http", "https"):
            return None
        source_url = urljoin(self.canonical, "" if source == "index.html" else quote(source))
        target = urlsplit(urljoin(source_url, reference))
        base = urlsplit(self.canonical)
        if target.netloc != base.netloc:
            return None
        target_path, base_path = unquote(target.path), unquote(base.path)
        if target_path.rstrip("/") == base_path.rstrip("/"):
            path = "index.html"
        elif target_path.startswith(base_path):
            path = target_path[len(base_path):]
            if path.endswith("/"):
                path += "index.html"
        else:
            # Explicit absolute links can lead elsewhere on the same host.
            if parsed_reference.netloc:
                return None
            raise ValueError(f"{source}: {reference!r} leaves the site's base path {base_path}")
        return path, unquote(target.fragment)

    def check_reference(self, reference, source="index.html"):
        target = self.local_target(reference, source)
        if target is None:
            return
        path, fragment = target
        self.resource(path)
        if fragment and PurePosixPath(path).suffix.lower() in (".html", ".htm"):
            require(fragment in self.page(path).ids,
                    f"{source}: missing fragment {reference!r}")


def jsonld_nodes(block):
    if isinstance(block, list):
        return [node for item in block for node in jsonld_nodes(item)]
    require(isinstance(block, dict), "JSON-LD must be an object or array of objects")
    require(block.get("@context") in ("https://schema.org", "https://schema.org/", "http://schema.org"),
            "JSON-LD must use the schema.org context")
    nodes = block.get("@graph", [block])
    require(isinstance(nodes, list) and nodes, "JSON-LD graph is empty or invalid")
    for node in nodes:
        require(isinstance(node, dict) and node.get("@type"), "JSON-LD entity has no type")
    return nodes


def check_page(site, page):
    require(page.lang, f"{page.path}: missing HTML language")
    require(page.title_count == 1 and "".join(page.title).strip(),
            f"{page.path}: expected one nonempty title")
    require(len(page.canonicals) == 1, f"{page.path}: expected one canonical URL")
    canonical = page.canonicals[0]
    require(urlsplit(canonical).scheme == "https" and urlsplit(canonical).netloc
            and not urlsplit(canonical).fragment,
            f"{page.path}: canonical must be an absolute HTTPS URL without a fragment")
    for name in ("description", "og:title", "og:description", "og:type", "og:url",
                 "twitter:card", "twitter:title", "twitter:description"):
        page.metadata(name)
    require(page.metadata("og:url") == canonical, f"{page.path}: Open Graph URL differs from canonical")
    for name in ("robots", "googlebot", "bingbot"):
        for value in page.meta.get(name, []):
            require(not {"noindex", "nofollow", "none"} & set(re.split(r"[\s,]+", value.lower())),
                    f"{page.path}: {name} blocks discovery")
    require(page.jsonld, f"{page.path}: missing JSON-LD")
    nodes = [node for block in page.jsonld for node in jsonld_nodes(block)]
    require(any(node.get("url") == canonical for node in nodes),
            f"{page.path}: no JSON-LD entity uses the canonical URL")
    for reference in page.references:
        site.check_reference(reference, page.path)
    images = []
    for name in ("og:image", "twitter:image"):
        if name in page.meta:
            image = page.metadata(name)
            page.metadata(name + ":alt")
            site.check_reference(image, page.path)
            images.append(urljoin(canonical, image))
        elif name + ":alt" in page.meta:
            raise ValueError(f"{page.path}: {name}:alt has no corresponding image")
    require(len(set(images)) <= 1, f"{page.path}: Open Graph and Twitter images differ")
    for identifier in page.idrefs:
        require(identifier in page.ids, f"{page.path}: missing referenced ID {identifier!r}")


def check_css(site):
    checked = set()
    while True:
        pending = [path for path in site.resources if path.endswith(".css") and path not in checked]
        if not pending:
            return
        for path in pending:
            checked.add(path)
            css = re.sub(r"/\*.*?\*/", "", site.resource(path).decode("utf-8"), flags=re.S)
            references = re.findall(r"url\(\s*['\"]?([^)'\"]+)['\"]?\s*\)", css)
            references += re.findall(r"@import\s+['\"]([^'\"]+)['\"]", css)
            for reference in references:
                site.check_reference(reference.strip(), path)


def check_discovery(site):
    robots = RobotFileParser()
    robots.parse(site.resource("robots.txt").decode("utf-8").splitlines())
    require(urljoin(site.canonical, "sitemap.xml") in (robots.site_maps() or []),
            "robots.txt sitemap URL differs from the canonical base")
    for bot in ("Googlebot", "bingbot", "OAI-SearchBot"):
        require(robots.can_fetch(bot, site.canonical), f"robots.txt blocks {bot}")
    sitemap = ET.fromstring(site.resource("sitemap.xml"))
    require(sitemap.tag == f"{{{SITEMAP_NS}}}urlset", "Invalid sitemap namespace or root")
    locations = []
    for entry in sitemap.findall(f"{{{SITEMAP_NS}}}url"):
        location = entry.findtext(f"{{{SITEMAP_NS}}}loc", "")
        parsed = urlsplit(location)
        require(parsed.scheme == "https" and parsed.netloc and not parsed.fragment,
                f"Invalid sitemap URL: {location!r}")
        require(site.local_target(location) is not None, f"Sitemap URL is outside this site: {location}")
        site.check_reference(location)
        locations.append(location)
        modified = entry.findtext(f"{{{SITEMAP_NS}}}lastmod")
        if modified:
            date = dt.datetime.fromisoformat(modified.replace("Z", "+00:00")).date()
            require(date <= dt.datetime.now(dt.timezone.utc).date(), f"Future sitemap date: {modified}")
    require(locations and len(locations) == len(set(locations)), "Sitemap is empty or has duplicate URLs")
    for page in site.pages.values():
        require(page.canonicals[0] in locations, f"{page.path}: canonical missing from sitemap")
    llms = site.resource("llms.txt").decode("utf-8")
    require(llms.startswith("# ") and site.canonical in llms, "llms.txt needs a title and canonical site URL")
    for reference in re.findall(r"\]\(([^)]+)\)", llms):
        site.check_reference(reference)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", help="Published base URL, including its trailing slash")
    args = parser.parse_args()
    if args.url:
        parsed = urlsplit(args.url)
        require(parsed.scheme in ("http", "https") and parsed.netloc
                and args.url.endswith("/") and not parsed.query and not parsed.fragment,
                "--url must be an HTTP(S) base URL ending with /, without a query or fragment")
    site = Site(args.url)
    homepage = site.page("index.html")
    require(len(homepage.canonicals) == 1, "index.html: expected one canonical URL")
    site.canonical = homepage.canonicals[0]
    require(site.canonical.endswith("/"), "Homepage canonical must end with /")
    for path in sorted(ROOT.rglob("*.html")):
        relative = path.relative_to(ROOT)
        if not any(part in SKIP_DIRECTORIES or part.startswith(".") for part in relative.parts):
            check_page(site, site.page(relative.as_posix()))
    check_css(site)
    check_discovery(site)
    require((ROOT / ".nojekyll").is_file(), "Missing .nojekyll for static GitHub Pages publication")
    mode = f"published site at {args.url}" if args.url else "local site"
    print(f"PASS: {mode} — {len(site.pages)} page(s), {len(site.resources)} resources, "
          "metadata, JSON-LD, IDs, links, assets, robots, sitemap and llms.txt")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, ET.ParseError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        sys.exit(1)
