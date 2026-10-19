"""Publica somente o artigo ANPD; preserva paginas e restaura em falha."""
import os, io, ssl, socket, ftplib, hashlib, json, pathlib, urllib.request, urllib.robotparser
from html.parser import HTMLParser
from datetime import datetime, timezone
URL = 'https://www.arquindex.com.br/noticias/anpd-dosimetria-sancoes-lgpd-2026.html'
SOURCE = pathlib.Path('publicacao-noticias/anpd-dosimetria-sancoes-lgpd-2026.html')
TARGET = '/public_html/noticias/anpd-dosimetria-sancoes-lgpd-2026.html'
class Page(HTMLParser):
 def __init__(self):
  super().__init__(); self.h1=0; self.canonical=[]; self.robots=[]; self.links=[]; self.jsonld=[]; self.ld=False
 def handle_starttag(self,t,a):
  a=dict(a)
  if t=='h1': self.h1+=1
  if t=='link' and a.get('rel')=='canonical': self.canonical.append(a.get('href'))
  if t=='meta' and a.get('name','').lower()=='robots': self.robots.append(a.get('content',''))
  if t=='a' and a.get('href','').startswith('https://'): self.links.append(a['href'])
  if t=='script': self.ld=a.get('type')=='application/ld+json'
 def handle_endtag(self,t):
  if t=='script': self.ld=False
 def handle_data(self,d):
  if self.ld: self.jsonld.append(json.loads(d))
def validate(data):
 p=Page();p.feed(data.decode('utf-8'))
 assert p.h1==1 and p.canonical==[URL], 'INVALID_H1_CANONICAL'
 assert p.robots==['index,follow'], 'INVALID_ROBOTS'
 assert len(p.jsonld)==1 and p.jsonld[0]['@type']=='Article'
 assert p.jsonld[0]['dateModified']=='2026-10-19'
 assert p.jsonld[0]['mainEntityOfPage']['@id']==URL
 for text in ['proposta em consulta','30 de novembro de 2026','14h30','50 milhões','não garante','2026-10-19']:
  assert text in data.decode(), text
 return p
def http(u):
 req=urllib.request.Request(u,headers={'User-Agent':'ArquindexEditorialVerification/1.0','Cache-Control':'no-cache'})
 with urllib.request.urlopen(req,timeout=35) as r:
  return r.status,r.url,r.headers,r.read()
def get(f,p):
 out=bytearray();f.retrbinary('RETR '+p,out.extend);return bytes(out)
def put(f,p,b):f.storbinary('STOR '+p,io.BytesIO(b))
data=SOURCE.read_bytes();page=validate(data)
report={'url':URL,'sha256':hashlib.sha256(data).hexdigest(),'public_verified':False,'links':[]}
pathlib.Path('publish-report').mkdir(exist_ok=True)
try:
 # Teste de links comerciais antes de alterar o servidor.
 for u in sorted(set(page.links)):
  try:
   status,final,headers,body=http(u)
   item={'url':u,'status':status,'final_url':final}
  except Exception as e:
   item={'url':u,'error':type(e).__name__}
  report['links'].append(item)
  if u.startswith('https://www.arquindex.com.br/'):
   assert item.get('status')==200, 'COMMERCIAL_LINK_UNAVAILABLE '+u
 expected_ips=set(socket.gethostbyname_ex('ftp.arquindex.com.br')[2])
 provider_ips=set(socket.gethostbyname_ex('h59.servidorhh.com')[2])
 assert expected_ips & provider_ips, 'PROVIDER_DNS_MISMATCH'
 with ftplib.FTP_TLS(context=ssl.create_default_context(),timeout=45) as f:
  f.connect('h59.servidorhh.com',21);
  assert f.sock.getpeername()[0] in expected_ips, 'PROVIDER_IP_MISMATCH'
 f.login('arquind2',os.environ['FTP_PASSWORD']);f.prot_p()
  # A raiz corresponde ao mecanismo existente; nao descobrir outras raizes.
  homepage=get(f,'/public_html/index.html')
  assert b'arquindex' in homepage.lower(), 'WRONG_DOCUMENT_ROOT'
  try: previous=get(f,TARGET)
  except ftplib.error_perm as e:
   if not str(e).startswith('550'):raise
   previous=None
  stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
  backup='/seo-backups/anpd-'+stamp
  try:f.mkd('/seo-backups')
  except ftplib.error_perm:pass
  f.mkd(backup);put(f,backup+'/.htaccess',b'Require all denied\n')
  if previous is not None:put(f,backup+'/article.html.bak',previous)
  report['backup']=backup
  try:
   if previous is not None:assert get(f,TARGET)==previous,'CONCURRENT_CHANGE'
   put(f,TARGET,data);assert get(f,TARGET)==data,'FTPS_READBACK_MISMATCH'
   status,final,headers,public=http(URL)
   assert status==200 and final==URL,'HTTP_OR_REDIRECT_MISMATCH'
   assert public==data,'PUBLIC_CONTENT_MISMATCH'
   validate(public)
   assert 'noindex' not in headers.get('X-Robots-Tag','').lower(),'X_ROBOTS_NOINDEX'
   rs,rf,rh,rb=http('https://www.arquindex.com.br/robots.txt')
   robot=urllib.robotparser.RobotFileParser();robot.parse(rb.decode().splitlines())
   assert robot.can_fetch('Googlebot',URL),'ROBOTS_BLOCKED'
   report.update(public_verified=True,http=status,canonical=URL,robots_allowed=True,x_robots_tag=headers.get('X-Robots-Tag'),sha256_public=hashlib.sha256(public).hexdigest())
   assert get(f,'/public_html/index.html')==homepage,'HOMEPAGE_CHANGED_DURING_DEPLOY'
   print('PUBLIC_HTTP_200_BYTES_CANONICAL_ROBOTS_VERIFIED',URL,flush=True)
  except Exception:
   # Evitar desfazer mudanca concorrente.
   if get(f,TARGET)==data:
    if previous is None:f.delete(TARGET)
    else:put(f,TARGET,previous);assert get(f,TARGET)==previous
    report['rolled_back']=True
   raise
finally:
 pathlib.Path('publish-report/anpd.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
 print(json.dumps(report,ensure_ascii=False),flush=True)
