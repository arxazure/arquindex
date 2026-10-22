import ftplib,hashlib,io,os,posixpath,time,urllib.request,xml.etree.ElementTree as ET
from datetime import datetime,timezone
from pathlib import Path
from bs4 import BeautifulSoup
from PIL import Image,ImageDraw,ImageFont
STAMP=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
TODAY='2026-10-22'
TARGETS=[
{'id':'ARQ-078','host':'organizacao-de-arquivos-empresariais.arquindex.com.br','file':'index.html','url':'https://organizacao-de-arquivos-empresariais.arquindex.com.br/','title':'Organização de Arquivos: Controle e Consulta | Arquindex','h1':'Como organizar e movimentar arquivos empresariais','description':'Veja como inventariar caixas, registrar solicitações, controlar retiradas e devoluções e aplicar temporalidade com evidências documentadas.','campaign':'arq078_organizacao_20261022','art':'organizacao-arquivos-20261022.jpg','art_title':['ARQUIVOS EMPRESARIAIS','Localização rápida.','Movimentação registrada.'],'bullets':['Inventário e identificação','Solicitação e retirada','Devolução e evidência'],'section':'''<section class="aq-aeo-answer" data-aq-aeo="ARQ-078"><h2>Como localizar, solicitar e devolver documentos guardados?</h2><p><strong>Resposta direta:</strong> cada caixa ou pasta precisa de identificador único, localização registrada e vínculo com a série documental. Toda movimentação deve informar solicitante, finalidade, data de retirada, responsável pela entrega, previsão e confirmação de devolução.</p><table><thead><tr><th>Etapa</th><th>Registro mínimo</th><th>Evidência</th></tr></thead><tbody><tr><td>Inventário</td><td>Identificador, série, período e localização</td><td>Relação conferida das unidades</td></tr><tr><td>Solicitação</td><td>Solicitante, finalidade e item pedido</td><td>Protocolo de atendimento</td></tr><tr><td>Retirada</td><td>Data, responsável e condição do item</td><td>Comprovante de movimentação</td></tr><tr><td>Devolução</td><td>Data, conferência e nova localização</td><td>Baixa do protocolo</td></tr><tr><td>Destinação</td><td>Prazo, fundamento e autorização</td><td>Registro da decisão e certificado quando aplicável</td></tr></tbody></table><p>Temporalidade e destinação devem seguir critérios aprovados para o acervo. Digitalização, por si só, não autoriza eliminar o original.</p><p class="aq-review">Revisão editorial Arquindex: 22/10/2026. Referência institucional: <a href="https://www.gov.br/conarq/pt-br">CONARQ</a>.</p><p><a href="https://www.arquindex.com.br/guarda_de_documentos.html">Guarda de documentos</a> · <a href="https://www.arquindex.com.br/gestao_documental_documentos.html">Gestão documental</a> · <a href="https://www.arquindex.com.br/solicitar-proposta-contratacao.html?utm_source=site&amp;utm_medium=pagina_servico&amp;utm_campaign=arq078_organizacao_20261022">Solicitar diagnóstico do acervo</a></p></section>'''},
{'id':'ARQ-081','host':'acervos-medico-baixada-fluminense.arquindex.com.br','file':'o-que-e.html','url':'https://acervos-medico-baixada-fluminense.arquindex.com.br/o-que-e.html','title':'Acervos Médicos: Organização, Guarda e Acesso | Arquindex','h1':'Como organizar e controlar grandes acervos médicos','description':'Organize prontuários e documentos de saúde com inventário, acesso por perfil, movimentação registrada, temporalidade e descarte autorizado.','campaign':'arq081_acervos_medicos_20261022','art':'acervos-medicos-20261022.jpg','art_title':['ACERVOS MÉDICOS','Acesso controlado.','Rastreabilidade real.'],'bullets':['Inventário do acervo','Acesso por perfil','Movimentação e devolução'],'section':'''<section class="aq-aeo-answer" data-aq-aeo="ARQ-081"><h2>Como organizar um grande acervo médico sem perder rastreabilidade?</h2><p><strong>Resposta direta:</strong> comece pelo inventário das séries e dos suportes, defina identificadores e localizações, restrinja o acesso conforme função e registre toda consulta, retirada, digitalização, devolução e destinação.</p><table><thead><tr><th>Controle</th><th>Pergunta de aceite</th><th>Evidência esperada</th></tr></thead><tbody><tr><td>Inventário</td><td>Quais séries, períodos e suportes existem?</td><td>Relação conferida e localização</td></tr><tr><td>Acesso</td><td>Quem pode consultar cada conjunto?</td><td>Perfis e autorizações registrados</td></tr><tr><td>Movimentação</td><td>Quem retirou, por qual motivo e quando devolveu?</td><td>Protocolo com histórico</td></tr><tr><td>Digitalização</td><td>Quais campos, formato e conferência foram definidos?</td><td>Amostra e relatório de qualidade</td></tr><tr><td>Destinação</td><td>Qual regra e autorização sustentam a decisão?</td><td>Registro e certificado quando aplicável</td></tr></tbody></table><p>A página não declara unidade física na Baixada Fluminense. Logística, coleta e formato do atendimento precisam ser confirmados na proposta. Exemplos públicos não devem expor dados de pacientes.</p><p class="aq-review">Revisão editorial Arquindex: 22/10/2026. Fontes primárias: <a href="https://www.gov.br/anpd/pt-br">ANPD</a> e <a href="https://www.gov.br/conarq/pt-br">CONARQ</a>.</p><p><a href="https://www.arquindex.com.br/digitalizacao-prontuarios-medicos.html">Digitalização de prontuários</a> · <a href="https://www.arquindex.com.br/guarda_de_documentos.html">Guarda documental</a> · <a href="https://www.arquindex.com.br/solicitar-proposta-contratacao.html?utm_source=site&amp;utm_medium=pagina_vertical&amp;utm_campaign=arq081_acervos_medicos_20261022">Avaliar o acervo</a></p></section>'''},
{'id':'ARQ-082','host':'adequacao-exin-sp.arquindex.com.br','file':'o-que-e.html','url':'https://adequacao-exin-sp.arquindex.com.br/o-que-e.html','title':'Consultoria LGPD: Credenciais, Escopo e Evidências | Arquindex','h1':'Como avaliar credenciais e escopo de uma consultoria LGPD','description':'Compare experiência, credenciais, diagnóstico, entregáveis, responsabilidades e evidências antes de contratar uma consultoria de adequação à LGPD.','campaign':'arq082_escopo_lgpd_20261022','art':'escopo-lgpd-20261022.jpg','art_title':['CONSULTORIA LGPD','Credencial ajuda.','Escopo comprova.'],'bullets':['Diagnóstico verificável','Entregáveis definidos','Responsáveis e revisão'],'section':'''<section class="aq-aeo-answer" data-aq-aeo="ARQ-082"><h2>O que verificar antes de contratar uma consultoria LGPD?</h2><p><strong>Resposta direta:</strong> credenciais ajudam a avaliar conhecimento, mas a contratação deve definir diagnóstico, unidades e processos abrangidos, entregáveis, responsáveis, critérios de revisão, tratamento de pendências e transferência de conhecimento.</p><table><thead><tr><th>Critério</th><th>O que perguntar</th><th>Evidência</th></tr></thead><tbody><tr><td>Experiência e credenciais</td><td>Quem executará e quais formações são pertinentes?</td><td>Responsáveis e qualificações verificáveis</td></tr><tr><td>Diagnóstico</td><td>Quais processos, sistemas e fornecedores serão examinados?</td><td>Escopo, achados e prioridades</td></tr><tr><td>Entregáveis</td><td>Quais registros, políticas e planos serão produzidos?</td><td>Lista, formato e critério de aceite</td></tr><tr><td>Responsabilidades</td><td>Quem valida informações e aprova decisões?</td><td>Matriz de papéis e prazos</td></tr><tr><td>Continuidade</td><td>Como ficam revisão, treinamento e pendências?</td><td>Plano de acompanhamento</td></tr></tbody></table><p>Certificação profissional não equivale a certificação da organização nem garante conformidade automática. A aplicação jurídica depende do contexto e das decisões documentadas pela empresa.</p><p class="aq-review">Revisão editorial Arquindex: 22/10/2026. Fonte primária: <a href="https://www.gov.br/anpd/pt-br">Autoridade Nacional de Proteção de Dados</a>.</p><p><a href="https://www.arquindex.com.br/lgpd-consultoria.html">Consultoria LGPD</a> · <a href="https://www.arquindex.com.br/dpo-terceirizado.html">DPO terceirizado</a> · <a href="https://www.arquindex.com.br/solicitar-proposta-contratacao.html?utm_source=site&amp;utm_medium=pagina_comercial&amp;utm_campaign=arq082_escopo_lgpd_20261022">Definir o escopo</a></p></section>'''}]
STYLE='<style id="arquindex-aeo-20261022-noite">.aq-aeo-answer{max-width:1120px;margin:36px auto;padding:28px;border:1px solid #d9e2ef;border-radius:16px;background:#fff;color:#0c1b33;box-sizing:border-box;overflow-wrap:anywhere}.aq-aeo-answer h2{color:#0b3d91}.aq-aeo-answer table{width:100%;border-collapse:collapse;margin:18px 0}.aq-aeo-answer th,.aq-aeo-answer td{padding:12px;border:1px solid #d9e2ef;text-align:left;vertical-align:top}.aq-aeo-answer th{background:#eaf0f8}.aq-review{font-size:.94rem;color:#42536b}@media(max-width:760px){.aq-aeo-answer{margin:24px 16px;padding:20px}.aq-aeo-answer table{display:block;overflow-x:auto}.aq-aeo-answer th,.aq-aeo-answer td{min-width:145px}}</style>'
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
 d,n=posixpath.dirname(p),posixpath.basename(p);tmp=d+'/.tmp-'+n+'-'+label;f.storbinary('STOR '+tmp,io.BytesIO(b));assert get(f,tmp)==b
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
 s=BeautifulSoup(b.decode('utf-8'),'html.parser');assert s.head and s.body
 for old in s.select('[data-aq-aeo="'+t['id']+'"]'):old.decompose()
 if s.title:s.title.string=t['title']
 else:n=s.new_tag('title');n.string=t['title'];s.head.append(n)
 desc=s.find('meta',attrs={'name':lambda v:v and v.lower()=='description'})
 if not desc:desc=s.new_tag('meta',attrs={'name':'description'});s.head.append(desc)
 desc['content']=t['description']
 h1s=s.find_all('h1');assert h1s;h1s[0].string=t['h1']
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
 a=BeautifulSoup(t['section'],'html.parser');footer=s.find('footer');footer.insert_before(a) if footer else s.body.append(a)
 out=str(s).encode();assert out.count(b'id="arq-floating"')==1 and t['id'].encode() in out;return out
def public(url):
 req=urllib.request.Request(url+('&' if '?' in url else '?')+'verify='+STAMP,headers={'User-Agent':'ArquindexSEO/1.0','Cache-Control':'no-cache'})
 with urllib.request.urlopen(req,timeout=40) as r:return r.status,r.read(9000000)
def art_bytes(t):
 im=Image.new('RGB',(1200,1200),'#f4f7fc');d=ImageDraw.Draw(im)
 def tx(x,y,s,z=32,c='#0c1b33',bold=False):
  font='/usr/share/fonts/truetype/dejavu/DejaVuSans'+('-Bold' if bold else '')+'.ttf';d.text((x,y),s,font=ImageFont.truetype(font,z),fill=c)
 tx(70,70,'ARQUINDEX',48,'#0b3d91',True);tx(70,210,t['art_title'][0],30,'#0b3d91',True);tx(70,290,t['art_title'][1],52,'#0c1b33',True);tx(70,365,t['art_title'][2],52,'#0c1b33',True)
 for i,label in enumerate(t['bullets']):
  y=530+i*135;d.rounded_rectangle((70,y,1130,y+106),radius=18,fill='white',outline='#cbd7e9',width=2);tx(100,y+27,label,34)
 d.rectangle((0,1050,1200,1200),fill='#0b3d91');tx(70,1080,'Veja o guia completo',35,'white',True);tx(70,1133,t['host'],26,'white')
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
 backup='/seo-backups/rodada-20261022-noite-'+STAMP;mkdir(f,backup);f.storbinary('STOR '+backup+'/.htaccess',io.BytesIO(b'Options -Indexes\nRequire all denied\n'))
 for t,p,o,u in rec:
  bp=backup+'/'+t['id'].lower()+'.html';f.storbinary('STOR '+bp,io.BytesIO(o));assert get(f,bp)==o;print('BACKUP_VERIFIED',t['id'],bp,hashlib.sha256(o).hexdigest(),flush=True)
 written=[]
 try:
  for t,p,o,u in rec:assert get(f,p)==o,'CONCURRENT_CHANGE '+t['id']
  for t,p,o,u in rec:put(f,p,u,STAMP);written.append((p,o));print('FTP_PUBLISHED_VERIFIED',t['id'],hashlib.sha256(u).hexdigest(),flush=True)
  time.sleep(2)
  for t,p,o,u in rec:
   st,body=public(t['url']);assert st==200 and t['id'].encode() in body and t['title'].encode() in body and t['url'].encode() in body and b'noindex' not in body.lower();print('PUBLIC_SOURCE_VERIFIED',t['id'],t['url'],hashlib.sha256(body).hexdigest(),flush=True)
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
  folder=base+'/assets/social-arq077-082';mkdir(f,folder)
  for t,p,o,u in rec:
   art=art_bytes(t);ap=folder+'/'+t['art'];f.storbinary('STOR '+ap,io.BytesIO(art));assert get(f,ap)==art
   photo='https://www.arquindex.com.br/assets/social-arq077-082/'+t['art'];st,b=public(photo);assert st==200 and hashlib.sha256(b).digest()==hashlib.sha256(art).digest();print('IMAGE_PUBLIC_VERIFIED',t['id'],photo,hashlib.sha256(art).hexdigest(),flush=True)
 except Exception:
  for p,o in reversed(written):put(f,p,o,'rollback-'+STAMP)
  print('ROLLBACK_COMPLETED',flush=True);raise
