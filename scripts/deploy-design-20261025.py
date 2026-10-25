"""Deploy limitado à campanha, com backup privado, readback, rollback e HTTP."""
from pathlib import Path
import ftplib,ssl,os,io,hashlib,json,urllib.request,time,xml.etree.ElementTree as ET,zipfile
from datetime import datetime,timezone
from html.parser import HTMLParser
BASE='https://www.arquindex.com.br/'
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'campanhas/design-20261025/public'
REPORT=ROOT/'publish-report/design-20261025.json';REPORT.parent.mkdir(exist_ok=True)
report={'published':False,'date':'2026-10-25','files':[]}
class Page(HTMLParser):
 def __init__(self):super().__init__();self.h1=0;self.c=[];self.ld=False;self.js=[]
 def handle_starttag(self,t,a):
  d=dict(a)
  if t=='h1':self.h1+=1
  if t=='link' and d.get('rel')=='canonical':self.c.append(d.get('href'))
  if t=='script' and d.get('type')=='application/ld+json':self.ld=True
 def handle_endtag(self,t):
  if t=='script':self.ld=False
 def handle_data(self,d):
  if self.ld:self.js.append(d)
def validate(data,url):
 p=Page();p.feed(data.decode());assert p.h1==1 and p.c==[url],url
 for j in p.js:assert json.loads(j)['@context']=='https://schema.org'
def http(path):
 req=urllib.request.Request(BASE+path,headers={'User-Agent':'ArquindexCampaignQA/20261025','Cache-Control':'no-cache'})
 with urllib.request.urlopen(req,timeout=45) as r:return r.status,r.url,r.headers,r.read()
from PIL import Image
for png in (OUT/'assets/campanha-20261025').glob('*.png'):
 with Image.open(png) as image:image.convert('RGB').save(png.with_suffix('.jpg'),quality=94)
files={p.relative_to(OUT).as_posix():p.read_bytes() for p in OUT.rglob('*') if p.is_file()}
for path,data in files.items():
 if path.endswith('/index.html'):validate(data,BASE+path.removesuffix('index.html'))
assert len([p for p in files if p.endswith('.mp4')])==11
assert len([p for p in files if p.endswith('.pdf')])==11
if os.environ.get('VALIDATE_ONLY')=='1':
 print('VALIDATED',len(files),'files, 12 pages, 11 manuals, 11 videos');raise SystemExit
before={};applied=[]
def read(f,p):
 b=bytearray();f.retrbinary('RETR '+p,b.extend);return bytes(b)
def maybe(f,p):
 try:return read(f,p)
 except ftplib.error_perm as e:
  if str(e).startswith('550'):return None
  raise
def mkdir(f,p):
 parts=p.strip('/').split('/');current=''
 for part in parts:
  current+='/'+part
  try:f.cwd(current)
  except ftplib.error_perm as e:
   if not str(e).startswith('550'):raise
   f.mkd(current)
def put(f,p,b):
 mkdir(f,p.rsplit('/',1)[0]);f.storbinary('STOR '+p,io.BytesIO(b));assert read(f,p)==b,('READBACK',p)
try:
 with ftplib.FTP_TLS(context=ssl.create_default_context(),timeout=60) as f:
  f.connect('h59.servidorhh.com',21);f.login('arquind2',os.environ['FTP_PASSWORD']);f.prot_p()
  f.cwd('/public_html');home=read(f,'/public_html/index.html');assert b'arquindex' in home.lower()
  plan={'/public_html/'+k:v for k,v in files.items()}
  ns='http://www.sitemaps.org/schemas/sitemap/0.9';ET.register_namespace('',ns)
  # Preserve live sitemap content and add entries to the existing articles sitemap.
  sm='/public_html/sitemap-artigos.xml';old=maybe(f,sm)
  tree=ET.fromstring(old) if old else ET.Element('{'+ns+'}urlset')
  assert tree.tag=='{'+ns+'}urlset'
  locations={e.text for e in tree.iter('{'+ns+'}loc')}
  for p in files:
   if not p.endswith('/index.html'):continue
   u=BASE+p.removesuffix('index.html')
   if u not in locations:
    node=ET.SubElement(tree,'{'+ns+'}url');ET.SubElement(node,'{'+ns+'}loc').text=u;ET.SubElement(node,'{'+ns+'}lastmod').text='2026-10-25'
  plan[sm]=ET.tostring(tree,encoding='utf-8',xml_declaration=True)
  robots='/public_html/robots.txt';rb=read(f,robots)
  sitemapline='Sitemap: '+BASE+'sitemap-campanha-20261025.xml'
  if sitemapline not in rb.decode():plan[robots]=rb.rstrip()+b'\n'+sitemapline.encode()+b'\n'
  for p,data in plan.items():
   before[p]=maybe(f,p)
   if p.endswith('/index.html') and before[p] and b'ARQ-DESIGN-20261025' not in before[p]:
    allowed={'alfresco-belo-horizonte','gestao-documental-belo-horizonte','consultoria-lgpd-belo-horizonte'}
    assert p.split('/')[-2] in allowed,('UNEXPECTED_EXISTING_PAGE',p)
  stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ');backup='/seo-backups/design-20261025-'+stamp
  mkdir(f,backup);manifest={}
  for p,data in before.items():
   if data is not None:
    name=hashlib.sha256(p.encode()).hexdigest()+'.bak';put(f,backup+'/'+name,data);manifest[p]={'name':name,'sha256':hashlib.sha256(data).hexdigest()}
  put(f,backup+'/manifest.json',json.dumps(manifest,indent=2).encode());report['backup']=backup
  try:
   for p,data in plan.items():
    if before[p]==data:continue
    assert maybe(f,p)==before[p],('CONCURRENT_CHANGE',p)
    applied.append(p);put(f,p,data)
   for path in files:
    if not path.endswith('/index.html'):continue
    u=path.removesuffix('index.html');candidate=None
    for attempt in range(4):
     try:
      status,url,headers,data=http(u)
      if status==200 and url==BASE+u and b'ARQ-DESIGN-20261025' in data:
       validate(data,BASE+u);assert 'noindex' not in headers.get('X-Robots-Tag','').lower();candidate={'url':url,'http':status};break
     except Exception:pass
     time.sleep(4)
    assert candidate,('PUBLIC_PAGE_NOT_VERIFIED',BASE+u)
    report['files'].append(candidate)
   for path in files:
    if path.endswith(('.mp4','.pdf','.css','.js','.png','.vtt')):
     status,url,headers,data=http(path);assert status==200 and hashlib.sha256(data).digest()==hashlib.sha256(files[path]).digest(),('PUBLIC_ASSET',path)
   assert read(f,'/public_html/index.html')==home
   report['published']=True;report['sitemap']=BASE+'sitemap-campanha-20261025.xml'
  except Exception:
   for p in reversed(applied):
    if maybe(f,p)!=plan[p]:continue
    if before[p] is None:f.delete(p)
    else:put(f,p,before[p])
   report['rollback']=True;raise
finally:
 REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(report,ensure_ascii=False),flush=True)
