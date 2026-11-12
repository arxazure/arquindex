"""Dependency-free structural QA for the PR Digital package."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import json
import sys
import xml.etree.ElementTree as ET

BASE = 'https://www.arquindex.com.br'
ROOT = Path(__file__).resolve().parents[1]
SLUGS = ('', 'custo-oculto-transformacao-digital/', 'ia-local-governanca-documental/', 'databooks-digitais-engenharia/', 'calculadora-tco/')
URLS = {BASE + '/pr-digital/' + slug for slug in SLUGS}
ARTICLES = set(SLUGS[1:4])

class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.canonicals, self.links, self.assets, self.schemas = [], [], [], []
        self.h1, self.ids, self.metas, self.titles = [], set(), {}, []
        self.lang = None
        self.capture = None
        self.buffer = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a:
            self.ids.add(a['id'])
        if tag == 'html': self.lang = a.get('lang')
        if tag == 'meta': self.metas[a.get('name', a.get('property'))] = a.get('content', '')
        if tag == 'link' and 'canonical' in a.get('rel', '').split(): self.canonicals.append(a.get('href'))
        if tag == 'a': self.links.append(a.get('href', ''))
        if tag in ('img', 'script') and a.get('src'): self.assets.append(a['src'])
        if tag == 'script' and a.get('type') == 'application/ld+json': self.capture, self.buffer = 'schema', []
        elif tag in ('title', 'h1'): self.capture, self.buffer = tag, []
    def handle_data(self, text):
        if self.capture: self.buffer.append(text)
    def handle_endtag(self, tag):
        if (tag == 'script' and self.capture == 'schema') or tag == self.capture:
            text = ''.join(self.buffer).strip()
            if self.capture == 'schema': self.schemas.append(json.loads(text))
            elif self.capture == 'title': self.titles.append(text)
            elif self.capture == 'h1': self.h1.append(text)
            self.capture = None

def validate(root=ROOT):
    errors, parsed = [], {}
    def check(ok, message):
        if not ok: errors.append(message)
    for slug in SLUGS:
        relative = 'pr-digital/' + slug + 'index.html'
        path = root / relative
        if not path.is_file():
            errors.append('Missing page: ' + relative)
            continue
        page = Page()
        try: page.feed(path.read_text(encoding='utf-8')); page.close()
        except (ValueError, json.JSONDecodeError) as exc:
            errors.append(relative + ': invalid JSON-LD: ' + str(exc)); continue
        parsed[relative] = page
        url = BASE + '/pr-digital/' + slug
        check(page.lang == 'pt-BR', relative + ': lang')
        check(len(page.titles) == 1 and bool(page.titles[0]), relative + ': unique nonempty title')
        check(len(page.h1) == 1 and bool(page.h1[0]), relative + ': unique nonempty H1')
        check(bool(page.metas.get('description', '').strip()), relative + ': description')
        check(page.canonicals == [url], relative + ': canonical must be unique and self-referencing')
        check(any(link.startswith(BASE + '/pr-digital/') and link != url for link in page.links), relative + ': actual editorial links required')
        if slug in ARTICLES:
            check(len(page.schemas) == 1, relative + ': one TechArticle required')
            for schema in page.schemas:
                check(schema.get('@context') == 'https://schema.org' and schema.get('@type') == 'TechArticle', relative + ': schema type/context')
                check(schema.get('headline') == page.h1[0], relative + ': schema headline')
                check(schema.get('description') == page.metas.get('description'), relative + ': schema description')
                check(schema.get('mainEntityOfPage') == url, relative + ': schema URL')
                check(schema.get('author', {}).get('name') == 'Arquindex', relative + ': author')
                check(schema.get('publisher', {}).get('url') == BASE + '/', relative + ': publisher')
                check(page.metas.get('og:url') == url, relative + ': og:url')
    for relative, page in parsed.items():
        for link in page.links + page.assets:
            target = urlsplit(link)
            if target.scheme not in ('', 'https', 'mailto', 'tel'):
                errors.append(relative + ': unsafe/insecure link ' + link)
            if target.netloc == 'www.arquindex.com.br' and target.path.startswith('/pr-digital/'):
                clean = unquote(target.path).lstrip('/')
                destination = root / (clean + 'index.html' if clean.endswith('/') else clean)
                check(destination.is_file(), relative + ': missing internal target ' + link)
                if target.fragment:
                    target_page = parsed.get(str(destination.relative_to(root)))
                    check(target_page is not None and target.fragment in target_page.ids, relative + ': missing anchor ' + link)
    try:
        tree = ET.parse(root / 'pr-digital/sitemap.xml')
        ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        locations = [x.text for x in tree.findall('s:url/s:loc', ns)]
        check(tree.getroot().tag == '{http://www.sitemaps.org/schemas/sitemap/0.9}urlset', 'Sitemap namespace/root')
        check(len(locations) == len(URLS) and set(locations) == URLS, 'Sitemap must contain the five unique canonical URLs')
    except (ET.ParseError, OSError) as exc: errors.append('Invalid sitemap: ' + str(exc))
    return errors

if __name__ == '__main__':
    failures = validate()
    for error in failures: print('FAIL:', error, file=sys.stderr)
    if failures: sys.exit(1)
    print('PASS: five pages; canonical tags, editorial links, JSON-LD and sitemap parsed and validated.')
