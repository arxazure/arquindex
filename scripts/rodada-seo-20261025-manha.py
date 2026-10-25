import ftplib,hashlib,io,os,posixpath,time,urllib.request,xml.etree.ElementTree as ET
from datetime import datetime,timezone
from pathlib import Path
from bs4 import BeautifulSoup
from PIL import Image,ImageDraw,ImageFont
STAMP=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ');TODAY='2026-10-25'
TARGETS=[
{'id':'ARQ-119','host':'contratar-digitalizacao-documentos-armazenamento-nuvem.arquindex.com.br','file':'index.html','url':'https://contratar-digitalizacao-documentos-armazenamento-nuvem.arquindex.com.br/','title':'Digitalização com Entrega em Nuvem: Escopo e Aceite | Arquindex','h1':'Como contratar digitalização com entrega e armazenamento em nuvem','description':'Defina inventário, captura, OCR, metadados, permissões, exportação e critérios de aceite ao contratar digitalização com entrega em nuvem.','art':'digitalizacao-entrega-nuvem-arq119-20261025.jpg','art_title':['DIGITALIZAÇÃO','Entrega segura','em nuvem.'],'bullets':['Inventário e captura','Acesso e metadados','Exportação e aceite'],'section':"""<section class="aq-aeo-answer" data-aq-aeo="ARQ-119"><h2>O que validar ao contratar digitalização com entrega em nuvem?</h2><p><strong>Resposta direta:</strong> o contrato deve separar a conversão do papel, a estrutura de metadados e o ambiente de consulta. Defina volume, preparação, resolução, OCR, campos, permissões, cópias de segurança, prazo de retenção, exportação e critérios de aceite. A nuvem não corrige uma captura incompleta nem substitui a conferência do lote.</p><table><thead><tr><th>Frente</th><th>Definição necessária</th><th>Evidência de aceite</th></tr></thead><tbody><tr><td>Inventário</td><td>Caixas, documentos, páginas e exceções</td><td>Lote conciliado com a entrega</td></tr><tr><td>Captura</td><td>Resolução, cor, corte e orientação</td><td>Amostra visual aprovada</td></tr><tr><td>OCR e índices</td><td>Pesquisa e campos críticos</td><td>Consultas e validação documentadas</td></tr><tr><td>Acesso</td><td>Perfis, autenticação e registros</td><td>Usuários testam operações autorizadas</td></tr><tr><td>Retenção</td><td>Prazos, backup e restauração</td><td>Política e teste compatíveis com o escopo</td></tr><tr><td>Saída</td><td>Formato, metadados e prazo de exportação</td><td>Pacote recuperável sem dependência indevida</td></tr></tbody></table><p>O armazenamento pode ser contratado junto ou separado da digitalização. Preço, região de coleta, capacidade e plataforma dependem do diagnóstico; esta página não promete cobertura nacional irrestrita nem gratuidade permanente.</p><p class="aq-review">Revisão editorial Arquindex: 25/10/2026. Referências: <a href="https://www.gov.br/conarq/pt-br">CONARQ</a> e <a href="https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2020/decreto/d10278.htm">Decreto 10.278/2020</a>.</p><p><a href="https://www.arquindex.com.br/digitalizacao.html">Digitalização de documentos</a> · <a href="https://www.arquindex.com.br/digitalizacao-com-ocr.html">OCR</a> · <a href="https://www.arquindex.com.br/solicitar-proposta-contratacao.html?utm_source=site&amp;utm_medium=guia_nuvem&amp;utm_campaign=arq119_nuvem_20261025">Definir o escopo</a></p></section>"""},
{'id':'ARQ-120','host':'compliance-digitalizacao-preco.arquindex.com.br','file':'index.html','url':'https://compliance-digitalizacao-preco.arquindex.com.br/','title':'Custo da Governança da Informação: Escopo e Etapas | Arquindex','h1':'Quais fatores entram no orçamento de governança da informação','description':'Veja como processos, repositórios, entrevistas, classificação, acessos, riscos e entregáveis influenciam o orçamento de governança da informação.','art':'custo-governanca-informacao-arq120-20261025.jpg','art_title':['GOVERNANÇA','Orçamento por','escopo real.'],'bullets':['Processos e repositórios','Entrevistas e riscos','Entregáveis e implantação'],'section':"""<section class="aq-aeo-answer" data-aq-aeo="ARQ-120"><h2>Quais fatores entram no orçamento de governança e mapeamento da informação?</h2><p><strong>Resposta direta:</strong> o custo depende do número de processos, unidades, repositórios, entrevistas, integrações, classes documentais, perfis de acesso e entregáveis. Uma proposta comparável separa diagnóstico, desenho das regras, implantação e acompanhamento; volume de arquivos sozinho não representa o esforço de governança.</p><table><thead><tr><th>Componente</th><th>O que dimensionar</th><th>Entregável</th></tr></thead><tbody><tr><td>Processos</td><td>Áreas, responsáveis e interfaces</td><td>Mapa de fluxo e decisões</td></tr><tr><td>Repositórios</td><td>Sistemas, pastas, nuvem e acervo físico</td><td>Inventário com responsáveis</td></tr><tr><td>Classificação</td><td>Tipos, metadados, acesso e retenção</td><td>Regras documentadas</td></tr><tr><td>Riscos</td><td>Exposição, indisponibilidade e duplicidade</td><td>Matriz priorizada</td></tr><tr><td>Implantação</td><td>Tecnologia, migração e treinamento</td><td>Plano com dependências e aceite</td></tr><tr><td>Acompanhamento</td><td>Revisões, indicadores e exceções</td><td>Rotina de governança</td></tr></tbody></table><p>Peça premissas, exclusões e responsabilidades. O diagnóstico pode apontar necessidades de gestão documental ou LGPD, mas não garante conformidade automática e não deve expor dados pessoais nos exemplos.</p><p class="aq-review">Revisão editorial Arquindex: 25/10/2026. Referências: <a href="https://www.gov.br/conarq/pt-br">CONARQ</a> e <a href="https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm">Lei 13.709/2018</a>.</p><p><a href="https://www.arquindex.com.br/gestao_documental_documentos.html">Gestão documental</a> · <a href="https://www.arquindex.com.br/lgpd-consultoria.html">Consultoria LGPD</a> · <a href="https://www.arquindex.com.br/solicitar-proposta-contratacao.html?utm_source=site&amp;utm_medium=guia_governanca&amp;utm_campaign=arq120_orcamento_20261025">Solicitar diagnóstico</a></p></section>"""},
{'id':'ARQ-123','host':'mapeamento-juridico.arquindex.com.br','file':'index.html','url':'https://mapeamento-juridico.arquindex.com.br/','title':'Mapeamento Jurídico: Contratos, Processos e Acessos | Arquindex','h1':'Como mapear documentos jurídicos, responsáveis e acessos','description':'Organize contratos, processos, pareceres e evidências com responsáveis, classificação, acesso, prazos, rastreabilidade e plano de implantação.','art':'mapeamento-documental-juridico-arq123-20261025.jpg','art_title':['JURÍDICO','Mapeie documentos','e acessos.'],'bullets':['Contratos e processos','Responsáveis e sigilo','Prazos e rastreabilidade'],'section':"""<section class="aq-aeo-answer" data-aq-aeo="ARQ-123"><h2>Como iniciar o mapeamento de documentos jurídicos?</h2><p><strong>Resposta direta:</strong> liste os tipos documentais e os eventos que os criam, atualizam, consultam e encerram. Para contratos, processos, pareceres e evidências, registre responsável, contraparte, assunto, prazo, local, nível de acesso e vínculo com o processo de negócio. Depois trate duplicidades, lacunas e riscos por prioridade.</p><table><thead><tr><th>Grupo</th><th>Campos úteis</th><th>Controle esperado</th></tr></thead><tbody><tr><td>Contratos</td><td>Partes, objeto, vigência e obrigações</td><td>Alertas e versão vigente identificada</td></tr><tr><td>Processos</td><td>Número, foro, partes, fase e prazo</td><td>Responsável e evidência vinculados</td></tr><tr><td>Pareceres</td><td>Tema, solicitante, versão e aprovação</td><td>Histórico e acesso restrito</td></tr><tr><td>Procurações</td><td>Outorgante, poderes e validade</td><td>Prazo e revogação controlados</td></tr><tr><td>Evidências</td><td>Origem, data, integridade e contexto</td><td>Rastreabilidade da guarda e consulta</td></tr><tr><td>Destinação</td><td>Prazo, fundamento e aprovação</td><td>Decisão registrada</td></tr></tbody></table><p>O mapeamento documental apoia a operação, mas não substitui análise jurídica. Exemplos devem ser anonimizados; confidencialidade, privilégio, retenção e acesso são definidos pela organização com seus responsáveis jurídicos.</p><p class="aq-review">Revisão editorial Arquindex: 25/10/2026. Referências: <a href="https://www.gov.br/conarq/pt-br">CONARQ</a> e <a href="https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm">Lei 13.709/2018</a>.</p><p><a href="https://www.arquindex.com.br/gestao_documental_documentos.html">Gestão documental</a> · <a href="https://www.arquindex.com.br/lgpd-consultoria.html">LGPD</a> · <a href="https://www.arquindex.com.br/solicitar-proposta-contratacao.html?utm_source=site&amp;utm_medium=guia_juridico&amp;utm_campaign=arq123_mapeamento_20261025">Mapear o acervo jurídico</a></p></section>"""}
]
STYLE='<style id="arquindex-aeo-20261025-manha">.aq-aeo-answer{max-width:1120px;margin:36px auto;padding:28px;border:1px solid #d9e2ef;border-radius:16px;background:#fff;color:#0c1b33;box-sizing:border-box;overflow-wrap:anywhere}.aq-aeo-answer h2{color:#0b3d91}.aq-aeo-answer table{width:100%;border-collapse:collapse;margin:18px 0}.aq-aeo-answer th,.aq-aeo-answer td{padding:12px;border:1px solid #d9e2ef;text-align:left;vertical-align:top}.aq-aeo-answer th{background:#eaf0f8}.aq-review{font-size:.94rem;color:#42536b}@media(max-width:760px){html,body{max-width:100%;overflow-x:clip}body a{overflow-wrap:anywhere;word-break:break-word}.aq-aeo-answer{margin:24px 16px;padding:20px;overflow:hidden}.aq-aeo-answer table{display:block;max-width:100%;overflow-x:auto}.aq-aeo-answer th,.aq-aeo-answer td{min-width:135px}#arq-floating{right:12px!important;max-width:calc(100vw - 24px)!important}}</style>'
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
 for old in s.select('[data-aq-aeo="'+t['id']+'"],#arquindex-aeo-20261025-manha'):old.decompose()
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
 backup='/seo-backups/rodada-20261025-manha-'+STAMP;mkdir(f,backup);f.storbinary('STOR '+backup+'/.htaccess',io.BytesIO(b'Options -Indexes\nRequire all denied\n'))
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
  folder=base+'/assets/social-arq119-124';mkdir(f,folder)
  for t,p,o,u in rec:
   art=art_bytes(t);ap=folder+'/'+t['art'];f.storbinary('STOR '+ap,io.BytesIO(art));assert get(f,ap)==art
   photo='https://www.arquindex.com.br/assets/social-arq119-124/'+t['art'];st,b=public(photo);assert st==200 and hashlib.sha256(b).digest()==hashlib.sha256(art).digest();print('IMAGE_PUBLIC_VERIFIED',t['id'],photo,hashlib.sha256(art).hexdigest(),flush=True)
 except Exception:
  for p,o in reversed(written):put(f,p,o,'rollback-'+STAMP)
  print('ROLLBACK_COMPLETED',flush=True);raise
