import ftplib,hashlib,io,os,posixpath,time,urllib.request
from datetime import datetime,timezone
from pathlib import Path
from bs4 import BeautifulSoup
STAMP=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
TARGETS=[
{'id':'ARQ-059','host':'digitalizar-digitalizacao-especializada.arquindex.com.br','file':'index.html','url':'https://digitalizar-digitalizacao-especializada.arquindex.com.br/','title':'Digitalização Profissional: Escopo e Qualidade | Arquindex','h1':'Digitalização profissional de documentos: escopo e critérios de aceite','description':'Entenda como preparar um lote, definir captura, OCR e indexação e validar a qualidade antes de aceitar uma entrega de digitalização profissional.','section':'''<section class="aq-aeo-answer" data-aq-aeo="ARQ-059"><h2>Como preparar documentos para digitalização e conferir a entrega?</h2><p><strong>Resposta direta:</strong> inventarie o lote por série documental, defina formato de saída e campos de indexação, separe exceções e aprove uma amostra antes da produção. No aceite, confira completude, ordem, legibilidade, pesquisa por OCR, metadados e regras de acesso.</p><table><thead><tr><th>Etapa</th><th>Definição</th><th>Evidência de aceite</th></tr></thead><tbody><tr><td>Inventário</td><td>Volume, tipos, tamanhos e restrições</td><td>Lote conciliado com a relação de entrada</td></tr><tr><td>Captura</td><td>Resolução, cor, formato e separação</td><td>Imagem completa, orientada e legível</td></tr><tr><td>OCR e indexação</td><td>Idioma, campos e regras de nomenclatura</td><td>Busca por amostra e campos críticos revisados</td></tr><tr><td>Entrega</td><td>PDF/PDF-A/TIFF conforme uso definido</td><td>Estrutura, acesso, exceções e aceite registrados</td></tr></tbody></table><p>O formato adequado depende do uso, da temporalidade e das obrigações aplicáveis; não há um padrão único para todo acervo.</p><p><a href="https://www.gov.br/conarq/pt-br">Conselho Nacional de Arquivos</a> · <a href="https://www.arquindex.com.br/digitalizacao.html">Digitalização de documentos</a> · <a href="https://www.arquindex.com.br/digitalizacao-com-ocr.html">Digitalização com OCR</a> · <a href="https://www.arquindex.com.br/solicitar-proposta-contratacao.html?utm_source=site&amp;utm_medium=pagina_servico&amp;utm_campaign=arq059_digitalizacao_20261021">Avaliar um lote</a></p></section>'''},
{'id':'ARQ-060','host':'digitalizacao-ocr-empresas.arquindex.com.br','file':'empresas.html','url':'https://digitalizacao-ocr-empresas.arquindex.com.br/empresas.html','title':'OCR para Empresas: Pesquisa e Validação | Arquindex','h1':'OCR para empresas: documentos pesquisáveis e validação','description':'Veja quando o OCR torna documentos pesquisáveis, quais imagens exigem revisão e como validar campos críticos, buscas e exceções antes da entrega.','section':'''<section class="aq-aeo-answer" data-aq-aeo="ARQ-060"><h2>Quando o OCR torna o documento pesquisável e quando precisa de revisão?</h2><p><strong>Resposta direta:</strong> o OCR adiciona uma camada de texto pesquisável quando a imagem tem resolução, contraste, orientação e idioma adequados. Manuscritos, carimbos, cópias degradadas, tabelas e campos críticos exigem validação específica.</p><table><thead><tr><th>Documento</th><th>Risco</th><th>Teste de aceite</th></tr></thead><tbody><tr><td>Texto impresso nítido</td><td>Troca pontual de caracteres</td><td>Pesquisar termos de amostra e comparar a imagem</td></tr><tr><td>Carimbo ou cópia degradada</td><td>Omissão e segmentação incorreta</td><td>Revisar páginas críticas e registrar exceções</td></tr><tr><td>Tabela ou formulário</td><td>Ordem de leitura inadequada</td><td>Validar estrutura e campos necessários</td></tr><tr><td>Dado crítico</td><td>Erro com impacto operacional</td><td>Conferência humana ou regra validada</td></tr></tbody></table><p>A precisão precisa ser medida em amostra representativa do lote; não existe taxa universal aplicável a todo documento.</p><p><a href="https://tesseract-ocr.github.io/">Documentação do Tesseract OCR</a> · <a href="https://www.arquindex.com.br/digitalizacao-com-ocr.html">Digitalização com OCR</a> · <a href="https://www.arquindex.com.br/digitalizacao.html">Digitalização de documentos</a> · <a href="https://www.arquindex.com.br/solicitar-proposta-contratacao.html?utm_source=site&amp;utm_medium=pagina_servico&amp;utm_campaign=arq060_ocr_empresas_20261021">Solicitar teste com amostra</a></p></section>'''},
{'id':'ARQ-063','host':'digitalizacao-rh-sao-bernardo-do-campo.arquindex.com.br','file':'o-que-e.html','url':'https://digitalizacao-rh-sao-bernardo-do-campo.arquindex.com.br/o-que-e.html','title':'Digitalização de Dossiês de RH em São Bernardo | Arquindex','h1':'Digitalização de dossiês de RH em São Bernardo do Campo','description':'Entenda como preparar, digitalizar, indexar e controlar o acesso a dossiês de RH em São Bernardo do Campo, com critérios de qualidade e validade contextualizada.','section':'''<section class="aq-aeo-answer" data-aq-aeo="ARQ-063"><h2>Como digitalizar dossiês de RH e avaliar a validade dos arquivos?</h2><p><strong>Resposta direta:</strong> classifique os documentos por empregado e tipo, limite acessos, registre o vínculo entre original e arquivo digital e valide legibilidade, integridade, metadados e exceções. A validade jurídica não decorre apenas do OCR ou do PDF: depende do processo, do tipo documental e dos requisitos aplicáveis.</p><table><thead><tr><th>Controle</th><th>Aplicação em RH</th><th>Evidência</th></tr></thead><tbody><tr><td>Preparação</td><td>Separar dossiê, competência e documento</td><td>Inventário e amostra aprovados</td></tr><tr><td>Captura</td><td>Preservar frente, verso, ordem e anexos</td><td>Conferência de completude e legibilidade</td></tr><tr><td>Indexação</td><td>Usar campos mínimos e necessários</td><td>Busca por amostra e registro de exceções</td></tr><tr><td>Acesso e retenção</td><td>Perfis, logs e prazo conforme finalidade</td><td>Permissões e descarte documentados</td></tr></tbody></table><p>Atendimento e logística em São Bernardo do Campo são confirmados no escopo; a página não pressupõe unidade física local.</p><p><a href="https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2020/decreto/d10278.htm">Decreto nº 10.278/2020</a> · <a href="https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm">Lei Geral de Proteção de Dados</a> · <a href="https://www.arquindex.com.br/digitalizacao.html">Digitalização de documentos</a> · <a href="https://www.arquindex.com.br/solicitar-proposta-contratacao.html?utm_source=site&amp;utm_medium=pagina_vertical&amp;utm_campaign=arq063_rh_sbc_20261021">Avaliar dossiês de RH</a></p></section>'''}]
STYLE='<style id="arquindex-aeo-20261021-noite">.aq-aeo-answer{max-width:1120px;margin:36px auto;padding:28px;border:1px solid #d9e2ef;border-radius:16px;background:#fff;color:#0c1b33;box-sizing:border-box;overflow-wrap:anywhere}.aq-aeo-answer h2{color:#0b3d91}.aq-aeo-answer table{width:100%;border-collapse:collapse;margin:18px 0}.aq-aeo-answer th,.aq-aeo-answer td{padding:12px;border:1px solid #d9e2ef;text-align:left;vertical-align:top}.aq-aeo-answer th{background:#eaf0f8}@media(max-width:760px){.aq-aeo-answer{margin:24px 16px;padding:20px}.aq-aeo-answer table{display:block;overflow-x:auto}.aq-aeo-answer th,.aq-aeo-answer td{min-width:145px}}</style>'
WIDGET=Path('conteudo/publicacao/_atendimento-flutuante.html').read_text('utf-8')
def get(f,p): b=bytearray();f.retrbinary('RETR '+p,b.extend);return bytes(b)
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
   if not x:continue
   try:f.mkd(x)
   except ftplib.error_perm as e:
    if not str(e).startswith('550'):raise
   f.cwd(x)
 finally:f.cwd(old)
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
 assert not s.select('[data-aq-aeo="'+t['id']+'"]')
 if s.title:s.title.string=t['title']
 else:
  n=s.new_tag('title');n.string=t['title'];s.head.append(n)
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
 f=BeautifulSoup(WIDGET,'html.parser')
 for n in list(f.contents):s.body.append(n)
 a=BeautifulSoup(t['section'],'html.parser');footer=s.find('footer');footer.insert_before(a) if footer else s.body.append(a)
 out=str(s).encode();assert out.count(b'id="arq-floating"')==1 and t['id'].encode() in out;return out
def public(url):
 req=urllib.request.Request(url+'?verify='+STAMP,headers={'User-Agent':'ArquindexSEO/1.0','Cache-Control':'no-cache'})
 with urllib.request.urlopen(req,timeout=40) as r:return r.status,r.read(9000000)
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
 backup='/seo-backups/rodada-20261021-noite-'+STAMP;mkdir(f,backup);f.storbinary('STOR '+backup+'/.htaccess',io.BytesIO(b'Options -Indexes\nRequire all denied\n'))
 for t,p,o,u in rec:
  bp=backup+'/'+t['id'].lower()+'.html';f.storbinary('STOR '+bp,io.BytesIO(o));assert get(f,bp)==o;print('BACKUP_VERIFIED',t['id'],bp,hashlib.sha256(o).hexdigest(),flush=True)
 written=[]
 try:
  for t,p,o,u in rec:assert get(f,p)==o,'CONCURRENT_CHANGE '+t['id']
  for t,p,o,u in rec:put(f,p,u,STAMP);written.append((p,o));print('FTP_PUBLISHED_VERIFIED',t['id'],hashlib.sha256(u).hexdigest(),flush=True)
  time.sleep(2)
  for t,p,o,u in rec:
   st,body=public(t['url']);assert st==200 and t['id'].encode() in body and b'id="arq-floating"' in body and t['url'].encode() in body and b'noindex' not in body.lower();print('PUBLIC_SOURCE_VERIFIED',t['id'],t['url'],hashlib.sha256(body).hexdigest(),flush=True)
 except Exception:
  for p,o in reversed(written):put(f,p,o,'rollback-'+STAMP)
  print('ROLLBACK_COMPLETED',flush=True);raise
