import ftplib,hashlib,io,os,posixpath,time,urllib.request
from datetime import datetime,timezone
from pathlib import Path
from bs4 import BeautifulSoup
STAMP=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
TARGETS=[
{'id':'ARQ-046','file':'seo-regional/gestao-documental-ecm-databooks/nova-lima/index.html','url':'https://www.arquindex.com.br/seo-regional/gestao-documental-ecm-databooks/nova-lima/','section':'''<section class="aq-aeo-answer" data-aq-aeo="ARQ-046"><h2>Como conferir um databook antes da entrega?</h2><p><strong>Resposta direta:</strong> comece pelo índice contratual, relacione cada documento ao pacote, equipamento ou etapa correspondente e confira identificação, revisão, aprovação, legibilidade e pendências. O aceite deve testar recuperação e rastreabilidade, não apenas contar arquivos.</p><table><thead><tr><th>Controle</th><th>Critério verificável</th></tr></thead><tbody><tr><td>Índice mestre</td><td>Cada requisito aponta para um documento entregue ou uma pendência justificada</td></tr><tr><td>Revisões</td><td>A revisão vigente está identificada e o histórico necessário foi preservado</td></tr><tr><td>Metadados</td><td>Contrato, disciplina, equipamento e tipo documental recuperam o conjunto correto</td></tr><tr><td>Aceite</td><td>Amostras são abertas, pesquisadas e comparadas com o índice antes da entrega final</td></tr></tbody></table><p>Em projetos de engenharia e mineração na região de Nova Lima, o escopo e a logística precisam ser confirmados antes da proposta; esta página não pressupõe unidade física local.</p><p><a href="https://www.gov.br/conarq/pt-br">Conselho Nacional de Arquivos</a> · <a href="https://www.arquindex.com.br/gestao_documental_documentos.html">Gestão documental</a> · <a href="https://www.arquindex.com.br/alfresco-incloud-gestao-arquivos.html">GED e ECM com Alfresco</a> · <a href="https://www.arquindex.com.br/solicitar-proposta-contratacao.html?utm_source=site&amp;utm_medium=pagina_local&amp;utm_campaign=arq046_databook_nova_lima_20261021">Definir o escopo do databook</a></p></section>'''},
{'id':'ARQ-048','file':'seo-regional/gestao-documental-ecm-databooks/betim/index.html','url':'https://www.arquindex.com.br/seo-regional/gestao-documental-ecm-databooks/betim/','section':'''<section class="aq-aeo-answer" data-aq-aeo="ARQ-048"><h2>Como organizar certificados, inspeções e desenhos em um databook?</h2><p><strong>Resposta direta:</strong> associe cada documento a lote, equipamento, fornecedor e revisão; separe vigentes, substituídos e pendentes; e valide a recuperação do conjunto completo por item de produção antes do aceite.</p><table><thead><tr><th>Documento</th><th>Vínculo mínimo</th><th>Teste</th></tr></thead><tbody><tr><td>Certificado</td><td>Lote, material, fornecedor e validade</td><td>Recuperar o certificado correto pelo lote</td></tr><tr><td>Inspeção</td><td>Equipamento, etapa, data e responsável</td><td>Identificar resultado e pendências</td></tr><tr><td>Desenho</td><td>Disciplina, código e revisão</td><td>Distinguir revisão vigente e substituída</td></tr><tr><td>Entrega</td><td>Índice, exceções e aprovação</td><td>Comparar amostra com requisitos do contrato</td></tr></tbody></table><p>Para operações industriais em Betim, atendimento, coleta e confidencialidade devem ser confirmados no escopo; a organização digital não substitui critérios técnicos de engenharia.</p><p><a href="https://www.gov.br/conarq/pt-br">Conselho Nacional de Arquivos</a> · <a href="https://www.arquindex.com.br/gestao_documental_documentos.html">Gestão documental</a> · <a href="https://www.arquindex.com.br/alfresco-incloud-gestao-arquivos.html">GED e ECM com Alfresco</a> · <a href="https://www.arquindex.com.br/solicitar-proposta-contratacao.html?utm_source=site&amp;utm_medium=pagina_local&amp;utm_campaign=arq048_databook_betim_20261021">Solicitar avaliação do lote</a></p></section>'''},
{'id':'ARQ-049','file':'seo-regional/gestao-documental-ecm-databooks/contagem/index.html','url':'https://www.arquindex.com.br/seo-regional/gestao-documental-ecm-databooks/contagem/','section':'''<section class="aq-aeo-answer" data-aq-aeo="ARQ-049"><h2>Como ligar pedidos, notas e comprovantes no mesmo dossiê?</h2><p><strong>Resposta direta:</strong> defina uma chave de negócio comum, como número do pedido, e vincule nota fiscal, comprovante de entrega, ocorrência e aceite. O teste de qualidade deve recuperar a operação completa e destacar documentos ausentes.</p><table><thead><tr><th>Etapa</th><th>Regra prática</th><th>Evidência</th></tr></thead><tbody><tr><td>Classificar</td><td>Separar pedido, nota, entrega, ocorrência e aceite</td><td>Tipo documental consistente</td></tr><tr><td>Indexar</td><td>Usar pedido, fornecedor, data e unidade como chaves controladas</td><td>Busca retorna o dossiê correto</td></tr><tr><td>Relacionar</td><td>Vincular anexos sem fundir documentos de naturezas diferentes</td><td>Operação completa e auditável</td></tr><tr><td>Conferir</td><td>Listar faltas, duplicidades e divergências antes da importação</td><td>Relatório de exceções aprovado</td></tr></tbody></table><p>Em Contagem, o desenho do fluxo deve considerar a realidade logística de cada contratante. A Arquindex confirma atendimento e movimentação somente após avaliar o escopo.</p><p><a href="https://www.gov.br/conarq/pt-br">Conselho Nacional de Arquivos</a> · <a href="https://www.arquindex.com.br/gestao_documental_documentos.html">Gestão documental</a> · <a href="https://www.arquindex.com.br/alfresco-incloud-gestao-arquivos.html">GED e ECM com Alfresco</a> · <a href="https://www.arquindex.com.br/solicitar-proposta-contratacao.html?utm_source=site&amp;utm_medium=pagina_local&amp;utm_campaign=arq049_databook_contagem_20261021">Mapear o fluxo documental</a></p></section>'''}]
STYLE='<style id="arquindex-aeo-20261021-manha">.aq-aeo-answer{max-width:1120px;margin:36px auto;padding:28px;border:1px solid #d9e2ef;border-radius:16px;background:#fff;color:#0c1b33;box-sizing:border-box}.aq-aeo-answer h2{color:#0b3d91}.aq-aeo-answer table{width:100%;border-collapse:collapse;margin:18px 0}.aq-aeo-answer th,.aq-aeo-answer td{padding:12px;border:1px solid #d9e2ef;text-align:left;vertical-align:top}.aq-aeo-answer th{background:#eaf0f8}@media(max-width:760px){.aq-aeo-answer{margin:24px 16px;padding:20px}.aq-aeo-answer table{display:block;overflow-x:auto}.aq-aeo-answer th,.aq-aeo-answer td{min-width:145px}}</style>'
WIDGET=Path('conteudo/publicacao/_atendimento-flutuante.html').read_text('utf-8')
def get(f,p):b=bytearray();f.retrbinary('RETR '+p,b.extend);return bytes(b)
def put(f,p,b,label):
 d,n=posixpath.dirname(p),posixpath.basename(p);tmp=d+'/.tmp-'+n+'-'+label;f.storbinary('STOR '+tmp,io.BytesIO(b));assert get(f,tmp)==b
 try:f.delete(p)
 except ftplib.error_perm as e:
  if not str(e).startswith('550'):raise
 f.rename(tmp,p);assert get(f,p)==b
def mkdir(f,p):
 old=f.pwd()
 try:
  f.cwd('/')
  for x in p.strip('/').split('/'):
   try:f.mkd(x)
   except ftplib.error_perm as e:
    if not str(e).startswith('550'):raise
   f.cwd(x)
 finally:f.cwd(old)
def transform(t,b):
 s=BeautifulSoup(b.decode('utf-8'),'html.parser');assert s.head and s.body and s.title and len(s.find_all('h1'))==1
 assert not s.select('[data-aq-aeo="'+t['id']+'"]')
 for c in s.find_all('link',rel=lambda v:v and 'canonical' in v):c.decompose()
 s.head.append(s.new_tag('link',rel='canonical',href=t['url']));s.head.append(BeautifulSoup(STYLE,'html.parser'))
 for sel in ['#arq-floating-style','#arq-floating','#arq-floating-script','#arq-dedup-floats','.aq-brand-wa','#wa-widget-send-button']:
  for n in s.select(sel):n.decompose()
 for n in list(s.find_all('script')):
  src=(n.get('src') or '').lower();txt=n.string or n.get_text() or ''
  if '__arqWhatsappOptions' in txt or 'whatsapp_replace_crisp' in src or 'watiwidget.js' in src:n.decompose()
 f=BeautifulSoup(WIDGET,'html.parser')
 for n in list(f.contents):s.body.append(n)
 a=BeautifulSoup(t['section'],'html.parser');footer=s.find('footer');footer.insert_before(a) if footer else s.body.append(a)
 out=str(s).encode();assert out.count(b'id="arq-floating"')==1 and t['id'].encode() in out;return out
def public(url):
 req=urllib.request.Request(url+'?verify='+STAMP,headers={'User-Agent':'ArquindexSEO/1.0','Cache-Control':'no-cache'})
 with urllib.request.urlopen(req,timeout=40) as r:return r.status,r.read(7000000)
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
  p=base+'/'+t['file'];o=get(f,p);rec.append((t,p,o,transform(t,o)))
 backup='/seo-backups/rodada-20261021-manha-'+STAMP;mkdir(f,backup);f.storbinary('STOR '+backup+'/.htaccess',io.BytesIO(b'Options -Indexes\nRequire all denied\n'))
 for t,p,o,u in rec:
  bp=backup+'/'+t['id'].lower()+'.html';f.storbinary('STOR '+bp,io.BytesIO(o));assert get(f,bp)==o;print('BACKUP_VERIFIED',t['id'],bp,hashlib.sha256(o).hexdigest(),flush=True)
 written=[]
 try:
  for t,p,o,u in rec:assert get(f,p)==o,'CONCURRENT_CHANGE '+t['id']
  for t,p,o,u in rec:put(f,p,u,STAMP);written.append((p,o));print('FTP_PUBLISHED_VERIFIED',t['id'],hashlib.sha256(u).hexdigest(),flush=True)
  time.sleep(2)
  for t,p,o,u in rec:
   st,body=public(t['url']);assert st==200 and t['id'].encode() in body and b'id="arq-floating"' in body and b'noindex' not in body.lower();print('PUBLIC_SOURCE_VERIFIED',t['id'],t['url'],hashlib.sha256(body).hexdigest(),flush=True)
 except Exception:
  for p,o in reversed(written):put(f,p,o,'rollback-'+STAMP)
  print('ROLLBACK_COMPLETED',flush=True);raise
