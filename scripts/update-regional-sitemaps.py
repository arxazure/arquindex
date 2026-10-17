import os,re,json,hashlib,subprocess,sys
from pathlib import Path
from urllib.parse import urlsplit
from urllib.request import Request,urlopen
from urllib.error import HTTPError
from xml.etree import ElementTree as ET
from datetime import datetime,timezone

BASE='https://www.arquindex.com.br'
NS='http://www.sitemaps.org/schemas/sitemap/0.9'
ET.register_namespace('',NS)
MAPS=['/digitalize/sitemap.xml','/seo-regional/gestao-documental-ecm-databooks/sitemap.xml']
work=Path('/tmp/arquindex-sitemap-update');work.mkdir(exist_ok=True)
def fetch(path):
    req=Request(BASE+path,headers={'User-Agent':'ArquindexSitemapValidation/1.0','Cache-Control':'no-cache'})
    with urlopen(req,timeout=35) as r:
        assert r.status==200
        return r.read()
def lftp_quote(s): return '"'+s.replace('\\','\\\\').replace('"','\\"')+'"'
def ftp(commands):
    user=os.environ['FTP_USER'];password=os.environ['FTP_PASS'];host=os.environ['FTP_HOST']
    script='set cmd:fail-exit yes\nset net:max-retries 2\nset net:timeout 25\nset ftp:ssl-force yes\nset ftp:ssl-protect-data yes\nset ssl:verify-certificate yes\nopen -u '+lftp_quote(user)+','+lftp_quote(password)+' '+lftp_quote(host)+'\n'+'\n'.join(commands)+'\nbye\n'
    result=subprocess.run(['lftp'],input=script,text=True,capture_output=True,timeout=240)
    if result.returncode:
        safe=(result.stderr or result.stdout).replace(password,'***')
        raise RuntimeError('FTPS falhou: '+safe[-1200:])

# Repair the observed accented source-directory mismatch without changing the content.
ascii_path='/seo-regional/gestao-documental-ecm-databooks/sabara/'
try: fetch(ascii_path)
except HTTPError as e:
    if e.code!=404: raise
    source=Path('seo-regional/gestao-documental-ecm-databooks/sabará/index.html')
    assert source.exists(),'Fonte Sabara ausente'
    target='public_html'+ascii_path
    ftp(['mkdir -f -p '+target,'put '+lftp_quote(str(source))+' -o '+target+'index.html'])
    assert b'<h1>' in fetch(ascii_path)
    print('PUBLIC_ROUTE_REPAIRED',BASE+ascii_path)

urls=[]
for path in MAPS:
    raw=fetch(path);root=ET.fromstring(raw)
    assert root.tag=='{'+NS+'}urlset'
    locs=[e.text for e in root.iter('{'+NS+'}loc')]
    assert len(locs)==len(set(locs)) and locs
    assert all(u.startswith(BASE+'/') for u in locs)
    for u in locs:
        page=fetch(urlsplit(u).path).decode('utf-8')
        canonical=re.search(r'<link\b[^>]*rel=[\'"]canonical[\'"][^>]*href=[\'"]([^\'"]+)',page,re.I)
        assert canonical and canonical.group(1)==u,('Canonical divergente',u)
        assert not re.search(r'<meta\b[^>]*name=[\'"]robots[\'"][^>]*content=[\'"][^\'"]*noindex',page,re.I)
    urls.extend(locs);print('SITEMAP_VALIDATED',BASE+path,'urls',len(locs))

robots=fetch('/robots.txt');robot_text=robots.decode('utf-8')
advertised=re.findall(r'^\s*Sitemap:\s*(\S+)',robot_text,re.M|re.I)
candidates=['/sitemap.xml']
for url in advertised:
    p=urlsplit(url)
    if p.netloc in {'www.arquindex.com.br','arquindex.com.br'} and p.path.count('/')==1 and p.path.endswith('.xml') and p.path not in candidates:
        candidates.append(p.path)
changes={};today=datetime.now(timezone.utc).date().isoformat()
for path in candidates[:8]:
    try: old=fetch(path);root=ET.fromstring(old)
    except (HTTPError,ET.ParseError) as e:
        if path=='/sitemap.xml': raise
        print('EXISTING_MAP_UNAVAILABLE',path,type(e).__name__);continue
    existing={e.text for e in root.iter('{'+NS+'}loc')};added=0
    if root.tag=='{'+NS+'}sitemapindex':
        targets=[BASE+p for p in MAPS];child='sitemap'
    elif root.tag=='{'+NS+'}urlset': targets=list(dict.fromkeys(urls));child='url'
    else: raise ValueError('Tipo XML inesperado: '+path)
    for url in targets:
        if url in existing: continue
        entry=ET.SubElement(root,'{'+NS+'}'+child)
        ET.SubElement(entry,'{'+NS+'}loc').text=url
        ET.SubElement(entry,'{'+NS+'}lastmod').text=today
        added+=1
    if added: changes[path]=(old,ET.tostring(root,encoding='utf-8',xml_declaration=True))
    print('ROOT_SITEMAP_CHECKED',BASE+path,'adicionados',added)
for path in ['/sitemap.xml']+MAPS:
    line='Sitemap: '+BASE+path
    if line not in robot_text: robot_text=robot_text.rstrip()+'\n'+line+'\n'
if robot_text.encode()!=robots:changes['/robots.txt']=(robots,robot_text.encode())

backup='seo-backups/sitemap-regional-'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
if changes:
    # Check the live originals again over FTPS to avoid overwriting concurrent edits.
    checks=[]
    for i,(path,(old,new)) in enumerate(changes.items()):
        (work/f'{i}-old').write_bytes(old);(work/f'{i}-new').write_bytes(new)
        checks.append('get public_html'+path+' -o '+str(work/f'{i}-live'))
    ftp(checks)
    for i,(path,(old,new)) in enumerate(changes.items()): assert (work/f'{i}-live').read_bytes()==old,('Alteracao concorrente',path)
    commands=['mkdir -f -p '+backup]
    for i,(path,(old,new)) in enumerate(changes.items()):
        commands+=['put '+str(work/f'{i}-old')+' -o '+backup+'/'+path.lstrip('/'),'put '+str(work/f'{i}-new')+' -o public_html'+path]
    ftp(commands)
    try:
        for path,(old,new) in changes.items(): assert fetch(path)==new,('Divergencia publica',path)
    except Exception:
        ftp(['put '+str(work/f'{i}-old')+' -o public_html'+path for i,path in enumerate(changes)])
        print('ROLLBACK_APPLIED');raise
    print('SITEMAPS_UPDATED',len(changes),'BACKUP',backup)
else: print('SITEMAPS_ALREADY_CURRENT')
print('GOOGLE_SUBMISSION_REQUIRED',*[BASE+p for p in ['/sitemap.xml']+MAPS],sep='\n')
