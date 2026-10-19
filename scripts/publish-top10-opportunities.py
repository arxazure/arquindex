import os,sys,io,ssl,ftplib,hashlib,json,re,pathlib,socket,urllib.request,urllib.robotparser
import xml.etree.ElementTree as ET
from datetime import datetime,timezone
from bs4 import BeautifulSoup
ROOT='https://www.arquindex.com.br/'
BASE='/public_html/'
P=json.loads(pathlib.Path('seo/top10-oportunidades-20261019/payload.json').read_text())
NEW='onde-digitalizar-documentos.html'
EXTRA=json.loads(pathlib.Path('seo/top10-oportunidades-20261019/pages.json').read_text())
def url_for(name):
 return ROOT+('' if name=='index.html' else name[:-10] if name.endswith('/index.html') else name)
STAMP=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
def digest(b):return hashlib.sha256(b).hexdigest()
def validate(b,url,marker=None):
 s=BeautifulSoup(b.decode('utf-8'),'html.parser')
 assert len(s.find_all('h1'))==1, ('H1',url)
 assert s.title and s.title.text.strip(),('TITLE',url)
 assert len(s.find_all('link',rel='canonical'))==1,('CANONICAL_COUNT',url)
 assert s.find('link',rel='canonical')['href']==url,('CANONICAL',url)
 assert s.find('meta',attrs={'name':'description'}),('DESCRIPTION',url)
 assert not any('noindex' in x.get('content','').lower() for x in s.find_all('meta',attrs={'name':re.compile('^(robots|googlebot)$',re.I)})),('NOINDEX',url)
 if marker:assert len(s.find_all(id=marker))==1,('MARKER',url)
 for tag in s.find_all('script',type='application/ld+json'):json.loads(tag.string or tag.text)
 return s
validate(P['html'].encode(),P['url'])
for name,page in EXTRA.items():
 assert name.startswith('guias-digitalizacao/') and '..' not in name
 assert page['url']==url_for(name)
 validate(page['html'].encode(),page['url'])
if '--check' in sys.argv:
 print('GUIDE_H1_CANONICAL_METADATA_JSONLD_VALID');sys.exit()
def http(u):
 req=urllib.request.Request(u,headers={'User-Agent':'ArquindexTop10Review/1.0','Cache-Control':'no-cache'})
 with urllib.request.urlopen(req,timeout=40) as r:return r.status,r.url,r.headers,r.read()
def get(f,p):
 b=bytearray();f.retrbinary('RETR '+p,b.extend);return bytes(b)
def put(f,p,b):f.storbinary('STOR '+p,io.BytesIO(b))
def meta_update(text,name,value,prop=False):
 key='property' if prop else 'name'
 matches=[]
 for m in re.finditer(r'<meta\b[^>]*>',text,re.I):
  tag=BeautifulSoup(m[0],'html.parser').find('meta')
  if str(tag.get(key,'')).lower()==name:matches.append(m)
 assert len(matches)<=1,('DUPLICATE_META',name)
 if matches:
  m=matches[0];old=BeautifulSoup(m[0],'html.parser').find('meta');old['content']=value
  return text[:m.start()]+str(old)+text[m.end():]
 return text
def augment(old,block,name):
 text=old.decode('utf-8');s=BeautifulSoup(text,'html.parser')
 marker=BeautifulSoup(block,'html.parser').find('section')['id']
 if s.find(id=marker):
  text,n=re.subn(r'<section\b[^>]*\bid=["\']'+re.escape(marker)+r'["\'][^>]*>.*?</section>',lambda _:block,text,count=1,flags=re.I|re.S);assert n==1
 else:
  # Inserir depois do primeiro bloco principal, preservando HTML e scripts existentes.
  start=re.search(r'</h1\s*>',text,re.I);assert start
  end=re.search(r'</section\s*>',text[start.end():],re.I)
  if end:at=start.end()+end.end()
  else:
   main_end=re.search(r'</main\s*>',text,re.I);assert main_end;at=main_end.start()
  text=text[:at]+'\n'+block+'\n'+text[at:]
 if name in P['metadata']:
  meta=P['metadata'][name]
  text,n=re.subn(r'<title\b[^>]*>.*?</title>',lambda _:'<title>'+meta['title']+'</title>',text,count=1,flags=re.I|re.S);assert n==1
  text=meta_update(text,'description',meta['description'])
  text=meta_update(text,'og:title',meta['title'],True)
  text=meta_update(text,'og:description',meta['description'],True)
 data=text.encode();url=url_for(name)
 after=validate(data,url,marker)
 # Nenhum script existente, rastreador, formulário ou H1 pode desaparecer.
 assert [str(x) for x in s.find_all('script')]==[str(x) for x in after.find_all('script')],('SCRIPTS_CHANGED',name)
 assert [str(x) for x in s.find_all('form')]==[str(x) for x in after.find_all('form')],('FORMS_CHANGED',name)
 assert s.h1.get_text()==after.h1.get_text(),('H1_CHANGED',name)
 return data,marker
report={'stamp':STAMP,'changes':[],'verified':False}
pathlib.Path('publish-report').mkdir(exist_ok=True)
expected=set(socket.gethostbyname_ex('ftp.arquindex.com.br')[2]);assert expected.intersection(socket.gethostbyname_ex('h59.servidorhh.com')[2])
try:
 with ftplib.FTP_TLS(context=ssl.create_default_context(),timeout=50) as f:
  f.connect('h59.servidorhh.com',21);assert f.sock.getpeername()[0] in expected
  f.login('arquind2',os.environ['FTP_PASSWORD']);f.prot_p()
  before={};planned={};markers={}
  for name,block in P['blocks'].items():
   old=get(f,BASE+name);assert b'arquindex' in old.lower()
   before[name]=old;planned[name],markers[name]=augment(old,block,name)
  try:before[NEW]=get(f,BASE+NEW)
  except ftplib.error_perm as e:
   if not str(e).startswith('550'):raise
   before[NEW]=None
  if before[NEW] is not None:
   assert b'top10-onde-digitalizar-20261019' in before[NEW] or before[NEW]==P['html'].encode(), 'DESTINATION_ALREADY_EXISTS_REVIEW_REQUIRED'
  planned[NEW]=P['html'].encode()
  for name,page in EXTRA.items():
   try:before[name]=get(f,BASE+name)
   except ftplib.error_perm as e:
    if not str(e).startswith('550'):raise
    before[name]=None
   if before[name] is not None:
    assert before[name]==page['html'].encode(), 'EXISTING_DESTINATION_NEEDS_REVIEW '+name
   planned[name]=page['html'].encode()
  ns='http://www.sitemaps.org/schemas/sitemap/0.9';ET.register_namespace('',ns)
  rootname='sitemap.xml';before[rootname]=get(f,BASE+rootname);root=ET.fromstring(before[rootname])
  childname='sitemap-top10-oportunidades-20261019.xml'
  if root.tag=='{'+ns+'}sitemapindex':
   try:before[childname]=get(f,BASE+childname)
   except ftplib.error_perm as e:
    if not str(e).startswith('550'):raise
    before[childname]=None
   child=ET.Element('{'+ns+'}urlset')
   for u in [P['url'],ROOT,ROOT+'digitalizacao.html',ROOT+'guarda_de_documentos.html']+[x['url'] for x in EXTRA.values()]:
    el=ET.SubElement(child,'{'+ns+'}url');ET.SubElement(el,'{'+ns+'}loc').text=u;ET.SubElement(el,'{'+ns+'}lastmod').text='2026-10-19'
   planned[childname]=ET.tostring(child,encoding='utf-8',xml_declaration=True)
   childurl=ROOT+childname
   if childurl not in [x.text for x in root.iter('{'+ns+'}loc')]:
    el=ET.SubElement(root,'{'+ns+'}sitemap');ET.SubElement(el,'{'+ns+'}loc').text=childurl
  elif root.tag=='{'+ns+'}urlset':
   for u in [P['url']]+[x['url'] for x in EXTRA.values()]:
    if u not in [x.text for x in root.iter('{'+ns+'}loc')]:
     el=ET.SubElement(root,'{'+ns+'}url');ET.SubElement(el,'{'+ns+'}loc').text=u;ET.SubElement(el,'{'+ns+'}lastmod').text='2026-10-19'
  else:raise RuntimeError('UNEXPECTED_SITEMAP')
  planned[rootname]=ET.tostring(root,encoding='utf-8',xml_declaration=True)
  assert set(x.text for x in ET.fromstring(before[rootname]).iter('{'+ns+'}loc')).issubset(x.text for x in root.iter('{'+ns+'}loc'))
  robot=urllib.robotparser.RobotFileParser();robot.parse(http(ROOT+'robots.txt')[3].decode().splitlines());assert robot.can_fetch('Googlebot',P['url'])
  assert all(robot.can_fetch('Googlebot',x['url']) for x in EXTRA.values()), 'ROBOTS_BLOCKS_NEW_COLLECTION'
  backup='/seo-backups/top10-oportunidades-'+STAMP
  try:f.mkd('/seo-backups')
  except ftplib.error_perm:pass
  f.mkd(backup);put(f,backup+'/.htaccess',b'Require all denied\n');report['backup']=backup
  for name,old in before.items():
   if old is not None:put(f,backup+'/'+hashlib.sha256(name.encode()).hexdigest()+'.bak',old)
  put(f,backup+'/manifest.json',json.dumps({name:hashlib.sha256(name.encode()).hexdigest()+'.bak' for name,old in before.items() if old is not None}).encode())
  # Criar apenas o diretorio da nova colecao, sem mover ou excluir paginas.
  try:f.cwd(BASE+'guias-digitalizacao')
  except ftplib.error_perm as e:
   if not str(e).startswith('550'):raise
   f.mkd(BASE+'guias-digitalizacao');f.cwd(BASE+'guias-digitalizacao')
  f.cwd('/')
  applied=[]
  try:
   # Todas as verificacoes anteriores precedem a primeira alteracao publica.
   for name,data in planned.items():
    if before[name] is not None:assert get(f,BASE+name)==before[name],('CONCURRENT_CHANGE',name)
    else:
     try:get(f,BASE+name)
     except ftplib.error_perm as e:
      if not str(e).startswith('550'):raise
     else:raise RuntimeError('NEW_DESTINATION_CREATED_CONCURRENTLY '+name)
    applied.append(name);put(f,BASE+name,data);assert get(f,BASE+name)==data
   for name,data in planned.items():
    url=url_for(name);status,final,headers,public=http(url)
    assert status==200 and final==url and public==data,('PUBLIC_BYTES_MISMATCH',url)
    if name.endswith('.html'):
     validate(public,url,markers.get(name));assert 'noindex' not in headers.get('X-Robots-Tag','').lower()
    elif name.endswith('.xml'):ET.fromstring(public)
    report['changes'].append({'url':url,'http':status,'sha256':digest(data),'canonical':url if name.endswith('.html') else None})
   report['verified']=True;print('TOP10_HOMEHOST_PUBLIC_HTTP200_HASH_CANONICAL_VERIFIED',flush=True)
  except Exception:
   rollback=[]
   for name in reversed(applied):
    if get(f,BASE+name)==planned[name]:
     if before[name] is None:f.delete(BASE+name)
     else:put(f,BASE+name,before[name]);assert get(f,BASE+name)==before[name]
     rollback.append(name)
   report['rolled_back']=rollback;raise
finally:
 pathlib.Path('publish-report/top10.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(report,ensure_ascii=False),flush=True)
