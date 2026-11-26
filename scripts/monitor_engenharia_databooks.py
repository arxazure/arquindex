#!/usr/bin/env python3
"""Auditoria somente leitura; Python 3.11+, sem dependências externas."""
import argparse, csv, hashlib, json, re, sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit
from urllib.request import Request, HTTPRedirectHandler, build_opener
from urllib.error import HTTPError


def allowed(url):
    p = urlsplit(url)
    return (p.scheme == 'https' and not p.username and not p.password
            and p.port in (None, 443) and
            (p.hostname == 'arquindex.com.br' or (p.hostname or '').endswith('.arquindex.com.br')))


class SafeRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if not allowed(newurl):
            raise ValueError('Redirecionamento fora do domínio autorizado')
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def fetch(url):
    if not allowed(url):
        raise ValueError('URL fora do domínio HTTPS autorizado')
    with build_opener(SafeRedirect()).open(Request(url, headers={'User-Agent': 'Arquindex-ReadOnly-QA/1.0'}), timeout=10) as r:
        data = r.read(2_000_001)
        if len(data) > 2_000_000:
            raise ValueError('Resposta excede limite de 2 MB')
        return r.status, r.url, {k.lower(): v for k,v in r.headers.items()}, data.decode('utf-8', errors='replace')


class Page(HTMLParser):
    def __init__(self):
        super().__init__(); self.canonical=[]; self.h1=0; self.links=[]; self.robots=[]; self.title=False; self.titles=[]
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if tag=='h1': self.h1+=1
        if tag=='title': self.title=True
        if tag=='link' and 'canonical' in a.get('rel','').lower().split(): self.canonical.append(a.get('href',''))
        if tag=='a' and a.get('href'): self.links.append(a['href'])
        if tag=='meta' and a.get('name','').lower() in ('robots','googlebot'): self.robots.append(a.get('content',''))
    def handle_endtag(self, tag):
        if tag=='title': self.title=False
    def handle_data(self, data):
        if self.title: self.titles.append(data)


def check(item):
    row={'id':item['id'],'url':item['url'],'checked_at':datetime.now(timezone.utc).isoformat(),'indexacao':'nao_verificada'}
    try:
        status, final, headers, body=fetch(item['url']); p=Page(); p.feed(body)
        row.update(http=status,final_url=final,title=''.join(p.titles).strip(),h1=p.h1,canonicals=p.canonical,
                   noindex=bool(re.search(r'\bnoindex\b', ' '.join(p.robots)+' '+headers.get('x-robots-tag',''), re.I)),
                   content_hash=hashlib.sha256(body.encode()).hexdigest(),
                   links=sorted(set(urljoin(final,x) for x in p.links if allowed(urljoin(final,x)))))
        from urllib.robotparser import RobotFileParser
        origin='https://'+urlsplit(final).netloc
        try:
            _,_,_,robots=fetch(origin+'/robots.txt'); rp=RobotFileParser(); rp.parse(robots.splitlines())
            row['robots_googlebot_allowed']=rp.can_fetch('Googlebot',final)
        except Exception as e: row['robots_error']=str(e)
        row['issues']=[]
        if len(p.canonical)!=1: row['issues'].append('canonical_ausente_ou_multiplo')
        elif not allowed(p.canonical[0]): row['issues'].append('canonical_nao_absoluto_ou_fora_do_dominio')
        elif p.canonical[0] != final: row['issues'].append('canonical_diferente_da_url_final')
        if p.h1!=1: row['issues'].append('h1_ausente_ou_multiplo')
        if not row['title']: row['issues'].append('title_ausente')
        if row['noindex']: row['issues'].append('noindex')
        if row.get('robots_googlebot_allowed') is False: row['issues'].append('robots_bloqueia_googlebot')
        if 'robots_error' in row: row['issues'].append('robots_nao_verificado')
    except HTTPError as e: row.update(http=e.code,error=str(e),issues=['http_nao_200'])
    except Exception as e: row.update(http=None,error=str(e),issues=['acesso_nao_verificado'])
    return row


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--fila',default='seo/fila-seo-geo-aeo.csv'); ap.add_argument('--output',default='resultado.json'); ap.add_argument('--previous'); args=ap.parse_args()
    with open(args.fila,encoding='utf-8-sig',newline='') as f:
        items=[r for r in csv.DictReader(f,delimiter=';') if re.search('engenharia|databook', ' '.join([r.get('servico',''),r.get('consulta_alvo',''),r.get('url','')]),re.I)]
    items=list({i['url']:i for i in items}.values())
    if not items:
        raise ValueError('Fila sem URLs de engenharia/Databooks; auditoria vazia não é sucesso')
    with ThreadPoolExecutor(max_workers=3) as pool: rows=list(pool.map(check,items))
    old={r['url']:r for r in json.loads(Path(args.previous).read_text())} if args.previous and Path(args.previous).exists() else {}
    for r in rows:
        before=old.get(r['url']); r['change']='baseline' if not old else ('new' if before is None else ('changed' if any(r.get(k)!=before.get(k) for k in ('http','content_hash','canonicals','h1','noindex','issues')) else 'unchanged'))
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'paginas':len(rows),'alertas':sum(bool(r['issues']) for r in rows),'arquivo':args.output},ensure_ascii=False))
    return int(any(r['issues'] for r in rows))

if __name__=='__main__': sys.exit(main())
