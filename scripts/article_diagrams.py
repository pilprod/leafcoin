"""Responsive, deterministic educational SVGs for the article library."""
from html import escape
import textwrap


STYLE = '''
:root { --bg:#f5faf7; --card:#e9f3ed; --ink:#12201a; --muted:#486054;
  --line:#b8cfc0; --accent:#146442; --water:#298b97; --root:#8c744f; }
@media (prefers-color-scheme:dark) { :root { --bg:#081411; --card:#10271d;
  --ink:#effcf3; --muted:#bed2c6; --line:#315b43; --accent:#9deb8f;
  --water:#75cbd0; --root:#dcc9a4; } }
text { font-family:Arial,sans-serif; fill:var(--ink); }
.label { font-size:21px; font-weight:600; }
.body { font-size:17px; fill:var(--muted); }
.small { font-size:16px; fill:var(--muted); }
.card { fill:var(--card); stroke:var(--line); stroke-width:1.5; }
.arrow { fill:none; stroke:var(--accent); stroke-width:2.5; }
.return { stroke-dasharray:5 6; }
.wire { fill:none; stroke:var(--muted); stroke-width:2.5; }
.roots { fill:none; stroke:var(--root); stroke-width:2; }
.water { fill:var(--water); fill-opacity:.14; stroke:var(--water); stroke-width:2; }
.leaf { fill:var(--accent); }
'''


def text_lines(lines, x, y, css='body', gap=24):
    return ''.join(f'<text class="{css}" x="{x}" y="{y + i * gap}">{escape(line)}</text>'
                   for i, line in enumerate(lines))


def svg_shell(figure, width, height, drawing):
    style = STYLE + ('.label {font-size:22px} .body {font-size:20px} .small {font-size:19px}' if width==320 else '')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title description">
<title id="title">{escape(figure['title'])}</title><desc id="description">{escape(figure['description'])}</desc>
<style>{style}</style><defs><marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 Z" fill="var(--accent)"/></marker></defs>
<rect width="{width}" height="{height}" rx="16" fill="var(--bg)"/>{drawing}</svg>\n'''


def plant(x, y):
    return f'''<g transform="translate({x} {y})"><path class="wire" d="M0 0 V-36"/>
<path class="leaf" d="M0-12 C-32-6-43-29-35-42 C-12-46 2-28 0-12 Z M0-22 C30-19 43-42 32-51 C10-50-1-38 0-22 Z"/>
<path class="wire" d="M-18 0 H18 L12 14 H-12 Z"/></g>'''


def root_paths(x, y, length=86):
    return f'''<g transform="translate({x} {y})"><path class="roots" d="M-7 0 C-20 25-3 44-28 {length} M0 0 C12 28-8 45 5 {length} M8 0 C31 32 11 53 32 {length}
M-12 25 L-32 42 M-14 45 L-38 61 M3 26 L22 43 M0 49 L-16 66 M18 37 L39 52 M23 61 L43 76"/></g>'''


def root_zones(figure, mobile=False):
    width = 320 if mobile else 800
    card_width = 280 if mobile else 240
    height = 1020 if mobile else 352
    drawing = ''
    for i, item in enumerate(figure['panels']):
        x, y = (20, 18 + i * 332) if mobile else (20 + i * 260, 16)
        center = x + card_width / 2
        drawing += f'<rect class="card" x="{x}" y="{y}" width="{card_width}" height="316" rx="12"/>'
        drawing += text_lines([item['title']], x+18, y+35, 'label')
        drawing += f'<rect class="card" x="{x+28}" y="{y+126}" width="{card_width-56}" height="107" rx="5"/>'
        drawing += plant(center, y+126)
        if i == 0:
            drawing += root_paths(center, y+140, 69)
            drawing += f'<path class="wire" d="M{x+29} {y+164} h18"/><path class="arrow" stroke-dasharray="2 7" d="M{x+48} {y+164} l42-17 M{x+48} {y+164} l42 12 M{x+48} {y+164} l42 35"/>'
        elif i == 1:
            drawing += root_paths(center, y+140, 54)
            drawing += f'<path class="wire" d="M{x+31} {y+194} L{x+card_width-31} {y+207}"/><path class="water" d="M{x+31} {y+190} L{x+card_width-31} {y+203} v4 L{x+31} {y+194} Z"/>'
            drawing += f'<path class="arrow" marker-end="url(#arrow)" d="M{x+44} {y+217} h{card_width-101}"/>'
        else:
            drawing += f'<path class="water" d="M{x+30} {y+152} h{card_width-60} v79 H{x+30} Z"/>'
            drawing += root_paths(center,y+140,67)
            drawing += f'<rect class="card" x="{center-15}" y="{y+216}" width="30" height="10" rx="4"/>'
            for bx, by in [(center,y+205),(center-10,y+193),(center+9,y+183),(center+3,y+166)]:
                drawing += f'<circle cx="{bx}" cy="{by}" r="3.5" fill="none" stroke="var(--water)" stroke-width="1.8"/>'
        drawing += text_lines(item['lines'], x+18, y+269, 'body', 23)
    return svg_shell(figure,width,height,drawing), width, height


def flow(figure, mobile=False):
    count = len(figure['steps'])
    if mobile:
        width, card_width, card_height = 320, 272, 145
        positions = [(24, 20+i*190) for i in range(count)]
        height = positions[-1][1]+card_height+108
    else:
        width, card_height = 800, 148
        if count == 5:
            card_width = 234
            positions = [(20,20),(283,20),(546,20),(546,225),(283,225)]
        else:
            card_width = 334
            positions = [(24,20),(442,20),(442,225),(24,225)]
        height = 466
    drawing = ''
    for i, (item,(x,y)) in enumerate(zip(figure['steps'],positions)):
        drawing += f'<rect class="card" x="{x}" y="{y}" width="{card_width}" height="{card_height}" rx="12"/>'
        drawing += f'<circle cx="{x+28}" cy="{y+28}" r="12" fill="var(--accent)"/><text x="{x+28}" y="{y+33}" text-anchor="middle" fill="var(--bg)" style="fill:var(--bg);font-size:14px;font-weight:700">{i+1}</text>'
        drawing += text_lines(textwrap.wrap(item['title'],26 if mobile or count==4 else 20),x+18,y+70,'label',25)
        drawing += text_lines(item['lines'],x+18,y+107,'body',22)
        if i < count-1:
            nx,ny=positions[i+1]
            if ny==y:
                start,end=(x+card_width+7,nx-9) if nx>x else (x-7,nx+card_width+9)
                path=f'M{start} {y+card_height/2} H{end}'
            else:
                path=f'M{x+card_width/2} {y+card_height+8} V{ny-10}'
            drawing += f'<path class="arrow" marker-end="url(#arrow)" d="{path}"/>'
    footer_y=height-55
    if mobile:
        last_x,last_y=positions[-1]
        drawing += f'<path class="arrow return" marker-end="url(#arrow)" d="M{last_x-3} {last_y+card_height/2} H10 V{positions[0][1]+card_height/2} H20"/>'
        footer=textwrap.wrap(figure['footer'],29)
        drawing += text_lines(footer,24,footer_y,'small',23)
    else:
        if count == 4:
            drawing += f'<path class="arrow return" marker-end="url(#arrow)" d="M{positions[-1][0]+card_width/2} 216 V178"/>'
        else:
            drawing += '<path class="arrow return" marker-end="url(#arrow)" d="M275 300 H10 V94 H14"/>'
        drawing += text_lines([figure['footer']],24,footer_y,'small')
    return svg_shell(figure,width,height,drawing),width,height


def render_svg(figure,mobile=False):
    return root_zones(figure,mobile) if figure['layout']=='root-zones' else flow(figure,mobile)
