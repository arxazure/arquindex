import ftplib, hashlib, html, io, json, os, posixpath, re, time, urllib.request
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit
from bs4 import BeautifulSoup

STAMP=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
PASSWORD=os.environ['FTP_PASSWORD']
TARGETS=[x.strip() for x in os.environ.get('ATENDIMENTO_TARGETS','').split(',') if x.strip()]
WIDGET=Path('conteudo/publicacao/_atendimento-flutuante.html').read_text('utf-8')
assert TARGETS, 'NO_TARGETS'
assert 'id="arq-floating"' in WIDGET and 'id="arq-dedup-floats"' in WIDGET

def get(ftp,path):
    b=bytearray(); ftp.retrbinary('RETR '+path,b.extend); return bytes(b)

def put_atomic(ftp,path,data,suffix):
    directory=posixpath.dirname(path); name=posixpath.basename(path)
    temp=posixpath.join(directory,'.'+name+'.tmp-'+suffix)
    ftp.storbinary('STOR '+temp,io.BytesIO(data))
    assert get(ftp,temp)==data, 'TEMP_HASH '+path
    try: ftp.delete(path)
    except ftplib.error_perm as exc:
        if not str(exc).startswith('550'): raise
    ftp.rename(temp,path)
    assert get(ftp,path)==data, 'FINAL_HASH '+path

def mkdir(ftp,path):
    current=ftp.pwd()
    try:
        ftp.cwd('/')
        for part in path.strip('/').split('/'):
            if not part: continue
            try: ftp.mkd(part)
            except ftplib.error_perm as exc:
                if not str(exc).startswith('550'): raise
            ftp.cwd(part)
    finally:
        ftp.cwd(current)

def seo_identity(soup):
    title=soup.title.get_text(strip=True) if soup.title else ''
    canonical=[x.get('href','') for x in soup.find_all('link',rel=lambda v:v and 'canonical' in v)]
    h1=[x.get_text(' ',strip=True) for x in soup.find_all('h1')]
    desc=''
    m=soup.find('meta',attrs={'name':re.compile('^description$',re.I)})
    if m: desc=m.get('content','')
    return title,canonical,h1,desc

def locate(ftp,base,url):
    p=urlsplit(url); host=p.hostname; filename=p.path.lstrip('/') or 'index.html'
    candidates=[
        base+'/subdominios/'+host, base+'/'+host,
        '/subdominios/'+host, '/'+host
    ]
    for root in dict.fromkeys(candidates):
        try:
            data=get(ftp,root+'/'+filename)
            if '<html' in data.decode('utf-8','ignore').lower():
                return root+'/'+filename
        except ftplib.all_errors:
            pass
    raise RuntimeError('TARGET_NOT_FOUND '+url)

def transform(original):
    soup=BeautifulSoup(original.decode('utf-8'),'html.parser')
    assert soup.head and soup.body, 'HTML_STRUCTURE'
    before=seo_identity(soup)

    for selector in ['#arq-floating-style','#arq-floating','#arq-floating-script','#arq-dedup-floats','.aq-brand-wa']:
        for node in soup.select(selector): node.decompose()

    for node in list(soup.find_all('script')):
        src=(node.get('src') or '').lower()
        text=node.string or node.get_text() or ''
        if ('__arqWhatsappOptions' in text or
            'whatsapp_replace_crisp/jquery.js' in src or
            'whatsapp_replace_crisp/user_main.js' in src or
            'watiwidget.js' in src):
            node.decompose()

    fragment=BeautifulSoup(WIDGET,'html.parser')
    for node in list(fragment.contents):
        soup.body.append(node)

    assert seo_identity(soup)==before, 'SEO_IDENTITY_CHANGED'
    result=str(soup).encode('utf-8')
    rendered=result.decode('utf-8')
    checks={
        'one_widget':rendered.count('id="arq-floating"')==1,
        'one_toggle':rendered.count('id="arq-float-toggle"')==1,
        'no_brand_float':'aq-brand-wa' not in rendered,
        'no_old_config':'__arqWhatsappOptions' not in rendered,
        'no_old_loader':'whatsapp_replace_crisp' not in rendered and 'watiWidget.js' not in rendered,
        'chat_option':'Conversar no chat' in rendered,
        'whatsapp_option':'https://wa.me/5531973632725' in rendered,
        'proposal_option':'solicitar-proposta-contratacao.html' in rendered
    }
    assert all(checks.values()), checks
    return result,checks,before

def public(url):
    sep='&' if '?' in url else '?'
    req=urllib.request.Request(url+sep+'atendcheck='+STAMP,headers={'User-Agent':'ArquindexAtendimento/1.0','Cache-Control':'no-cache'})
    with urllib.request.urlopen(req,timeout=35) as r:
        body=r.read(4000000)
        return r.status,body

with ftplib.FTP_TLS(timeout=60) as ftp:
    ftp.connect('ftp.arquindex.com.br',21); ftp.login('arquind2',PASSWORD); ftp.prot_p(); ftp.set_pasv(True)
    base=None
    for candidate in ['/public_html','/home/arquind2/public_html']:
        try:
            if b'arquindex' in get(ftp,candidate+'/index.html').lower(): base=candidate; break
        except ftplib.all_errors: pass
    assert base, 'PUBLIC_ROOT_NOT_FOUND'

    records=[]
    for url in TARGETS:
        path=locate(ftp,base,url); original=get(ftp,path)
        updated,checks,seo=transform(original)
        records.append((url,path,original,updated,checks,seo))
        print('TARGET_CONFIRMED',url,path,hashlib.sha256(original).hexdigest(),flush=True)

    backup='/seo-backups/atendimento-unico-'+STAMP
    mkdir(ftp,backup)
    ftp.storbinary('STOR '+backup+'/.htaccess',io.BytesIO(b'Options -Indexes\nRequire all denied\n'))
    for url,path,original,updated,checks,seo in records:
        name=hashlib.sha256(path.encode()).hexdigest()[:20]+'.html'
        bpath=backup+'/'+name
        ftp.storbinary('STOR '+bpath,io.BytesIO(original))
        assert get(ftp,bpath)==original
        print('BACKUP_VERIFIED',url,bpath,hashlib.sha256(original).hexdigest(),flush=True)

    written=[]
    report=[]
    try:
        for url,path,original,updated,checks,seo in records:
            if get(ftp,path)!=original: raise RuntimeError('CONCURRENT_CHANGE '+url)
        for url,path,original,updated,checks,seo in records:
            put_atomic(ftp,path,updated,STAMP); written.append((path,original))
            print('FTP_PUBLISHED_VERIFIED',url,path,hashlib.sha256(updated).hexdigest(),checks,flush=True)
        for url,path,original,updated,checks,seo in records:
            last=None
            for attempt in range(3):
                try:
                    status,body=public(url); text=body.decode('utf-8','replace')
                    public_checks={
                        'http_200':status==200,
                        'one_widget':text.count('id="arq-floating"')==1,
                        'one_toggle':text.count('id="arq-float-toggle"')==1,
                        'no_brand_float':'aq-brand-wa' not in text,
                        'no_old_config':'__arqWhatsappOptions' not in text,
                        'no_old_loader':'whatsapp_replace_crisp' not in text and 'watiWidget.js' not in text,
                        'chat_option':'Conversar no chat' in text,
                        'whatsapp_option':'https://wa.me/5531973632725' in text,
                        'proposal_option':'solicitar-proposta-contratacao.html' in text,
                        'title_preserved':seo[0] in html.unescape(text),
                        'h1_preserved':all(x in html.unescape(text) for x in seo[2]),
                        'indexable':'noindex' not in text.lower()
                    }
                    if not all(public_checks.values()): raise RuntimeError(repr(public_checks))
                    row={'url':url,'path':path,'sha256':hashlib.sha256(updated).hexdigest(),'state':'public_verified','checks':public_checks}
                    report.append(row)
                    print('PUBLIC_VERIFIED',json.dumps(row,ensure_ascii=False),flush=True)
                    last=None; break
                except Exception as exc:
                    last=exc
                    if attempt<2: time.sleep(5)
            if last: raise last
    except Exception:
        for path,original in written: put_atomic(ftp,path,original,'rollback-'+STAMP)
        print('ROLLBACK_COMPLETED',','.join(path for path,_ in written),flush=True)
        raise

Path('design-report').mkdir(exist_ok=True)
Path('design-report/atendimento-unico.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),'utf-8')
