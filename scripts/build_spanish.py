#!/usr/bin/env python3
"""Build static Spanish pages from reviewed copy, retaining source relationships.

English markup remains the layout source. Article translations are keyed by
stable content paths and bound to a digest, so source edits require review.
"""
import argparse
from copy import deepcopy
import hashlib
from html import escape
from html.parser import HTMLParser
import json
import posixpath
from pathlib import Path
import re
from urllib.parse import urljoin, urlsplit, urlunsplit
import xml.etree.ElementTree as ET
from article_diagrams import render_svg

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = 'https://leafcoin.org/'
PAGES = ['index.html', 'articles/index.html', *[
    'articles/'+slug+'.html' for slug in (
        'what-is-aeroponics', 'aeroponics-vs-hydroponics',
        'aeroponic-system-control', 'future-of-aeroponics')]]
VOID = {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}

def normalize(value):
    return ' '.join(value.split())

def source_leaves(value, path=''):
    if isinstance(value, dict):
        for key, item in value.items():
            if key not in {'slug','image','provenance','id','kind','layout','sources','related','url','published','modified'}:
                yield from source_leaves(item, path+'.'+key)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            yield from source_leaves(item, path+'.'+str(index))
    elif isinstance(value, str):
        yield path.lstrip('.'), value

def set_path(value, path, translated):
    bits = path.split('.')
    for bit in bits[:-1]:
        value = value[int(bit)] if isinstance(value,list) else value[bit]
    last = int(bits[-1]) if isinstance(value,list) else bits[-1]
    value[last] = translated

def load_copy():
    data_path = ROOT/'articles/content.json'
    english = json.loads(data_path.read_text())
    reviewed = json.loads((ROOT/'locales/es/articles.json').read_text())
    assert reviewed['source_sha256'] == hashlib.sha256(data_path.read_bytes()).hexdigest(), 'English articles changed: review Spanish translations'
    spanish = deepcopy(english)
    catalog = json.loads((ROOT/'locales/es/home.json').read_text())
    catalog.update(json.loads((ROOT/'locales/es/ui.json').read_text()))
    for en, es in zip(english['articles'], spanish['articles']):
        values = reviewed['articles'][en['slug']]
        assert set(values) == {key for key,_ in source_leaves(en)}, 'Incomplete translation: '+en['slug']
        for key, original in source_leaves(en):
            translated = values[key]
            set_path(es,key,translated)
            catalog[original] = translated
            # Markdown links split paragraphs into separate visible text nodes.
            en_bits = re.split(r'\[([^\]]+)\]\([^)]+\)', original)
            es_bits = re.split(r'\[([^\]]+)\]\([^)]+\)', translated)
            assert len(en_bits)==len(es_bits), 'Link structure changed: '+en['slug']+'/'+key
            for a,b in zip(en_bits,es_bits):
                if a.strip(): catalog[normalize(a)] = normalize(b)
            catalog[re.sub(r'\[([^\]]+)\]\([^)]+\)',r'\1',original)] = re.sub(r'\[([^\]]+)\]\([^)]+\)',r'\1',translated)
            if key=='category': catalog[original.split(' / ',1)[1]] = translated.split(' / ',1)[1]
        # Figure text is also serialized as joined lines and text descriptions.
        for en_section,es_section in zip(en['sections'],es['sections']):
            for a,b in zip(en_section.get('figures',[]),es_section.get('figures',[])):
                for x,y in zip(a.get('steps',a.get('panels',[])),b.get('steps',b.get('panels',[]))):
                    catalog[' '.join(x['lines'])] = ' '.join(y['lines'])
    return english,spanish,{normalize(a):b for a,b in catalog.items()}

class Translator:
    def __init__(self,catalog,data):
        self.catalog = catalog
        self.allowed = {'Leafcoin','Ilya Papou','GitHub','IoT','ML / QR','NFT','Español','ES','EN','English'}
        for source in data['sources'].values():
            self.allowed.add(source['title'])
            self.allowed.add(source['authors'])
        changed={a:b for a,b in catalog.items() if a!=b and a}
        self.pattern=re.compile('|'.join(r'(?<!\w)'+re.escape(k)+r'(?!\w)' for k in sorted(changed,key=len,reverse=True)))
        self.changed=changed
        self.missing=set()

    def text(self,value,strict=False):
        key=normalize(value)
        if not key:return value
        if key in self.catalog:
            translated=self.catalog[key]
        else:
            translated=self.pattern.sub(lambda m:self.changed[m[0]],value)
            translated=re.sub(r'(\d+) min read',r'\1 min de lectura',translated)
            translated=translated.replace('13 October 2026','13 de octubre de 2026')
            if strict and translated==value and re.search('[A-Za-z]{3}',key) and key not in self.allowed:
                self.missing.add(key)
        # Preserve inline spaces around anchors and emphasized text.
        leading=value[:len(value)-len(value.lstrip())]
        trailing=value[len(value.rstrip()):]
        return leading+translated.strip()+trailing

    def url(self,value):
        if value.startswith(ORIGIN):
            path=value[len(ORIGIN):]
            if path.startswith(('assets/','docs/')): return value
            if path.startswith('es/'): return value
            return ORIGIN+'es/'+path
        return value

    def graph(self,value,key=''):
        if isinstance(value,dict):
            result={k:self.graph(v,k) for k,v in value.items()}
            if result.get('@type') in {'Article','WebPage','CreativeWork','CollectionPage','WebSite','ImageObject'}:
                result['inLanguage']='es'
            if result.get('@type')=='Article' and 'articleBody' in result:
                result['wordCount']=len(result['articleBody'].split())
            return result
        if isinstance(value,list): return [self.graph(v,key) for v in value]
        if not isinstance(value,str): return value
        if key=='inLanguage': return 'es'
        if value.startswith(('https://','http://')):
            mapped=self.url(value)
            return mapped.replace('/assets/diagrams/','/assets/diagrams/es/') if '/assets/diagrams/' in mapped else mapped
        # Keep machine-readable provenance statuses shared between locales.
        if key in {'creativeWorkStatus','@type','encodingFormat','@context'}: return value
        return '\n\n'.join(self.text(part) for part in value.split('\n\n'))

class SpanishHTML(HTMLParser):
    def __init__(self,source,path,translator):
        super().__init__(convert_charrefs=True)
        self.path=path;self.translator=translator;self.out=[];self.script=None;self.json_text=[]
        self.feed(source);self.close()

    def asset_path(self,value):
        if not value or value.startswith(('#','http:','https:','mailto:','data:')): return value
        target=posixpath.normpath(posixpath.join(posixpath.dirname(self.path),urlsplit(value).path))
        if target.startswith(('assets/','docs/')) or target.endswith(('.css','.js')):
            if target.startswith('assets/diagrams/'):target=target.replace('assets/diagrams/','assets/diagrams/es/',1)
            relative=posixpath.relpath(target,posixpath.dirname('es/'+self.path))
            parsed=urlsplit(value)
            return urlunsplit(('', '',relative,parsed.query,parsed.fragment))
        return value

    def handle_decl(self,value): self.out.append('<!'+value+'>')
    def handle_comment(self,value): self.out.append('<!--'+value+'-->')
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='html':a['lang']='es'
        if 'data-language-switch' in a:
            current='' if self.path=='index.html' else self.path.removesuffix('index.html') if self.path.endswith('/index.html') else self.path
            a.update(href=posixpath.relpath(current or '.',posixpath.dirname('es/'+self.path))+('/' if not current or current.endswith('/') else ''),lang='en',hreflang='en')
            a['aria-label']='Leer en inglés'
        for key,value in list(a.items()):
            if value is None: continue
            if key in {'alt','title','aria-label'}:
                if value!='Leer en inglés':a[key]=self.translator.text(value,strict=True)
            elif key in {'src','href','poster'}:
                if tag=='link' and a.get('hreflang'):continue
                a[key]=self.asset_path(self.translator.url(value))
            elif key=='srcset':
                a[key]=', '.join(self.asset_path(part.strip().split()[0])+' '+ ' '.join(part.strip().split()[1:]) for part in value.split(','))
            elif tag=='meta' and key=='content':
                name=a.get('name',a.get('property',''))
                if name=='og:locale':a[key]='es_ES'
                elif name=='og:url':a[key]=self.translator.url(value)
                elif name in {'description','og:title','og:description','og:image:alt','twitter:title','twitter:description','twitter:image:alt'}:a[key]=self.translator.text(value,strict=True)
        self.out.append('<'+tag+''.join(' '+key+('="'+escape(value,quote=True)+'"' if value is not None else '') for key,value in a.items())+'>')
        if tag=='script':self.script=a.get('type','script');self.json_text=[]

    def handle_startendtag(self,tag,attrs):self.handle_starttag(tag,attrs)
    def handle_endtag(self,tag):
        if tag=='script':
            if self.script=='application/ld+json':self.out.append(json.dumps(self.translator.graph(json.loads(''.join(self.json_text))),ensure_ascii=False).replace('<',r'\u003c'))
            else:self.out.extend(self.json_text)
            self.script=None
        if tag not in VOID:self.out.append('</'+tag+'>')
    def handle_data(self,value):
        if self.script is not None:self.json_text.append(value)
        else:self.out.append(escape(self.translator.text(value,strict=True),quote=False))

def build(check=False):
    english,spanish,catalog=load_copy()
    translator=Translator(catalog,english)
    outputs={}
    for path in PAGES:
        parser=SpanishHTML((ROOT/path).read_text(),path,translator)
        html=''.join(parser.out).replace('>Español</span>','>English</span>').replace('>ES</span>','>EN</span>')
        outputs['es/'+path]=html
    if translator.missing:
        raise SystemExit('Missing Spanish UI translations:\n'+'\n'.join(sorted(translator.missing)))
    for article in spanish['articles']:
        for section in article['sections']:
            for figure in section.get('figures',[]):
                if figure['kind']=='diagram':
                    for suffix,mobile in [('',False),('-mobile',True)]:
                        svg,_,_=render_svg(figure,mobile)
                        outputs['assets/diagrams/es/'+figure['id']+suffix+'.svg']=svg
    # Complete text and graphs are localized companions, not runtime translation.
    for path in ['index.md','concept.jsonld','articles/index.md','articles/library.jsonld',*['articles/'+a['slug']+'.md' for a in english['articles']]]:
        value=(ROOT/path).read_text()
        if path.endswith('.jsonld'):value=json.dumps(translator.graph(json.loads(value)),ensure_ascii=False,indent=2)+'\n'
        else:
            value=translator.text(value)
            value=re.sub(r'https://leafcoin\.org/[^\s)\]]*',lambda m:translator.url(m[0]),value)
            value=value.replace('/assets/diagrams/','/assets/diagrams/es/')
        outputs['es/'+path]=value
    outputs['es/articles/llms-full.txt']='\n'.join(outputs['es/articles/'+a['slug']+'.md'] for a in english['articles'])+'\n'
    outputs['es/llms-full.txt']=outputs['es/index.md'].rstrip()+'\n\n\n'+outputs['es/articles/llms-full.txt']
    outputs['es/llms.txt']='# Leafcoin en español\n\nConcepto personal de I+D agrotecnológica. La arquitectura y el ciclo de ML son propuestas; los materiales del laboratorio documentan prototipos históricos.\n\n- [Inicio](https://leafcoin.org/es/)\n- [Concepto completo](https://leafcoin.org/es/index.md)\n- [Texto completo del sitio](https://leafcoin.org/es/llms-full.txt)\n- [Artículos](https://leafcoin.org/es/articles/)\n- [Biblioteca completa](https://leafcoin.org/es/articles/llms-full.txt)\n- [Relaciones estructuradas](https://leafcoin.org/es/concept.jsonld)\n- [English](https://leafcoin.org/)\n'
    for path,value in outputs.items():
        value=value.rstrip()+'\n'
        target=ROOT/path
        if check:
            assert target.is_file() and target.read_text()==value,'Stale Spanish resource: '+path
        else:
            target.parent.mkdir(parents=True,exist_ok=True);target.write_text(value)
    # Keep all twelve pages in one root sitemap. English builder runs first.
    ns='http://www.sitemaps.org/schemas/sitemap/0.9';img='http://www.google.com/schemas/sitemap-image/1.1'
    ET.register_namespace('',ns);ET.register_namespace('image',img)
    sitemap=ET.parse(ROOT/'sitemap.xml').getroot()
    for entry in list(sitemap):
        if entry.findtext('{'+ns+'}loc','').startswith(ORIGIN+'es/'):sitemap.remove(entry)
    for entry in list(sitemap):
        translated=deepcopy(entry)
        translated.find('{'+ns+'}loc').text=translator.url(entry.findtext('{'+ns+'}loc'))
        translated.find('{'+ns+'}lastmod').text='2026-10-14'
        for image in translated.findall('{'+img+'}image/{'+img+'}loc'):
            if '/assets/diagrams/' in image.text:image.text=image.text.replace('/assets/diagrams/','/assets/diagrams/es/')
        sitemap.append(translated)
    ET.indent(sitemap,space='  ')
    sitemap_text=ET.tostring(sitemap,encoding='utf-8',xml_declaration=True)+b'\n'
    if check:assert (ROOT/'sitemap.xml').read_bytes()==sitemap_text,'Stale bilingual sitemap'
    else:(ROOT/'sitemap.xml').write_bytes(sitemap_text)
    print(f'{"Checked" if check else "Built"} six Spanish pages, complete text, metadata and eight localized diagrams.')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true')
    build(parser.parse_args().check)
