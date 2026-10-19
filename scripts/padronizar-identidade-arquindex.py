import ftplib,io,os,re,json,hashlib,urllib.request,concurrent.futures,posixpath
from datetime import datetime,timezone
from bs4 import BeautifulSoup
STAMP=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
HEADER="<header class=\"aq-header\"><div class=\"aq-top\">\n<a aria-label=\"Arquindex — início\" href=\"https://www.arquindex.com.br/\"><img alt=\"Arquindex — eficiência máxima em gestão de documentos\" class=\"aq-logo\" height=\"71\" src=\"https://www.arquindex.com.br/assets/arquindex-restored/arquindex-logo-oficial.webp\" width=\"205\"/></a>\n<button aria-controls=\"aq-nav\" aria-expanded=\"false\" class=\"aq-toggle\" type=\"button\">Menu</button>\n<nav aria-label=\"Navegação principal\" class=\"aq-nav\" id=\"aq-nav\">\n<a href=\"https://www.arquindex.com.br/servicos/\">Soluções</a><a href=\"https://www.arquindex.com.br/institucional/\">Institucional</a><a href=\"https://www.arquindex.com.br/clientes-cases/\">Clientes e cases</a><a href=\"https://www.arquindex.com.br/blog/\">Artigos</a><a href=\"https://www.arquindex.com.br/fornecedores/\">Fornecedores</a><a href=\"https://www.arquindex.com.br/compliance-transparencia/\">Transparência</a></nav>\n<div class=\"aq-contact\">Fale com nossa equipe<br/><a href=\"https://wa.me/5531973632725?text=Ol%C3%A1%2C%20Arquindex!%20Gostaria%20de%20falar%20com%20um%20especialista%20e%20solicitar%20um%20or%C3%A7amento.\">31 97363-2725</a><br/><a href=\"mailto:comercial@arquindex.com.br\" style=\"font-size:12px\">comercial@arquindex.com.br</a></div></div></header>"
FOOTER="<footer class=\"aq-footer\"><div class=\"aq-foot\"><div><img alt=\"Arquindex\" class=\"aq-logo\" height=\"71\" src=\"https://www.arquindex.com.br/assets/arquindex-restored/arquindex-logo-oficial.webp\" width=\"205\"/><p>20 anos de experiência em gestão documental, digitalização, privacidade e tecnologia.<br/>Sede em Belo Horizonte. Unidades em São Paulo e Lisboa.</p></div><div>\n<a href=\"https://www.arquindex.com.br/institucional/\">Institucional</a><a href=\"https://www.arquindex.com.br/quem-somos/\">Quem somos</a><a href=\"https://www.arquindex.com.br/fornecedores/\">Fornecedores</a><a href=\"https://www.arquindex.com.br/trabalhe-conosco/\">Trabalhe conosco</a><a href=\"https://www.arquindex.com.br/compliance-transparencia/\">Compliance e Transparência</a></div><div>\n<a href=\"https://www.arquindex.com.br/blog/\">Artigos e guias</a><a href=\"https://www.arquindex.com.br/blog-acervo.html\">Acervo de artigos</a><a href=\"https://www.arquindex.com.br/#soro-blog\">Blog original</a><a href=\"https://arquindex-web-production.up.railway.app/\">Website corporativo no Railway</a><a href=\"https://www.arquindex.com.br/mapa-plataformas.html\">Mapa dos sites</a><a href=\"https://www.arquindex.com.br/portal-do-cliente\">Portal do Cliente</a><a href=\"https://www.arquindex.com.br/contato-orcamento/\">Solicitar orçamento</a><a href=\"https://www.arquindex.com.br/politica-de-privacidade/\">Política de Privacidade</a><a href=\"https://www.arquindex.com.br/cookies/\">Política de Cookies</a></div></div></footer>"
MARK='arquindex-identidade-20261018'
CSS="""body[data-aq-brand] #hero h2{font-size:20px!important;line-height:1.6!important;max-width:850px;color:#fff!important;margin:14px 0!important}body[data-aq-brand] #hero .btn-get-started{white-space:nowrap!important}body[data-aq-brand] #hero .container{padding-left:24px!important;padding-right:24px!important}@media(max-width:760px){body[data-aq-brand] #hero h2{font-size:17px!important}body[data-aq-brand] #hero .d-flex{flex-wrap:wrap;gap:16px}body[data-aq-brand] #hero .btn-get-started{font-size:14px!important}}body[data-aq-brand] #hero{height:auto!important;min-height:460px;padding:64px 0!important}body[data-aq-brand] #hero h1{color:#fff!important;line-height:1.2!important;font-size:42px!important;max-width:900px}body[data-aq-brand] #hero p{color:#fff!important;font-size:18px!important;line-height:1.65!important;max-width:800px}body[data-aq-brand] #hero a.btn-get-started{background:#0b3d91!important;color:#fff!important;border-radius:8px!important;padding:14px 22px!important;text-decoration:none!important}body[data-aq-brand] .aq-trust-grid{display:grid!important;grid-template-columns:repeat(3,minmax(0,1fr))!important;gap:20px!important}body[data-aq-brand] .trust-card{min-width:0!important;width:auto!important;overflow-wrap:anywhere}body[data-aq-brand] .aq-legacy{min-width:0}body[data-aq-brand] table{max-width:100%}@media(max-width:760px){body[data-aq-brand] #hero{min-height:0;padding:40px 0!important}body[data-aq-brand] #hero h1{font-size:30px!important}body[data-aq-brand] #hero p{font-size:17px!important}body[data-aq-brand] .aq-trust-grid{grid-template-columns:1fr!important}body[data-aq-brand] table{width:100%;max-width:100%;box-sizing:border-box}body[data-aq-brand] .aq-contact{width:100%;text-align:left;padding-top:8px}}body[data-aq-brand]{background:#fff!important;color:#0c1b33!important;font-family:Arial,Helvetica,sans-serif!important;margin:0!important;line-height:1.65}body[data-aq-brand]>.aq-header{background:#fff!important;color:#0c1b33!important;padding:0!important}body[data-aq-brand]>.aq-footer{background:#071a3a!important;color:#dce7f7!important}body[data-aq-brand] main{max-width:1200px;margin:auto}body[data-aq-brand] main.wrap{padding:40px 22px}body[data-aq-brand] main h2{color:#0b3d91}body[data-aq-brand] main p,body[data-aq-brand] main li{font-size:16px}body[data-aq-brand] main a:not(.btn):not(.cta):not(.cta-primary){color:#0b3d91}body[data-aq-brand] .aq-header a{color:#0b3d91!important}body[data-aq-brand] .aq-footer a{color:#dce7f7!important}body[data-aq-brand] .cta,body[data-aq-brand] .cta-primary{display:inline-block;background:#0b3d91!important;color:white!important;padding:12px 20px;border-radius:8px;text-decoration:none}body[data-aq-brand] main .card,body[data-aq-brand] main .box{background:#fff;color:#0c1b33;border:1px solid #d9e2ef;border-radius:14px}body[data-aq-brand] table{background:#fff;color:#0c1b33}body[data-aq-brand] th{background:#eaf0f8}body[data-aq-brand] main .hero,body[data-aq-brand] #hero{background:linear-gradient(105deg,rgba(7,31,77,.95),rgba(11,79,167,.72)),url('https://www.arquindex.com.br/assets/arquindex-restored/corporativo-hero-wide.webp') center/cover!important}body[data-aq-brand] main .hero h1,body[data-aq-brand] main .hero p{color:#fff!important}body[data-aq-brand] .aq-brand-wa{position:fixed;left:18px;bottom:18px;z-index:105;background:#187c3d;color:#fff!important;padding:12px 18px;border-radius:30px;text-decoration:none;box-shadow:0 5px 20px #0003;font-weight:700}@media(max-width:760px){body[data-aq-brand] main.wrap{padding:28px 18px}body[data-aq-brand] main h1{font-size:32px}body[data-aq-brand] table{display:block;overflow-x:auto}}"""
JS="""document.querySelectorAll('.aq-toggle').forEach(function(b){b.addEventListener('click',function(){var n=document.getElementById('aq-nav');if(n){var on=n.classList.toggle('aq-open');b.setAttribute('aria-expanded',String(on));}});});"""
def get(f,p):
 b=bytearray();f.retrbinary('RETR '+p,b.extend);return bytes(b)
def put(f,p,b):
 f.storbinary('STOR '+p,io.BytesIO(b));assert get(f,p)==b
def mkdir(f,p):
 current=f.pwd()
 try:
  f.cwd('/')
  for part in p.strip('/').split('/'):
   try:f.mkd(part)
   except ftplib.error_perm:pass
   f.cwd(part)
 finally:f.cwd(current)
def public(url):
 req=urllib.request.Request(url,headers={'User-Agent':'ArquindexDesign/1.0','Cache-Control':'no-cache'})
 with urllib.request.urlopen(req,timeout=25) as r:return r.status,r.read()
def identity(s):
 return ([x.get_text() for x in s.find_all('h1')],[str(x) for x in s.find_all('link',rel='canonical')],s.title.get_text() if s.title else '')
def transform(original):
 s=BeautifulSoup(original.decode('utf8'),'html.parser')
 if not s.body or not s.head or not s.find('main') or 'arquindex' not in s.get_text().lower():return None
 if s.find(id=MARK):
  before=identity(s)
  s.find(id=MARK).string=CSS
  for card in s.select('.trust-card'):
   card.parent['class']=list(set(card.parent.get('class',[])+['aq-trust-grid']))
  assert identity(s)==before
  return str(s).encode('utf8')
 before=identity(s)
 for h in s.find_all('header'):h.decompose()
 for h in s.find_all('footer'):h.decompose()
 top=s.find(id='topbar')
 if top:top.decompose()
 s.body['data-aq-brand']='20261018'
 for card in s.select('.trust-card'):
  card.parent['class']=list(set(card.parent.get('class',[])+['aq-trust-grid']))
 main=s.find('main');cl=main.get('class',[])
 if 'aq-legacy' not in cl:main['class']=cl+['aq-legacy']
 for href in ['https://www.arquindex.com.br/assets/arquindex-restored/bootstrap.css','https://www.arquindex.com.br/assets/arquindex-restored/theme.css?v=3739ea98ed']:
  s.head.append(s.new_tag('link',rel='stylesheet',href=href))
 style=s.new_tag('style',id=MARK);style.string=CSS;s.head.append(style)
 s.body.insert(0,BeautifulSoup(HEADER,'html.parser'))
 s.body.append(BeautifulSoup(FOOTER,'html.parser'))
 if not s.select('.aq-wa,.aq-brand-wa'):
  a=s.new_tag('a',href='https://wa.me/5531973632725');a['class']='aq-brand-wa';a['aria-label']='Conversar com a Arquindex no WhatsApp';a.string='WhatsApp';s.body.append(a)
 js=s.new_tag('script');js.string=JS;s.body.append(js)
 assert identity(s)==before,'SEO_IDENTITY_CHANGED'
 return str(s).encode('utf8')
with ftplib.FTP_TLS(timeout=50) as f:
 f.connect('ftp.arquindex.com.br',21);f.login('arquind2',os.environ['FTP_PASSWORD']);f.prot_p()
 base=None
 for p in ['/public_html','/home/arquind2/public_html']:
  try:
   if b'arquindex' in get(f,p+'/index.html').lower():base=p;break
  except ftplib.error_perm:pass
 assert base,'PUBLIC_ROOT_NOT_FOUND'
 def listing(path):
  try:return list(f.mlsd(path))
  except ftplib.all_errors:return []
 selected=os.getenv('DESIGN_TARGET','')
 roots={};targets=[]
 if selected:
  from urllib.parse import urlsplit
  parsed=urlsplit(selected);host=parsed.hostname;filename=parsed.path.lstrip('/') or 'index.html'
  for root in [base+'/subdominios/'+host,base+'/'+host,'/subdominios/'+host,'/'+host]:
   try:
    b=get(f,root+'/'+filename)
    decoded=b.decode('utf8','ignore')
    if '<html' in decoded.lower() and 'arquindex' in decoded.lower():
     targets=[(root+'/'+filename,selected)];roots[root]='https://'+host+'/';break
   except ftplib.error_perm:pass
 else:
  for parent in [base,base+'/subdominios']:
   for name,meta in listing(parent):
    if name.endswith('.arquindex.com.br') and meta.get('type')=='dir':roots[parent+'/'+name]='https://'+name+'/'
  roots[base+'/noticias']='https://www.arquindex.com.br/noticias/'
  roots[base+'/blog']='https://www.arquindex.com.br/blog/'
  def walk(root,url,depth=0):
   for name,meta in listing(root):
    if name.startswith('.') or name in ['assets','node_modules','seo-backups']:continue
    path=root+'/'+name
    if meta.get('type')=='dir' and depth<2:walk(path,url+name+'/',depth+1)
    elif meta.get('type')=='file' and name.endswith('.html') and not re.match(r'(sitechecker|google[0-9a-f])',name):targets.append((path,url+('' if name=='index.html' else name)))
  for root,url in roots.items():walk(root,url)
 assert targets,'NO_TARGETS'
 assert len(targets)<=3000,('INVENTORY_TOO_LARGE',len(targets))
 print('INVENTORY',len(roots),'roots',len(targets),'pages',flush=True)
 backup='/seo-backups/identidade-'+STAMP;mkdir(f,backup)
 put(f,backup+'/.htaccess',b'Options -Indexes\nRequire all denied\n')
 report=[]
 for i,(path,url) in enumerate(targets):
  try:
   original=get(f,path);new=transform(original)
   if new is None:continue
   key=hashlib.sha256(path.encode()).hexdigest()[:20]+'.html'
   put(f,backup+'/'+key,original)
   if get(f,path)!=original:raise RuntimeError('CONCURRENT_CHANGE')
   put(f,path,new)
   report.append({'path':path,'url':url,'backup':backup+'/'+key,'sha256':hashlib.sha256(new).hexdigest(),'state':'ftp_verified'})
   print('UPDATED',url,flush=True)
  except Exception as e:
   print('FAILED',url,type(e).__name__,str(e),flush=True)
   report.append({'url':url,'state':'failed','error':str(e)})
 def verify(rec):
  if rec['state']!='ftp_verified':return rec
  try:
   code,b=public(rec['url']+'?brandcheck='+STAMP)
   assert code==200 and MARK.encode() in b and b'arquindex-logo-oficial.webp' in b
   rec['state']='public_verified'
  except Exception as e:rec['state']='public_pending';rec['error']=str(e)
  return rec
 with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:report=list(pool.map(verify,report))
 os.makedirs('design-report',exist_ok=True)
 with open('design-report/identity-report.json','w') as out:json.dump(report,out,ensure_ascii=False,indent=2)
 counts={state:sum(r['state']==state for r in report) for state in set(r['state'] for r in report)}
 print('RESULT_COUNTS',json.dumps(counts),flush=True)
 print('ARQ099',json.dumps([r for r in report if 'custo-beneficio.html' in r['url']],ensure_ascii=False),flush=True)
 assert any(r['state']=='public_verified' for r in report),'NO_PUBLIC_VERIFIED'
