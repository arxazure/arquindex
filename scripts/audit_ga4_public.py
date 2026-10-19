"""Read public HTML only: no JS execution, Analytics hits, forms or secrets."""
import concurrent.futures
import hashlib
import json
import re
import urllib.request
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit

BASE = 'https://www.arquindex.com.br/'
URLS = [BASE + p for p in ('', 'solucoes-documentais-brasil.html',
    'assets/js/arquindex-conversions-v1.js', 'alfresco-belo-horizonte/',
    'gestao-documental-belo-horizonte/', 'consultoria-lgpd-belo-horizonte/',
    'blog/montagem-de-databooks-de-engenharia/')]
URLS += ['https://guardadocumentalembh.arquindex.com.br/',
         'https://digitalizacaodedocumentosembh.arquindex.com.br/']

class Tags(HTMLParser):
    def __init__(self):
        super().__init__()
        self.scripts, self.forms, self.contacts = [], [], Counter()
    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == 'script' and d.get('src'):
            self.scripts.append(d['src'])
        if tag == 'form':
            self.forms.append({k: d.get(k, '') for k in ('id', 'action', 'method')})
        if tag == 'a':
            href = d.get('href', '')
            kind = ('whatsapp' if re.match(r'^(https?://)?(wa\.me/|api\.whatsapp\.com/|web\.whatsapp\.com/)', href, re.I)
                    else 'phone' if href.lower().startswith('tel:')
                    else 'email' if href.lower().startswith('mailto:') else '')
            if kind: self.contacts[kind] += 1

def fetch(url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent':'ArquindexGA4Audit/1.0', 'Cache-Control':'no-cache'})
        with urllib.request.urlopen(req, timeout=25) as r:
            body, final, status, mime = r.read(2_000_000), r.url, r.status, r.headers.get('content-type', '')
        s = body.decode('utf-8', 'replace')
        p = Tags(); p.feed(s)
        scripts = [urljoin(final, src) for src in p.scripts]
        tracker = [src for src in scripts if urlsplit(src).path.endswith('/arquindex-conversions-v1.js')]
        analytics = [src for src in scripts if re.search(r'googletagmanager|google-analytics|analytics', src, re.I)]
        result = dict(url=url, final_url=final, status=status, content_type=mime,
            sha256=hashlib.sha256(body).hexdigest(), tracker_tags=len(tracker),
            tracker_urls=tracker, analytics_scripts=analytics,
            measurement_ids=sorted(set(re.findall(r'\bG-[A-Z0-9]{6,}\b', s))),
            gtm_ids=sorted(set(re.findall(r'\bGTM-[A-Z0-9]+\b', s))),
            config_calls=re.findall(r"gtag\s*\(\s*['\"]config['\"]\s*,\s*['\"]([^'\"]+)['\"]", s),
            inline_gtag=bool(re.search(r'function\s+gtag\s*\(|window\.gtag\s*=', s)),
            lead_dispatch=bool(re.search(r"dispatchEvent\([\s\S]{0,100}arquindex:lead-confirmed", s)),
            forms=p.forms, contact_links=dict(p.contacts),
            duplicate_script_urls=[src for src,n in Counter(scripts).items() if n > 1])
        if url.endswith('.js'):
            result['matches_repo_bytes'] = body == Path('assets/js/arquindex-conversions-v1.js').read_bytes()
        # Inspect only same-origin JS referenced by the page, never load Google tags.
        local = [src for src in scripts if urlsplit(src).netloc == urlsplit(final).netloc
                 and not urlsplit(src).path.endswith('/arquindex-conversions-v1.js')][:15]
        result['local_scripts'] = local
        result['tag_loader_urls_in_source'] = sorted(set(re.findall(r'https://(?:www\.)?(?:googletagmanager\.com|google-analytics\.com)/[^\s<>\"\x27]+', s)))
        result['local_script_checks'] = []
        for src in local:
            try:
                with urllib.request.urlopen(src, timeout=12) as asset:
                    js = asset.read(500000).decode('utf-8', 'replace')
                result['local_script_checks'].append(dict(url=src,
                    measurement_ids=sorted(set(re.findall(r'\bG-[A-Z0-9]{6,}\b', js))),
                    has_gtag_or_gtm=bool(re.search(r'gtag|googletagmanager|GTM-', js))))
            except Exception as e:
                result['local_script_checks'].append(dict(url=src,error=str(e)))
        if p.forms:
            result['form_integration_evidence'] = [s[max(0,m.start()-60):m.end()+240]
                for m in list(re.finditer(r'addEventListener\([\x27\"]submit|fetch\(|arquindex:lead-confirmed|location\.assign|window\.open', s))[:8]]
        return result
    except Exception as e:
        return {'url':url, 'error':type(e).__name__ + ': ' + str(e)}

if __name__ == '__main__':
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        rows = list(pool.map(fetch, URLS))
    Path('ga4-public-audit.json').write_text(json.dumps(rows, ensure_ascii=False, indent=2))
    print(json.dumps(rows, ensure_ascii=False, indent=2))
