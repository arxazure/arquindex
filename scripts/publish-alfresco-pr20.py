"""Scoped FTPS release of PR20. Preserve existing pages; back up and roll back on failure."""
import ftplib,io,json,os,re,ssl,socket,hashlib,time,sys,subprocess
from pathlib import Path
from datetime import datetime,timezone
from urllib.request import Request,urlopen
from urllib.parse import quote,urlencode
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
BASE='https://www.arquindex.com.br/'
MARKER=b'ARQ-PR20-20261021'
ROWS=json.loads((ROOT/'seo/alfresco-cloud-manifest.json').read_text())
NS='http://www.sitemaps.org/schemas/sitemap/0.9';ET.register_namespace('',NS)
CHILD='sitemap-alfresco-cloud-20261021.xml'
OUT=ROOT/'publish-report';OUT.mkdir(exist_ok=True)
REPORT={'published':False,'commit':os.environ.get('GITHUB_SHA'),'pages':[],'discovery':{}}
def sha(b):return hashlib.sha256(b).hexdigest()
def save(): (OUT/'pr20-publication.json').write_text(json.dumps(REPORT,ensure_ascii=False,indent=2)+'\n')
def http(url):
 with urlopen(Request(url,headers={'User-Agent':'ArquindexPR20/1.0','Cache-Control':'no-cache'}),timeout=40) as r:return r.status,r.url,r.headers,r.read()
def get(f,p):
 b=bytearray()
 try:f.retrbinary('RETR '+p,b.extend)
 except ftplib.error_perm as e:
  if str(e).startswith('550'):return None
  raise
 return bytes(b)
def mkdir(f,p):
 cur=''
 for part in p.strip('/').split('/'):
  cur+='/'+part
  try:f.cwd(cur)
  except ftplib.error_perm as e:
   if not str(e).startswith('550'):raise
   f.mkd(cur)
def put(f,p,b):
 mkdir(f,p.rsplit('/',1)[0]);f.storbinary('STOR '+p,io.BytesIO(b));assert get(f,p)==b,('READBACK',p)
def verify(url,data):
 for attempt in range(4):
  try:
   status,final,headers,body=http(url)
   assert status==200 and final==url and body==data,('PUBLIC_MISMATCH',url,status,final)
   assert 'noindex' not in headers.get('X-Robots-Tag','').lower()
   return {'url':url,'http':status,'final_url':final,'sha256':sha(body)}
  except Exception:
   if attempt==3:raise
   time.sleep(3)
def check():
 subprocess.run([sys.executable,str(ROOT/'scripts/qa/alfresco-geo-aeo-check.py')],check=True)
 for row in ROWS:
  b=(ROOT/row['source']).read_bytes();assert MARKER in b
  assert ('rel="canonical" href="'+row['url']+'"').encode() in b
 tree=ET.fromstring((ROOT/CHILD).read_bytes());assert {x.text for x in tree.iter('{'+NS+'}loc')}=={r['url'] for r in ROWS}
 print('LOCAL_CHECK_OK',len(ROWS))
def publish():
 planned={'/public_html/'+row['source']:(ROOT/row['source']).read_bytes() for row in ROWS}
 planned['/public_html/'+CHILD]=(ROOT/CHILD).read_bytes()
 previous={};applied=[]
 ips=set(socket.gethostbyname_ex('ftp.arquindex.com.br')[2]);assert ips & set(socket.gethostbyname_ex('h59.servidorhh.com')[2])
 with ftplib.FTP_TLS(context=ssl.create_default_context(),timeout=55) as f:
  f.connect('h59.servidorhh.com',21);assert f.sock.getpeername()[0] in ips
  f.login('arquind2',os.environ['FTP_PASSWORD']);f.prot_p();f.set_pasv(True)
  home=get(f,'/public_html/index.html');assert home and b'arquindex' in home.lower()
  for row in ROWS:
   old=get(f,'/public_html/'+row['source']);assert old is None or MARKER in old,('EXISTING_PAGE_NEEDS_REVIEW',row['url'])
  # Add one bounded, idempotent discovery block to existing navigation. Never replace its body.
  block='<section id="arq-pr20-guides"><!-- ARQ-PR20-20261021 --><h2>Alfresco Cloud e OCR: guias de implantação</h2><p><a href="/alfresco-cloud-ocr-ia/">Acesse três guias técnicos e roteiros de aplicação para dez cidades</a>: dimensionamento de OCR, governança da nuvem e testes de pesquisa ECM.</p></section>'
  nav='/public_html/campanha-oportunidades-20261021/index.html';old=get(f,nav);assert old and b'</main>' in old
  if b'id="arq-pr20-guides"' not in old:planned[nav]=old.replace(b'</main>',block.encode()+b'</main>',1)
  raw=get(f,'/public_html/sitemap.xml');assert raw
  tree=ET.fromstring(raw);locs={x.text for x in tree.iter('{'+NS+'}loc')}
  if tree.tag=='{'+NS+'}sitemapindex':
   if BASE+CHILD not in locs:
    n=ET.SubElement(tree,'{'+NS+'}sitemap');ET.SubElement(n,'{'+NS+'}loc').text=BASE+CHILD
  elif tree.tag=='{'+NS+'}urlset':
   for row in ROWS:
    if row['url'] not in locs:
     n=ET.SubElement(tree,'{'+NS+'}url');ET.SubElement(n,'{'+NS+'}loc').text=row['url'];ET.SubElement(n,'{'+NS+'}lastmod').text='2026-10-21'
  else:raise RuntimeError('Unexpected sitemap type')
  planned['/public_html/sitemap.xml']=ET.tostring(tree,encoding='utf-8',xml_declaration=True)
  backup='/seo-backups/pr20-'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ');mkdir(f,backup);put(f,backup+'/.htaccess',b'Require all denied\n')
  for target in planned:
   old=get(f,target);previous[target]=old
   if old is not None:put(f,backup+'/'+sha(target.encode())+'.bak',old)
  put(f,backup+'/manifest.json',json.dumps({p:{'backup':sha(p.encode())+'.bak','sha256':sha(v)} for p,v in previous.items() if v is not None},indent=2).encode());REPORT['backup']=backup
  try:
   for target,data in planned.items():
    if previous[target]==data:continue
    assert get(f,target)==previous[target],('CONCURRENT_CHANGE',target)
    applied.append(target);put(f,target,data)
   for target,data in planned.items():
    url=BASE+target.removeprefix('/public_html/');url=url.removesuffix('index.html') if url.endswith('/index.html') else url
    row=verify(url,data);REPORT['pages'].append(row);print('HTTP_VERIFIED',url,flush=True)
   assert get(f,'/public_html/index.html')==home,'HOMEPAGE_CHANGED'
   # Check all same-host links from campaign pages, including pre-existing service pages.
   links=set()
   from urllib.parse import urljoin
   for row in ROWS:
    text=(ROOT/row['source']).read_text()
    for href in re.findall(r'<a[^>]+href="([^"]+)"',text):
     u=urljoin(row['url'],href)
     if u.startswith(BASE):links.add(u)
   REPORT['links']=[]
   for u in sorted(links):
    status,final,headers,body=http(u);assert status==200 and final==u,('LINK_FAILURE',u,status,final)
    REPORT['links'].append({'url':u,'http':status})
   from urllib.robotparser import RobotFileParser
   status,final,headers,robots=http(BASE+'robots.txt');rp=RobotFileParser();rp.parse(robots.decode().splitlines())
   assert all(rp.can_fetch('Googlebot',r['url']) and rp.can_fetch('bingbot',r['url']) for r in ROWS),'ROBOTS_BLOCK'
   REPORT['robots']='Googlebot and bingbot allowed';REPORT['published']=True
  except Exception:
   for target in reversed(applied):
    if get(f,target)!=planned[target]:continue
    if previous[target] is None:f.delete(target)
    else:put(f,target,previous[target])
   REPORT['rolled_back']=applied
   raise
  finally:save()

def discover():
 # Official IndexNow endpoint, existing publicly verifiable key only.
 try:
  status,final,headers,b=http(BASE+'indexnow-key.txt');key=b.decode('ascii').strip();assert re.fullmatch('[A-Za-z0-9-]{8,128}',key)
  keyurl=BASE+key+'.txt';assert http(keyurl)[3].decode('ascii').strip()==key
  payload=json.dumps({'host':'www.arquindex.com.br','key':key,'keyLocation':keyurl,'urlList':[r['url'] for r in ROWS]}).encode()
  req=Request('https://api.indexnow.org/indexnow',data=payload,headers={'Content-Type':'application/json'})
  with urlopen(req,timeout=40) as r:REPORT['discovery']['indexnow']={'http':r.status,'submitted':len(ROWS),'key_verified':True,'indexed':False}
 except Exception as e:REPORT['discovery']['indexnow']={'status':'pending','reason':str(e)[:250]}
 # Existing GitHub secrets are consumed in-memory; no credentials in artifacts or logs.
 try:
  names=['GSC_CLIENT_ID','GSC_CLIENT_SECRET','GSC_REFRESH_TOKEN'];assert all(os.environ.get(n) for n in names),'GSC OAuth configuration missing'
  params=urlencode({'client_id':os.environ[names[0]],'client_secret':os.environ[names[1]],'refresh_token':os.environ[names[2]],'grant_type':'refresh_token'}).encode()
  with urlopen(Request('https://oauth2.googleapis.com/token',data=params),timeout=35) as r:token=json.load(r)['access_token']
  auth={'Authorization':'Bearer '+token}
  with urlopen(Request('https://www.googleapis.com/webmasters/v3/sites',headers=auth),timeout=35) as r:sites=json.load(r).get('siteEntry',[])
  allowed=[s for s in sites if s.get('siteUrl') in ('sc-domain:arquindex.com.br',BASE) and s.get('permissionLevel') in ('siteOwner','siteFullUser')]
  assert allowed,'No verified writable property for exact host'
  site=next((s['siteUrl'] for s in allowed if s['siteUrl']=='sc-domain:arquindex.com.br'),allowed[0]['siteUrl'])
  endpoint='https://www.googleapis.com/webmasters/v3/sites/'+quote(site,safe='')+'/sitemaps/'+quote(BASE+CHILD,safe='')
  with urlopen(Request(endpoint,data=b'',headers=auth,method='PUT'),timeout=35) as r:REPORT['discovery']['google']={'property':site,'sitemap':BASE+CHILD,'http':r.status,'status':'submitted','indexed':False}
 except Exception as e:REPORT['discovery']['google']={'status':'pending','reason':str(e)[:250]}
 save();print(json.dumps(REPORT['discovery'],ensure_ascii=False),flush=True)
if __name__=='__main__':
 try:
  check()
  if '--check' not in sys.argv:publish();discover()
 except Exception as e:REPORT['error']=str(e)[:500];save();raise
