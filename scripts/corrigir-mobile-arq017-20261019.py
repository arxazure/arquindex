import ftplib,io,os,posixpath,hashlib,time,urllib.request
from datetime import datetime,timezone
STAMP=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
HOST='ia.arquindex.com.br'; FILE='custo.html'; MARK='arquindex-mobile-arq017-20261019'
CSS='''<style id="'''+MARK+'''">
@media (max-width:600px){
  html,body{max-width:100%;overflow-x:hidden}
  [data-aq-aeo="ARQ-017"]{max-width:100%;overflow-x:auto}
  [data-aq-aeo="ARQ-017"] table{width:100%;max-width:100%;table-layout:fixed}
  [data-aq-aeo="ARQ-017"] th,[data-aq-aeo="ARQ-017"] td{overflow-wrap:anywhere;word-break:normal}
}
</style>'''
def get(f,p):
 b=bytearray();f.retrbinary('RETR '+p,b.extend);return bytes(b)
def put(f,p,data,label):
 d=posixpath.dirname(p);n=posixpath.basename(p);tmp=d+'/.tmp-'+n+'-'+label
 f.storbinary('STOR '+tmp,io.BytesIO(data));assert get(f,tmp)==data
 f.delete(p);f.rename(tmp,p);assert get(f,p)==data
def locate(f,base):
 for root in [base+'/subdominios/'+HOST,base+'/'+HOST,'/subdominios/'+HOST,'/'+HOST]:
  p=root+'/'+FILE
  try:
   b=get(f,p)
   if b'<html' in b.lower():return p,b
  except ftplib.all_errors:pass
 raise RuntimeError('TARGET_NOT_FOUND ARQ-017')
with ftplib.FTP_TLS(timeout=60) as f:
 f.connect('ftp.arquindex.com.br',21);f.login('arquind2',os.environ['FTP_PASSWORD']);f.prot_p();f.set_pasv(True)
 base=None
 for cand in ['/public_html','/home/arquind2/public_html']:
  try:
   if b'arquindex' in get(f,cand+'/index.html').lower():base=cand;break
  except ftplib.all_errors:pass
 assert base
 path,old=locate(f,base); text=old.decode('utf-8')
 assert 'data-aq-aeo="ARQ-017"' in text
 if MARK in text:
  print('ALREADY_PRESENT',path); new=old
 else:
  i=text.lower().rindex('</head>');new=(text[:i]+CSS+'\n'+text[i:]).encode('utf-8')
 backup=base+'/seo-backups/arq017-mobile-'+STAMP
 try:f.mkd(backup)
 except ftplib.error_perm as e:
  if not str(e).startswith('550'):raise
 f.storbinary('STOR '+backup+'/.htaccess',io.BytesIO(b'Options -Indexes\nRequire all denied\n'))
 bp=backup+'/custo-'+hashlib.sha256(old).hexdigest()[:12]+'.html'
 f.storbinary('STOR '+bp,io.BytesIO(old));assert get(f,bp)==old
 print('BACKUP_VERIFIED',bp,hashlib.sha256(old).hexdigest())
 if new!=old:
  try:put(f,path,new,STAMP)
  except Exception:
   put(f,path,old,'rollback-'+STAMP);print('ROLLBACK_COMPLETED');raise
 print('FTP_PUBLISHED_VERIFIED',path,hashlib.sha256(new).hexdigest())
url='https://'+HOST+'/'+FILE+'?post=relatorio-de-impacto-o-que-e&verify='+STAMP
last=None
for n in range(3):
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'ArquindexSEO/1.0','Cache-Control':'no-cache'})
  with urllib.request.urlopen(req,timeout=40) as r: code=r.status;body=r.read(6000000)
  assert code==200 and MARK.encode() in body and b'noindex' not in body.lower()
  print('PUBLIC_SOURCE_VERIFIED',url,hashlib.sha256(body).hexdigest());last=None;break
 except Exception as e:
  last=e
  if n<2:time.sleep(5)
if last:raise last
