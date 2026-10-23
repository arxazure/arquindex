import ftplib,hashlib,io,os,posixpath,urllib.request
from datetime import datetime,timezone
from bs4 import BeautifulSoup
STAMP=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
EXPECTED='3dce5e20eb46dae20931e045dcd88fc1544c138861990d7d1997c0fec4a0b011'
HOST='digitalizardocumentos.arquindex.com.br';URL='https://'+HOST+'/o-que-e.html'
def get(f,p):b=bytearray();f.retrbinary('RETR '+p,b.extend);return bytes(b)
def put(f,p,b):
 d,n=posixpath.dirname(p),posixpath.basename(p);tmp=d+'/.tmp-'+n+'-'+STAMP
 f.storbinary('STOR '+tmp,io.BytesIO(b));assert get(f,tmp)==b
 f.delete(p);f.rename(tmp,p);assert get(f,p)==b
with ftplib.FTP_TLS(timeout=60) as f:
 f.connect('ftp.arquindex.com.br',21);f.login('arquind2',os.environ['FTP_PASSWORD']);f.prot_p();f.set_pasv(True)
 base=None
 for c in ['/public_html','/home/arquind2/public_html']:
  try:
   if b'arquindex' in get(f,c+'/index.html').lower():base=c;break
  except ftplib.all_errors:pass
 assert base
 path=None
 for root in [base+'/subdominios/'+HOST,base+'/'+HOST,'/subdominios/'+HOST,'/'+HOST]:
  try:
   old=get(f,root+'/o-que-e.html')
   if b'<html' in old.lower():path=root+'/o-que-e.html';break
  except ftplib.all_errors:pass
 assert path and hashlib.sha256(old).hexdigest()==EXPECTED,'CONCURRENT_CHANGE'
 backup='/seo-backups/correcao-arq098-'+STAMP+'.html';f.storbinary('STOR '+backup,io.BytesIO(old));assert get(f,backup)==old
 s=BeautifulSoup(old.decode('utf-8','ignore'),'html.parser')
 for n in s.select('#arq098-mobile-fix'):n.decompose()
 style=s.new_tag('style',id='arq098-mobile-fix');style.string='''@media(max-width:760px){html,body{max-width:100%;overflow-x:clip}body a{overflow-wrap:anywhere;word-break:break-word}.aq-aeo-answer{overflow:hidden}.aq-aeo-answer table{max-width:100%;overflow-x:auto}#arq-floating{right:12px!important;max-width:calc(100vw - 24px)!important}#arq-float-toggle{max-width:calc(100vw - 24px)!important}}'''
 s.head.append(style);new=str(s).encode();put(f,path,new)
 req=urllib.request.Request(URL+'?fix='+STAMP,headers={'User-Agent':'ArquindexSEO/1.0','Cache-Control':'no-cache'})
 with urllib.request.urlopen(req,timeout=40) as r:body=r.read(10000000);assert r.status==200 and b'arq098-mobile-fix' in body
 print('BACKUP_VERIFIED',backup,hashlib.sha256(old).hexdigest(),flush=True)
 print('ARQ098_FIX_PUBLIC_VERIFIED',hashlib.sha256(body).hexdigest(),flush=True)
