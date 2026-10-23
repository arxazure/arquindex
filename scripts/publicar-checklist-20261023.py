"""Publica guia e arte com TLS verificado, backup, sitemap e comprovação HTTP."""
import ftplib,io,json,os,ssl,hashlib,urllib.request,xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime,timezone
from bs4 import BeautifulSoup
from PIL import Image,ImageDraw,ImageFont
ROOT='https://www.arquindex.com.br/'
PAGE='blog/digitalizacao-ocr-ecm-checklist/index.html'
URL=ROOT+'blog/digitalizacao-ocr-ecm-checklist/'
ART='assets/social/checklist-documental-20261023.jpg'
def get(f,p):
 b=bytearray();f.retrbinary('RETR '+p,b.extend);return bytes(b)
def put(f,p,b):
 f.storbinary('STOR '+p,io.BytesIO(b));assert get(f,p)==b
def dirs(f,p):
 a=''
 for part in p.split('/')[:-1]:
  a+='/'+part
  try:f.mkd(a)
  except ftplib.error_perm:pass
def http(u):
 with urllib.request.urlopen(urllib.request.Request(u,headers={'Cache-Control':'no-cache','User-Agent':'ArquindexEditorial/1.0'}),timeout=25) as r:
  return r.status,r.url,r.headers,r.read()
def main():
 stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
 im=Image.new('RGB',(1200,1200),'#102d4e');d=ImageDraw.Draw(im)
 font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
 bold='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
 def txt(x,y,s,n=40,color='white',b=False):d.text((x,y),s,font=ImageFont.truetype(bold if b else font,n),fill=color)
 d.rectangle((70,75,125,83),fill='#7ebcf1');txt(145,48,'ARQUINDEX',43,b=True)
 txt(70,175,'Da caixa ao',70,b=True);txt(70,264,'documento',70,b=True);txt(70,353,'pesquisável',70,color='#8cc7f7',b=True)
 for i,(title,detail) in enumerate([('01  Preparação','Defina o acervo e a sequência'),('02  Captura + OCR','Teste a leitura em uma amostra'),('03  Indexação','Combine campos e nomes'),('04  Acesso + conferência','Valide permissões e entrega')]):
  y=485+i*125;d.rounded_rectangle((65,y,1135,y+105),radius=16,fill='#1c3d60');txt(90,y+8,title,34,b=True);txt(90,y+56,detail,29,color='#d8e6f3')
 txt(70,1030,'Belo Horizonte e região • avaliação de escopo',30)
 txt(70,1090,'www.arquindex.com.br',34,b=True)
 out=io.BytesIO();im.save(out,format='JPEG',quality=94);image=out.getvalue()
 soup=BeautifulSoup(Path(PAGE).read_text(),'html.parser')
 assert len(soup.find_all('h1'))==1 and soup.find('link',rel='canonical')['href']==URL
 faq=[]
 for h in soup.find_all('h3'):
  p=h.find_next_sibling('p')
  if p:faq.append({'@type':'Question','name':h.get_text(),'acceptedAnswer':{'@type':'Answer','text':p.get_text()}})
 schema={'@context':'https://schema.org','@graph':[{'@type':'Organization','@id':ROOT+'#organization','name':'Arquindex','url':ROOT},{'@type':'Article','@id':URL+'#article','headline':soup.h1.get_text(),'mainEntityOfPage':URL,'inLanguage':'pt-BR','author':{'@id':ROOT+'#organization'},'publisher':{'@id':ROOT+'#organization'},'image':ROOT+ART,'datePublished':'2026-10-23'},{'@type':'FAQPage','@id':URL+'#faq','mainEntity':faq}]}
 ld=soup.new_tag('script',type='application/ld+json');ld.string=json.dumps(schema,ensure_ascii=False);soup.head.append(ld)
 page=str(soup).encode()
 report={'page':URL,'image':ROOT+ART,'status':'pending'}
 Path('publish-report').mkdir(exist_ok=True)
 with ftplib.FTP_TLS(context=ssl.create_default_context(),timeout=45) as f:
  f.connect('h59.servidorhh.com',21);f.login('arquind2',os.environ['FTP_PASSWORD']);f.prot_p()
  assert b'arquindex' in get(f,'/public_html/index.html').lower()
  backup='/seo-backups/checklist-'+stamp
  dirs(f,backup+'/placeholder');put(f,backup+'/.htaccess',b'Require all denied\n')
  def save(path,b):
   target='/public_html/'+path;dirs(f,target)
   try:old=get(f,target)
   except ftplib.error_perm:old=None
   if old is not None:
    put(f,backup+'/'+hashlib.sha256(path.encode()).hexdigest()+'.bak',old)
    assert get(f,target)==old,'CONCURRENT_CHANGE'
   put(f,target,b)
   return old
  oldart=save(ART,image);oldpage=save(PAGE,page)
  try:
   st,fin,hd,body=http(URL);assert st==200 and fin==URL
   s=BeautifulSoup(body,'html.parser');assert s.h1.get_text()==soup.h1.get_text()
   assert 'noindex' not in hd.get('X-Robots-Tag','').lower()
   assert s.find('link',rel='canonical')['href']==URL
   st,fin,hd,body=http(ROOT+ART);assert st==200 and body==image
  except Exception:
   for p,old in [(PAGE,oldpage),(ART,oldart)]:
    if old is None:f.delete('/public_html/'+p)
    else:put(f,'/public_html/'+p,old)
   raise
  # Link from existing news page, preserving other content.
  try:
   p='noticias.html';old=get(f,'/public_html/'+p);text=old.decode()
   if URL not in text:
    fragment='<section id="aq-checklist-20261023" style="max-width:1100px;margin:24px auto;padding:24px;background:#fff;color:#102d4e"><h2>Digitalização, OCR e ECM: checklist de contratação</h2><p>Confira como definir amostra, metadados, permissões e critérios de aceite.</p><a href="'+URL+'">Ler o guia da Arquindex</a></section>'
    assert '</body>' in text
    save(p,text.replace('</body>',fragment+'</body>',1).encode())
   report['internal_link']='updated'
  except Exception as e:report['internal_link_pending']=str(e)
  ns='http://www.sitemaps.org/schemas/sitemap/0.9';ET.register_namespace('',ns)
  name='sitemap-checklist-documental.xml';root=ET.Element('{'+ns+'}urlset')
  u=ET.SubElement(root,'{'+ns+'}url');ET.SubElement(u,'{'+ns+'}loc').text=URL
  ET.SubElement(u,'{'+ns+'}lastmod').text='2026-10-23'
  xml=ET.tostring(root,encoding='utf-8',xml_declaration=True);save(name,xml)
  assert http(ROOT+name)[0]==200
  try:
   old=get(f,'/public_html/robots.txt');text=old.decode()
   line='Sitemap: '+ROOT+name
   if line not in text:save('robots.txt',(text.rstrip()+'\n'+line+'\n').encode())
   report['sitemap_discovery']='robots.txt'
  except Exception as e:report['sitemap_discovery_pending']=str(e)
  try:
   key=get(f,'/public_html/indexnow-key.txt').decode().strip()
   assert key and http(ROOT+key+'.txt')[3].decode().strip()==key
   req=urllib.request.Request('https://api.indexnow.org/indexnow',data=json.dumps({'host':'www.arquindex.com.br','key':key,'keyLocation':ROOT+key+'.txt','urlList':[URL]}).encode(),headers={'Content-Type':'application/json'})
   with urllib.request.urlopen(req,timeout=25) as r:report['indexnow_http']=r.status
  except Exception as e:report['indexnow_pending']=str(e)
  report.update(status='published',sha256=hashlib.sha256(page).hexdigest(),backup=backup)
 Path('publish-report/checklist-20261023.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
 print(json.dumps(report,ensure_ascii=False),flush=True)
if __name__=='__main__':main()
