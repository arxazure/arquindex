import ftplib,hashlib,io,os,posixpath,time,urllib.request,xml.etree.ElementTree as ET
from datetime import datetime,timezone
from pathlib import Path
from bs4 import BeautifulSoup
from PIL import Image,ImageDraw,ImageFont
STAMP=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ');TODAY='2026-10-24'
TARGETS=[
{'id':'ARQ-102','host':'gestao-eletronica-de-documentos-ged.arquindex.com.br','file':'index.html','url':'https://gestao-eletronica-de-documentos-ged.arquindex.com.br/','title':'GED e ECM: Permissões, Versões e Recuperação | Arquindex','h1':'Como escolher e validar uma solução GED ou ECM','description':'Compare organização, GED e ECM por metadados, permissões, versões, pesquisa, integrações, recuperação e critérios de aceite do piloto.','art':'ged-ecm-permissoes-recuperacao-20261024.jpg','art_title':['GED E ECM','Teste acesso,','versão e busca.'],'bullets':['Metadados e pesquisa','Permissões e versões','Piloto e recuperação'],'section':'''<section class="aq-aeo-answer" data-aq-aeo="ARQ-102"><h2>Como escolher entre organizar arquivos, implantar GED e adotar ECM?</h2><p><strong>Resposta direta:</strong> organize primeiro quando o problema é classificação, nomes e responsabilidades. Use GED quando precisa pesquisar, controlar versões, permissões e documentos. Considere ECM quando documentos participam de processos, integrações, formulários e regras corporativas. A decisão deve ser validada em um piloto com documentos reais e sem dados pessoais desnecessários.</p><table><thead><tr><th>Necessidade</th><th>Recurso a testar</th><th>Evidência de aceite</th></tr></thead><tbody><tr><td>Localização</td><td>Metadados, OCR e filtros</td><td>Consultas recuperam a amostra esperada</td></tr><tr><td>Acesso</td><td>Perfis, grupos e exceções</td><td>Matriz de permissões aprovada</td></tr><tr><td>Histórico</td><td>Versões, auditoria e restauração</td><td>Versão anterior recuperada em teste</td></tr><tr><td>Processo</td><td>Entrada, revisão, aprovação e publicação</td><td>Fluxo executado com responsáveis</td></tr><tr><td>Saída</td><td>Exportação de arquivos e metadados</td><td>Pacote aberto e conferido fora do sistema</td></tr></tbody></table><p>O software não corrige sozinho classificação, temporalidade ou qualidade de metadados. Escopo, infraestrutura, suporte e responsabilidades devem constar do projeto.</p><p class="aq-review">Revisão editorial Arquindex: 24/10/2026. Referência: <a href="https://www.gov.br/conarq/pt-br">CONARQ</a>.</p><p><a href="https://www.arquindex.com.br/gestao_documental_documentos.html">Gestão documental</a> · <a href="https://www.arquindex.com.br/alfresco-belo-horizonte.html">Alfresco GED/ECM</a> · <a href="https://www.arquindex.com.br/solicitar-proposta-contratacao.html?utm_source=site&amp;utm_medium=guia_ged&amp;utm_campaign=arq102_ged_ecm_20261024">Planejar um piloto</a></p></section>'''},
{'id':'ARQ-104','host':'arquivamento.arquindex.com.br','file':'o-que-e.html','url':'https://arquivamento.arquindex.com.br/o-que-e.html','title':'Arquivamento de Documentos: Consulta e Devolução | Arquindex','h1':'Como organizar a consulta, retirada e devolução de documentos','description':'Entenda como inventário, localização, autorização, protocolo, retirada, consulta e devolução reduzem perdas na guarda e organização documental.','art':'arquivamento-consulta-devolucao-20261024.jpg','art_title':['ARQUIVAMENTO','Localize, retire','e devolva.'],'bullets':['Inventário e localização','Autorização e protocolo','Devolução rastreável'],'section':'''<section class="aq-aeo-answer" data-aq-aeo="ARQ-104"><h2>Como localizar, solicitar e devolver documentos guardados?</h2><p><strong>Resposta direta:</strong> cada caixa ou unidade deve ter identificador, localização e conteúdo resumido. A solicitação precisa registrar solicitante, finalidade, autorização, item, data e prazo. Na retirada e na devolução, confira o identificador e atualize a localização para manter a cadeia de responsabilidade.</p><table><thead><tr><th>Etapa</th><th>Registro mínimo</th><th>Controle</th></tr></thead><tbody><tr><td>Inventário</td><td>Código, tipo, período e unidade responsável</td><td>Relação conciliada com o acervo</td></tr><tr><td>Localização</td><td>Ambiente, estante e posição</td><td>Endereço lógico sem divulgar área restrita</td></tr><tr><td>Solicitação</td><td>Solicitante, finalidade, autorização e prazo</td><td>Protocolo numerado</td></tr><tr><td>Retirada</td><td>Item, data e responsável pela entrega</td><td>Status temporário e recibo</td></tr><tr><td>Devolução</td><td>Condição, data e posição final</td><td>Baixa do protocolo e conferência</td></tr><tr><td>Destinação</td><td>Prazo, fundamento e aprovação</td><td>Decisão documentada</td></tr></tbody></table><p>A página não divulga endereço operacional restrito. Atendimento, coleta e logística dependem de confirmação comercial. Eliminação exige temporalidade, autorização e requisitos aplicáveis.</p><p class="aq-review">Revisão editorial Arquindex: 24/10/2026. Referência: <a href="https://www.gov.br/conarq/pt-br">CONARQ</a>.</p><p><a href="https://www.arquindex.com.br/guarda_de_documentos.html">Guarda documental</a> · <a href="https://www.arquindex.com.br/gestao_documental_documentos.html">Gestão documental</a> · <a href="https://www.arquindex.com.br/solicitar-proposta-contratacao.html?utm_source=site&amp;utm_medium=guia_arquivamento&amp;utm_campaign=arq104_consulta_devolucao_20261024">Avaliar o acervo</a></p></section>'''},
{'id':'ARQ-106','host':'empresas-digitalizacao-documental-brasil-grandes-empresas.arquindex.com.br','file':'index.html','url':'https://empresas-digitalizacao-documental-brasil-grandes-empresas.arquindex.com.br/','title':'Digitalização em Grande Escala: Planejamento e Aceite | Arquindex','h1':'Como planejar a digitalização de grandes lotes documentais','description':'Planeje grandes lotes por inventário, lotes piloto, capacidade, logística, segurança, OCR, metadados, conferência, entregas parciais e aceite.','art':'digitalizacao-grande-escala-20261024.jpg','art_title':['GRANDES LOTES','Planeje capacidade','e aceite.'],'bullets':['Inventário e piloto','Capacidade e logística','Entregas e conciliação'],'section':'''<section class="aq-aeo-answer" data-aq-aeo="ARQ-106"><h2>Como planejar a digitalização de grandes lotes sem perder controle?</h2><p><strong>Resposta direta:</strong> transforme o acervo em lotes mensuráveis, faça inventário e amostra, valide preparação e captura, estime capacidade por etapa e planeje entregas parciais conciliadas. O cronograma deve considerar formatos especiais, exceções, transporte, segurança, OCR, indexação, conferência e correções — não apenas a velocidade do scanner.</p><table><thead><tr><th>Frente</th><th>Decisão</th><th>Evidência</th></tr></thead><tbody><tr><td>Inventário</td><td>Volumes, tipos, períodos e estado físico</td><td>Planilha e amostra representativa</td></tr><tr><td>Piloto</td><td>Perfis de captura, OCR, nomes e metadados</td><td>Lote teste aprovado</td></tr><tr><td>Capacidade</td><td>Preparação, captura, indexação e conferência</td><td>Produção medida por etapa</td></tr><tr><td>Logística</td><td>Coleta, custódia, prioridade e devolução</td><td>Protocolos e cadeia de responsabilidade</td></tr><tr><td>Entrega</td><td>Lotes, formatos, índices e correções</td><td>Inventário conciliado com arquivos</td></tr><tr><td>Aceite</td><td>Amostragem, exceções e prazos de ajuste</td><td>Relatório e aprovação por lote</td></tr></tbody></table><p>A URL não comprova atendimento nacional irrestrito. Região, coleta, capacidade e prazo dependem de avaliação comercial e logística. Não há promessa de volume, precisão ou prazo universal.</p><p class="aq-review">Revisão editorial Arquindex: 24/10/2026. Referências: <a href="https://www.gov.br/conarq/pt-br">CONARQ</a> e <a href="https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2020/decreto/d10278.htm">Decreto 10.278/2020</a>.</p><p><a href="https://www.arquindex.com.br/digitalizacao.html">Digitalização de documentos</a> · <a href="https://www.arquindex.com.br/digitalizacao-com-ocr.html">OCR e PDF pesquisável</a> · <a href="https://www.arquindex.com.br/solicitar-proposta-contratacao.html?utm_source=site&amp;utm_medium=guia_grandes_lotes&amp;utm_campaign=arq106_grande_escala_20261024">Dimensionar o projeto</a></p></section>'''}]
STYLE='<style id="arquindex-aeo-20261024-manha">.aq-aeo-answer{max-width:1120px;margin:36px auto;padding:28px;border:1px solid #d9e2ef;border-radius:16px;background:#fff;color:#0c1b33;box-sizing:border-box;overflow-wrap:anywhere}.aq-aeo-answer h2{color:#0b3d91}.aq-aeo-answer table{width:100%;border-collapse:collapse;margin:18px 0}.aq-aeo-answer th,.aq-aeo-answer td{padding:12px;border:1px solid #d9e2ef;text-align:left;vertical-align:top}.aq-aeo-answer th{background:#eaf0f8}.aq-review{font-size:.94rem;color:#42536b}@media(max-width:760px){html,body{max-width:100%;overflow-x:clip}body a{overflow-wrap:anywhere;word-break:break-word}.aq-aeo-answer{margin:24px 16px;padding:20px;overflow:hidden}.aq-aeo-answer table{display:block;max-width:100%;overflow-x:auto}.aq-aeo-answer th,.aq-aeo-answer td{min-width:135px}#arq-floating{right:12px!important;max-width:calc(100vw - 24px)!important}}</style>'
WIDGET=Path('conteudo/publicacao/_atendimento-flutuante.html').read_text('utf-8')
def get(f,p):b=bytearray();f.retrbinary('RETR '+p,b.extend);return bytes(b)
def mkdir(f,p):
 old=f.pwd()
 try:
  f.cwd('/')
  for x in p.strip('/').split('/'):
   if not x:continue
   try:f.mkd(x)
   except ftplib.error_perm as e:
    if not str(e).startswith('550'):raise
   f.cwd(x)
 finally:f.cwd(old)
def put(f,p,b,label):
 d,n=posixpath.dirname(p),posixpath.basename(p);tmp=d+'/.tmp-'+n+'-'+label
 f.storbinary('STOR '+tmp,io.BytesIO(b));assert get(f,tmp)==b
 try:f.delete(p)
 except ftplib.error_perm as e:
  if not str(e).startswith('550'):raise
 f.rename(tmp,p);assert get(f,p)==b
def locate(f,base,t):
 for root in [base+'/subdominios/'+t['host'],base+'/'+t['host'],'/subdominios/'+t['host'],'/'+t['host']]:
  p=root+'/'+t['file']
  try:
   b=get(f,p)
   if b'<html' in b.lower():return p,b
  except ftplib.all_errors:pass
 raise RuntimeError('TARGET_NOT_FOUND '+t['id'])
def transform(t,b):
 s=BeautifulSoup(b.decode('utf-8','ignore'),'html.parser');assert s.head and s.body
 for old in s.select('[data-aq-aeo="'+t['id']+'"],#arquindex-aeo-20261024-manha'):old.decompose()
 if s.title:s.title.string=t['title']
 else:n=s.new_tag('title');n.string=t['title'];s.head.append(n)
 desc=s.find('meta',attrs={'name':lambda v:v and v.lower()=='description'})
 if not desc:desc=s.new_tag('meta',attrs={'name':'description'});s.head.append(desc)
 desc['content']=t['description']
 h1s=s.find_all('h1');assert h1s;h1s[0].clear();h1s[0].append(t['h1'])
 for h in h1s[1:]:h.name='h2'
 for c in s.find_all('link',rel=lambda v:v and 'canonical' in v):c.decompose()
 s.head.append(s.new_tag('link',rel='canonical',href=t['url']));s.head.append(BeautifulSoup(STYLE,'html.parser'))
 for sel in ['#arq-floating-style','#arq-floating','#arq-floating-script','#arq-dedup-floats','.aq-brand-wa','#wa-widget-send-button']:
  for n in s.select(sel):n.decompose()
 for n in list(s.find_all('script')):
  src=(n.get('src') or '').lower();txt=n.string or n.get_text() or ''
  if '__arqWhatsappOptions' in txt or 'whatsapp_replace_crisp' in src or 'watiwidget.js' in src:n.decompose()
 frag=BeautifulSoup(WIDGET,'html.parser')
 for n in list(frag.contents):s.body.append(n)
 sec=BeautifulSoup(t['section'],'html.parser');footer=s.find('footer');footer.insert_before(sec) if footer else s.body.append(sec)
 out=str(s).encode();assert out.count(b'id="arq-floating"')==1 and t['id'].encode() in out and t['url'].encode() in out;return out
def public(url):
 req=urllib.request.Request(url+('&' if '?' in url else '?')+'verify='+STAMP,headers={'User-Agent':'ArquindexSEO/1.0','Cache-Control':'no-cache'})
 with urllib.request.urlopen(req,timeout=40) as r:return r.status,r.read(10000000)
def art_bytes(t):
 im=Image.new('RGB',(1200,1200),'#f4f7fc');d=ImageDraw.Draw(im)
 def tx(x,y,s,z=32,c='#0c1b33',bold=False):
  font='/usr/share/fonts/truetype/dejavu/DejaVuSans'+('-Bold' if bold else '')+'.ttf';d.text((x,y),s,font=ImageFont.truetype(font,z),fill=c)
 tx(70,70,'ARQUINDEX',48,'#0b3d91',True);tx(70,210,t['art_title'][0],30,'#0b3d91',True);tx(70,290,t['art_title'][1],52,'#0c1b33',True);tx(70,365,t['art_title'][2],52,'#0c1b33',True)
 for i,label in enumerate(t['bullets']):
  y=530+i*135;d.rounded_rectangle((70,y,1130,y+106),radius=18,fill='white',outline='#cbd7e9',width=2);tx(100,y+27,label,34)
 d.rectangle((0,1050,1200,1200),fill='#0b3d91');tx(70,1080,'Veja o guia completo',35,'white',True);tx(70,1133,t['host'],24,'white')
 b=io.BytesIO();im.save(b,'JPEG',quality=94);return b.getvalue()
with ftplib.FTP_TLS(timeout=60) as f:
 f.connect('ftp.arquindex.com.br',21);f.login('arquind2',os.environ['FTP_PASSWORD']);f.prot_p();f.set_pasv(True)
 base=None
 for c in ['/public_html','/home/arquind2/public_html']:
  try:
   if b'arquindex' in get(f,c+'/index.html').lower():base=c;break
  except ftplib.all_errors:pass
 assert base
 rec=[]
 for t in TARGETS:
  p,o=locate(f,base,t);rec.append((t,p,o,transform(t,o)))
 backup='/seo-backups/rodada-20261024-manha-'+STAMP;mkdir(f,backup);f.storbinary('STOR '+backup+'/.htaccess',io.BytesIO(b'Options -Indexes\nRequire all denied\n'))
 for t,p,o,u in rec:
  bp=backup+'/'+t['id'].lower()+'.html';f.storbinary('STOR '+bp,io.BytesIO(o));assert get(f,bp)==o;print('BACKUP_VERIFIED',t['id'],bp,hashlib.sha256(o).hexdigest(),flush=True)
 written=[]
 try:
  for t,p,o,u in rec:assert get(f,p)==o,'CONCURRENT_CHANGE '+t['id']
  for t,p,o,u in rec:put(f,p,u,STAMP);written.append((p,o));print('FTP_PUBLISHED_VERIFIED',t['id'],hashlib.sha256(u).hexdigest(),flush=True)
  time.sleep(2)
  for t,p,o,u in rec:
   st,body=public(t['url']);assert st==200 and t['id'].encode() in body and t['title'].encode() in body and t['url'].encode() in body and b'noindex' not in body.lower()
   print('PUBLIC_SOURCE_VERIFIED',t['id'],t['url'],hashlib.sha256(body).hexdigest(),flush=True)
  ns='http://www.sitemaps.org/schemas/sitemap/0.9';ET.register_namespace('',ns)
  for t,p,o,u in rec:
   sm=posixpath.dirname(p)+'/sitemap.xml'
   try:oldsm=get(f,sm)
   except ftplib.error_perm:oldsm=None
   root=ET.fromstring(oldsm) if oldsm else ET.Element('{'+ns+'}urlset');assert root.tag=='{'+ns+'}urlset'
   found=False
   for node in root:
    loc=node.find('{'+ns+'}loc')
    if loc is not None and (loc.text or '').rstrip('/')==t['url'].rstrip('/'):
     found=True;lm=node.find('{'+ns+'}lastmod')
     if lm is None:lm=ET.SubElement(node,'{'+ns+'}lastmod')
     lm.text=TODAY
   if not found:
    n=ET.SubElement(root,'{'+ns+'}url');ET.SubElement(n,'{'+ns+'}loc').text=t['url'];ET.SubElement(n,'{'+ns+'}lastmod').text=TODAY
   new=ET.tostring(root,encoding='utf-8',xml_declaration=True)
   if oldsm!=new:
    if oldsm:f.storbinary('STOR '+backup+'/'+t['id'].lower()+'-sitemap.xml',io.BytesIO(oldsm))
    put(f,sm,new,'sm-'+STAMP)
   st,b=public('https://'+t['host']+'/sitemap.xml');assert st==200 and t['url'].encode() in b;print('SITEMAP_PUBLIC_VERIFIED',t['id'],hashlib.sha256(b).hexdigest(),flush=True)
  folder=base+'/assets/social-arq101-106';mkdir(f,folder)
  for t,p,o,u in rec:
   art=art_bytes(t);ap=folder+'/'+t['art'];f.storbinary('STOR '+ap,io.BytesIO(art));assert get(f,ap)==art
   photo='https://www.arquindex.com.br/assets/social-arq101-106/'+t['art'];st,b=public(photo);assert st==200 and hashlib.sha256(b).digest()==hashlib.sha256(art).digest();print('IMAGE_PUBLIC_VERIFIED',t['id'],photo,hashlib.sha256(art).hexdigest(),flush=True)
 except Exception:
  for p,o in reversed(written):put(f,p,o,'rollback-'+STAMP)
  print('ROLLBACK_COMPLETED',flush=True);raise
