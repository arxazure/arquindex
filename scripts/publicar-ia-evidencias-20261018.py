import os,io,ftplib,hashlib,json,urllib.request,xml.etree.ElementTree as ET
from datetime import datetime,timezone
from bs4 import BeautifulSoup
URL='https://www.arquindex.com.br/noticias/ia-documental-evidencias-sandbox-anpd-2026.html'
STAMP=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
IMAGE="https://lh3.googleusercontent.com/p/AF1QipMR4ruLP5ehClgeoP4Dkh0yVJMvJD2EOTtZXWVS"
def fetch(u):
 with urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'ArquindexEditorial/1.0','Cache-Control':'no-cache'}),timeout=40) as r:
  assert r.status==200
  return r.read()
def get(f,p):
 b=bytearray();f.retrbinary('RETR '+p,b.extend);return bytes(b)
def mkdir(f,p):
 current=f.pwd()
 try:
  f.cwd('/')
  for x in p.strip('/').split('/'):
   try:f.mkd(x)
   except ftplib.error_perm:pass
   f.cwd(x)
 finally:f.cwd(current)
def rawput(f,p,b):f.storbinary('STOR '+p,io.BytesIO(b))
report=[]
with ftplib.FTP_TLS(timeout=50) as f:
 f.connect('ftp.arquindex.com.br',21);f.login('arquind2',os.environ['FTP_PASSWORD']);f.prot_p()
 base='/public_html';get(f,base+'/index.html')
 backup='/seo-backups/ia-evidencias-'+STAMP;mkdir(f,backup);rawput(f,backup+'/.htaccess',b'Require all denied\n')
 def put(p,b):
  try:old=get(f,p)
  except ftplib.error_perm:old=None
  if old==b:return
  if old is not None:rawput(f,backup+'/'+hashlib.sha256(p.encode()).hexdigest()+'.bak',old)
  mkdir(f,p.rsplit('/',1)[0])
  if old is not None:assert get(f,p)==old,'CONCURRENT_CHANGE'
  rawput(f,p,b);assert get(f,p)==b
  report.append({'path':p,'sha256':hashlib.sha256(b).hexdigest()})
 image=fetch(IMAGE);assert len(image)>10000 and image[:2]==b'\xff\xd8'
 put(base+'/assets/social/ia-evidencias-20261018.jpg',image)
 article=open('publicacao-noticias/ia-documental-evidencias-sandbox-anpd-2026.html','rb').read()
 soup=BeautifulSoup(article,'html.parser')
 assert len(soup.find_all('h1'))==1 and soup.find('link',rel='canonical')['href']==URL
 put(base+'/noticias/ia-documental-evidencias-sandbox-anpd-2026.html',article)
 assert fetch(URL)==article,'PUBLIC_ARTICLE_MISMATCH'
 assert fetch('https://www.arquindex.com.br/assets/social/ia-evidencias-20261018.jpg')==image
 card='<section id="noticia-ia-evidencias-20261018"><h2><a href="'+URL+'">IA documental: quais evidências pedir ao fornecedor?</a></h2><p>Análise de 18/10/2026 sobre controles declarados, testados e pendentes, com referência ao terceiro relatório do Sandbox da ANPD.</p></section>'
 for relative in ['noticias/index.html','blog/index.html']:
  try:original=get(f,base+'/'+relative);s=BeautifulSoup(original,'html.parser')
  except ftplib.error_perm:
   if relative.startswith('blog'):continue
   s=BeautifulSoup('<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Notícias e análises | Arquindex</title><link rel="canonical" href="https://www.arquindex.com.br/noticias/"><link rel="stylesheet" href="https://www.arquindex.com.br/assets/arquindex-restored/theme.css?v=3739ea98ed"><style>body{font:17px/1.7 Arial;color:#0c1b33;max-width:1100px;margin:auto;padding:24px}a{color:#0b3d91}section{padding:24px;border:1px solid #d9e2ef;border-radius:12px;margin:20px 0}</style></head><body><a href="https://www.arquindex.com.br/"><img width="205" src="https://www.arquindex.com.br/assets/arquindex-restored/arquindex-logo-oficial.webp" alt="Arquindex"></a><main><h1>Notícias e análises</h1></main><footer><a href="https://www.arquindex.com.br/blog/">Artigos</a></footer></body></html>','html.parser')
  if not s.find(id='noticia-ia-evidencias-20261018'):
   m=s.find('main');assert m is not None
   m.append(BeautifulSoup(card,'html.parser'));put(base+'/'+relative,str(s).encode())
 ns='http://www.sitemaps.org/schemas/sitemap/0.9';ET.register_namespace('',ns)
 child=ET.Element('{'+ns+'}urlset')
 for u in [URL,'https://www.arquindex.com.br/noticias/']:
  e=ET.SubElement(child,'{'+ns+'}url');ET.SubElement(e,'{'+ns+'}loc').text=u;ET.SubElement(e,'{'+ns+'}lastmod').text='2026-10-18'
 childpath=base+'/sitemap-noticias-20261018.xml';put(childpath,ET.tostring(child,encoding='utf-8',xml_declaration=True))
 rootpath=base+'/sitemap.xml';root=ET.fromstring(get(f,rootpath))
 if root.tag.endswith('sitemapindex'):
  location='https://www.arquindex.com.br/sitemap-noticias-20261018.xml'
  if location not in [x.text for x in root.iter('{'+ns+'}loc')]:
   e=ET.SubElement(root,'{'+ns+'}sitemap');ET.SubElement(e,'{'+ns+'}loc').text=location
 elif root.tag.endswith('urlset'):
  if URL not in [x.text for x in root.iter('{'+ns+'}loc')]:
   e=ET.SubElement(root,'{'+ns+'}url');ET.SubElement(e,'{'+ns+'}loc').text=URL;ET.SubElement(e,'{'+ns+'}lastmod').text='2026-10-18'
 else:raise RuntimeError('UNEXPECTED_SITEMAP_ROOT')
 put(rootpath,ET.tostring(root,encoding='utf-8',xml_declaration=True))
 ET.fromstring(fetch('https://www.arquindex.com.br/sitemap-noticias-20261018.xml'))
 ET.fromstring(fetch('https://www.arquindex.com.br/sitemap.xml'))
 print('PUBLIC_ARTICLE_HTTP200_IMAGE_SITEMAPS_VERIFIED',URL,flush=True)
 print('REPORT',json.dumps(report),flush=True)
os.makedirs('publish-report',exist_ok=True)
with open('publish-report/report.json','w') as out:json.dump({'url':URL,'backup':backup,'changes':report,'public_verified':True},out,indent=2)
