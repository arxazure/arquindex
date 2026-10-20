import ftplib,hashlib,io,os,posixpath,urllib.request
from datetime import datetime,timezone
from bs4 import BeautifulSoup
stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ');host='ged.arquindex.com.br';url='https://ged.arquindex.com.br/bh.html'
def get(f,p):b=bytearray();f.retrbinary('RETR '+p,b.extend);return bytes(b)
def put(f,p,b):
 d,n=posixpath.dirname(p),posixpath.basename(p);t=d+'/.tmp-'+n+'-'+stamp;f.storbinary('STOR '+t,io.BytesIO(b));assert get(f,t)==b
 f.delete(p);f.rename(t,p);assert get(f,p)==b
with ftplib.FTP_TLS(timeout=60) as f:
 f.connect('ftp.arquindex.com.br',21);f.login('arquind2',os.environ['FTP_PASSWORD']);f.prot_p();f.set_pasv(True)
 path=None
 for p in ['/public_html/subdominios/'+host+'/bh.html','/public_html/'+host+'/bh.html','/subdominios/'+host+'/bh.html','/'+host+'/bh.html']:
  try:
   old=get(f,p)
   if b'<html' in old.lower():path=p;break
  except ftplib.all_errors:pass
 assert path
 s=BeautifulSoup(old.decode(),'html.parser');s.title.string='Sistema GED em BH: Gestão Eletrônica de Documentos | Arquindex'
 style=s.find(id='arquindex-mobile-overflow-arq038')
 if not style:
  style=s.new_tag('style',id='arquindex-mobile-overflow-arq038');style.string='html,body{max-width:100%;overflow-x:hidden}.aq-aeo-answer{box-sizing:border-box}.aq-aeo-answer *{max-width:100%}';s.head.append(style)
 new=str(s).encode();backup='/seo-backups/arq038-mobile-'+stamp+'.html';f.storbinary('STOR '+backup,io.BytesIO(old));assert get(f,backup)==old
 put(f,path,new);print('BACKUP_VERIFIED',backup,hashlib.sha256(old).hexdigest());print('PATCH_PUBLISHED',hashlib.sha256(new).hexdigest())
req=urllib.request.Request(url+'?fix='+stamp,headers={'User-Agent':'ArquindexSEO/1.0','Cache-Control':'no-cache'})
with urllib.request.urlopen(req,timeout=40) as r:
 body=r.read();assert r.status==200 and b'Sistema GED em BH: Gest' in body and b'arquindex-mobile-overflow-arq038' in body;print('PUBLIC_PATCH_VERIFIED',r.status,hashlib.sha256(body).hexdigest())
