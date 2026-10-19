"""Read-only public audit. Never treats FTP presence or HTTP 200 alone as success."""
import concurrent.futures as cf
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import socket
import sys
import ssl
import urllib.parse as up
import urllib.robotparser
import xml.etree.ElementTree as ET
import requests
from bs4 import BeautifulSoup

ROOT = Path('seo-regional/56-sites')
OUT = Path('audit-56')

def fetch(url):
    try:
        r = requests.get(url, timeout=(8, 20), headers={'User-Agent': 'Arquindex-Audit/1.0'}, allow_redirects=True)
        return {'requested': url, 'status': r.status_code, 'url': r.url,
                'redirects': [{'status': h.status_code, 'url': h.url, 'location': h.headers.get('Location')} for h in r.history],
                'headers': dict(r.headers), 'text': r.text, 'sha256': hashlib.sha256(r.content).hexdigest()}
    except requests.RequestException as e:
        return {'requested': url, 'error': str(e)}

def parsed(text):
    s = BeautifulSoup(text, 'html.parser')
    canon = [x.get('href', '') for x in s.select('link[rel~=canonical]')]
    for x in s(['script', 'style', 'nav', 'footer']): x.decompose()
    return {'title': [x.get_text(' ', strip=True) for x in s.find_all('title')],
            'h1': [x.get_text(' ', strip=True) for x in s.find_all('h1')],
            'canonical': canon, 'text_words': len(s.get_text(' ', strip=True).split()),
            'sample': s.get_text(' ', strip=True)[:700]}

def audit(entry):
    host = entry['host']; base = 'https://' + host + '/'
    a = {'host': host, 'checked_at': dt.datetime.now(dt.timezone.utc).isoformat(), 'issues': []}
    try:
        a['dns'] = sorted({v[4][0] for v in socket.getaddrinfo(host, 443, type=socket.SOCK_STREAM)})
    except OSError as e:
        a['dns_error'] = str(e); a['issues'].append('DNS indisponível')
    try:
        with socket.create_connection((host, 443), timeout=8) as sock:
            with ssl.create_default_context().wrap_socket(sock, server_hostname=host) as tls:
                c = tls.getpeercert()
                a['tls'] = {'valid': True, 'notAfter': c.get('notAfter'), 'SAN': c.get('subjectAltName'), 'version': tls.version()}
    except OSError as e:
        a['tls'] = {'valid': False, 'error': str(e)}; a['issues'].append('TLS não validado')
    for key, url in [('page', base), ('http', 'http://' + host + '/'), ('robots', base+'robots.txt'), ('sitemap', base+'sitemap.xml')]:
        a[key] = fetch(url)
    page = a['page']
    if page.get('status') != 200: a['issues'].append('HTTPS sem HTTP 200')
    if page.get('url') and page['url'] != base: a['issues'].append('Destino HTTPS diferente da raiz esperada')
    if a['http'].get('status') and (a['http'].get('url') != base or not a['http'].get('redirects')): a['issues'].append('HTTP não redireciona à raiz HTTPS')
    if page.get('status') == 200:
        a['html'] = parsed(page['text']); local = parsed((ROOT/host/'index.html').read_text())
        a['expected'] = local
        for key in ['title', 'h1', 'canonical']:
            if len(a['html'][key]) != 1: a['issues'].append(key+' ausente/múltiplo')
            if a['html'][key] != local[key]: a['issues'].append(key+' diverge do manifesto de conteúdo')
        if a['html']['canonical'] != [base]: a['issues'].append('canonical não é próprio')
        if a['html']['text_words'] < 300: a['issues'].append('Conteúdo ausente/curto')
        soup = BeautifulSoup(page['text'], 'html.parser')
        directives = ' '.join(x.get('content','') for x in soup.select('meta[name=robots],meta[name=googlebot]')) + ' ' + page['headers'].get('X-Robots-Tag','')
        if 'noindex' in directives.lower(): a['issues'].append('noindex público')
        a['robots_directives'] = directives
        links = sorted({up.urljoin(base, x.get('href','')) for x in soup.select('a[href]')})
        a['commercial_links'] = [x for x in links if any(v in x for v in ['wa.me', 'api.whatsapp.com', 'solicitar-proposta', 'contato', 'contratacao'])]
        a['link_tests'] = []
        for url in a['commercial_links']:
            if up.urlparse(url).hostname in ['wa.me','api.whatsapp.com']:
                a['link_tests'].append({'url':url,'result':'syntax_only; no message sent'})
            elif up.urlparse(url).scheme in ['http','https']:
                t=fetch(url); t.pop('text',None); a['link_tests'].append(t)
                if t.get('status') != 200: a['issues'].append('Destino comercial sem HTTP 200')
        if not a['commercial_links']: a['issues'].append('Link comercial ausente')
    robots=a['robots']; sitemap=a['sitemap']
    if robots.get('status') != 200 or up.urlparse(robots.get('url','')).hostname != host:
        a['issues'].append('robots indisponível/redirecionado')
    else:
        rp=urllib.robotparser.RobotFileParser(); rp.parse(robots['text'].splitlines())
        a['robots_allows_root']=rp.can_fetch('Googlebot',base)
        if not a['robots_allows_root']: a['issues'].append('robots bloqueia raiz')
        if base+'sitemap.xml' not in robots['text']: a['issues'].append('Sitemap não anunciado em robots')
    if sitemap.get('status') != 200 or up.urlparse(sitemap.get('url','')).hostname != host:
        a['issues'].append('sitemap indisponível/redirecionado')
    else:
        try:
            xml=ET.fromstring(sitemap['text'])
            locs=[x.text or '' for x in xml.iter() if x.tag.split('}')[-1]=='loc']; a['sitemap_locs']=locs
            if base not in locs: a['issues'].append('Raiz canônica ausente no sitemap')
            if any(up.urlparse(x).scheme!='https' or up.urlparse(x).hostname!=host for x in locs): a['issues'].append('Sitemap contém URL relativa/externa/HTTP')
            a['sitemap_tests']=[]
            for url in locs:
                if url == base: continue
                if up.urlparse(url).hostname==host and up.urlparse(url).scheme=='https':
                    t=fetch(url); t.pop('text',None); a['sitemap_tests'].append(t)
                    if t.get('status')!=200 or t.get('url')!=url: a['issues'].append('URL sitemap não retorna 200 direto')
        except ET.ParseError as e:
            a['sitemap_error']=str(e); a['issues'].append('XML sitemap inválido')
    a['classification']=('DNS indisponível; demais camadas não verificáveis' if not a.get('dns') else ('conteúdo de outro destino/alias; preservar aplicação' if a.get('html',{}).get('canonical')==['https://www.arquindex.com.br/'] else ('funcional nos testes técnicos' if not a['issues'] else 'falha ou divergência; revisar evidência')))
    if not a.get('dns'):
        a['issues']=['DNS indisponível; TLS/HTTP/conteúdo/SEO não verificáveis']
    for k in ['page','http','robots','sitemap']:
        a[k].pop('text',None)
    print(host, a['classification'], a['issues'], flush=True)
    return a

def public_gate(results, preflight=False):
    if preflight:
        return len(results)==56 and all(a.get('dns') and a['tls']['valid'] and a['page'].get('status')==200 and a['page'].get('url')=='https://'+a['host']+'/' and a.get('html',{}).get('canonical')==['https://'+a['host']+'/'] for a in results)
    return len(results)==56 and all(not a['issues'] for a in results)

def main():
    entries=json.loads((ROOT/'manifest.json').read_text())
    assert len(entries)==56 and len({e['host'] for e in entries})==56
    OUT.mkdir(exist_ok=True)
    with cf.ThreadPoolExecutor(max_workers=6) as pool: results=list(pool.map(audit, entries))
    (OUT/'results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
    counts=sum(not a['issues'] for a in results)
    lines=['## Auditoria pública individual dos 56 subdomínios', '',
           f'Commit auditado: `{os.getenv("GITHUB_SHA","local")}`. Execução: '+os.getenv('AUDIT_RUN_URL','local'), '',
           f'{counts}/56 sem falhas nos testes; {56-counts}/56 com falhas ou divergências. Evidência DNS/TLS/HTTP e detalhes de title, H1, canonical, robots, sitemap e links no artefato audit-56/results.json.',
           '', 'Auditoria somente leitura, sem deploy, sem submissão de indexação. Raiz principal e ARQ-007/008/009 preservadas. HTTP 200 não comprova indexação. Falha de rede não prova conteúdo ausente.', '',
           '| Endereço | DNS | TLS | HTTPS / HTTP final | Resultado |','|---|---|---|---|---|']
    for a in results:
        lines.append('| https://'+a['host']+'/ | '+(', '.join(a.get('dns',[])) or 'erro')+' | '+('válido' if a['tls']['valid'] else 'erro')+' | '+str(a['page'].get('status','erro'))+' / '+str(a['http'].get('status','erro'))+' | '+('; '.join(a['issues']) or 'funcional nos testes técnicos')+' |')
    (OUT/'report.md').write_text('\n'.join(lines)+'\n')
    if '--gate' in sys.argv or '--preflight-gate' in sys.argv:
        if not public_gate(results, '--preflight-gate' in sys.argv):
            raise SystemExit('PUBLIC_VALIDATION_FAILED: publicação não aprovada; consulte audit-56/results.json')
if __name__=='__main__': main()
