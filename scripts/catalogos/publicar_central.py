import os,io,ftplib,posixpath,datetime,urllib.request,time,xml.etree.ElementTree as ET
from pathlib import Path
from gerar_central import OUT,BASE

host=os.environ['FTP_HOST'];user=os.environ['FTP_USERNAME'];password=os.environ['FTP_PASSWORD']
try:
 f=ftplib.FTP_TLS(host,timeout=40);f.login(user,password);f.prot_p()
except (OSError,ftplib.Error):
 try:f.close()
 except Exception:pass
 f=ftplib.FTP(host,timeout=40);f.login(user,password)
start=f.pwd();found=False
for candidate in ['public_html','/public_html','/home/arquind2/public_html']:
 try:f.cwd(start);f.cwd(candidate);names=f.nlst()
 except ftplib.error_perm:continue
 if 'index.html' in names or 'index.php' in names:found=True;break
if not found:raise RuntimeError('Raiz publica nao confirmada; publicacao interrompida sem alteracoes')
root=f.pwd();stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
backup=posixpath.dirname(root.rstrip('/'))+'/backup-central-'+stamp
f.mkd(backup)
def read(n):
 b=bytearray()
 try:f.retrbinary('RETR '+n,b.extend)
 except ftplib.error_perm as e:
  if str(e).startswith('550'):return None
  raise
 return bytes(b)
def mkdirs(n):
 d=posixpath.dirname(n)
 if not d:return
 part=''
 for p in d.split('/'):
  part=posixpath.join(part,p)
  try:f.mkd(part)
  except ftplib.error_perm:
   f.cwd(part);f.cwd(root)
files={str(p.relative_to(OUT.parent)):p.read_bytes() for p in OUT.rglob('*') if p.is_file()}
home=read('index.html')
if home and b'/central-de-servicos/index.html' not in home:
 text=home.decode('utf-8');assert '</body>' in text
 block='<aside style="max-width:1120px;margin:28px auto;padding:24px;background:#e5f3f1;color:#143247"><h2>Servicos e catalogos Arquindex</h2><p>Conheca Alfresco, Databook, gestao documental e digitalizacao certificada. <a href="/central-de-servicos/index.html">Acessar paginas e baixar os quatro catalogos em PDF</a>.</p></aside>'
 files['index.html']=text.replace('</body>',block+'</body>',1).encode()
NS='http://www.sitemaps.org/schemas/sitemap/0.9';ET.register_namespace('',NS)
sm=read('sitemap.xml')
if sm:
 tree=ET.fromstring(sm);locs=[x.text for x in tree.iter('{'+NS+'}loc')]
 if tree.tag=='{'+NS+'}sitemapindex':
  if BASE+'sitemap.xml' not in locs:
   x=ET.SubElement(tree,'{'+NS+'}sitemap');ET.SubElement(x,'{'+NS+'}loc').text=BASE+'sitemap.xml'
 elif tree.tag=='{'+NS+'}urlset':
  for p in OUT.glob('*.html'):
   if BASE+p.name not in locs:
    x=ET.SubElement(tree,'{'+NS+'}url');ET.SubElement(x,'{'+NS+'}loc').text=BASE+p.name
 else:raise RuntimeError('Sitemap desconhecido; sem alteracoes')
 files['sitemap.xml']=ET.tostring(tree,encoding='utf-8',xml_declaration=True)
original={};applied=[]
for n in files:
 original[n]=read(n)
 if original[n] is not None:f.storbinary('STOR '+backup+'/'+n.replace('/','__'),io.BytesIO(original[n]))
try:
 for n,data in files.items():
  mkdirs(n);temp=n+'.upload-'+stamp
  f.storbinary('STOR '+temp,io.BytesIO(data))
  try:f.rename(temp,n)
  except ftplib.error_perm:
   if original[n] is not None:f.delete(n)
   f.rename(temp,n)
  applied.append(n)
  if read(n)!=data:raise RuntimeError('Falha de verificacao FTP: '+n)
 for n,data in files.items():
  if not n.startswith('central-de-servicos/'):continue
  url='https://www.arquindex.com.br/'+n
  for attempt in range(3):
   try:
    req=urllib.request.Request(url+'?verify='+stamp,headers={'Cache-Control':'no-cache','User-Agent':'ArquindexCatalogos/1.0'})
    with urllib.request.urlopen(req,timeout=40) as r:
     if r.status!=200 or r.read()!=data:raise RuntimeError('Conteudo publico divergente')
    break
   except Exception:
    if attempt==2:raise
    time.sleep(3)
  print('PUBLIC_VERIFIED',url,flush=True)
except Exception:
 for n in reversed(applied):
  if original[n] is None:f.delete(n)
  else:f.storbinary('STOR '+n,io.BytesIO(original[n]))
 raise
finally:f.quit()
print('CENTRAL_DEPLOYED',BASE+'index.html',flush=True)
