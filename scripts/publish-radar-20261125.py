"""Publicacao editorial limitada ao radar autorizado em 25/11/2026."""
import ftplib, ssl, socket, os, io, json, hashlib, time, sys, re
from pathlib import Path
from datetime import datetime, timezone
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
BASE='https://www.arquindex.com.br/'
MARK=b'ARQ-RADAR-20261125'
ROWS=json.loads((ROOT/'seo/radar-20261125-manifest.json').read_text())
OUT=ROOT/'publish-report/radar-20261125'
OUT.mkdir(parents=True,exist_ok=True)
report={'published':False,'pages':[],'commit':os.getenv('GITHUB_SHA')}
def save():
 (OUT/'publication.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
def digest(b): return hashlib.sha256(b).hexdigest()
def http(url):
 with urlopen(Request(url,headers={'User-Agent':'ArquindexEditorialCheck/1.0','Cache-Control':'no-cache'}),timeout=35) as r:
  return r.status,r.url,r.headers,r.read()
def get(f,p):
 b=bytearray()
 try: f.retrbinary('RETR '+p,b.extend)
 except ftplib.error_perm as e:
  if str(e).startswith('550'): return None
  raise
 return bytes(b)
def mkdir(f,p):
 cur=''
 for bit in p.strip('/').split('/'):
  cur+='/'+bit
  try: f.mkd(cur)
  except ftplib.error_perm:
   f.cwd(cur)
def put(f,p,b):
 mkdir(f,p.rsplit('/',1)[0]);f.storbinary('STOR '+p,io.BytesIO(b))
 assert get(f,p)==b,'FTPS_READBACK_MISMATCH'
def check():
 from html.parser import HTMLParser
 class Parser(HTMLParser):
  def __init__(self): super().__init__();self.h1=0;self.canonical=[];self.links=[]
  def handle_starttag(self,t,a):
   a=dict(a)
   if t=='h1':self.h1+=1
   if t=='link' and a.get('rel')=='canonical':self.canonical.append(a.get('href'))
   if t=='a':self.links.append(a.get('href',''))
 paths={r['url'] for r in ROWS}
 for r in ROWS:
  b=(ROOT/r['path']).read_bytes();assert MARK in b
  p=Parser();p.feed(b.decode());assert p.h1==1 and p.canonical==[r['url']]
  assert b'noindex' not in b
  for link in p.links:
   if link.startswith('/open-source-documental/radar/'):assert BASE.rstrip('/')+link in paths,link
  assert b'SMS DP' not in b and b'/root/' not in b
 ET.fromstring((ROOT/'sitemap-radar-20261125.xml').read_bytes())
 print('LOCAL_CHECK_OK',len(ROWS),flush=True)
def publish():
 check()
 # Origin identity must match both the public domain and the verified HomeHost endpoint.
 status,final,headers,public_home=http(BASE)
 assert status==200 and 'arquindex' in public_home.decode('utf-8','replace').lower(),'PUBLIC_ORIGIN_UNAVAILABLE'
 host=os.getenv('FTP_TLS_HOST') or 'h59.servidorhh.com'
 assert host in ('h59.servidorhh.com','ftp.arquindex.com.br'),'UNREVIEWED_FTPS_HOST'
 ips=set(socket.gethostbyname_ex('ftp.arquindex.com.br')[2])
 assert ips & set(socket.gethostbyname_ex(host)[2]),'FTPS_ORIGIN_IP_MISMATCH'
 previous={};applied=[]
 with ftplib.FTP_TLS(context=ssl.create_default_context(),timeout=45) as f:
  f.connect(host,21);f.login('arquind2',os.environ['FTP_PASSWORD']);f.prot_p()
  home=get(f,'/public_html/index.html') or get(f,'/public_html/index.php')
  assert home and b'arquindex' in home.lower(),'PUBLIC_ROOT_NOT_CONFIRMED'
  planned={'/public_html/'+r['path']:(ROOT/r['path']).read_bytes() for r in ROWS}
  planned['/public_html/sitemap-radar-20261125.xml']=(ROOT/'sitemap-radar-20261125.xml').read_bytes()
  for r in ROWS:
   old=get(f,'/public_html/'+r['path'])
   assert old is None or MARK in old,'EXISTING_ARTICLE_REQUIRES_REVIEW'
  nav='/public_html/open-source-documental/alfresco/index.html'
  old=get(f,nav)
  if old:
   public=http(BASE+'open-source-documental/alfresco/')[3]
   assert digest(public)==digest(old),'PORTAL_ORIGIN_MISMATCH'
   assert b'</main>' in old,'PORTAL_STRUCTURE_CHANGED'
   if MARK not in old:
    block=b'<section id="arq-radar-20261125"><!-- ARQ-RADAR-20261125 --><h2>Radar documental de 25/11/2026</h2><p><a href="/open-source-documental/radar/2026-11-25/">Alfresco, OpenArch, Nextcloud, Omeka e Hostinger: fontes, riscos e testes de homologacao</a></p></section>'
    planned[nav]=old.replace(b'</main>',block+b'</main>',1)
  NS='http://www.sitemaps.org/schemas/sitemap/0.9';ET.register_namespace('',NS)
  sitemap='/public_html/sitemap.xml';raw=get(f,sitemap)
  if raw:
   tree=ET.fromstring(raw);locs={x.text for x in tree.iter('{'+NS+'}loc')}
   if tree.tag=='{'+NS+'}sitemapindex':
    u=BASE+'sitemap-radar-20261125.xml'
    if u not in locs:n=ET.SubElement(tree,'{'+NS+'}sitemap');ET.SubElement(n,'{'+NS+'}loc').text=u
   elif tree.tag=='{'+NS+'}urlset':
    for r in ROWS:
     if r['url'] not in locs:
      n=ET.SubElement(tree,'{'+NS+'}url');ET.SubElement(n,'{'+NS+'}loc').text=r['url'];ET.SubElement(n,'{'+NS+'}lastmod').text='2026-11-25'
   else:raise RuntimeError('SITEMAP_FORMAT_UNKNOWN')
   planned[sitemap]=ET.tostring(tree,encoding='utf-8',xml_declaration=True)
  robots='/public_html/robots.txt';rawrobots=get(f,robots)
  if rawrobots is not None and b'sitemap-radar-20261125.xml' not in rawrobots:
   planned[robots]=rawrobots.rstrip()+b'\nSitemap: https://www.arquindex.com.br/sitemap-radar-20261125.xml\n'
  backup='/seo-backups/radar-20261125-'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
  mkdir(f,backup);put(f,backup+'/.htaccess',b'Require all denied\n')
  for p in planned:
   previous[p]=get(f,p)
   if previous[p] is not None:put(f,backup+'/'+digest(p.encode())+'.bak',previous[p])
  put(f,backup+'/manifest.json',json.dumps({p:{'backup':digest(p.encode())+'.bak','sha256':digest(v)} for p,v in previous.items() if v is not None}).encode())
  report['backup_created']=True
  try:
   for p,b in planned.items():
    assert get(f,p)==previous[p],'CONCURRENT_REMOTE_CHANGE'
    if previous[p]==b:continue
    applied.append(p);put(f,p,b)
   for r in ROWS:
    success=False
    for attempt in range(3):
     try:
      status,final,headers,b=http(r['url'])
      assert status==200 and final==r['url'] and b==(ROOT/r['path']).read_bytes()
      assert 'noindex' not in headers.get('X-Robots-Tag','').lower()
      success=True;break
     except Exception:
      if attempt==2:raise
      time.sleep(4)
    assert success
    report['pages'].append({'url':r['url'],'http':200,'sha256':digest(b)})
    print('PUBLIC_HTTP_VERIFIED',r['url'],flush=True)
   from urllib.robotparser import RobotFileParser
   rp=RobotFileParser();rp.parse(http(BASE+'robots.txt')[3].decode().splitlines())
   assert all(rp.can_fetch('Googlebot',r['url']) and rp.can_fetch('bingbot',r['url']) for r in ROWS),'ROBOTS_BLOCK'
   report['published']=True
  except Exception:
   for p in reversed(applied):
    if get(f,p)!=planned[p]:continue
    if previous[p] is None:f.delete(p)
    else:put(f,p,previous[p])
   report['rolled_back']=True
   raise
  finally:save()
if __name__=='__main__':
 try:
  if '--check' in sys.argv:check()
  else:publish()
 except Exception as e:
  report['error']=type(e).__name__+': '+str(e)[:300];save();raise
