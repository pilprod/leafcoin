#!/usr/bin/env python3
"""Build the reviewed Leafcoin learning library without runtime dependencies."""
import argparse
from datetime import date
from html import escape, unescape
import json
import math
from pathlib import Path
import re
from article_diagrams import render_svg

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / 'articles/content.json').read_text())
ORIGIN = 'https://leafcoin.org/'
LIBRARY = ORIGIN + 'articles/'
HOME = (ROOT / 'index.html').read_text()
CHECK = argparse.ArgumentParser()
CHECK.add_argument('--check', action='store_true')
args = CHECK.parse_args()
outputs = {}
articles = DATA['articles']
by_slug = {a['slug']: a for a in articles}


def inline(value):
    result = escape(value)
    result = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', lambda m: f'<a href="{m[2]}">{m[1]}</a>', result)
    return result


def plain(value):
    return re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', value)


def figure_text(figure):
    parts = [figure['title'], figure['caption']]
    if figure['kind'] == 'diagram':
        parts.extend([figure['description'], figure.get('footer', '')])
        for item in figure.get('steps', figure.get('panels', [])):
            parts.extend([item['title'], *item['lines']])
    return [p for p in parts if p]


def render_figure(figure):
    title = escape(figure['title'])
    caption = escape(figure['caption'])
    identifier = 'fig-' + figure['id']
    if figure['kind'] == 'image':
        return f'''<figure id="{identifier}" class="article-inline-image"><img src="../assets/images/{figure['image']}" width="1536" height="1024" loading="lazy" decoding="async" alt="AI-generated concept illustration. {escape(figure['alt'])}"><figcaption><strong>{title}</strong><p>{caption}</p><a href="../docs/generated-illustrations.md#{figure['provenance']}">AI-generated concept illustration</a></figcaption></figure>'''
    svg, width, height = render_svg(figure)
    mobile_svg, mobile_width, mobile_height = render_svg(figure, mobile=True)
    path = 'assets/diagrams/' + figure['id'] + '.svg'
    mobile_path = 'assets/diagrams/' + figure['id'] + '-mobile.svg'
    outputs[path], outputs[mobile_path] = svg, mobile_svg
    descriptions = ''.join('<li><strong>'+escape(item['title'])+'</strong>: '+escape(item.get('text', ' '.join(item['lines'])))+'.</li>' for item in figure.get('steps', figure.get('panels', [])))
    footer = '<p>'+escape(figure['footer'])+'</p>' if figure.get('footer') else ''
    return f'''<figure id="{identifier}" class="article-diagram"><p class="eyebrow">Explained visually</p><h3>{title}</h3><picture style="--diagram-ratio:{width}/{height};--diagram-mobile-ratio:{mobile_width}/{mobile_height}"><source media="(max-width: 600px)" srcset="../{mobile_path}"><img src="../{path}" width="{width}" height="{height}" loading="lazy" decoding="async" alt="{escape(figure['description'])}"></picture><figcaption><p>{caption}</p><details class="diagram-description"><summary>Read the diagram as text</summary><p>{escape(figure['description'])}</p><ol>{descriptions}</ol>{footer}</details><a class="diagram-download" href="../{path}">Open full-size diagram</a></figcaption></figure>'''


def figure_markdown(figure):
    image_path = 'assets/images/' + figure['image'] if figure['kind']=='image' else 'assets/diagrams/'+figure['id']+'.svg'
    alt = ('AI-generated concept illustration. ' + figure['alt']) if figure['kind']=='image' else figure['description']
    text = f'### {figure["title"]}\n\n![{alt}]({ORIGIN+image_path})\n\n{figure["caption"]}\n\n'
    if figure['kind']=='diagram':
        text += figure['description']+'\n\n'
        for item in figure.get('steps',figure.get('panels',[])):
            text += '- **'+item['title']+'**: '+item.get('text', ' '.join(item['lines']))+'.\n'
        text += '\n'+(figure['footer']+'\n\n' if figure.get('footer') else '')
    else:
        text += '[AI image provenance]('+ORIGIN+'docs/generated-illustrations.md#'+figure['provenance']+')\n\n'
    return text


def article_images(a, url):
    images=[{'@type':'ImageObject','contentUrl':ORIGIN+'assets/images/'+a['image'],'width':1536,'height':1024,'caption':'AI-generated concept illustration. '+a['image_alt'],'creativeWorkStatus':'AI-generated concept illustration','isBasedOn':ORIGIN+'docs/generated-illustrations.md#'+a['provenance']}]
    for section in a['sections']:
        for figure in section.get('figures',[]):
            if figure['kind']=='image':
                images.append({'@type':'ImageObject','contentUrl':ORIGIN+'assets/images/'+figure['image'],'width':1536,'height':1024,'caption':'AI-generated concept illustration. '+figure['caption'],'creativeWorkStatus':'AI-generated concept illustration','isBasedOn':ORIGIN+'docs/generated-illustrations.md#'+figure['provenance']})
            else:
                _,width,height=render_svg(figure)
                images.append({'@type':'ImageObject','contentUrl':ORIGIN+'assets/diagrams/'+figure['id']+'.svg','width':width,'height':height,'caption':figure['caption'],'description':figure['description'],'creativeWorkStatus':'Educational schematic','isBasedOn':url+'#fig-'+figure['id']})
    return images


def article_body(a):
    parts = [a['title'], a['summary']]
    for s in a['sections']:
        parts.extend([s['title'], *s['paragraphs'], *s.get('bullets', []), *s.get('ordered', [])])
        if 'table' in s:
            parts.extend([s['table']['caption'], *s['table']['headers']])
            parts.extend(cell for row in s['table']['rows'] for cell in row)
        for figure in s.get('figures', []):
            parts.extend(figure_text(figure))
    for q in a['questions']:
        parts.extend([q['question'], q['answer']])
    return '\n\n'.join(plain(p) for p in parts)


def read_minutes(a):
    return math.ceil(len(article_body(a).split()) / 200)


def card(a, prefix=''):
    return f'''<article class="guide-card">
      <a class="guide-card-cover" href="{prefix}{a['slug']}.html" aria-label="Read: {escape(a['title'])}"><img src="{prefix}../assets/images/{a['image']}" width="1536" height="1024" loading="lazy" decoding="async" alt="AI-generated concept illustration. {escape(a['image_alt'])}"></a>
      <div class="guide-card-copy"><p class="eyebrow">{escape(a['category'])} · {read_minutes(a)} min read</p><h2><a href="{prefix}{a['slug']}.html">{escape(a['title'])}</a></h2><p>{escape(a['description'])}</p><p class="guide-card-note">AI-generated concept illustration</p></div>
    </article>'''


header = re.search(r'  <header class="site-toolbar">[\s\S]*?</header>', HOME).group(0)
header = header.replace('href="./"', 'href="../index.html"').replace('src="assets/', 'src="../assets/')
header = re.sub(r'href="#(concept|architecture|calibration|roadmap|prototype)"', r'href="../index.html#\1"', header)
header = header.replace('href="articles/index.html"', 'href="index.html" aria-current="location"')
footer = re.search(r'  <footer class="site-footer">[\s\S]*?</footer>', HOME).group(0)
footer = footer.replace('href="articles/index.html"', 'href="index.html"')
notice = re.search(r'<section id="analytics-consent"[\s\S]*?</section>', HOME).group(0)
shared_tail = footer + '\n' + notice


def shell(title, description, canonical, graph, content, social_image=None, social_alt=None, markdown=None, hub=False):
    image = social_image or ORIGIN + 'assets/images/' + articles[0]['image']
    alt = social_alt or 'AI-generated concept illustration. ' + articles[0]['image_alt']
    alternates = f'<link rel="alternate" href="{escape(markdown)}" type="text/markdown" title="Full article in Markdown">' if markdown else '<link rel="alternate" href="index.md" type="text/markdown" title="Learning library in Markdown">'
    graph_json = json.dumps({'@context':'https://schema.org','@graph':graph},ensure_ascii=False).replace('<', chr(92)+'u003c')
    return f'''<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)}</title><meta name="description" content="{escape(description)}"><meta name="author" content="Ilya Papou">
<meta name="robots" content="index, follow, max-image-preview:large"><meta name="color-scheme" content="light dark">
<meta name="theme-color" content="#f5faf7" media="(prefers-color-scheme: light)"><meta name="theme-color" content="#081411" media="(prefers-color-scheme: dark)">
<link rel="canonical" href="{canonical}">{alternates}
<link rel="alternate" hreflang="en" href="{canonical}"><link rel="alternate" hreflang="es" href="{ORIGIN+'es/'+canonical.removeprefix(ORIGIN)}"><link rel="alternate" hreflang="x-default" href="{canonical}">
<link rel="describedby" href="../llms.txt" type="text/plain" title="Leafcoin reading guide"><link rel="describedby" href="llms-full.txt" type="text/plain" title="Complete learning library text">
<link rel="icon" href="../assets/favicon-96.png" type="image/png" sizes="96x96"><link rel="apple-touch-icon" href="../assets/ios_ligth_leafcoin.png">
<link rel="stylesheet" href="../styles.css?v=20261014-es-spacing"><link rel="stylesheet" href="../articles.css?v=20261014-es-spacing"><link rel="stylesheet" href="../analytics-ui.css?v=20260930-footer-center">
<link rel="stylesheet" href="../language.css?v=20261014-es">
<meta property="og:type" content="{'website' if hub else 'article'}"><meta property="og:site_name" content="Leafcoin"><meta property="og:locale" content="en_US">
<meta property="og:title" content="{escape(title)}"><meta property="og:description" content="{escape(description)}"><meta property="og:url" content="{canonical}">
<meta property="og:image" content="{image}"><meta property="og:image:type" content="image/jpeg"><meta property="og:image:width" content="1536"><meta property="og:image:height" content="1024"><meta property="og:image:alt" content="{escape(alt)}">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{escape(title)}"><meta name="twitter:description" content="{escape(description)}"><meta name="twitter:image" content="{image}"><meta name="twitter:image:alt" content="{escape(alt)}">
{'' if hub else f'<meta property="article:published_time" content="{DATA["published"]}"><meta property="article:modified_time" content="{DATA["modified"]}">'}
<script type="application/ld+json">{graph_json}</script>
<script src="../visitor-region.js?v=20261014-es" defer></script><script src="../language.js?v=20261014-es" defer></script><script src="../site.js?v=20261014-es" defer></script><script src="../analytics.js?v=20261014-es" defer></script>
</head><body class="learning-page">
<a class="skip-link" href="#main">Skip to content</a>
{header.replace('href="es/"', 'href="../es/'+canonical.removeprefix(ORIGIN)+'"')}
<main id="main" class="learning-main">{content}</main>
{shared_tail}
</body></html>
'''


def common_graph():
    return [
      {'@type':'WebSite','@id':ORIGIN+'#website','url':ORIGIN,'name':'Leafcoin','alternateName':'leafcoin.org','publisher':{'@id':'https://papou.work/#person'}},
      {'@type':'Person','@id':'https://papou.work/#person','name':'Ilya Papou','url':'https://papou.work/'}
    ]


def breadcrumbs(canonical, title=None):
    items = [{'@type':'ListItem','position':1,'name':'Leafcoin','item':ORIGIN}, {'@type':'ListItem','position':2,'name':'Articles','item':LIBRARY}]
    if title: items.append({'@type':'ListItem','position':3,'name':title,'item':canonical})
    return {'@type':'BreadcrumbList','@id':canonical+'#breadcrumbs','itemListElement':items}


hub_title = 'Aeroponics Guides: Methods, Control and Future | Leafcoin'
hub_description = 'Research-based guides to aeroponics, hydroponic comparisons, system control and the future of agriculture, with sources and practical tradeoffs.'
hub_intro = 'Aeroponics, explained.'
hub_copy = 'Four guides connecting plant cultivation with the engineering behind it. Start with the growing method, compare the alternatives, then explore control and the possibilities ahead.'
hub_graph = common_graph() + [
    {'@type':'CollectionPage','@id':LIBRARY+'#library','url':LIBRARY,'name':hub_title,'description':hub_description,'inLanguage':'en','datePublished':DATA['published'],'dateModified':DATA['modified'],'isPartOf':{'@id':ORIGIN+'#website'},'publisher':{'@id':'https://papou.work/#person'},'mainEntity':{'@id':LIBRARY+'#reading-order'}},
    {'@type':'ItemList','@id':LIBRARY+'#reading-order','itemListElement':[{'@type':'ListItem','position':i+1,'name':a['title'],'url':LIBRARY+a['slug']+'.html'} for i,a in enumerate(articles)]},breadcrumbs(LIBRARY)
]
hub_content = f'''<nav class="breadcrumbs" aria-label="Breadcrumb"><a href="../index.html">Leafcoin</a><span aria-hidden="true">/</span><span>Articles</span></nav>
<header class="library-header" id="library"><p class="eyebrow">The Leafcoin learning library</p><h1>{hub_intro}</h1><p class="library-intro">{hub_copy}</p><p class="editorial-note">Educational articles published by Leafcoin. Research findings are attributed to their sources; engineering suggestions and future possibilities are identified as such.</p></header>
<section class="guide-grid" aria-label="Aeroponics articles">{''.join(card(a) for a in articles)}</section>
<section class="library-context"><h2>From understanding to experimentation</h2><p>Aeroponics can be a useful growing method, but a convincing system needs reliable delivery, sound measurements and evidence across repeated cycles. These guides explain the questions behind Leafcoin’s proposed research.</p><a href="../index.html#calibration">Explore the proposed ML calibration loop</a><p class="editorial-note">Leafcoin remains a concept and personal R&amp;D project. Historical lab materials and proposed capabilities are described separately in the <a href="../index.html#prototype">project overview</a>.</p><p><a href="llms-full.txt">Read the complete library as text</a></p></section>'''
outputs['articles/index.html'] = shell(hub_title,hub_description,LIBRARY,hub_graph,hub_content,hub=True)
outputs['articles/index.md'] = '# '+hub_intro+'\n\nCanonical library: '+LIBRARY+'\n\n'+hub_copy+'\n\n'+ '\n\n'.join(f"## {a['title']}\n\n{a['description']}\n\n[Read article]({LIBRARY+a['slug']+'.html'}) · [Full text]({LIBRARY+a['slug']+'.md'})" for a in articles) + '\n'
collection_text = '# Leafcoin learning library\n\nFour educational articles. Each article preserves its sources and scope. Leafcoin remains a concept and personal R&D project.\n\n'
published = date.fromisoformat(DATA['published'])
published_label = f'{published.day} {published.strftime("%B %Y")}'
for a in articles:
    url=LIBRARY+a['slug']+'.html'
    image=ORIGIN+'assets/images/'+a['image']
    sections=[]
    for s in a['sections']:
        block=f'<section id="{s["id"]}"><h2>{escape(s["title"])}</h2>' + ''.join('<p>'+inline(p)+'</p>' for p in s['paragraphs'])
        for key,tag in [('bullets','ul'),('ordered','ol')]:
            if key in s: block+=f'<{tag}>'+''.join('<li>'+inline(item)+'</li>' for item in s[key])+f'</{tag}>'
        if 'table' in s:
            table=s['table']
            block+='<p class="comparison-hint">Scroll sideways to compare all columns.</p><div class="comparison-scroll" role="region" aria-label="Growing-system comparison" tabindex="0"><table><caption>'+escape(table['caption'])+'</caption><thead><tr>'+''.join('<th scope="col">'+escape(h)+'</th>' for h in table['headers'])+'</tr></thead><tbody>'+''.join('<tr><th scope="row">'+inline(row[0])+'</th>'+''.join('<td>'+inline(cell)+'</td>' for cell in row[1:])+'</tr>' for row in table['rows'])+'</tbody></table></div>'
        block += ''.join(render_figure(figure) for figure in s.get('figures', []))
        sections.append(block+'</section>')
    faq='<section id="questions"><h2>Common questions</h2>'+''.join('<div class="article-question"><h3>'+escape(q['question'])+'</h3><p>'+escape(q['answer'])+'</p></div>' for q in a['questions'])+'</section>'
    source_list=''.join(f'<li><a href="{DATA["sources"][key]["url"]}">{escape(DATA["sources"][key]["title"])}</a><p>{escape(DATA["sources"][key]["authors"])}{", "+str(DATA["sources"][key]["year"]) if DATA["sources"][key]["year"] else ""}. {escape(DATA["sources"][key]["kind"])}.</p></li>' for key in a['sources'])
    toc=''.join(f'<li><a href="#{s["id"]}">{escape(s["title"])}</a></li>' for s in a['sections']) + '<li><a href="#questions">Common questions</a></li><li><a href="#sources">Sources</a></li>'
    related=''.join(f'<li><a href="{slug}.html">{escape(by_slug[slug]["title"])}</a></li>' for slug in a['related'])
    content=f'''<nav class="breadcrumbs" aria-label="Breadcrumb"><a href="../index.html">Leafcoin</a><span aria-hidden="true">/</span><a href="index.html">Articles</a></nav>
<article class="learning-article"><header class="article-header"><p class="eyebrow">{escape(a['category'])}</p><h1>{escape(a['title'])}</h1><p class="article-meta">By <a href="https://papou.work/">Ilya Papou</a> · Published <time datetime="{DATA['published']}">{published_label}</time> · {read_minutes(a)} min read</p><p class="article-answer">{escape(a['summary'])}</p><p class="article-text-link"><a href="{a['slug']}.md">Read as text</a></p></header>
<figure class="article-cover"><img src="../assets/images/{a['image']}" width="1536" height="1024" fetchpriority="high" decoding="async" alt="AI-generated concept illustration. {escape(a['image_alt'])}"><figcaption><a href="../docs/generated-illustrations.md#{a['provenance']}">AI-generated concept illustration</a><span>Educational illustration, not experimental evidence.</span></figcaption></figure>
<div class="article-layout"><aside class="article-toc"><nav aria-label="In this article"><p class="eyebrow">In this article</p><ol>{toc}</ol></nav></aside><div class="article-prose">{''.join(sections)}{faq}<section id="sources" class="article-sources"><h2>Sources and scope</h2><p>These are original research publications or institutional technical guidance. Experimental findings apply to the crop and conditions studied. Suggestions in this guide are an engineering synthesis; they are not presented as measured Leafcoin results.</p><ol>{source_list}</ol></section><section class="article-related" aria-labelledby="related-heading"><h2 id="related-heading">Continue exploring</h2><ul>{related}</ul><a href="index.html">All aeroponics articles</a></section></div></div></article>'''
    graph=common_graph()+[
      {'@type':'WebPage','@id':url+'#webpage','url':url,'name':a['title'],'description':a['description'],'inLanguage':'en','isPartOf':{'@id':ORIGIN+'#website'},'mainEntity':{'@id':url+'#article'},'breadcrumb':{'@id':url+'#breadcrumbs'},'encoding':{'@type':'MediaObject','encodingFormat':'text/markdown','contentUrl':LIBRARY+a['slug']+'.md'}},
      {'@type':'Article','@id':url+'#article','url':url,'headline':a['title'],'description':a['description'],'inLanguage':'en','datePublished':DATA['published'],'dateModified':DATA['modified'],'author':{'@id':'https://papou.work/#person'},'publisher':{'@id':'https://papou.work/#person'},'mainEntityOfPage':{'@id':url+'#webpage'},'isPartOf':{'@id':LIBRARY+'#library'},'articleSection':a['category'].split(' / ',1)[1],'articleBody':article_body(a),'wordCount':len(article_body(a).split()),'image':article_images(a,url),'citation':[{'@type':'CreativeWork','name':DATA['sources'][key]['title'],'url':DATA['sources'][key]['url']} for key in a['sources']]},
      breadcrumbs(url,a['title'])
    ]
    outputs['articles/'+a['slug']+'.html']=shell(a['seo_title'],a['description'],url,graph,content,image,'AI-generated concept illustration. '+a['image_alt'],a['slug']+'.md')
    markdown=f'# {a["title"]}\n\nCanonical article: {url}\n\nBy Ilya Papou · Published {DATA["published"]} · {read_minutes(a)} min read\n\n{a["summary"]}\n\n'
    for s in a['sections']:
        markdown+='## '+s['title']+'\n\n'+'\n\n'.join(s['paragraphs'])+'\n\n'
        for key in ('bullets','ordered'):
            for i,item in enumerate(s.get(key,[]),1): markdown+=(f'{i}.' if key=='ordered' else '-')+' '+item+'\n'
            if s.get(key): markdown+='\n'
        if 'table' in s:
            t=s['table'];markdown+=t['caption']+'\n\n'
            for row in t['rows']:markdown+='- **'+row[0]+'** '+ '; '.join(t['headers'][i]+': '+row[i] for i in range(1,len(row)))+'\n'
            markdown+='\n'
        markdown += ''.join(figure_markdown(figure) for figure in s.get('figures', []))
    markdown+='## Common questions\n\n'+''.join('### '+q['question']+'\n\n'+q['answer']+'\n\n' for q in a['questions'])
    markdown+='## Sources and scope\n\nOriginal research publications or institutional technical guidance. Experimental findings apply to the crop and conditions studied. Engineering suggestions are not measured Leafcoin results.\n\n'
    for key in a['sources']:
        ref=DATA['sources'][key];markdown+=f'- [{ref["title"]}]({ref["url"]}): {ref["authors"]}'+(', '+str(ref['year']) if ref['year'] else '')+'. '+ref['kind']+'.\n'
    markdown+='\n## Continue exploring\n\n'+''.join(f'- [{by_slug[slug]["title"]}]({LIBRARY+slug}.html)\n' for slug in a['related'])+'\n'
    outputs['articles/'+a['slug']+'.md']=markdown
    collection_text+=markdown+'\n'
outputs['articles/llms-full.txt']=collection_text
outputs['articles/library.jsonld']=json.dumps({'@context':'https://schema.org','@graph':hub_graph},ensure_ascii=False,indent=2)+'\n'
for relative,content in outputs.items():
    content = content.rstrip() + '\n'
    path=ROOT/relative
    if args.check:
        if not path.is_file() or path.read_text()!=content:raise SystemExit('Stale generated article resource: '+relative)
    else:
        path.parent.mkdir(parents=True,exist_ok=True);path.write_text(content)
print(('Checked' if args.check else 'Built')+f' {len(articles)} articles, learning hub, full Markdown, library graph and combined article text.')
