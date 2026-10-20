import ftplib, hashlib, io, os, posixpath, time, urllib.request
from datetime import datetime, timezone
from pathlib import Path
from bs4 import BeautifulSoup

STAMP=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
TARGETS=[
 {'id':'ARQ-036','host':'conarq-juridico-nova-lima.arquindex.com.br','file':'index.html','url':'https://conarq-juridico-nova-lima.arquindex.com.br/','section':'''<section class="aq-aeo-answer" data-aq-aeo="ARQ-036"><h2>Como preparar contratos e anexos técnicos para digitalização em Nova Lima?</h2><p><strong>Resposta direta:</strong> comece por uma amostra representativa, preserve a relação entre contrato, aditivos e anexos, defina metadados e critérios de aceite e registre as exceções antes da produção em lote.</p><table><thead><tr><th>Controle</th><th>Decisão verificável</th></tr></thead><tbody><tr><td>Vínculo documental</td><td>Manter contrato, aditivos, plantas e anexos associados pelo identificador acordado</td></tr><tr><td>Captura</td><td>Definir resolução, cor, frente e verso e tratamento de formatos especiais na amostra</td></tr><tr><td>Indexação</td><td>Validar número, parte, data, projeto e confidencialidade sem inferir dados ilegíveis</td></tr><tr><td>Aceite</td><td>Conferir completude, legibilidade, busca, permissões e cópia de segurança</td></tr></tbody></table><p>Os requisitos do Decreto nº 10.278/2020 dependem do tipo documental e da finalidade. Digitalizar não autoriza, por si só, eliminar o original.</p><p><a href="https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2020/decreto/d10278.htm">Decreto nº 10.278/2020</a> · <a href="https://www.arquindex.com.br/digitalizacao.html">Digitalização de documentos</a> · <a href="https://www.arquindex.com.br/solicitar-proposta-contratacao.html?utm_source=site&amp;utm_medium=pagina_local&amp;utm_campaign=arq036_novalima_20261020">Avaliar uma amostra</a></p></section>'''},
 {'id':'ARQ-038','host':'ged.arquindex.com.br','file':'bh.html','url':'https://ged.arquindex.com.br/bh.html','section':'''<section class="aq-aeo-answer" data-aq-aeo="ARQ-038"><h2>Quando uma empresa em Belo Horizonte precisa de organização, GED ou ECM?</h2><p><strong>Resposta direta:</strong> organização resolve classificação e localização; GED acrescenta captura, índice, permissões e recuperação; ECM coordena conteúdo, processos, integrações e governança em escala. A escolha deve nascer de um processo piloto, não apenas do nome da tecnologia.</p><table><thead><tr><th>Cenário</th><th>Prioridade</th><th>Teste no piloto</th></tr></thead><tbody><tr><td>Acervo físico disperso</td><td>Inventário e organização</td><td>Localização, movimentação, temporalidade e responsáveis</td></tr><tr><td>Arquivos digitais sem padrão</td><td>GED</td><td>Metadados, busca, acesso, versão e recuperação</td></tr><tr><td>Fluxos entre áreas e sistemas</td><td>ECM</td><td>Integração, regras, auditoria e continuidade</td></tr></tbody></table><p>Antes da contratação, defina usuários, volume, documentos críticos, permissões, integrações, migração e critérios de aceite.</p><p><a href="https://www.arquindex.com.br/gestao-documental-belo-horizonte.html">Gestão documental em Belo Horizonte</a> · <a href="https://www.arquindex.com.br/gestao_documental_documentos.html">Gestão de documentos</a> · <a href="https://www.arquindex.com.br/solicitar-proposta-contratacao.html?utm_source=site&amp;utm_medium=pagina_servico&amp;utm_campaign=arq038_ged_bh_20261020">Definir um piloto</a></p></section>'''},
 {'id':'ARQ-039','host':'ocr-prontuarios-contagem.arquindex.com.br','file':'index.html','url':'https://ocr-prontuarios-contagem.arquindex.com.br/','section':'''<section class="aq-aeo-answer" data-aq-aeo="ARQ-039"><h2>Quando o OCR torna um prontuário pesquisável e quando exige revisão?</h2><p><strong>Resposta direta:</strong> OCR ajuda a localizar texto impresso com boa captura, mas manuscritos, carimbos, tabelas, páginas degradadas e identificadores clínicos exigem revisão proporcional ao risco. A imagem original deve permanecer vinculada ao texto reconhecido.</p><table><thead><tr><th>Material</th><th>Uso prudente do OCR</th></tr></thead><tbody><tr><td>Texto impresso legível</td><td>Busca e pré-indexação, com amostragem de qualidade</td></tr><tr><td>Manuscritos e carimbos</td><td>Não depender de leitura automática sem conferência humana</td></tr><tr><td>Tabelas e formulários</td><td>Validar campos, ordem de leitura e associação com a imagem</td></tr><tr><td>Identificadores do paciente</td><td>Conferência obrigatória segundo o processo e o risco definidos</td></tr></tbody></table><p>O escopo deve incluir acesso restrito, rastreabilidade, critérios de aceite e tratamento de exceções. Não existe percentual único de precisão aplicável a todo acervo.</p><p><a href="https://www.arquindex.com.br/digitalizacao-com-ocr.html">Digitalização com OCR</a> · <a href="https://www.arquindex.com.br/solicitar-proposta-contratacao.html?utm_source=site&amp;utm_medium=pagina_vertical&amp;utm_campaign=arq039_ocr_contagem_20261020">Avaliar uma amostra</a></p></section>'''}
]
STYLE='<style id="arquindex-aeo-20261020-tarde">.aq-aeo-answer{max-width:1120px;margin:36px auto;padding:28px;border:1px solid #d9e2ef;border-radius:16px;background:#fff;color:#0c1b33}.aq-aeo-answer h2{color:#0b3d91}.aq-aeo-answer table{width:100%;border-collapse:collapse;margin:18px 0}.aq-aeo-answer th,.aq-aeo-answer td{padding:12px;border:1px solid #d9e2ef;text-align:left;vertical-align:top}.aq-aeo-answer th{background:#eaf0f8}@media(max-width:760px){.aq-aeo-answer{margin:24px 16px;padding:20px}.aq-aeo-answer table{display:block;overflow-x:auto}.aq-aeo-answer th,.aq-aeo-answer td{min-width:145px}}</style>'
WIDGET=Path('conteudo/publicacao/_atendimento-flutuante.html').read_text('utf-8')
def get(ftp,path):
 data=bytearray();ftp.retrbinary('RETR '+path,data.extend);return bytes(data)
def put(ftp,path,data,label):
 d,n=posixpath.dirname(path),posixpath.basename(path);tmp=d+'/.tmp-'+n+'-'+label
 ftp.storbinary('STOR '+tmp,io.BytesIO(data));assert get(ftp,tmp)==data
 try:ftp.delete(path)
 except ftplib.error_perm as e:
  if not str(e).startswith('550'):raise
 ftp.rename(tmp,path);assert get(ftp,path)==data
def mkdir(ftp,path):
 old=ftp.pwd()
 try:
  ftp.cwd('/')
  for p in path.strip('/').split('/'):
   try:ftp.mkd(p)
   except ftplib.error_perm as e:
    if not str(e).startswith('550'):raise
   ftp.cwd(p)
 finally:ftp.cwd(old)
def locate(ftp,base,t):
 for root in [base+'/subdominios/'+t['host'],base+'/'+t['host'],'/subdominios/'+t['host'],'/'+t['host']]:
  p=root+'/'+t['file']
  try:
   b=get(ftp,p)
   if b'<html' in b.lower():return p,b
  except ftplib.all_errors:pass
 raise RuntimeError('TARGET_NOT_FOUND '+t['id'])
def transform(t,b):
 s=BeautifulSoup(b.decode('utf-8'),'html.parser');assert s.head and s.body and s.title and s.find('h1')
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
 a=BeautifulSoup(t['section'],'html.parser');footer=s.find('footer')
 footer.insert_before(a) if footer else s.body.append(a)
 out=str(s).encode();assert out.count(b'id="arq-floating"')==1 and t['id'].encode() in out;return out
def public(url):
 req=urllib.request.Request(url+('?verify=' if '?' not in url else '&verify=')+STAMP,headers={'User-Agent':'ArquindexSEO/1.0','Cache-Control':'no-cache'})
 with urllib.request.urlopen(req,timeout=40) as r:return r.status,r.read(6000000)
with ftplib.FTP_TLS(timeout=60) as ftp:
 ftp.connect('ftp.arquindex.com.br',21);ftp.login('arquind2',os.environ['FTP_PASSWORD']);ftp.prot_p();ftp.set_pasv(True)
 base=None
 for c in ['/public_html','/home/arquind2/public_html']:
  try:
   if b'arquindex' in get(ftp,c+'/index.html').lower():base=c;break
  except ftplib.all_errors:pass
 assert base
 rec=[(t,*locate(ftp,base,t)) for t in TARGETS];rec=[(t,p,o,transform(t,o)) for t,p,o in rec]
 backup='/seo-backups/rodada-20261020-tarde-'+STAMP;mkdir(ftp,backup);ftp.storbinary('STOR '+backup+'/.htaccess',io.BytesIO(b'Options -Indexes\nRequire all denied\n'))
 for t,p,o,u in rec:
  bp=backup+'/'+t['id'].lower()+'-'+hashlib.sha256(p.encode()).hexdigest()[:12]+'.html';ftp.storbinary('STOR '+bp,io.BytesIO(o));assert get(ftp,bp)==o;print('BACKUP_VERIFIED',t['id'],bp,hashlib.sha256(o).hexdigest(),flush=True)
 written=[]
 try:
  for t,p,o,u in rec:assert get(ftp,p)==o,'CONCURRENT_CHANGE '+t['id']
  for t,p,o,u in rec:put(ftp,p,u,STAMP);written.append((p,o));print('FTP_PUBLISHED_VERIFIED',t['id'],hashlib.sha256(u).hexdigest(),flush=True)
  for t,p,o,u in rec:
   last=None
   for attempt in range(3):
    try:
     st,body=public(t['url']);assert st==200 and t['id'].encode() in body and b'id="arq-floating"' in body and b'noindex' not in body.lower();print('PUBLIC_SOURCE_VERIFIED',t['id'],t['url'],hashlib.sha256(body).hexdigest(),flush=True);last=None;break
    except Exception as e:last=e;time.sleep(5)
   if last:raise last
 except Exception:
  for p,o in reversed(written):put(ftp,p,o,'rollback-'+STAMP)
  print('ROLLBACK_COMPLETED',flush=True);raise
