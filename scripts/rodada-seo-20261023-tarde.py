import ftplib,hashlib,io,os,posixpath,time,urllib.request,xml.etree.ElementTree as ET
from datetime import datetime,timezone
from pathlib import Path
from bs4 import BeautifulSoup
from PIL import Image,ImageDraw,ImageFont
STAMP=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ'); TODAY='2026-10-23'
TARGETS=[
{'id':'ARQ-089','host':'escolher-consultoria-especializada-protecao-dados.arquindex.com.br','file':'checklist.html','url':'https://escolher-consultoria-especializada-protecao-dados.arquindex.com.br/checklist.html','title':'Governança da Informação: Checklist de Contratação | Arquindex','h1':'Como comparar fornecedores de governança e mapeamento da informação','description':'Use critérios objetivos para comparar escopo, inventário de repositórios, responsáveis, classificação, acessos, ciclo de vida e plano de implantação.','campaign':'arq089_governanca_20261023','art':'governanca-checklist-20261023.jpg','art_title':['GOVERNANÇA','Compare escopo','e evidências.'],'bullets':['Repositórios e responsáveis','Acesso e ciclo de vida','Plano e critérios de aceite'],'section':'''<section class="aq-aeo-answer" data-aq-aeo="ARQ-089"><h2>Como comparar fornecedores de governança e mapeamento da informação?</h2><p><strong>Resposta direta:</strong> compare o que será inventariado, quais responsáveis participarão, como repositórios e fluxos serão classificados, quais riscos serão priorizados e quais entregáveis permitirão acompanhar a implantação. Uma proposta genérica sem limites, responsáveis e critérios de aceite não é comparável.</p><table><thead><tr><th>Critério</th><th>Pergunta</th><th>Evidência esperada</th></tr></thead><tbody><tr><td>Escopo</td><td>Quais áreas, repositórios e fluxos entram?</td><td>Relação de unidades e exclusões</td></tr><tr><td>Responsáveis</td><td>Quem informa, valida e decide?</td><td>Matriz de papéis e agenda</td></tr><tr><td>Classificação</td><td>Como tipo, sensibilidade e prazo serão definidos?</td><td>Critérios documentados e amostra</td></tr><tr><td>Acessos</td><td>Como permissões e exceções serão levantadas?</td><td>Mapa de perfis e aprovações</td></tr><tr><td>Implantação</td><td>Como riscos viram ações priorizadas?</td><td>Plano, prazo, responsável e aceite</td></tr></tbody></table><p>Este checklist trata de governança e mapeamento da informação, não substitui parecer jurídico nem promete conformidade automática. Exemplos e mapas devem ser anonimizados quando contiverem dados pessoais.</p><p class="aq-review">Revisão editorial Arquindex: 23/10/2026. Fontes: <a href="https://www.gov.br/anpd/pt-br">ANPD</a> e <a href="https://www.gov.br/conarq/pt-br">CONARQ</a>.</p><p><a href="https://www.arquindex.com.br/gestao_documental_documentos.html">Gestão documental</a> · <a href="https://www.arquindex.com.br/lgpd-consultoria.html">Consultoria LGPD</a> · <a href="https://www.arquindex.com.br/solicitar-proposta-contratacao.html?utm_source=site&amp;utm_medium=checklist&amp;utm_campaign=arq089_governanca_20261023">Definir escopo de governança</a></p></section>'''},
{'id':'ARQ-090','host':'mapeamento-prontuarios-ibirite.arquindex.com.br','file':'vantagens.html','url':'https://mapeamento-prontuarios-ibirite.arquindex.com.br/vantagens.html','title':'Mapeamento de Prontuários em Ibirité: Fluxo e Acesso | Arquindex','h1':'Como mapear prontuários, fluxos e responsabilidades em Ibirité','description':'Entenda como levantar tipos de prontuário, pontos de entrada, responsáveis, acessos, movimentação, retenção e riscos antes de digitalizar ou implantar GED.','campaign':'arq090_prontuarios_ibirite_20261023','art':'mapeamento-prontuarios-ibirite-20261023.jpg','art_title':['PRONTUÁRIOS','Mapeie fluxo,','acesso e risco.'],'bullets':['Tipos e pontos de entrada','Acesso por responsabilidade','Movimentação e retenção'],'section':'''<section class="aq-aeo-answer" data-aq-aeo="ARQ-090"><h2>Como iniciar o mapeamento de prontuários e definir responsáveis?</h2><p><strong>Resposta direta:</strong> identifique tipos de prontuário e documentos associados, onde entram e são atualizados, quem registra, consulta e autoriza, como ocorre a movimentação e quais regras sustentam retenção e destinação. O mapa deve mostrar o fluxo real, inclusive exceções e registros fora do sistema principal.</p><table><thead><tr><th>Etapa</th><th>O que levantar</th><th>Resultado</th></tr></thead><tbody><tr><td>Inventário</td><td>Tipos, suportes, períodos e volumes</td><td>Escopo verificável do acervo</td></tr><tr><td>Entrada</td><td>Origem, conferência e identificação</td><td>Ponto de controle inicial</td></tr><tr><td>Acesso</td><td>Função, finalidade e autorização</td><td>Perfis e exceções documentados</td></tr><tr><td>Movimentação</td><td>Consulta, retirada, devolução e digitalização</td><td>Trilha de responsabilidade</td></tr><tr><td>Retenção</td><td>Fundamento, prazo e decisão</td><td>Regra aprovada e evidência</td></tr></tbody></table><p>A página não declara unidade física em Ibirité. Atendimento, coleta e logística dependem de confirmação comercial. Exemplos não devem expor dados de pacientes; dados de saúde exigem cuidados compatíveis com sua sensibilidade.</p><p class="aq-review">Revisão editorial Arquindex: 23/10/2026. Fontes: <a href="https://www.gov.br/anpd/pt-br">ANPD</a> e <a href="https://www.gov.br/conarq/pt-br">CONARQ</a>.</p><p><a href="https://www.arquindex.com.br/digitalizacao-prontuarios-medicos.html">Digitalização de prontuários</a> · <a href="https://www.arquindex.com.br/gestao_documental_documentos.html">Gestão documental</a> · <a href="https://www.arquindex.com.br/solicitar-proposta-contratacao.html?utm_source=site&amp;utm_medium=pagina_saude&amp;utm_campaign=arq090_prontuarios_ibirite_20261023">Avaliar o fluxo documental</a></p></section>'''},
{'id':'ARQ-094','host':'vantagens-contratar-dpo-terceirizado-empresa.arquindex.com.br','file':'index.html','url':'https://vantagens-contratar-dpo-terceirizado-empresa.arquindex.com.br/','title':'DPO Terceirizado: Contrato, Rotina e Indicadores | Arquindex','h1':'Quando contratar DPO terceirizado e o que definir no contrato','description':'Veja como definir papel, canais, demandas de titulares, incidentes, responsáveis, limites, frequência e indicadores ao contratar DPO terceirizado.','campaign':'arq094_dpo_terceirizado_20261023','art':'dpo-terceirizado-contrato-20261023.jpg','art_title':['DPO TERCEIRIZADO','Contrato claro.','Rotina verificável.'],'bullets':['Canais e responsabilidades','Titulares e incidentes','Relatórios e indicadores'],'section':'''<section class="aq-aeo-answer" data-aq-aeo="ARQ-094"><h2>Quando contratar DPO terceirizado e o que deve constar no contrato?</h2><p><strong>Resposta direta:</strong> a terceirização pode apoiar organizações que precisam de canal estruturado, conhecimento especializado e rotina contínua sem formar imediatamente uma equipe dedicada. O contrato deve definir responsabilidades, canais, tempos de resposta, tratamento de demandas, escalonamento de incidentes, reuniões, relatórios, limites e responsáveis internos.</p><table><thead><tr><th>Elemento</th><th>Definição necessária</th><th>Evidência</th></tr></thead><tbody><tr><td>Papel</td><td>Atividades do encarregado e decisões que permanecem com a organização</td><td>Escopo e matriz de responsabilidades</td></tr><tr><td>Canais</td><td>Contato de titulares e comunicação interna</td><td>Canais publicados e fluxo de triagem</td></tr><tr><td>Demandas</td><td>Recebimento, validação, prazo e resposta</td><td>Registro de solicitações e decisões</td></tr><tr><td>Incidentes</td><td>Acionamento, escalonamento e documentação</td><td>Fluxo, contatos e registro do evento</td></tr><tr><td>Acompanhamento</td><td>Reuniões, pendências e indicadores</td><td>Relatório periódico e plano de ação</td></tr></tbody></table><p>O DPO terceirizado não assume sozinho todas as obrigações da organização e não garante conformidade automática. Recursos, decisões e execução dependem dos responsáveis internos e do contexto de tratamento.</p><p class="aq-review">Revisão editorial Arquindex: 23/10/2026. Fonte primária: <a href="https://www.gov.br/anpd/pt-br/assuntos/noticias/anpd-publica-guia-orientativo-sobre-o-encarregado-pelo-tratamento-de-dados-pessoais">ANPD — encarregado pelo tratamento</a>.</p><p><a href="https://www.arquindex.com.br/dpo-as-a-service-consultoria-lgpd.html">DPO as a Service</a> · <a href="https://www.arquindex.com.br/lgpd-consultoria.html">Consultoria LGPD</a> · <a href="https://www.arquindex.com.br/solicitar-proposta-contratacao.html?utm_source=site&amp;utm_medium=pagina_comercial&amp;utm_campaign=arq094_dpo_terceirizado_20261023">Definir escopo do DPO</a></p></section>'''}]
STYLE='<style id="arquindex-aeo-20261023-tarde">.aq-aeo-answer{max-width:1120px;margin:36px auto;padding:28px;border:1px solid #d9e2ef;border-radius:16px;background:#fff;color:#0c1b33;box-sizing:border-box;overflow-wrap:anywhere}.aq-aeo-answer h2{color:#0b3d91}.aq-aeo-answer table{width:100%;border-collapse:collapse;margin:18px 0}.aq-aeo-answer th,.aq-aeo-answer td{padding:12px;border:1px solid #d9e2ef;text-align:left;vertical-align:top}.aq-aeo-answer th{background:#eaf0f8}.aq-review{font-size:.94rem;color:#42536b}@media(max-width:760px){.aq-aeo-answer{margin:24px 16px;padding:20px}.aq-aeo-answer table{display:block;overflow-x:auto}.aq-aeo-answer th,.aq-aeo-answer td{min-width:145px}}</style>'
WIDGET=Path('conteudo/publicacao/_atendimento-flutuante.html').read_text('utf-8')
def get(f,p): b=bytearray(); f.retrbinary('RETR '+p,b.extend); return bytes(b)
def mkdir(f,p):
 old=f.pwd()
 try:
  f.cwd('/')
  for x in p.strip('/').split('/'):
   if not x: continue
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
 for old in s.select('[data-aq-aeo="'+t['id']+'"],#arquindex-aeo-20261023-tarde'):old.decompose()
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
 backup='/seo-backups/rodada-20261023-tarde-'+STAMP;mkdir(f,backup);f.storbinary('STOR '+backup+'/.htaccess',io.BytesIO(b'Options -Indexes\nRequire all denied\n'))
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
  folder=base+'/assets/social-arq089-094';mkdir(f,folder)
  for t,p,o,u in rec:
   art=art_bytes(t);ap=folder+'/'+t['art'];f.storbinary('STOR '+ap,io.BytesIO(art));assert get(f,ap)==art
   photo='https://www.arquindex.com.br/assets/social-arq089-094/'+t['art'];st,b=public(photo);assert st==200 and hashlib.sha256(b).digest()==hashlib.sha256(art).digest();print('IMAGE_PUBLIC_VERIFIED',t['id'],photo,hashlib.sha256(art).hexdigest(),flush=True)
 except Exception:
  for p,o in reversed(written):put(f,p,o,'rollback-'+STAMP)
  print('ROLLBACK_COMPLETED',flush=True);raise
