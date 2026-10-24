import ftplib,hashlib,io,os,posixpath,time,urllib.request,xml.etree.ElementTree as ET
from datetime import datetime,timezone
from pathlib import Path
from bs4 import BeautifulSoup
from PIL import Image,ImageDraw,ImageFont
STAMP=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ');TODAY='2026-10-24'
TARGETS=[
{'id':'ARQ-107','host':'consultoria-ocr-vantagens.arquindex.com.br','file':'empresas.html','url':'https://consultoria-ocr-vantagens.arquindex.com.br/empresas.html','title':'OCR: Pesquisa, Revisão e Critérios de Aceite | Arquindex','h1':'Quando o OCR torna documentos pesquisáveis e quando revisar','description':'Entenda como testar OCR, definir campos críticos, revisar exceções e aceitar uma entrega pesquisável sem prometer precisão universal.','art':'ocr-pesquisa-revisao-aceite-20261024.jpg','art_title':['OCR PESQUISÁVEL','Teste, revise','e aceite.'],'bullets':['Amostra representativa','Campos críticos','Exceções e aceite'],'section':"""<section class="aq-aeo-answer" data-aq-aeo="ARQ-107"><h2>Quando OCR torna o documento pesquisável e quando precisa de revisão?</h2><p><strong>Resposta direta:</strong> o OCR cria uma camada de texto que permite pesquisa e cópia, mas o resultado varia conforme resolução, contraste, idioma, tipografia, carimbos, manuscritos e estado físico. Para campos críticos, a entrega deve incluir amostra, regras de validação e revisão das exceções; não basta verificar se o PDF abre.</p><table><thead><tr><th>Etapa</th><th>O que testar</th><th>Evidência de aceite</th></tr></thead><tbody><tr><td>Amostra</td><td>Tipos, períodos, qualidade e exceções reais</td><td>Lote representativo documentado</td></tr><tr><td>Captura</td><td>Orientação, corte, legibilidade e páginas completas</td><td>Conferência visual por amostragem</td></tr><tr><td>OCR</td><td>Pesquisa por termos presentes na amostra</td><td>Consultas recuperam os arquivos esperados</td></tr><tr><td>Campos</td><td>Identificadores, datas e nomes definidos no escopo</td><td>Validação adicional para dados críticos</td></tr><tr><td>Exceções</td><td>Baixo contraste, carimbos, tabelas e manuscritos</td><td>Fila de revisão e registro da decisão</td></tr><tr><td>Entrega</td><td>PDF pesquisável, índices e relatório</td><td>Inventário conciliado com os arquivos</td></tr></tbody></table><p>Não existe taxa universal de precisão. O critério deve ser definido no piloto conforme o uso e o risco de cada campo.</p><p class="aq-review">Revisão editorial Arquindex: 24/10/2026. Referência: <a href="https://www.gov.br/conarq/pt-br">CONARQ</a>.</p><p><a href="https://www.arquindex.com.br/digitalizacao-com-ocr.html">Digitalização com OCR</a> · <a href="https://www.arquindex.com.br/digitalizacao.html">Digitalização de documentos</a> · <a href="https://www.arquindex.com.br/solicitar-proposta-contratacao.html?utm_source=site&amp;utm_medium=guia_ocr&amp;utm_campaign=arq107_ocr_aceite_20261024">Solicitar avaliação de amostra</a></p></section>"""},
{'id':'ARQ-110','host':'empresas-adequacao-lgpd-paulo.arquindex.com.br','file':'diagnostico.html','url':'https://empresas-adequacao-lgpd-paulo.arquindex.com.br/diagnostico.html','title':'Diagnóstico LGPD: Escopo, Entregáveis e Responsáveis | Arquindex','h1':'Como definir o escopo de um diagnóstico e plano de adequação LGPD','description':'Veja como delimitar tratamentos, riscos, responsáveis, entregáveis e prioridades de um diagnóstico LGPD sem promessa automática de conformidade.','art':'diagnostico-lgpd-escopo-entregaveis-20261024.jpg','art_title':['DIAGNÓSTICO LGPD','Defina escopo','e entregáveis.'],'bullets':['Tratamentos e riscos','Responsáveis e evidências','Plano priorizado'],'section':"""<section class="aq-aeo-answer" data-aq-aeo="ARQ-110"><h2>O que um diagnóstico LGPD entrega e como definir o escopo?</h2><p><strong>Resposta direta:</strong> o diagnóstico deve delimitar unidades, processos, sistemas, terceiros e categorias de dados; registrar responsáveis e evidências; priorizar riscos e transformar achados em plano de ação. Inventário, ROPA, RIPD, políticas, contratos e treinamentos entram conforme a necessidade apurada, não como pacote automático.</p><table><thead><tr><th>Frente</th><th>Pergunta de escopo</th><th>Entregável verificável</th></tr></thead><tbody><tr><td>Tratamentos</td><td>Quais processos usam dados pessoais?</td><td>Inventário com finalidade, fluxo e responsáveis</td></tr><tr><td>Bases e retenção</td><td>Qual fundamento e por quanto tempo?</td><td>Critérios documentados e lacunas</td></tr><tr><td>Risco</td><td>Quais impactos e controles existentes?</td><td>Matriz priorizada e evidências</td></tr><tr><td>Terceiros</td><td>Quem recebe ou opera dados?</td><td>Mapa de fornecedores e pontos contratuais</td></tr><tr><td>Governança</td><td>Quem decide, executa e revisa?</td><td>Plano com responsáveis, prazos e dependências</td></tr><tr><td>Acompanhamento</td><td>Como comprovar evolução?</td><td>Indicadores, revisões e registro das decisões</td></tr></tbody></table><p>Consultoria não garante conformidade automática: a organização continua responsável por decisões, recursos e implementação. Atendimento regional e presencial depende de confirmação comercial.</p><p class="aq-review">Revisão editorial Arquindex: 24/10/2026. Fontes: <a href="https://www.gov.br/anpd/pt-br">ANPD</a> e <a href="https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm">Lei 13.709/2018</a>.</p><p><a href="https://www.arquindex.com.br/lgpd-consultoria.html">Consultoria LGPD</a> · <a href="https://www.arquindex.com.br/dpo-terceirizado.html">DPO terceirizado</a> · <a href="https://www.arquindex.com.br/solicitar-proposta-contratacao.html?utm_source=site&amp;utm_medium=guia_lgpd&amp;utm_campaign=arq110_diagnostico_20261024">Definir o escopo</a></p></section>"""},
{'id':'ARQ-111','host':'gestao-de-arquivos-fisicos.arquindex.com.br','file':'index.html','url':'https://gestao-de-arquivos-fisicos.arquindex.com.br/','title':'Gestão de Arquivos Físicos: Consulta e Rastreabilidade | Arquindex','h1':'Como organizar, localizar e movimentar arquivos físicos','description':'Organize arquivos físicos com inventário, localização, autorização, protocolo de retirada, devolução, temporalidade e rastreabilidade.','art':'arquivos-fisicos-consulta-rastreabilidade-20261024.jpg','art_title':['ARQUIVOS FÍSICOS','Localize e','rastreie.'],'bullets':['Inventário e endereço','Retirada autorizada','Devolução registrada'],'section':"""<section class="aq-aeo-answer" data-aq-aeo="ARQ-111"><h2>Como localizar, solicitar e devolver documentos guardados?</h2><p><strong>Resposta direta:</strong> identifique caixas e documentos, associe cada unidade a uma localização lógica e registre toda movimentação. A solicitação deve indicar quem pediu, finalidade, autorização, item, data e prazo; a devolução encerra o protocolo após conferir condição e posição final.</p><table><thead><tr><th>Etapa</th><th>Registro mínimo</th><th>Controle esperado</th></tr></thead><tbody><tr><td>Inventário</td><td>Código, série, período e unidade responsável</td><td>Relação conciliada com o acervo</td></tr><tr><td>Localização</td><td>Ambiente, estante e posição</td><td>Endereço lógico atualizado</td></tr><tr><td>Solicitação</td><td>Solicitante, finalidade e autorização</td><td>Protocolo numerado e prazo</td></tr><tr><td>Retirada</td><td>Item, data e responsável pela entrega</td><td>Status temporário e recibo</td></tr><tr><td>Devolução</td><td>Condição, data e posição final</td><td>Baixa e conferência</td></tr><tr><td>Destinação</td><td>Prazo, fundamento e aprovação</td><td>Decisão documentada</td></tr></tbody></table><p>O fluxo não divulga endereço operacional restrito. Coleta, guarda, consulta e região de atendimento dependem de confirmação comercial. Digitalização não autoriza eliminação automática.</p><p class="aq-review">Revisão editorial Arquindex: 24/10/2026. Referência: <a href="https://www.gov.br/conarq/pt-br">CONARQ</a>.</p><p><a href="https://www.arquindex.com.br/guarda_de_documentos.html">Guarda de documentos</a> · <a href="https://www.arquindex.com.br/gestao_documental_documentos.html">Gestão documental</a> · <a href="https://www.arquindex.com.br/solicitar-proposta-contratacao.html?utm_source=site&amp;utm_medium=guia_arquivo_fisico&amp;utm_campaign=arq111_rastreabilidade_20261024">Avaliar o acervo</a></p></section>"""}
]
STYLE='<style id="arquindex-aeo-20261024-tarde">.aq-aeo-answer{max-width:1120px;margin:36px auto;padding:28px;border:1px solid #d9e2ef;border-radius:16px;background:#fff;color:#0c1b33;box-sizing:border-box;overflow-wrap:anywhere}.aq-aeo-answer h2{color:#0b3d91}.aq-aeo-answer table{width:100%;border-collapse:collapse;margin:18px 0}.aq-aeo-answer th,.aq-aeo-answer td{padding:12px;border:1px solid #d9e2ef;text-align:left;vertical-align:top}.aq-aeo-answer th{background:#eaf0f8}.aq-review{font-size:.94rem;color:#42536b}@media(max-width:760px){html,body{max-width:100%;overflow-x:clip}body a{overflow-wrap:anywhere;word-break:break-word}.aq-aeo-answer{margin:24px 16px;padding:20px;overflow:hidden}.aq-aeo-answer table{display:block;max-width:100%;overflow-x:auto}.aq-aeo-answer th,.aq-aeo-answer td{min-width:135px}#arq-floating{right:12px!important;max-width:calc(100vw - 24px)!important}}</style>'
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
 for old in s.select('[data-aq-aeo="'+t['id']+'"],#arquindex-aeo-20261024-tarde'):old.decompose()
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
 backup='/seo-backups/rodada-20261024-tarde-'+STAMP;mkdir(f,backup);f.storbinary('STOR '+backup+'/.htaccess',io.BytesIO(b'Options -Indexes\nRequire all denied\n'))
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
  folder=base+'/assets/social-arq107-112';mkdir(f,folder)
  for t,p,o,u in rec:
   art=art_bytes(t);ap=folder+'/'+t['art'];f.storbinary('STOR '+ap,io.BytesIO(art));assert get(f,ap)==art
   photo='https://www.arquindex.com.br/assets/social-arq107-112/'+t['art'];st,b=public(photo);assert st==200 and hashlib.sha256(b).digest()==hashlib.sha256(art).digest();print('IMAGE_PUBLIC_VERIFIED',t['id'],photo,hashlib.sha256(art).hexdigest(),flush=True)
 except Exception:
  for p,o in reversed(written):put(f,p,o,'rollback-'+STAMP)
  print('ROLLBACK_COMPLETED',flush=True);raise
