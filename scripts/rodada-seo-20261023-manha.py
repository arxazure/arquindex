import ftplib,hashlib,io,os,posixpath,time,urllib.request,xml.etree.ElementTree as ET
from datetime import datetime,timezone
from pathlib import Path
from bs4 import BeautifulSoup
from PIL import Image,ImageDraw,ImageFont
STAMP=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
TODAY='2026-10-23'
TARGETS=[
{'id':'ARQ-086','host':'databook-petrobras-elaboracao.arquindex.com.br','file':'index.html','url':'https://databook-petrobras-elaboracao.arquindex.com.br/','title':'Montagem de Databook: Índice, Revisões e Aceite | Arquindex','h1':'Como montar e conferir um databook técnico','description':'Veja como estruturar índice mestre, controlar revisões, relacionar certificados e equipamentos e conferir pendências antes do aceite de um databook.','campaign':'arq086_databook_20261023','art':'databook-controle-revisoes-20261023.jpg','art_title':['DATABOOK TÉCNICO','Índice, revisão','e aceite.'],'bullets':['Índice mestre','Rastreio de revisões','Conferência de pendências'],'section':'''<section class="aq-aeo-answer" data-aq-aeo="ARQ-086"><h2>Quais documentos entram no databook e como conferir revisões?</h2><p><strong>Resposta direta:</strong> o escopo deve nascer de uma lista de documentos requerida pelo contrato ou projeto. O índice mestre relaciona cada item ao equipamento, pacote, fornecedor, revisão, situação e evidência de aceite. A entrega só deve ser fechada depois de tratar faltas, duplicidades e versões superadas.</p><table><thead><tr><th>Controle</th><th>Campo mínimo</th><th>Critério de aceite</th></tr></thead><tbody><tr><td>Índice mestre</td><td>Código, título, disciplina e responsável</td><td>Todos os itens requeridos estão representados</td></tr><tr><td>Revisão</td><td>Número, data, origem e situação</td><td>Versão vigente distinguida das anteriores</td></tr><tr><td>Vínculo técnico</td><td>Equipamento, tag, pacote ou contrato</td><td>Documento recuperável pelo contexto correto</td></tr><tr><td>Pendência</td><td>Item, responsável, prazo e decisão</td><td>Exceções registradas antes do fechamento</td></tr><tr><td>Entrega</td><td>Estrutura, formato e protocolo</td><td>Amostra e índice conferidos pelo contratante</td></tr></tbody></table><p>O nome do endereço descreve uma intenção de busca e não declara vínculo, homologação ou contrato com a Petrobras. O índice e os requisitos variam conforme o contrato e precisam ser confirmados para cada projeto.</p><p class="aq-review">Revisão editorial Arquindex: 23/10/2026. Referência institucional: <a href="https://www.gov.br/arquivonacional/pt-br">Arquivo Nacional</a>.</p><p><a href="https://www.arquindex.com.br/seo-regional/gestao-documental-ecm-databooks/">Gestão documental, ECM e databooks</a> · <a href="https://www.arquindex.com.br/gestao_documental.html">Gestão documental</a> · <a href="https://www.arquindex.com.br/solicitar-proposta-contratacao.html?utm_source=site&amp;utm_medium=pagina_servico&amp;utm_campaign=arq086_databook_20261023">Definir escopo do databook</a></p></section>'''},
{'id':'ARQ-087','host':'decreto10278-nova-lima.arquindex.com.br','file':'custo.html','url':'https://decreto10278-nova-lima.arquindex.com.br/custo.html','title':'Orçamento de Digitalização em Nova Lima: Como Calcular | Arquindex','h1':'Quais fatores formam o orçamento de digitalização em Nova Lima','description':'Entenda como volume, formato, preparação, OCR, indexação, controle de qualidade e logística influenciam o orçamento de digitalização em Nova Lima.','campaign':'arq087_orcamento_novalima_20261023','art':'orcamento-digitalizacao-nova-lima-20261023.jpg','art_title':['DIGITALIZAÇÃO','Orçamento sem','número inventado.'],'bullets':['Volume e formato','OCR e indexação','Logística confirmada'],'section':'''<section class="aq-aeo-answer" data-aq-aeo="ARQ-087"><h2>Quais fatores entram no orçamento de digitalização de documentos em Nova Lima?</h2><p><strong>Resposta direta:</strong> o preço depende do volume conferido, estado e formato dos documentos, preparação necessária, resolução e formato de saída, OCR, campos de indexação, controle de qualidade, prazo e logística. Sem uma amostra ou inventário, um preço por página isolado pode omitir etapas relevantes.</p><table><thead><tr><th>Fator</th><th>O que medir</th><th>Impacto no escopo</th></tr></thead><tbody><tr><td>Volume</td><td>Páginas, caixas, plantas ou livros</td><td>Capacidade, prazo e forma de cobrança</td></tr><tr><td>Preparação</td><td>Grampos, dobras, fragilidade e ordem</td><td>Tempo antes da captura</td></tr><tr><td>Captura</td><td>Formato, cor, resolução e frente/verso</td><td>Equipamento e tamanho dos arquivos</td></tr><tr><td>OCR e indexação</td><td>Idiomas, campos e precisão esperada</td><td>Processamento e conferência</td></tr><tr><td>Qualidade</td><td>Amostra, critérios e correção</td><td>Evidência de aceite</td></tr><tr><td>Logística</td><td>Local, retirada, cadeia de custódia e devolução</td><td>Condições confirmadas na proposta</td></tr></tbody></table><p>Esta página não declara unidade física em Nova Lima. Coleta, atendimento presencial e demais condições logísticas dependem de confirmação comercial. A referência ao Decreto 10.278/2020 exige análise do contexto e não transforma qualquer arquivo digital em equivalente ao original automaticamente.</p><p class="aq-review">Revisão editorial Arquindex: 23/10/2026. Fonte primária: <a href="https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2020/decreto/d10278.htm">Decreto 10.278/2020</a>.</p><p><a href="https://www.arquindex.com.br/digitalizacao.html">Digitalização de documentos</a> · <a href="https://www.arquindex.com.br/digitalizacao-documentos-nova-lima.html">Digitalização em Nova Lima</a> · <a href="https://www.arquindex.com.br/solicitar-proposta-contratacao.html?utm_source=site&amp;utm_medium=pagina_local&amp;utm_campaign=arq087_orcamento_novalima_20261023">Solicitar orçamento com amostra</a></p></section>'''},
{'id':'ARQ-088','host':'encontrar-consultoria-conformidade-lgpd-bom-custo-beneficio.arquindex.com.br','file':'comparativo.html','url':'https://encontrar-consultoria-conformidade-lgpd-bom-custo-beneficio.arquindex.com.br/comparativo.html','title':'Preço da Consultoria LGPD: Escopo e Entregáveis | Arquindex','h1':'Como comparar preço, escopo e entregáveis de uma consultoria LGPD','description':'Compare diagnóstico, processos abrangidos, entregáveis, responsáveis, revisão e acompanhamento antes de avaliar o preço de uma consultoria LGPD.','campaign':'arq088_preco_lgpd_20261023','art':'preco-consultoria-lgpd-20261023.jpg','art_title':['CONSULTORIA LGPD','Compare escopo,','não só preço.'],'bullets':['Diagnóstico definido','Entregáveis verificáveis','Responsabilidades claras'],'section':'''<section class="aq-aeo-answer" data-aq-aeo="ARQ-088"><h2>Quais fatores entram no orçamento de consultoria de adequação LGPD?</h2><p><strong>Resposta direta:</strong> o orçamento varia com quantidade de unidades e processos, maturidade existente, volume de sistemas e fornecedores, categorias de dados, entrevistas, entregáveis, treinamento, revisão jurídica necessária e acompanhamento. Propostas só são comparáveis quando descrevem o mesmo escopo e o mesmo critério de aceite.</p><table><thead><tr><th>Critério</th><th>Pergunta para comparar</th><th>Evidência contratual</th></tr></thead><tbody><tr><td>Diagnóstico</td><td>Quais áreas, processos e sistemas entram?</td><td>Escopo e agenda de levantamento</td></tr><tr><td>Entregáveis</td><td>Quais registros, políticas e planos serão produzidos?</td><td>Lista, formato e responsável pela validação</td></tr><tr><td>Responsabilidades</td><td>Quem fornece dados, revisa e aprova?</td><td>Matriz de papéis e prazos</td></tr><tr><td>Pendências</td><td>Como riscos e ações não concluídas serão tratados?</td><td>Plano priorizado e registro de decisão</td></tr><tr><td>Continuidade</td><td>Há revisão, treinamento ou DPO após o projeto?</td><td>Período, canais e limites do suporte</td></tr></tbody></table><p>Consultoria não garante conformidade automática: a organização continua responsável por decisões, recursos e execução. Preço baixo sem escopo comparável pode apenas transferir atividades para a equipe interna.</p><p class="aq-review">Revisão editorial Arquindex: 23/10/2026. Fonte primária: <a href="https://www.gov.br/anpd/pt-br">Autoridade Nacional de Proteção de Dados</a>.</p><p><a href="https://www.arquindex.com.br/lgpd-consultoria.html">Consultoria LGPD</a> · <a href="https://www.arquindex.com.br/dpo-terceirizado.html">DPO terceirizado</a> · <a href="https://www.arquindex.com.br/solicitar-proposta-contratacao.html?utm_source=site&amp;utm_medium=pagina_comercial&amp;utm_campaign=arq088_preco_lgpd_20261023">Comparar escopo da consultoria</a></p></section>'''}]
STYLE='<style id="arquindex-aeo-20261023-manha">.aq-aeo-answer{max-width:1120px;margin:36px auto;padding:28px;border:1px solid #d9e2ef;border-radius:16px;background:#fff;color:#0c1b33;box-sizing:border-box;overflow-wrap:anywhere}.aq-aeo-answer h2{color:#0b3d91}.aq-aeo-answer table{width:100%;border-collapse:collapse;margin:18px 0}.aq-aeo-answer th,.aq-aeo-answer td{padding:12px;border:1px solid #d9e2ef;text-align:left;vertical-align:top}.aq-aeo-answer th{background:#eaf0f8}.aq-review{font-size:.94rem;color:#42536b}@media(max-width:760px){.aq-aeo-answer{margin:24px 16px;padding:20px}.aq-aeo-answer table{display:block;overflow-x:auto}.aq-aeo-answer th,.aq-aeo-answer td{min-width:145px}}</style>'
WIDGET=Path('conteudo/publicacao/_atendimento-flutuante.html').read_text('utf-8')
def get(f,p): b=bytearray(); f.retrbinary('RETR '+p,b.extend); return bytes(b)
def mkdir(f,p):
 old=f.pwd()
 try:
  f.cwd('/')
  for x in p.strip('/').split('/'):
   if not x: continue
   try: f.mkd(x)
   except ftplib.error_perm as e:
    if not str(e).startswith('550'): raise
   f.cwd(x)
 finally: f.cwd(old)
def put(f,p,b,label):
 d,n=posixpath.dirname(p),posixpath.basename(p); tmp=d+'/.tmp-'+n+'-'+label
 f.storbinary('STOR '+tmp,io.BytesIO(b)); assert get(f,tmp)==b
 try: f.delete(p)
 except ftplib.error_perm as e:
  if not str(e).startswith('550'): raise
 f.rename(tmp,p); assert get(f,p)==b
def locate(f,base,t):
 for root in [base+'/subdominios/'+t['host'],base+'/'+t['host'],'/subdominios/'+t['host'],'/'+t['host']]:
  p=root+'/'+t['file']
  try:
   b=get(f,p)
   if b'<html' in b.lower(): return p,b
  except ftplib.all_errors: pass
 raise RuntimeError('TARGET_NOT_FOUND '+t['id'])
def transform(t,b):
 s=BeautifulSoup(b.decode('utf-8','ignore'),'html.parser'); assert s.head and s.body
 for old in s.select('[data-aq-aeo="'+t['id']+'"]'): old.decompose()
 if s.title: s.title.string=t['title']
 else: n=s.new_tag('title'); n.string=t['title']; s.head.append(n)
 desc=s.find('meta',attrs={'name':lambda v:v and v.lower()=='description'})
 if not desc: desc=s.new_tag('meta',attrs={'name':'description'}); s.head.append(desc)
 desc['content']=t['description']
 h1s=s.find_all('h1'); assert h1s; h1s[0].clear(); h1s[0].append(t['h1'])
 for h in h1s[1:]: h.name='h2'
 for c in s.find_all('link',rel=lambda v:v and 'canonical' in v): c.decompose()
 s.head.append(s.new_tag('link',rel='canonical',href=t['url']))
 for old in s.select('#arquindex-aeo-20261023-manha'): old.decompose()
 s.head.append(BeautifulSoup(STYLE,'html.parser'))
 for sel in ['#arq-floating-style','#arq-floating','#arq-floating-script','#arq-dedup-floats','.aq-brand-wa','#wa-widget-send-button']:
  for n in s.select(sel): n.decompose()
 for n in list(s.find_all('script')):
  src=(n.get('src') or '').lower(); txt=n.string or n.get_text() or ''
  if '__arqWhatsappOptions' in txt or 'whatsapp_replace_crisp' in src or 'watiwidget.js' in src: n.decompose()
 frag=BeautifulSoup(WIDGET,'html.parser')
 for n in list(frag.contents): s.body.append(n)
 sec=BeautifulSoup(t['section'],'html.parser'); footer=s.find('footer'); footer.insert_before(sec) if footer else s.body.append(sec)
 out=str(s).encode()
 assert out.count(b'id="arq-floating"')==1 and t['id'].encode() in out and t['url'].encode() in out
 return out
def public(url):
 req=urllib.request.Request(url+('&' if '?' in url else '?')+'verify='+STAMP,headers={'User-Agent':'ArquindexSEO/1.0','Cache-Control':'no-cache'})
 with urllib.request.urlopen(req,timeout=40) as r: return r.status,r.read(10000000)
def art_bytes(t):
 im=Image.new('RGB',(1200,1200),'#f4f7fc'); d=ImageDraw.Draw(im)
 def tx(x,y,s,z=32,c='#0c1b33',bold=False):
  font='/usr/share/fonts/truetype/dejavu/DejaVuSans'+('-Bold' if bold else '')+'.ttf'; d.text((x,y),s,font=ImageFont.truetype(font,z),fill=c)
 tx(70,70,'ARQUINDEX',48,'#0b3d91',True); tx(70,210,t['art_title'][0],30,'#0b3d91',True); tx(70,290,t['art_title'][1],52,'#0c1b33',True); tx(70,365,t['art_title'][2],52,'#0c1b33',True)
 for i,label in enumerate(t['bullets']):
  y=530+i*135; d.rounded_rectangle((70,y,1130,y+106),radius=18,fill='white',outline='#cbd7e9',width=2); tx(100,y+27,label,34)
 d.rectangle((0,1050,1200,1200),fill='#0b3d91'); tx(70,1080,'Veja o guia completo',35,'white',True); tx(70,1133,t['host'],25,'white')
 b=io.BytesIO(); im.save(b,'JPEG',quality=94); return b.getvalue()
with ftplib.FTP_TLS(timeout=60) as f:
 f.connect('ftp.arquindex.com.br',21); f.login('arquind2',os.environ['FTP_PASSWORD']); f.prot_p(); f.set_pasv(True)
 base=None
 for c in ['/public_html','/home/arquind2/public_html']:
  try:
   if b'arquindex' in get(f,c+'/index.html').lower(): base=c; break
  except ftplib.all_errors: pass
 assert base
 rec=[]
 for t in TARGETS:
  p,o=locate(f,base,t); rec.append((t,p,o,transform(t,o)))
 backup='/seo-backups/rodada-20261023-manha-'+STAMP; mkdir(f,backup); f.storbinary('STOR '+backup+'/.htaccess',io.BytesIO(b'Options -Indexes\nRequire all denied\n'))
 for t,p,o,u in rec:
  bp=backup+'/'+t['id'].lower()+'.html'; f.storbinary('STOR '+bp,io.BytesIO(o)); assert get(f,bp)==o; print('BACKUP_VERIFIED',t['id'],bp,hashlib.sha256(o).hexdigest(),flush=True)
 written=[]
 try:
  for t,p,o,u in rec: assert get(f,p)==o,'CONCURRENT_CHANGE '+t['id']
  for t,p,o,u in rec:
   put(f,p,u,STAMP); written.append((p,o)); print('FTP_PUBLISHED_VERIFIED',t['id'],hashlib.sha256(u).hexdigest(),flush=True)
  time.sleep(2)
  for t,p,o,u in rec:
   st,body=public(t['url']); assert st==200 and t['id'].encode() in body and t['title'].encode() in body and t['url'].encode() in body and b'noindex' not in body.lower()
   print('PUBLIC_SOURCE_VERIFIED',t['id'],t['url'],hashlib.sha256(body).hexdigest(),flush=True)
  ns='http://www.sitemaps.org/schemas/sitemap/0.9'; ET.register_namespace('',ns)
  for t,p,o,u in rec:
   sm=posixpath.dirname(p)+'/sitemap.xml'
   try: oldsm=get(f,sm)
   except ftplib.error_perm: oldsm=None
   root=ET.fromstring(oldsm) if oldsm else ET.Element('{'+ns+'}urlset'); assert root.tag=='{'+ns+'}urlset'
   found=False
   for node in root:
    loc=node.find('{'+ns+'}loc')
    if loc is not None and (loc.text or '').rstrip('/')==t['url'].rstrip('/'):
     found=True; lm=node.find('{'+ns+'}lastmod')
     if lm is None: lm=ET.SubElement(node,'{'+ns+'}lastmod')
     lm.text=TODAY
   if not found:
    n=ET.SubElement(root,'{'+ns+'}url'); ET.SubElement(n,'{'+ns+'}loc').text=t['url']; ET.SubElement(n,'{'+ns+'}lastmod').text=TODAY
   new=ET.tostring(root,encoding='utf-8',xml_declaration=True)
   if oldsm!=new:
    if oldsm: f.storbinary('STOR '+backup+'/'+t['id'].lower()+'-sitemap.xml',io.BytesIO(oldsm))
    put(f,sm,new,'sm-'+STAMP)
   st,b=public('https://'+t['host']+'/sitemap.xml'); assert st==200 and t['url'].encode() in b
   print('SITEMAP_PUBLIC_VERIFIED',t['id'],hashlib.sha256(b).hexdigest(),flush=True)
  folder=base+'/assets/social-arq083-088'; mkdir(f,folder)
  for t,p,o,u in rec:
   art=art_bytes(t); ap=folder+'/'+t['art']; f.storbinary('STOR '+ap,io.BytesIO(art)); assert get(f,ap)==art
   photo='https://www.arquindex.com.br/assets/social-arq083-088/'+t['art']; st,b=public(photo); assert st==200 and hashlib.sha256(b).digest()==hashlib.sha256(art).digest()
   print('IMAGE_PUBLIC_VERIFIED',t['id'],photo,hashlib.sha256(art).hexdigest(),flush=True)
 except Exception:
  for p,o in reversed(written): put(f,p,o,'rollback-'+STAMP)
  print('ROLLBACK_COMPLETED',flush=True); raise
