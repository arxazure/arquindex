"""Scoped campaign publication with FTPS readback, private backups and guarded updates."""
from pathlib import Path
import os,io,ftplib,ssl,socket,json,hashlib,datetime,secrets,re,xml.etree.ElementTree as ET
BASE='https://www.arquindex.com.br/'
ROOT=Path(__file__).resolve().parents[1]
MAN=ROOT/'seo/alfresco-automacao-manifest.json'
ROWS=json.loads(MAN.read_text());REPORT=ROOT/'publish-report/alfresco-automacao';REPORT.mkdir(parents=True,exist_ok=True)
result={'ftps_verified':False,'http_verified':False,'indexed':False,'pages':[r['url'] for r in ROWS]}
def sha(b):return hashlib.sha256(b).hexdigest()
def get(f,p):
 b=bytearray()
 try:f.retrbinary('RETR '+p,b.extend)
 except ftplib.error_perm as e:
  if str(e).startswith('550'):return None
  raise
 return bytes(b)
def mkdir(f,p):
 cur=''
 for bit in p.strip('/').split('/'):
  cur+='/'+bit
  try:f.mkd(cur)
  except ftplib.error_perm as e:
   if not str(e).startswith('550'):raise

def put(f,p,b):
 mkdir(f,p.rsplit('/',1)[0]);f.storbinary('STOR '+p,io.BytesIO(b));assert get(f,p)==b,'FTPS_READBACK_MISMATCH'
def save():(REPORT/'publication.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
planned={'/public_html/'+r['path']:(ROOT/r['path']).read_bytes() for r in ROWS}
planned['/public_html/sitemap-alfresco-automacao.xml']=(ROOT/'sitemap-alfresco-automacao.xml').read_bytes()
# IndexNow verification keys are deliberately public and separate from account credentials.
key=secrets.token_hex(16);planned['/public_html/'+key+'.txt']=key.encode()
previous={};applied=[]
host=os.environ.get('FTP_TLS_HOST','h59.servidorhh.com')
assert host in ('h59.servidorhh.com','ftp.arquindex.com.br')
with ftplib.FTP_TLS(context=ssl.create_default_context(),timeout=55) as f:
 f.connect(host,21);f.login(os.environ.get('FTP_USER','arquind2'),os.environ['FTP_PASSWORD']);f.prot_p()
 marker=b'ARQ-ALFRESCO-AUTOMACAO-20261029'
 for row in ROWS:
  old=get(f,'/public_html/'+row['path'])
  assert old is None or marker in old,'EXISTING_PAGE_REQUIRES_REVIEW'
 block=b'<section id="arq-alfresco-automacao-20261029"><h2>Automacao documental com Alfresco</h2><p><a href="/alfresco-automacao-documental/">Custos, RPA, conectores com IA e fluxos de recebimento, aprovacao e compartilhamento</a></p></section>'
 for p in ['alfresco-cloud-ocr-ia/index.html','blog/alfresco-community-gestao-documental-sem-amps/index.html','manuais/alfresco-community-aspectos-temporalidade/index.html']:
  target='/public_html/'+p;old=get(f,target)
  if old is not None:
   assert b'</main>' in old,'NAV_STRUCTURE_CHANGED'
   if b'id="arq-alfresco-automacao-20261029"' not in old:planned[target]=old.replace(b'</main>',block+b'</main>',1)
 NS='http://www.sitemaps.org/schemas/sitemap/0.9';ET.register_namespace('',NS)
 sitemap='/public_html/sitemap.xml';raw=get(f,sitemap)
 if raw:
  tree=ET.fromstring(raw);locs={n.text for n in tree.iter('{'+NS+'}loc')}
  if tree.tag=='{'+NS+'}sitemapindex':
   u=BASE+'sitemap-alfresco-automacao.xml'
   if u not in locs:n=ET.SubElement(tree,'{'+NS+'}sitemap');ET.SubElement(n,'{'+NS+'}loc').text=u
  elif tree.tag=='{'+NS+'}urlset':
   for row in ROWS:
    if row['url'] not in locs:
     n=ET.SubElement(tree,'{'+NS+'}url');ET.SubElement(n,'{'+NS+'}loc').text=row['url'];ET.SubElement(n,'{'+NS+'}lastmod').text='2026-10-29'
  else:raise RuntimeError('UNEXPECTED_SITEMAP_FORMAT')
  planned[sitemap]=ET.tostring(tree,encoding='utf-8',xml_declaration=True)
 robots='/public_html/robots.txt';oldrobots=get(f,robots)
 if oldrobots is not None and b'sitemap-alfresco-automacao.xml' not in oldrobots:
  planned[robots]=oldrobots.rstrip()+b'\nSitemap: https://www.arquindex.com.br/sitemap-alfresco-automacao.xml\n'
 backup='/seo-backups/alfresco-automacao-'+datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
 mkdir(f,backup);put(f,backup+'/.htaccess',b'Require all denied\n')
 for p in planned:
  previous[p]=get(f,p)
  if previous[p] is not None:put(f,backup+'/'+sha(p.encode())+'.bak',previous[p])
 put(f,backup+'/manifest.json',json.dumps({p:{'file':sha(p.encode())+'.bak','sha256':sha(b)} for p,b in previous.items() if b is not None}).encode())
 try:
  for p,b in planned.items():
   if previous[p]==b:continue
   assert get(f,p)==previous[p],'CONCURRENT_REMOTE_CHANGE'
   applied.append(p);put(f,p,b)
  result['ftps_verified']=True;result['backup_created']=True
  result['hashes']={p.removeprefix('/public_html/'):sha(b) for p,b in planned.items()};save()
 except Exception:
  for p in reversed(applied):
   if get(f,p)!=planned[p]:continue
   if previous[p] is None:f.delete(p)
   else:put(f,p,previous[p])
  result['rolled_back']=True;save();raise
(ROOT/'publish-report/alfresco-automacao/indexnow-public-key.json').write_text(json.dumps({'key':key,'url':BASE+key+'.txt'}))
print('FTPS_VERIFIED',len(planned),'FILES; PRIVATE_BACKUP_CREATED',flush=True)
