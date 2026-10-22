import ftplib,hashlib,io,os,posixpath,time,urllib.request,xml.etree.ElementTree as ET
from datetime import datetime,timezone
from urllib.parse import urljoin
STAMP=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
TARGETS=[('ocr-maua.arquindex.com.br','https://ocr-maua.arquindex.com.br/'),('mapeamento-educacao.arquindex.com.br','https://mapeamento-educacao.arquindex.com.br/'),('digitalizar-lgpd-solucao.arquindex.com.br','https://digitalizar-lgpd-solucao.arquindex.com.br/empresas.html')]
def get(f,p):b=bytearray();f.retrbinary('RETR '+p,b.extend);return bytes(b)
def put(f,p,b,label):
 d,n=posixpath.dirname(p),posixpath.basename(p);tmp=d+'/.tmp-'+n+'-'+label;f.storbinary('STOR '+tmp,io.BytesIO(b));assert get(f,tmp)==b
 try:f.delete(p)
 except ftplib.error_perm as e:
  if not str(e).startswith('550'):raise
 f.rename(tmp,p);assert get(f,p)==b
def mkdir(f,p):
 old=f.pwd()
 try:
  f.cwd('/')
  for x in p.strip('/').split('/'):
   if not x:continue
   try:f.mkd(x)
   except ftplib.error_perm as e:
    if not str(e).startswith('550'):raise
   f.cwd(x)
 finally:f.cwd(old)
def locate(f,base,host):
 for root in [base+'/subdominios/'+host,base+'/'+host,'/subdominios/'+host,'/'+host]:
  p=root+'/sitemap.xml'
  try:b=get(f,p);ET.fromstring(b);return p,b
  except ftplib.all_errors+(ET.ParseError,):pass
 raise RuntimeError('SITEMAP_NOT_FOUND '+host)
def transform(old,target):
 root=ET.fromstring(old);ns=''
 if root.tag.startswith('{'):ns=root.tag.split('}',1)[0][1:];ET.register_namespace('',ns)
 q=lambda x:'{'+ns+'}'+x if ns else x
 locs=[e.text.strip() for e in root.iter(q('loc')) if e.text];assert target not in [urljoin(target,x) for x in locs]
 url=ET.SubElement(root,q('url'));ET.SubElement(url,q('loc')).text=target;ET.SubElement(url,q('lastmod')).text='2026-10-22'
 out=ET.tostring(root,encoding='utf-8',xml_declaration=True);ET.fromstring(out);return out
def check(url):
 last=None
 for attempt in range(2):
  try:
   req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 ArquindexSEO','Cache-Control':'no-cache'})
   with urllib.request.urlopen(req,timeout=35) as r:return r.status,r.read(3000000)
  except Exception as e:last=e;time.sleep(2)
 raise last
with ftplib.FTP_TLS(timeout=60) as f:
 f.connect('ftp.arquindex.com.br',21);f.login('arquind2',os.environ['FTP_PASSWORD']);f.prot_p();f.set_pasv(True)
 base=None
 for c in ['/public_html','/home/arquind2/public_html']:
  try:
   if b'arquindex' in get(f,c+'/index.html').lower():base=c;break
  except ftplib.all_errors:pass
 assert base;rec=[]
 for host,target in TARGETS:
  path,old=locate(f,base,host);new=transform(old,target);root=ET.fromstring(new);locs=[e.text.strip() for e in root.iter() if e.tag.endswith('loc') and e.text];assert len(locs)==len(set(locs))
  for u in locs:
   absolute=urljoin('https://'+host+'/',u);st,_=check(absolute);assert st==200,(absolute,st)
  rec.append((host,target,path,old,new));print('PREFLIGHT_VALID',host,len(locs),flush=True)
 backup='/seo-backups/sitemaps-rodada-20261022-tarde-'+STAMP;mkdir(f,backup);f.storbinary('STOR '+backup+'/.htaccess',io.BytesIO(b'Options -Indexes\nRequire all denied\n'))
 for host,target,path,old,new in rec:
  bp=backup+'/'+host+'.xml';f.storbinary('STOR '+bp,io.BytesIO(old));assert get(f,bp)==old;print('BACKUP_VERIFIED',host,bp,hashlib.sha256(old).hexdigest(),flush=True)
 written=[]
 try:
  for host,target,path,old,new in rec:assert get(f,path)==old,'CONCURRENT_CHANGE '+host
  for host,target,path,old,new in rec:put(f,path,new,STAMP);written.append((path,old));print('SITEMAP_FTP_VERIFIED',host,hashlib.sha256(new).hexdigest(),flush=True)
  time.sleep(2)
  for host,target,path,old,new in rec:
   st,body=check('https://'+host+'/sitemap.xml?verify='+STAMP);ET.fromstring(body);assert st==200 and target.encode() in body;print('SITEMAP_PUBLIC_VERIFIED',host,target,hashlib.sha256(body).hexdigest(),flush=True)
 except Exception:
  for path,old in reversed(written):put(f,path,old,'rollback-'+STAMP)
  print('ROLLBACK_COMPLETED',flush=True);raise
