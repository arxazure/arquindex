"""Bounded HomeHost FTPS publication: new technical collection + blog discovery.
Never changes DNS, email, application deployments or site homepage.
"""
from pathlib import Path,PurePosixPath
import ftplib,ssl,io,os,json,gzip,hashlib,time,re,socket,urllib.request,urllib.error,xml.etree.ElementTree as ET
from html.parser import HTMLParser
from datetime import datetime,timezone
P=json.loads(gzip.decompress(Path('publicacoes/open-source-documental-20261106/payload.json.gz').read_bytes()).decode())
RELEASE=P['release'];ORIGIN=P['base'];NAMES=set(P['files']);OUT=Path('publish-report/open-source-documental-20261106');OUT.mkdir(parents=True,exist_ok=True)
NS='http://www.sitemaps.org/schemas/sitemap/0.9';ET.register_namespace('',NS)
report={'release':RELEASE,'status':'preflight','published':[],'rollback':[],'verified':False};stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
class Page(HTMLParser):
 def __init__(self,s):super().__init__();self.tags=[];self.ld=[];self.inld=False;self.feed(s)
 def handle_starttag(self,t,a):
  d=dict(a);self.tags.append((t,d))
  if t=='script' and d.get('type')=='application/ld+json':self.inld=True
 def handle_endtag(self,t):
  if t=='script':self.inld=False
 def handle_data(self,d):
  if self.inld:self.ld.append(d)
def sha(b):return hashlib.sha256(b).hexdigest()
def url(name):return ORIGIN+'/'+(name[:-10] if name.endswith('index.html') else name)
def validate(name,data):
 if not name.endswith('.html'):return
 h=Page(data.decode());assert sum(t=='h1' for t,a in h.tags)==1,('h1',name)
 assert [a['href'] for t,a in h.tags if t=='link' and a.get('rel')=='canonical']==[url(name)],('canonical',name)
 for t,a in h.tags:
  if t=='script' and a.get('type')=='application/ld+json':pass
  if t=='meta' and a.get('name')=='robots':assert 'noindex' not in a.get('content','')
 json.loads(''.join(h.ld))
def public(name,attempts=3):
 last=None
 for i in range(attempts):
  try:
   req=urllib.request.Request(url(name)+'?arq_verify='+stamp,headers={'User-Agent':'ArquindexPublisher/1.0','Cache-Control':'no-cache'})
   with urllib.request.urlopen(req,timeout=35) as r:
    data=r.read();assert r.status==200;return data,r.headers
  except Exception as e:
   last=e
   if i+1<attempts:time.sleep(2)
 raise last
def get(f,path):
 b=bytearray();f.retrbinary('RETR '+path,b.extend);return bytes(b)
def optional(f,path):
 try:return get(f,path)
 except ftplib.error_perm as e:
  if str(e).startswith('550'):return None
  raise
def put(f,path,data):f.storbinary('STOR '+path,io.BytesIO(data))
def mkdirs(f,path):
 current=''
 for piece in PurePosixPath(path).parts:
  if piece=='/':continue
  current+='/'+piece
  try:f.cwd(current)
  except ftplib.error_perm:
   f.mkd(current)
 f.cwd('/')
files={k:v.encode() for k,v in P['files'].items()}
for name,data in files.items():
 assert '..' not in PurePosixPath(name).parts and not name.startswith('/')
 assert name.startswith('open-source-documental/') or name=='blog/open-source-documental-alfresco-nextcloud-omeka-openarch/index.html'
 assert sha(data)==P['sha256'][name]
 validate(name,data)
assert sum(n.endswith('.html') for n in files)==19
if '--check' in __import__('sys').argv:
 print('LOCAL_PREFLIGHT_OK pages=19 files='+str(len(files)));raise SystemExit(0)
f=None;before={};planned={};applied=[]
try:
 secret=os.environ.get('FTP_PASSWORD')
 if not secret:raise RuntimeError('FTP_CREDENTIAL_NOT_AVAILABLE')
 # Require successful public response before any remote write.
 live,_=public('index.html');assert b'arquindex' in live.lower()
 f=ftplib.FTP_TLS(context=ssl.create_default_context(),timeout=50)
 f.connect('h59.servidorhh.com',21);f.login('arquind2',secret);f.prot_p();print('FTPS_TLS_AUTHENTICATED',flush=True)
 # Verify the actual document root against the content served by the official domain.
 roots=[]
 for base in ['/public_html/','/']:
  remote=optional(f,base+'index.html')
  if remote is not None and remote==live:roots.append(base)
 if len(roots)!=1:raise RuntimeError('DOCUMENT_ROOT_NOT_UNIQUELY_VERIFIED')
 base=roots[0];report['root']=base;report['root_sha256']=sha(live)
 print('OFFICIAL_DOMAIN_DOCUMENT_ROOT_VERIFIED',flush=True)
 for name,data in files.items():
  old=optional(f,base+name);before[name]=old
  if old is not None and old!=data:
   # Refuse to overwrite a page or asset created independently.
   raise RuntimeError('COLLECTION_DESTINATION_ALREADY_EXISTS '+name)
  planned[name]=data
 # Blog discovery is a narrow insertion into the current file, guarded by a marker.
 blogname='blog/index.html';old=get(f,base+blogname);before[blogname]=old
 blog=old.decode('utf-8');assert b'arquindex' in old.lower()
 if 'id="arquindex-oss-docs-20261106"' not in blog:
  assert blog.lower().count('</main>')==1,'BLOG_MAIN_NOT_UNIQUE'
  block='<section id="arquindex-oss-docs-20261106" style="max-width:1180px;margin:32px auto;padding:24px;border:1px solid #dce4e9"><h2>Documentação técnica open-source documental</h2><p>Manuais em português sobre Alfresco Community, Nextcloud, Omeka e OpenArch: arquitetura, instalação, configuração, código e downloads oficiais.</p><p><a href="/blog/open-source-documental-alfresco-nextcloud-omeka-openarch/">Ler o artigo técnico</a> · <a href="/open-source-documental/">Consultar a biblioteca de manuais</a></p></section>'
  blog=re.sub(r'</main\s*>',lambda m:block+m[0],blog,count=1,flags=re.I)
  assert 'id="arquindex-oss-docs-20261106"' in blog
  assert all(x in blog for x in re.findall(r'<script\b.*?</script>',old.decode(),re.S|re.I))
 planned[blogname]=blog.encode()
 # Append URLs without deleting or rewriting existing entries or changing DNS.
 sm='sitemap.xml';old=get(f,base+sm);before[sm]=old;tree=ET.fromstring(old)
 known=set(x.text for x in tree.iter('{'+NS+'}loc'))
 if tree.tag=='{'+NS+'}sitemapindex':
  target=ORIGIN+'/open-source-documental/sitemap.xml'
  if target not in known:
   item=ET.SubElement(tree,'{'+NS+'}sitemap');ET.SubElement(item,'{'+NS+'}loc').text=target
 elif tree.tag=='{'+NS+'}urlset':
  for name in files:
   if name.endswith('.html') and url(name) not in known:
    item=ET.SubElement(tree,'{'+NS+'}url');ET.SubElement(item,'{'+NS+'}loc').text=url(name);ET.SubElement(item,'{'+NS+'}lastmod').text='2026-11-06'
 else:raise RuntimeError('SITEMAP_FORMAT_UNRECOGNIZED')
 planned[sm]=ET.tostring(tree,encoding='utf-8',xml_declaration=True)
 assert known.issubset(set(x.text for x in tree.iter('{'+NS+'}loc')))
 # Store exact pre-change bytes privately and include them in the workflow artifact.
 backup=OUT/'backup';backup.mkdir(exist_ok=True);mapping={}
 for name,data in before.items():
  if data is not None:
   key=hashlib.sha256(name.encode()).hexdigest()+'.bak';(backup/key).write_bytes(data);mapping[name]={'file':key,'sha256':sha(data)}
 (backup/'manifest.json').write_text(json.dumps(mapping,ensure_ascii=False,indent=2))
 report['backup_files']=len(mapping);report['status']='backup_complete'
 # All validation and backup precede the first public mutation. New pages first, discovery last.
 for name,data in planned.items():
  old=before[name]
  if old==data:continue
  assert optional(f,base+name)==old,('CONCURRENT_MODIFICATION',name)
  mkdirs(f,str(PurePosixPath(base+name).parent))
  applied.append(name);put(f,base+name,data);assert get(f,base+name)==data,('UPLOAD_VERIFY',name)
 print('FTPS_FILES_UPLOADED count='+str(len(applied)),flush=True)
 for name,data in planned.items():
  body,headers=public(name)
  assert body==data,('PUBLIC_CONTENT_MISMATCH',name)
  if name.endswith('.html'):
   validate(name,body) if name in files else None
   assert 'noindex' not in headers.get('X-Robots-Tag','').lower()
   report['published'].append({'url':url(name),'http':200,'sha256':sha(body)})
 # Ensure homepage bytes stayed unchanged.
 assert get(f,base+'index.html')==live,'HOMEPAGE_CHANGED_DURING_PUBLICATION'
 report['verified']=True;report['status']='published_verified';print('HOMEHOST_OPEN_SOURCE_PUBLICATION_VERIFIED',flush=True)
except Exception as e:
 report['status']='failed';report['error_type']=type(e).__name__
 # Exception messages are structured identifiers and paths; never include credentials.
 report['error']=str(e)[:350]
 if f is not None and applied:
  for name in reversed(applied):
   try:
    current=optional(f,report['root']+name)
    if current==planned[name]:
     if before[name] is None:f.delete(report['root']+name)
     else:put(f,report['root']+name,before[name]);assert get(f,report['root']+name)==before[name]
     report['rollback'].append(name)
    else:report.setdefault('rollback_conflicts',[]).append(name)
   except Exception:report.setdefault('rollback_failed',[]).append(name)
 raise
finally:
 if f is not None:
  try:f.quit()
  except Exception:pass
 (OUT/'publication.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(report,ensure_ascii=False),flush=True)
