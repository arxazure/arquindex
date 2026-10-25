"""Publica somente novas artes individuais com FTPS, backup e leitura HTTPS."""
from pathlib import Path
import io,ftplib,ssl,os,json,hashlib,urllib.request,zipfile
from datetime import datetime,timezone
R=Path(__file__).resolve().parents[1]; package=R/'campanhas/design-20261025/posts-individuais'
report={'published':False,'images':[]};target='/public_html/assets/campanha-20261025/posts'
output=R/'publish-report/artes-individuais-20261025.json';output.parent.mkdir(exist_ok=True)
with zipfile.ZipFile(package/'artes.zip') as z:
 names=z.namelist();assert len(names)==11 and all(n.endswith('.jpg') and '/' not in n and '..' not in n for n in names)
 images={n:z.read(n) for n in names}
for n,b in images.items():assert b[:2]==b'\xff\xd8' and len(b)>10000

def read(f,p):
 b=bytearray();f.retrbinary('RETR '+p,b.extend);return bytes(b)
def optional(f,p):
 try:return read(f,p)
 except ftplib.error_perm as e:
  if str(e).startswith('550'):return None
  raise
def ensure(f,path):
 for i in range(2,len(path.split('/'))+1):
  p='/'.join(path.split('/')[:i])
  if not p:continue
  try:f.cwd(p)
  except ftplib.error_perm as e:
   if not str(e).startswith('550'):raise
   f.mkd(p)
def put(f,p,b):
 f.storbinary('STOR '+p,io.BytesIO(b));assert read(f,p)==b,p
before={};written=[]
try:
 with ftplib.FTP_TLS(context=ssl.create_default_context(),timeout=50) as f:
  f.connect('h59.servidorhh.com',21);f.login('arquind2',os.environ['FTP_PASSWORD']);f.prot_p();f.set_pasv(True)
  home=read(f,'/public_html/index.html');assert b'arquindex' in home.lower()
  ensure(f,target)
  for n in images:before[n]=optional(f,target+'/'+n)
  backup='/seo-backups/artes-posts-'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ');ensure(f,backup)
  for n,b in before.items():
   if b is not None:put(f,backup+'/'+n,b)
  put(f,backup+'/manifest.json',json.dumps({n:hashlib.sha256(b).hexdigest() if b else None for n,b in before.items()}).encode());report['backup']=backup
  try:
   for n,b in images.items():
    if b==before[n]:continue
    assert optional(f,target+'/'+n)==before[n],('CONCURRENT',n)
    written.append(n);put(f,target+'/'+n,b)
   for n,b in images.items():
    url='https://www.arquindex.com.br/assets/campanha-20261025/posts/'+n
    req=urllib.request.Request(url,headers={'User-Agent':'ArquindexPostImageQA/20261025','Cache-Control':'no-cache'})
    with urllib.request.urlopen(req,timeout=45) as r:
     assert r.status==200 and r.read()==b,url
    report['images'].append({'file':n,'url':url,'http':200,'sha256':hashlib.sha256(b).hexdigest()})
   assert read(f,'/public_html/index.html')==home
   report['published']=True
  except Exception:
   for n in reversed(written):
    if optional(f,target+'/'+n)!=images[n]:continue
    if before[n] is None:f.delete(target+'/'+n)
    else:put(f,target+'/'+n,before[n])
   report['rollback']=True;raise
finally:
 output.write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(report,ensure_ascii=False))
