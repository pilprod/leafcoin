#!/usr/bin/env python3
"""Regenerate the Leafcoin discovery companions from the current homepage."""

from html.parser import HTMLParser
import argparse
from pathlib import Path
from urllib.parse import urljoin
import json
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
arguments = argparse.ArgumentParser()
arguments.add_argument('--output-dir', type=Path, default=ROOT)
OUTPUT = arguments.parse_args().output_dir
OUTPUT.mkdir(parents=True, exist_ok=True)
VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}

class Node:
    def __init__(self, tag='', attrs=None, parent=None):
        self.tag, self.attrs, self.parent = tag, dict(attrs or []), parent
        self.children = []

class DOM(HTMLParser):
    def __init__(self, html):
        super().__init__(convert_charrefs=True)
        self.root = Node('document')
        self.stack = [self.root]
        self.feed(html)
    def handle_starttag(self, tag, attrs):
        node = Node(tag, attrs, self.stack[-1])
        self.stack[-1].children.append(node)
        if tag not in VOID:
            self.stack.append(node)
    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)
    def handle_endtag(self, tag):
        for index in range(len(self.stack)-1, 0, -1):
            if self.stack[index].tag == tag:
                self.stack = self.stack[:index]
                break
    def handle_data(self, data):
        self.stack[-1].children.append(data)

def descendants(node, tag=None):
    result = []
    for child in node.children:
        if isinstance(child, Node):
            if tag is None or child.tag == tag:
                result.append(child)
            result.extend(descendants(child, tag))
    return result

def classes(node):
    return set(node.attrs.get('class', '').split())

def plain(node):
    if isinstance(node, str):
        return ' '.join(node.split())
    if node.tag == 'br':
        return ' '
    return ' '.join(filter(None, (plain(child) for child in node.children)))

dom = DOM((ROOT/'index.html').read_text())
canonical = next(node.attrs['href'] for node in descendants(dom.root, 'link')
                 if 'canonical' in node.attrs.get('rel', '').split())
title = plain(descendants(dom.root, 'title')[0])
main = descendants(dom.root, 'main')[0]

def inline(node):
    if isinstance(node, str):
        return plain(node)
    if node.tag == 'br':
        return ' '
    text = ' '.join(filter(None, (inline(child) for child in node.children)))
    text = re.sub(r'\s+', ' ', text).strip()
    if node.tag == 'a' and node.attrs.get('href'):
        return f'[{text}]({urljoin(canonical, node.attrs["href"])})' if text else ''
    if node.tag in ('strong', 'b'):
        return f'**{text}**'
    return text

def render(node):
    if isinstance(node, str):
        text = plain(node)
        return text + '\n\n' if text else ''
    tag = node.tag
    if tag in ('button', 'script', 'style', 'source'):
        return ''
    if tag == 'img':
        return f'![{node.attrs.get("alt", "")} ]({urljoin(canonical, node.attrs["src"])})\n\n'.replace(' ](', '](')
    if tag in ('h1', 'h2', 'h3', 'summary'):
        depth = 4 if tag == 'summary' else int(tag[1])+1
        if tag == 'summary':
            labels = [child for child in node.children if isinstance(child, Node) and child.tag == 'span']
            if len(labels) > 1:
                return '#### ' + ' · '.join(inline(label) for label in labels) + '\n\n'
        return '#' * depth + ' ' + inline(node) + '\n\n'
    if tag == 'p':
        return inline(node) + '\n\n'
    if tag == 'figure':
        images = descendants(node, 'img')
        result = ''.join(f'![{image.attrs.get("alt", "")} ]({urljoin(canonical, image.attrs["src"])})\n\n'.replace(' ](', '](')
                         for image in images)
        caption = descendants(node, 'figcaption')
        if caption:
            if descendants(caption[0], 'h3'):
                for child in caption[0].children:
                    if isinstance(child, Node):
                        if child.tag == 'small':
                            result += '*' + inline(child) + '*\n\n'
                        else:
                            result += render(child)
            else:
                result += inline(caption[0]) + '\n\n'
        context = [link.attrs['href'] for link in descendants(node, 'a')
                   if descendants(link, 'img') and link.attrs.get('href')]
        if context:
            label = 'Photograph and source context' if context[0].startswith('http') else 'Full image'
            result += f'[{label}]({urljoin(canonical, context[0])}).\n\n'
        return result
    if tag == 'dl':
        result = ''
        for child in node.children:
            if isinstance(child, Node):
                terms, values = descendants(child, 'dt'), descendants(child, 'dd')
                if terms and values:
                    result += f'- **{inline(terms[0])}**: {inline(values[0])}\n'
        return result + '\n'
    if tag in ('ul', 'ol'):
        items = [child for child in node.children if isinstance(child, Node) and child.tag == 'li']
        if 'gallery-track' in classes(node):
            return '### Historical lab images\n\n' + ''.join(render(figure) for item in items
                                                               for figure in descendants(item, 'figure'))
        if 'roadmap' in classes(node):
            result = ''
            for index, item in enumerate(items, 1):
                heading = descendants(item, 'h3')[0]
                result += f'#### {index:02d} — {inline(heading)}\n\n'
                result += ''.join(render(p) for p in descendants(item, 'p'))
            return result
        if 'data-flow' in classes(node):
            result = ''
            for index, item in enumerate(items, 1):
                result += f'{index}. {inline(descendants(item, "strong")[0])} — {inline(descendants(item, "small")[0])}\n'
            return result + '\n'
        result = ''
        for index, item in enumerate(items, 1):
            prefix = f'{index}.' if tag == 'ol' else '-'
            result += prefix + ' ' + inline(item) + '\n'
        return result + '\n'
    if 'section-label' in classes(node):
        labels = [child for child in node.children if isinstance(child, Node) and child.tag == 'span']
        result = '## ' + inline(labels[0]) + '\n\n' if labels else ''
        return result + ''.join(render(child) for child in node.children
                                if not isinstance(child, Node) or child.tag != 'span')
    if tag == 'a':
        return inline(node) + '\n\n'
    return ''.join(render(child) for child in node.children)

intro = (f'# {title}\n\nCanonical presentation: [Leafcoin]({canonical}).\n\n'
         'This Markdown preserves the current homepage’s concept, including all expandable architecture details, '
         'the proposed roadmap, archival prototype scope and displayed image captions. '
         f'[Structured relationships]({canonical}concept.jsonld) identify the concept, prototype, repositories and images separately.\n\n')
markdown = intro + render(main)
markdown += ('## Site assets and source context\n\n'
             f'- [Supplied SVG brand mark]({canonical}assets/leafcoin_revert.svg)\n'
             f'- [Supplied SVG favicon]({canonical}assets/favicon.svg)\n'
             f'- [Supplied touch icon]({canonical}assets/ios_ligth_leafcoin.png)\n'
             f'- [IBM Plex font license]({canonical}assets/fonts/OFL.txt): SIL Open Font License 1.1.\n'
             '- [Original Leafcoin presentation](https://old.leafcoin.org/): The source concept context used for the redesign, at the designated archive URL.\n\n'
             'The five AI-generated concept illustrations are separate from the historical Home Aeroponics photographs. '
             'The photograph captions identify privacy retouching. Use the page’s scope statements '
             'and repository documentation when interpreting prototype evidence.\n')
provenance_file = ROOT/'docs/generated-illustrations.md'
if provenance_file.is_file():
    markdown += (f'\n[Generated-illustration prompts and provenance]({canonical}docs/generated-illustrations.md): '
                 'The home-lab hero and four section illustrations are AI-generated concept visuals. The provenance record associates '
                 'each image with its prompt and the proposed subject it depicts.\n')
footer = descendants(dom.root, 'footer')
if footer:
    footer_links = [link for link in descendants(footer[0], 'a') if link.attrs.get('href', '').startswith('http')]
    if footer_links:
        markdown += '\n## Footer reference\n\n' + ''.join('- ' + inline(link) + '\n' for link in footer_links)
markdown = re.sub(r'\n{3,}', '\n\n', markdown).strip() + '\n'
(OUTPUT/'index.md').write_text(markdown)
(OUTPUT/'llms-full.txt').write_text(markdown)

person_id = 'https://papou.work/#person'
prototype_id = 'https://papou.work/portfolio.html#home'
original_id = 'https://old.leafcoin.org/#original-presentation'
provenance = {}
if provenance_file.is_file():
    anchor = ''
    for line in provenance_file.read_text().splitlines():
        explicit = re.search(r'<a\s+id=["\']([^"\']+)', line)
        if explicit:
            anchor = explicit.group(1)
        if re.match(r'^#{2,6}\s', line):
            heading = re.sub(r'^#+\s+', '', line).strip()
            for section_id in ('concept', 'architecture', 'calibration', 'roadmap'):
                if section_id in heading.casefold():
                    anchor = section_id
                    break
        for asset in re.findall(r'assets/images/[\w./-]+\.(?:avif|gif|jpe?g|png|svg|webp)', line):
            if anchor:
                provenance[asset] = urljoin(canonical, 'docs/generated-illustrations.md#' + anchor)
images = []
for image in descendants(main, 'img'):
    ancestor = image.parent
    figure = None
    section_id = ''
    while ancestor:
        if ancestor.tag == 'figure' and figure is None:
            figure = ancestor
        if ancestor.tag == 'section' and ancestor.attrs.get('id'):
            section_id = ancestor.attrs['id']
            break
        ancestor = ancestor.parent
    captions = descendants(figure, 'figcaption') if figure else []
    caption = plain(captions[0]) if captions else ''
    sources = [urljoin(canonical, link.attrs['href']) for link in descendants(figure, 'a')
               if link.attrs.get('href')] if figure else []
    external_sources = [source for source in sources if not source.startswith(canonical)]
    is_prototype = section_id == 'prototype'
    src = image.attrs['src']
    slug = re.sub(r'[^a-z0-9]+', '-', Path(src).stem.lower()).strip('-')
    local_provenance = next((source for source in sources if 'docs/generated-illustrations.md' in source),
                            provenance.get(src))
    source = local_provenance or (external_sources[0] if external_sources else
                                 (prototype_id if is_prototype else 'https://old.leafcoin.org/'))
    about = prototype_id if is_prototype else canonical + '#' + (
        section_id if section_id in ('architecture', 'calibration', 'roadmap') else 'concept')
    record = {'@type': 'ImageObject', '@id': canonical + '#image-' + slug,
              'contentUrl': urljoin(canonical, src), 'name': image.attrs.get('alt', ''),
              'caption': caption or image.attrs.get('alt', ''), 'inLanguage': 'en',
              'isBasedOn': source, 'about': {'@id': about}}
    if local_provenance:
        record['creativeWorkStatus'] = 'AI-generated concept illustration'
    for field in ('width', 'height'):
        if image.attrs.get(field, '').isdigit():
            record[field] = int(image.attrs[field])
    images.append(record)

repository_nodes = []
seen_repositories = set()
for link in descendants(main, 'a'):
    url = link.attrs.get('href', '').rstrip('/')
    if not re.fullmatch(r'https://github\.com/[^/]+/[^/#?]+', url) or url in seen_repositories:
        continue
    seen_repositories.add(url)
    article = link.parent
    while article and article.tag != 'article':
        article = article.parent
    paragraphs = descendants(article, 'p') if article else []
    descriptions = [plain(p) for p in paragraphs if 'eyebrow' not in classes(p)]
    is_site = url == 'https://github.com/pilprod/leafcoin'
    node = {'@type': 'SoftwareSourceCode', '@id': url + '#source-code',
            'name': plain(link), 'url': url, 'codeRepository': url,
            'description': descriptions[-1] if descriptions else 'Static website source for the Leafcoin concept presentation.',
            'isPartOf': {'@id': canonical + '#concept' if is_site else prototype_id},
            'creativeWorkStatus': 'Static concept website' if is_site else 'Historical personal R&D examples'}
    repository_nodes.append(node)

hero_paragraphs = [plain(node) for node in descendants(main, 'p')
                   if classes(node) & {'hero-description', 'hero-context'}]
prototype_section = next(node for node in descendants(main, 'section') if node.attrs.get('id') == 'prototype')
prototype_paragraphs = [plain(node) for node in descendants(prototype_section, 'p')
                        if classes(node) & {'section-intro', 'scope-note'}]
embedded_concept = {}
for script in descendants(dom.root, 'script'):
    if script.attrs.get('type') == 'application/ld+json':
        block = json.loads(''.join(child for child in script.children if isinstance(child, str)))
        for node in block.get('@graph', [block]):
            if node.get('@id') == canonical + '#concept':
                embedded_concept = node
graph = {'@context': 'https://schema.org', '@graph': [
    {'@type': 'WebSite', '@id': canonical+'#website', 'url': canonical, 'name': 'Leafcoin',
     'inLanguage': 'en', 'creator': {'@id': person_id}},
    {'@type': 'WebPage', '@id': canonical+'#webpage', 'url': canonical, 'name': title,
     'inLanguage': 'en', 'isPartOf': {'@id': canonical+'#website'},
     'mainEntity': {'@id': canonical+'#concept'},
     'encoding': {'@type': 'MediaObject', 'encodingFormat': 'text/markdown', 'contentUrl': canonical+'index.md'}},
    {'@type': 'CreativeWork', '@id': canonical+'#concept', 'url': canonical, 'name': title,
     'description': embedded_concept.get('description', ' '.join(hero_paragraphs)),
     'creativeWorkStatus': 'Concept / personal R&D', 'inLanguage': 'en', 'creator': {'@id': person_id},
     'isPartOf': {'@id': canonical+'#website'},
     'isBasedOn': [{'@id': prototype_id}, {'@id': original_id}],
     'image': [{'@id': image['@id']} for image in images],
     'subjectOf': [{'@id': canonical+'#webpage'}, {'@id': 'https://github.com/pilprod/leafcoin#source-code'}]},
    {'@type': 'Person', '@id': person_id, 'name': 'Ilya Papou', 'url': 'https://papou.work/',
     'sameAs': ['https://github.com/pilprod', 'https://www.linkedin.com/in/pilprod/']},
    {'@type': 'CreativeWork', '@id': prototype_id, 'url': prototype_id,
     'name': 'Home Aeroponics & IoT automation', 'creativeWorkStatus': 'Historical personal R&D prototype',
     'description': ' '.join(prototype_paragraphs),
     'subjectOf': [{'@id': image['@id']} for image in images if image['about']['@id'] == prototype_id],
     'hasPart': [{'@id': node['@id']} for node in repository_nodes if node['isPartOf']['@id'] == prototype_id]},
    {'@type': 'CreativeWork', '@id': original_id, 'url': 'https://old.leafcoin.org/',
     'name': 'Original Leafcoin concept presentation', 'creativeWorkStatus': 'Source concept presentation',
     'description': 'The original concept presentation used as source context for this redesign. Its historical presentation is distinct from the current site’s concept and prototype scope statements.'},
    *repository_nodes, *images
]}
component_nodes = []
for section in descendants(main, 'section'):
    section_id = section.attrs.get('id')
    if section_id not in ('architecture', 'calibration', 'roadmap'):
        continue
    headings = descendants(section, 'h2')
    paragraphs = [plain(node) for node in descendants(section, 'p')
                  if classes(node) & {'section-intro', 'scope-note'}]
    component_nodes.append({'@type': 'CreativeWork', '@id': canonical+'#'+section_id,
                            'url': canonical+'#'+section_id, 'name': plain(headings[0]),
                            'description': ' '.join(paragraphs),
                            'creativeWorkStatus': 'Proposed concept component', 'inLanguage': 'en',
                            'isPartOf': {'@id': canonical+'#concept'}})
graph['@graph'].extend(component_nodes)
graph['@graph'][2]['hasPart'] = [{'@id': node['@id']} for node in component_nodes]
(OUTPUT/'concept.jsonld').write_text(json.dumps(graph, ensure_ascii=False, indent=2)+'\n')

S = 'http://www.sitemaps.org/schemas/sitemap/0.9'
I = 'http://www.google.com/schemas/sitemap-image/1.1'
previous = ET.parse(ROOT/'sitemap.xml').getroot()
modified = previous.findtext(f'{{{S}}}url/{{{S}}}lastmod')
ET.register_namespace('', S)
ET.register_namespace('image', I)
sitemap = ET.Element(f'{{{S}}}urlset')
entry = ET.SubElement(sitemap, f'{{{S}}}url')
ET.SubElement(entry, f'{{{S}}}loc').text = canonical
if modified:
    ET.SubElement(entry, f'{{{S}}}lastmod').text = modified
for image in images:
    item = ET.SubElement(entry, f'{{{I}}}image')
    ET.SubElement(item, f'{{{I}}}loc').text = image['contentUrl']
ET.indent(sitemap, space='  ')
(OUTPUT/'sitemap.xml').write_bytes(ET.tostring(sitemap, encoding='utf-8', xml_declaration=True)+b'\n')
print(f'Generated full concept text, {len(graph["@graph"])} graph entities and {len(images)} sitemap image entries.')
