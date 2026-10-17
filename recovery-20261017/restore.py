#!/usr/bin/env python3
"""Idempotent cPanel registration + verified FTPS deployment. No deletions."""
import base64, concurrent.futures, ftplib, hashlib, io, json, os, posixpath, re, socket, sys, urllib.request, urllib.parse, zipfile
from pathlib import Path
BASE=Path(__file__).resolve().parent
REPORT={'registered':[],'uploaded':[],'public':[],'pending':[],'preserved':[]}
BACKUP=BASE/'previous-public-files.zip'

def report():
 (BASE/'result.json').write_text(json.dumps(REPORT,ensure_ascii=False,indent=2))

def auth():
 host=os.getenv('CPANEL_HOST','').strip().rstrip('/')
 user=os.getenv('CPANEL_USER','').strip() or 'arquind2'
 token=os.getenv('CPANEL_API_TOKEN','').strip()
 password=os.getenv('CPANEL_PASSWORD','')
 if not host or not (token or password):
  raise RuntimeError('CPANEL_ACCESS_REQUIRED: CPANEL_HOST e CPANEL_API_TOKEN ou CPANEL_PASSWORD; FTP nao cadastra subdominios')
 if not host.startswith('https://'):host='https://'+host
 parsed=urllib.parse.urlsplit(host)
 if parsed.username or parsed.password or parsed.path or parsed.query or parsed.fragment or parsed.scheme!='https' or parsed.port!=2083:
  raise RuntimeError('CPANEL_HOST deve ser origem HTTPS na porta 2083')
 if parsed.hostname not in {'arquindex.com.br','www.arquindex.com.br','ftp.arquindex.com.br','cpanel.arquindex.com.br'}:
  raise RuntimeError('CPANEL_HOST fora dos destinos Arquindex confirmados')
 header='cpanel '+user+':'+token if token else 'Basic '+base64.b64encode((user+':'+password).encode()).decode()
 def call(path,params=None):
  req=urllib.request.Request(host+path+('?' + urllib.parse.urlencode(params) if params else ''),headers={'Authorization':header,'Accept':'application/json'})
  with urllib.request.urlopen(req,timeout=30) as r:return json.load(r)
 info=call('/execute/DomainInfo/list_domains')
 if info.get('status')!=1 or (info.get('data') or {}).get('main_domain')!='arquindex.com.br':
  raise RuntimeError('CPANEL_ACCOUNT_NOT_VERIFIED')
 print('CPANEL_AUTHENTICATED',flush=True)
 return user,call,info['data']

def domain_root(call,host):
 r=call('/execute/DomainInfo/single_domain_data',{'domain':host})
 if r.get('status')!=1:raise RuntimeError('DOCUMENT_ROOT_NOT_CONFIRMED')
 root=(r.get('data') or {}).get('documentroot','')
 if not root.startswith('/') or '..' in root.split('/'):raise RuntimeError('INVALID_DOCUMENT_ROOT')
 return root.rstrip('/')

def register(rows):
 user,call,info=auth()
 known=set(info.get('sub_domains',[]))|set(info.get('addon_domains',[]))
 roots={}; mainroot=domain_root(call,'arquindex.com.br')
 for row in rows:
  if row['kind']=='technical':REPORT['preserved'].append({'entry':row['slug'],'reason':'pasta ou nome ambiguo sem dominio completo'});continue
  host=row['host']
  try:
   if host not in known:
    desired='public_html/subdominios/'+host
    p={'cpanel_jsonapi_user':user,'cpanel_jsonapi_apiversion':2,'cpanel_jsonapi_module':'SubDomain','cpanel_jsonapi_func':'addsubdomain','domain':row['slug'],'rootdomain':'arquindex.com.br','dir':desired,'disallowdot':0}
    r=call('/json-api/cpanel',p).get('cpanelresult') or {}
    if r.get('event',{}).get('result')!=1 or not any(x.get('result')==1 for x in r.get('data',[])):
     raise RuntimeError('CPANEL_DID_NOT_CONFIRM_CREATION')
    known.add(host)
   root=domain_root(call,host)
   if root==mainroot or root in roots.values():raise RuntimeError('SHARED_ROOT_REQUIRES_REVIEW')
   roots[host]=root;REPORT['registered'].append(host)
   print('REGISTERED',host,flush=True)
  except Exception as exc:
   REPORT['pending'].append({'host':host,'stage':'registration','error':type(exc).__name__+': '+str(exc)[:120]})
 report()
 return roots,mainroot,call

def ftp_root(ftp,root,user):
 candidates=[root]
 prefix='/home/'+user+'/'
 if root.startswith(prefix):candidates+=['/'+root[len(prefix):],root[len(prefix):]]
 for path in dict.fromkeys(candidates):
  try:ftp.cwd('/');ftp.cwd(path);return ftp.pwd()
  except ftplib.error_perm:continue
 raise RuntimeError('FTPS_CANNOT_ACCESS_CONFIRMED_ROOT')

def get(ftp,name):
 out=bytearray();ftp.retrbinary('RETR '+name,out.extend);return bytes(out)

def upload(ftp,root,files,backup,key):
 ftp.cwd(root)
 existing={posixpath.basename(x.rstrip('/')) for x in ftp.nlst()}
 if 'index.php' in existing or 'wp-config.php' in existing:
  raise RuntimeError('EXISTING_APPLICATION_PRESERVED')
 for name,data in files.items():
  old=get(ftp,name) if name in existing else None
  if name=='.htaccess':
   text=(old or b'').decode('utf-8')
   text=re.sub(r'(?ms)^# BEGIN ARQUINDEX RECOVERY\n.*?^# END ARQUINDEX RECOVERY\n?','',text)
   data=('# BEGIN ARQUINDEX RECOVERY\n'+data.decode()+'# END ARQUINDEX RECOVERY\n'+text).encode()
  if old==data:continue
  if old is not None:backup.writestr(key+'/'+name,old)
  temp='.arquindex-recovery-'+name.lstrip('.')+'.tmp'
  ftp.storbinary('STOR '+temp,io.BytesIO(data))
  if hashlib.sha256(get(ftp,temp)).digest()!=hashlib.sha256(data).digest():raise RuntimeError('TRANSFER_HASH_MISMATCH')
  ftp.rename(temp,name)
  if get(ftp,name)!=data:raise RuntimeError('PUBLISHED_HASH_MISMATCH')


def deploy(rows,roots,mainroot):
 password=os.getenv('FTP_PASSWORD','')
 if not password:raise RuntimeError('FTP_PASSWORD_REQUIRED')
 with zipfile.ZipFile(BACKUP,'w',zipfile.ZIP_DEFLATED) as backup,ftplib.FTP_TLS(timeout=45) as ftp:
  ftp.connect('ftp.arquindex.com.br',21);ftp.login('arquind2',password);ftp.prot_p();ftp.set_pasv(True)
  for row in sorted(rows,key=lambda x:x.get('action')!='hub'):
   host=row['host']
   if host not in roots:continue
   if row['kind']=='application':
    REPORT['preserved'].append({'host':host,'reason':'registro restaurado; aplicacao e dados exigem backup proprio'});continue
   # Do not redirect any host into a destination that failed registration.
   if row['action']=='alias' and row['target'] not in REPORT['uploaded']:
    REPORT['pending'].append({'host':host,'stage':'upload','error':'canonical target not registered'});continue
   try:
    root=ftp_root(ftp,roots[host],'arquind2')
    files={p.name:p.read_bytes() for p in (BASE/'dist'/host).iterdir() if p.is_file()}
    upload(ftp,root,files,backup,host)
    REPORT['uploaded'].append(host);print('FILES_VERIFIED',host,flush=True)
   except Exception as exc:REPORT['pending'].append({'host':host,'stage':'upload','error':type(exc).__name__+': '+str(exc)[:120]})
  # Publish only a dedicated directory in the main site. Existing homepage and
  # robots/sitemap files are not replaced by this restoration.
  root=ftp_root(ftp,mainroot,'arquind2');ftp.cwd(root)
  try:ftp.mkd('rede-documental')
  except ftplib.error_perm:pass
  ftp.cwd('rede-documental')
  # Directory links only to successfully uploaded hubs; no broken new graph.
  index=(BASE/'dist/portal/index.html').read_text()
  for row in rows:
   if row.get('action')=='hub' and row['host'] not in REPORT['uploaded']:
    index=re.sub(r'<li><a href="'+re.escape(row['canonical'])+r'">.*?</a></li>','',index)
  files={'index.html':index.encode(),'sitemap.xml':(BASE/'dist/portal/sitemap.xml').read_bytes()}
  upload(ftp,ftp.pwd(),files,backup,'rede-documental')
  # Add a single discovery link without replacing the main website.
  ftp.cwd(root)
  names={posixpath.basename(x.rstrip('/')) for x in ftp.nlst()}
  if 'index.html' in names:
   original=get(ftp,'index.html')
   html=original.decode('utf-8')
   marker='data-arquindex-recovery="directory"'
   if marker not in html and len(re.findall('</body>',html,re.I))==1:
    link='<nav '+marker+' aria-label="Guias documentais" style="padding:20px;text-align:center"><a href="https://www.arquindex.com.br/rede-documental/">Serviços e guias documentais da Arquindex</a></nav>'
    updated=re.sub('</body>',lambda m:link+m.group(),html,count=1,flags=re.I).encode()
    backup.writestr('portal-original/index.html',original)
    temp='.arquindex-recovery-home.tmp'
    ftp.storbinary('STOR '+temp,io.BytesIO(updated))
    if get(ftp,temp)!=updated:raise RuntimeError('HOMEPAGE_TRANSFER_MISMATCH')
    ftp.rename(temp,'index.html')
    if get(ftp,'index.html')!=updated:raise RuntimeError('HOMEPAGE_PUBLICATION_MISMATCH')
    REPORT['portal_link']='installed'
   elif marker in html:REPORT['portal_link']='already-installed'
   else:REPORT['portal_link']='requires-review'
  else:REPORT['portal_link']='requires-review'
 report()

def check(row):
 host=row['host']
 result={'host':host,'dns':False,'https':False,'sitemap':False}
 try:
  socket.getaddrinfo(host,443,type=socket.SOCK_STREAM);result['dns']=True
  expected=row['canonical']
  for part in ('','sitemap.xml'):
   req=urllib.request.Request('https://'+host+'/'+part,headers={'User-Agent':'Arquindex-Recovery/1.0'})
   with urllib.request.urlopen(req,timeout=12) as response:
    data=response.read(300000).decode('utf-8')
    if response.status!=200 or response.url!=expected+part:raise RuntimeError('UNEXPECTED_CANONICAL_RESPONSE')
    if part:
     from xml.etree import ElementTree as ET
     xml=ET.fromstring(data)
     assert [x.text for x in xml.iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]==[expected]
     result['sitemap']=True
    else:
     assert '<link rel="canonical" href="'+expected+'">' in data
     assert '<h1>' in data and 'noindex' not in data.lower()
     result['https']=True
 except Exception as exc:result['error']=type(exc).__name__
 return result

def main():
 rows=json.loads((BASE/'manifest.json').read_text())
 try:
  roots,mainroot,call=register(rows)
  if not roots:raise RuntimeError('NO_REGISTERED_DOMAINS')
  deploy(rows,roots,mainroot)
  try:REPORT['autossl_status']=call('/execute/SSL/start_autossl_check').get('status')
  except Exception as exc:REPORT['autossl_status']=type(exc).__name__
  selected=[r for r in rows if r['host'] in REPORT['uploaded']]
  with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
   REPORT['public']=list(pool.map(check,selected))
  failures=[r for r in REPORT['public'] if not (r['https'] and r['sitemap'])]
  if failures or REPORT['pending']:raise RuntimeError('RESTORATION_HAS_PENDING_ITEMS: see result.json')
  # Applications are explicitly pending backup recovery, not successful websites.
  if any(r['kind']=='application' for r in rows):raise RuntimeError('APPLICATIONS_REQUIRE_ORIGINAL_BACKUPS: see result.json')
 finally:report()
if __name__=='__main__':
 try:main()
 except Exception as exc:
  REPORT['blocker']=type(exc).__name__+': '+str(exc)[:220];report();print(REPORT['blocker'],flush=True);sys.exit(1)
