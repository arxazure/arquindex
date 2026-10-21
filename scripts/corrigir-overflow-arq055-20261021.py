import ftplib,hashlib,io,os,posixpath,time,urllib.request
from datetime import datetime,timezone
from bs4 import BeautifulSoup
STAMP=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
HOST='arquivo.arquindex.com.br';FILE='bh.html';URL='https://arquivo.arquindex.com.br/bh.html'
STYLE='<style id="arquindex-overflow-arq055-20261021">body[data-aq-brand] section a{overflow-wrap:anywhere;word-break:break-word}</style>'
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
with ftplib.FTP_TLS(timeout=60) as f:
 f.connect('ftp.arquindex.com.br',21);f.login('arquind2',os.environ['FTP_PASSWORD']);f.prot_p();f.set_pasv(True)
 base=None
 for c in ['/public_html','/home/arquind2/public_html']:
  try:
   if b'arquindex' in get(f,c+'/index.html').lower():base=c;break
  except ftplib.all_errors:pass
 assert base
 path=old=None
 for root in [base+'/subdominios/'+HOST,base+'/'+HOST,'/subdominios/'+HOST,'/'+HOST]:
  try:
   b=get(f,root+'/'+FILE)
   if b'<html' in b.lower():path,old=root+'/'+FILE,b;break
  except ftplib.all_errors:pass
 assert path
 s=BeautifulSoup(old.decode('utf-8'),'html.parser');assert not s.select('#arquindex-overflow-arq055-20261021');s.head.append(BeautifulSoup(STYLE,'html.parser'));new=str(s).encode()
 backup='/seo-backups/correcao-overflow-arq055-'+STAMP;mkdir(f,backup);f.storbinary('STOR '+backup+'/.htaccess',io.BytesIO(b'Options -Indexes\nRequire all denied\n'));f.storbinary('STOR '+backup+'/arq-055.html',io.BytesIO(old));assert get(f,backup+'/arq-055.html')==old;print('BACKUP_VERIFIED',backup,hashlib.sha256(old).hexdigest(),flush=True)
 assert get(f,path)==old,'CONCURRENT_CHANGE'
 try:
  put(f,path,new,STAMP);print('FTP_PUBLISHED_VERIFIED',hashlib.sha256(new).hexdigest(),flush=True);time.sleep(2)
  req=urllib.request.Request(URL+'?verify='+STAMP,headers={'User-Agent':'ArquindexSEO/1.0','Cache-Control':'no-cache'})
  with urllib.request.urlopen(req,timeout=40) as r:body=r.read(9000000);assert r.status==200 and b'arquindex-overflow-arq055-20261021' in body
  print('PUBLIC_SOURCE_VERIFIED',URL,hashlib.sha256(body).hexdigest(),flush=True)
 except Exception:
  put(f,path,old,'rollback-'+STAMP);print('ROLLBACK_COMPLETED',flush=True);raise
