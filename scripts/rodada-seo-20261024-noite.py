import ftplib,hashlib,io,os,posixpath,time,urllib.request,xml.etree.ElementTree as ET
from datetime import datetime,timezone
from pathlib import Path
from bs4 import BeautifulSoup
from PIL import Image,ImageDraw,ImageFont
STAMP=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ');TODAY='2026-10-24'
TARGETS=[
{'id':'ARQ-113','host':'mapeamento-ocr-rj.arquindex.com.br','file':'index.html','url':'https://mapeamento-ocr-rj.arquindex.com.br/','title':'OCR e Indexação: Teste, Revisão e Aceite | Arquindex','h1':'Como testar OCR, indexação e pesquisa antes do aceite','description':'Veja como testar OCR e indexação, revisar campos críticos, tratar exceções e validar uma entrega pesquisável sem prometer precisão universal.','art':'ocr-indexacao-teste-aceite-arq113-20261024.jpg','art_title':['OCR E INDEXAÇÃO','Teste antes','do aceite.'],'bullets':['Amostra representativa','Campos e pesquisa','Exceções registradas'],'section':"""<section class="aq-aeo-answer" data-aq-aeo="ARQ-113"><h2>Quando OCR torna o documento pesquisável e quando precisa de revisão?</h2><p><strong>Resposta direta:</strong> o OCR adiciona uma camada de texto para pesquisa, mas a qualidade depende do original, resolução, contraste, idioma, tabelas, carimbos e manuscritos. O aceite deve testar uma amostra representativa, os campos críticos e as exceções; abrir o PDF não comprova que a informação foi reconhecida corretamente.</p><table><thead><tr><th>Etapa</th><th>Teste</th><th>Evidência</th></tr></thead><tbody><tr><td>Amostra</td><td>Tipos, períodos e condições reais</td><td>Lote representativo documentado</td></tr><tr><td>Captura</td><td>Corte, orientação e legibilidade</td><td>Conferência visual por amostragem</td></tr><tr><td>Pesquisa</td><td>Termos presentes e ausentes</td><td>Arquivos esperados recuperados</td></tr><tr><td>Campos</td><td>Datas, nomes e identificadores</td><td>Validação adicional dos dados críticos</td></tr><tr><td>Exceções</td><td>Baixo contraste, tabelas e manuscritos</td><td>Fila de revisão e decisão registrada</td></tr><tr><td>Entrega</td><td>PDF pesquisável, índices e inventário</td><td>Conciliação entre lote e arquivos</td></tr></tbody></table><p>Não existe taxa universal de precisão. Em projetos no Rio de Janeiro, coleta, visita e logística dependem de confirmação na proposta; esta página não afirma unidade física local.</p><p class="aq-review">Revisão editorial Arquindex: 24/10/2026. Referências: <a href="https://www.gov.br/conarq/pt-br">CONARQ</a> e <a href="https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2020/decreto/d10278.htm">Decreto 10.278/2020</a>.</p><p><a href="https://www.arquindex.com.br/digitalizacao-com-ocr.html">Digitalização com OCR</a> · <a href="https://www.arquindex.com.br/digitalizacao.html">Digitalização de documentos</a> · <a href="https://www.arquindex.com.br/solicitar-proposta-contratacao.html?utm_source=site&amp;utm_medium=guia_ocr&amp;utm_campaign=arq113_ocr_aceite_20261024">Solicitar avaliação de amostra</a></p></section>"""},
{'id':'ARQ-114','host':'compliance-arquivos-corporativo.arquindex.com.br','file':'index.html','url':'https://compliance-arquivos-corporativo.arquindex.com.br/','title':'Governança da Informação: Mapeamento e Responsáveis | Arquindex','h1':'Como mapear informações, repositórios e responsáveis','description':'Inicie a governança da informação com inventário de repositórios, responsáveis, acessos, ciclo de vida, riscos e plano de implantação verificável.','art':'governanca-informacao-mapeamento-arq114-20261024.jpg','art_title':['GOVERNANÇA','Mapeie dados','e responsáveis.'],'bullets':['Repositórios e donos','Acesso e ciclo de vida','Riscos e prioridades'],'section':"""<section class="aq-aeo-answer" data-aq-aeo="ARQ-114"><h2>Como iniciar o mapeamento de informações e definir responsáveis?</h2><p><strong>Resposta direta:</strong> comece pelos processos e repositórios que sustentam a operação. Para cada conjunto documental, registre finalidade, conteúdo, formato, responsável, acesso, localização, prazo e risco. Depois priorize lacunas e defina quem aprova, executa, revisa e comprova cada ação.</p><table><thead><tr><th>Frente</th><th>Pergunta</th><th>Registro esperado</th></tr></thead><tbody><tr><td>Repositórios</td><td>Onde a informação está?</td><td>Sistema, pasta, arquivo físico ou terceiro</td></tr><tr><td>Responsáveis</td><td>Quem decide e mantém?</td><td>Dono do processo e custodiante</td></tr><tr><td>Acesso</td><td>Quem consulta, altera ou exporta?</td><td>Perfis, aprovações e exceções</td></tr><tr><td>Ciclo de vida</td><td>Quando criar, revisar, reter e destinar?</td><td>Critérios e evidências de decisão</td></tr><tr><td>Risco</td><td>O que pode falhar ou ser exposto?</td><td>Impacto, controle e prioridade</td></tr><tr><td>Plano</td><td>Qual ação vem primeiro?</td><td>Responsável, prazo, dependência e aceite</td></tr></tbody></table><p>O mapa deve usar exemplos anonimizados e não expor dados pessoais. O escopo pode integrar gestão documental e LGPD, mas cada frente precisa de finalidade e evidência próprias.</p><p class="aq-review">Revisão editorial Arquindex: 24/10/2026. Referências: <a href="https://www.gov.br/conarq/pt-br">CONARQ</a> e <a href="https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm">Lei 13.709/2018</a>.</p><p><a href="https://www.arquindex.com.br/gestao_documental_documentos.html">Gestão documental</a> · <a href="https://www.arquindex.com.br/lgpd-consultoria.html">Consultoria LGPD</a> · <a href="https://www.arquindex.com.br/solicitar-proposta-contratacao.html?utm_source=site&amp;utm_medium=guia_governanca&amp;utm_campaign=arq114_mapeamento_20261024">Planejar o mapeamento</a></p></section>"""},
{'id':'ARQ-118','host':'arquivamento.arquindex.com.br','file':'custo.html','url':'https://arquivamento.arquindex.com.br/custo.html','title':'Custo da Guarda Documental: Fatores do Orçamento | Arquindex','h1':'Quais fatores entram no orçamento de guarda e organização de documentos','description':'Entenda como inventário, volume, acondicionamento, logística, consultas, temporalidade e nível de serviço influenciam o orçamento de guarda documental.','art':'custo-guarda-documental-arq118-20261024.jpg','art_title':['GUARDA DOCUMENTAL','Entenda o','orçamento.'],'bullets':['Volume e inventário','Logística e consultas','Prazo e nível de serviço'],'section':"""<section class="aq-aeo-answer" data-aq-aeo="ARQ-118"><h2>Quais fatores entram no orçamento de guarda e organização de documentos?</h2><p><strong>Resposta direta:</strong> o custo depende do inventário inicial, volume e condição do acervo, acondicionamento, coleta, frequência de consultas, prazo de atendimento, controles de acesso, temporalidade e destinação. Um orçamento comparável deve separar implantação, recorrência e serviços sob demanda; não existe preço universal por caixa.</p><table><thead><tr><th>Componente</th><th>O que medir</th><th>Impacto no escopo</th></tr></thead><tbody><tr><td>Inventário</td><td>Caixas, séries, períodos e estado</td><td>Esforço de implantação e conciliação</td></tr><tr><td>Acondicionamento</td><td>Padronização, etiquetas e substituições</td><td>Materiais e preparação</td></tr><tr><td>Logística</td><td>Coleta, acesso e condições do local</td><td>Rota, equipe e cronograma</td></tr><tr><td>Consulta</td><td>Frequência, urgência e formato</td><td>Nível de serviço e movimentação</td></tr><tr><td>Segurança</td><td>Perfis, protocolo e rastreabilidade</td><td>Controles e evidências</td></tr><tr><td>Temporalidade</td><td>Revisões, retenção e destinação</td><td>Rotina técnica e aprovações</td></tr></tbody></table><p>Peça premissas, quantidades, exclusões e critérios de reajuste. Digitalizar documentos não autoriza eliminação automática, e nenhum endereço operacional restrito é divulgado nesta página.</p><p class="aq-review">Revisão editorial Arquindex: 24/10/2026. Referência: <a href="https://www.gov.br/conarq/pt-br">CONARQ</a>.</p><p><a href="https://www.arquindex.com.br/guarda_de_documentos.html">Guarda de documentos</a> · <a href="https://www.arquindex.com.br/gestao_documental_documentos.html">Gestão documental</a> · <a href="https://www.arquindex.com.br/solicitar-proposta-contratacao.html?utm_source=site&amp;utm_medium=guia_guarda&amp;utm_campaign=arq118_orcamento_20261024">Solicitar diagnóstico do acervo</a></p></section>"""}
]
STYLE='<style id="arquindex-aeo-20261024-noite">.aq-aeo-answer{max-width:1120px;margin:36px auto;padding:28px;border:1px solid #d9e2ef;border-radius:16px;background:#fff;color:#0c1b33;box-sizing:border-box;overflow-wrap:anywhere}.aq-aeo-answer h2{color:#0b3d91}.aq-aeo-answer table{width:100%;border-collapse:collapse;margin:18px 0}.aq-aeo-answer th,.aq-aeo-answer td{padding:12px;border:1px solid #d9e2ef;text-align:left;vertical-align:top}.aq-aeo-answer th{background:#eaf0f8}.aq-review{font-size:.94rem;color:#42536b}@media(max-width:760px){html,body{max-width:100%;overflow-x:clip}body a{overflow-wrap:anywhere;word-break:break-word}.aq-aeo-answer{margin:24px 16px;padding:20px;overflow:hidden}.aq-aeo-answer table{display:block;max-width:100%;overflow-x:auto}.aq-aeo-answer th,.aq-aeo-answer td{min-width:135px}#arq-floating{right:12px!important;max-width:calc(100vw - 24px)!important}}</style>'
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
 for old in s.select('[data-aq-aeo="'+t['id']+'"],#arquindex-aeo-20261024-noite'):old.decompose()
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
 backup='/seo-backups/rodada-20261024-noite-'+STAMP;mkdir(f,backup);f.storbinary('STOR '+backup+'/.htaccess',io.BytesIO(b'Options -Indexes\nRequire all denied\n'))
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
  folder=base+'/assets/social-arq113-118';mkdir(f,folder)
  for t,p,o,u in rec:
   art=art_bytes(t);ap=folder+'/'+t['art'];f.storbinary('STOR '+ap,io.BytesIO(art));assert get(f,ap)==art
   photo='https://www.arquindex.com.br/assets/social-arq113-118/'+t['art'];st,b=public(photo);assert st==200 and hashlib.sha256(b).digest()==hashlib.sha256(art).digest();print('IMAGE_PUBLIC_VERIFIED',t['id'],photo,hashlib.sha256(art).hexdigest(),flush=True)
 except Exception:
  for p,o in reversed(written):put(f,p,o,'rollback-'+STAMP)
  print('ROLLBACK_COMPLETED',flush=True);raise
