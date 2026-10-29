from pathlib import Path
import ftplib,os,io,hashlib,urllib.request,json
paths=['blog/alfresco-community-gestao-documental-sem-amps/index.html','manuais/alfresco-community-aspectos-temporalidade/index.html']
base='https://www.arquindex.com.br/'
backup=Path('backup-alfresco-publicacao');backup.mkdir(exist_ok=True)
f=ftplib.FTP_TLS(os.environ['FTP_HOST'],timeout=40);f.login(os.environ['FTP_USER'],os.environ['FTP_PASS']);f.prot_p();f.cwd('public_html')
def get(path):
 b=bytearray()
 try:f.retrbinary('RETR '+path,b.extend)
 except ftplib.error_perm as e:
  if str(e).startswith('550'):return None
  raise
 return bytes(b)
def put(path,data):
 old=get(path)
 if old==data:return
 if old is not None:
  dest=backup/path;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(old)
 parent=''
 for bit in path.split('/')[:-1]:
  parent+=bit+'/'
  try:f.mkd(parent)
  except ftplib.error_perm:pass
 temp=path+'.arq-20261029.tmp';f.storbinary('STOR '+temp,io.BytesIO(data));assert get(temp)==data
 f.rename(temp,path);assert get(path)==data
for path in paths:put(path,Path(path).read_bytes())
hub='alfresco-cloud-ocr-ia/index.html';old=get(hub)
if old is not None:
 s=old.decode('utf-8');marker='id="alfresco-aspectos-temporalidade"'
 if marker not in s:
  block='<section '+marker+'><h2>Alfresco Community: aspectos e temporalidade</h2><p><a href="/blog/alfresco-community-gestao-documental-sem-amps/">Artigo: gestão documental sem AMPs</a> · <a href="/manuais/alfresco-community-aspectos-temporalidade/">Manual: os 16 campos, regras e validação</a></p></section>'
  assert '</main>' in s;put(hub,s.replace('</main>',block+'</main>',1).encode())
f.quit()
for path in paths:
 u=base+path.removesuffix('index.html');r=urllib.request.urlopen(u,timeout=40);body=r.read().decode();assert r.status==200 and 'Alfresco Community' in body and 'canonical' in body
 print('PUBLIC_OK',u)
