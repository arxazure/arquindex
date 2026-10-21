import ftplib,hashlib,io,os,posixpath,time,urllib.request
from datetime import datetime,timezone
from pathlib import Path
from bs4 import BeautifulSoup
STAMP=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
TARGETS=[
{'id':'ARQ-054','host':'aplicativos-facilitam-digitalizacao-documentos-pelo-celular.arquindex.com.br','file':'faq.html','url':'https://aplicativos-facilitam-digitalizacao-documentos-pelo-celular.arquindex.com.br/faq.html','title':'Digitalização pelo celular: limites e conferência | Arquindex','h1':'Digitalização de documentos pelo celular: quando usar?','description':'Entenda quando digitalizar pelo celular é suficiente, quais limites de qualidade observar e quando contratar captura, OCR e indexação profissional.','section':'''<section class="aq-aeo-answer" data-aq-aeo="ARQ-054"><h2>Quando um aplicativo de celular é suficiente para digitalizar documentos?</h2><p><strong>Resposta direta:</strong> o celular pode atender cópias ocasionais e documentos simples quando há boa iluminação, enquadramento e conferência. Para lotes corporativos, OCR, metadados, controle de acesso ou requisitos de conformidade, é necessário definir processo, amostragem e critérios de aceite.</p><table><thead><tr><th>Cenário</th><th>Abordagem adequada</th><th>Conferência</th></tr></thead><tbody><tr><td>Cópia ocasional</td><td>Aplicativo com correção de perspectiva</td><td>Imagem completa, legível e orientada</td></tr><tr><td>Lote corporativo</td><td>Captura controlada, separação e indexação</td><td>Completude, ordem, duplicidades e exceções</td></tr><tr><td>Pesquisa textual</td><td>OCR com idioma e resolução definidos</td><td>Busca por amostra e revisão de campos críticos</td></tr><tr><td>Conformidade</td><td>Escopo técnico e documental próprio</td><td>Evidências, responsáveis e aceite documentado</td></tr></tbody></table><p>Uma imagem legível não comprova sozinha autenticidade, integridade ou atendimento a requisitos legais. Esses critérios dependem do contexto e do processo adotado.</p><p><a href="https://www.gov.br/conarq/pt-br">Conselho Nacional de Arquivos</a> · <a href="https://www.arquindex.com.br/digitalizacao.html">Digitalização de documentos</a> · <a href="https://www.arquindex.com.br/digitalizacao-com-ocr.html">Digitalização com OCR</a> · <a href="https://www.arquindex.com.br/solicitar-proposta-contratacao.html?utm_source=site&amp;utm_medium=faq&amp;utm_campaign=arq054_digitalizacao_celular_20261021">Avaliar o lote</a></p></section>'''},
{'id':'ARQ-055','host':'arquivo.arquindex.com.br','file':'bh.html','url':'https://arquivo.arquindex.com.br/bh.html','title':'Guarda de Documentos em BH: Consulta e Controle | Arquindex','h1':'Guarda e organização de documentos em Belo Horizonte','description':'Guarda e organização documental em Belo Horizonte com inventário, protocolos de retirada, consulta e devolução, controle de acesso e destinação documentada.','section':'''<section class="aq-aeo-answer" data-aq-aeo="ARQ-055"><h2>Como localizar, solicitar e devolver documentos guardados?</h2><p><strong>Resposta direta:</strong> cada caixa e pasta precisa de identificação controlada; a solicitação deve registrar requerente, finalidade, data e item; a retirada e a devolução precisam manter cadeia de custódia e atualizar a localização.</p><table><thead><tr><th>Etapa</th><th>Registro mínimo</th><th>Evidência de controle</th></tr></thead><tbody><tr><td>Entrada</td><td>Código, conteúdo, período e responsável</td><td>Inventário conciliado com volumes recebidos</td></tr><tr><td>Solicitação</td><td>Requerente, motivo, item e prioridade</td><td>Pedido autorizado e data registrada</td></tr><tr><td>Retirada</td><td>Responsável pela movimentação e destino</td><td>Protocolo e localização atual</td></tr><tr><td>Devolução</td><td>Data, condição e conferência</td><td>Baixa do empréstimo e posição atualizada</td></tr></tbody></table><p>Temporalidade e destinação dependem da série documental e das obrigações aplicáveis. Atendimento, coleta e condições logísticas em Belo Horizonte são confirmados na avaliação do acervo; nenhum endereço operacional restrito é divulgado.</p><p><a href="https://www.gov.br/conarq/pt-br">Conselho Nacional de Arquivos</a> · <a href="https://www.arquindex.com.br/guarda_de_documentos.html">Guarda de documentos</a> · <a href="https://www.arquindex.com.br/gestao_documental_documentos.html">Gestão documental</a> · <a href="https://www.arquindex.com.br/solicitar-proposta-contratacao.html?utm_source=site&amp;utm_medium=pagina_local&amp;utm_campaign=arq055_guarda_bh_20261021">Solicitar diagnóstico do acervo</a></p></section>'''},
{'id':'ARQ-057','host':'solucoes-ocr-sp.arquindex.com.br','file':'vantagens.html','url':'https://solucoes-ocr-sp.arquindex.com.br/vantagens.html','title':'OCR de Documentos em São Paulo: Pesquisa e Revisão | Arquindex','h1':'OCR de documentos em São Paulo: pesquisa e critérios de revisão','description':'Entenda quando o OCR torna documentos pesquisáveis, quais imagens exigem revisão e como validar campos críticos antes da entrega em São Paulo.','section':'''<section class="aq-aeo-answer" data-aq-aeo="ARQ-057"><h2>Quando o OCR torna o documento pesquisável e quando precisa de revisão?</h2><p><strong>Resposta direta:</strong> o OCR cria uma camada de texto que permite busca quando a imagem tem resolução, contraste, orientação e idioma adequados. Carimbos, manuscritos, tabelas, cópias degradadas e campos críticos exigem revisão ou validação específica.</p><table><thead><tr><th>Condição</th><th>Risco</th><th>Teste de aceite</th></tr></thead><tbody><tr><td>Texto impresso nítido</td><td>Troca pontual de caracteres</td><td>Pesquisar termos de amostra e comparar com a imagem</td></tr><tr><td>Carimbo ou baixa qualidade</td><td>Omissão e segmentação incorreta</td><td>Revisar páginas críticas e registrar exceções</td></tr><tr><td>Tabela e formulário</td><td>Ordem de leitura inadequada</td><td>Validar campos e estrutura de saída</td></tr><tr><td>Dado crítico</td><td>Erro com impacto operacional</td><td>Conferência humana ou regra automatizada validada</td></tr></tbody></table><p>Não existe precisão universal: a taxa de acerto deve ser medida em amostra representativa do lote. Atendimento e logística em São Paulo são confirmados no escopo; a página não pressupõe unidade física local.</p><p><a href="https://tesseract-ocr.github.io/">Documentação do projeto Tesseract OCR</a> · <a href="https://www.arquindex.com.br/digitalizacao-com-ocr.html">Digitalização com OCR</a> · <a href="https://www.arquindex.com.br/digitalizacao.html">Digitalização de documentos</a> · <a href="https://www.arquindex.com.br/solicitar-proposta-contratacao.html?utm_source=site&amp;utm_medium=pagina_servico&amp;utm_campaign=arq057_ocr_sp_20261021">Solicitar teste com amostra</a></p></section>'''}]
STYLE='<style id="arquindex-aeo-20261021-tarde">.aq-aeo-answer{max-width:1120px;margin:36px auto;padding:28px;border:1px solid #d9e2ef;border-radius:16px;background:#fff;color:#0c1b33;box-sizing:border-box;overflow-wrap:anywhere}.aq-aeo-answer h2{color:#0b3d91}.aq-aeo-answer table{width:100%;border-collapse:collapse;margin:18px 0}.aq-aeo-answer th,.aq-aeo-answer td{padding:12px;border:1px solid #d9e2ef;text-align:left;vertical-align:top}.aq-aeo-answer th{background:#eaf0f8}@media(max-width:760px){.aq-aeo-answer{margin:24px 16px;padding:20px}.aq-aeo-answer table{display:block;overflow-x:auto}.aq-aeo-answer th,.aq-aeo-answer td{min-width:145px}}</style>'
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
 s.title.string=t['title']
 desc=s.find('meta',attrs={'name':lambda v:v and v.lower()=='description'})
 if not desc:
  desc=s.new_tag('meta',attrs={'name':'description'});s.head.append(desc)
 desc['content']=t['description']
 h1s=s.find_all('h1');assert h1s
 h1s[0].string=t['h1']
 for h in h1s[1:]:
  h.name='h2'
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
 backup='/seo-backups/rodada-20261021-tarde-'+STAMP;mkdir(f,backup);f.storbinary('STOR '+backup+'/.htaccess',io.BytesIO(b'Options -Indexes\nRequire all denied\n'))
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
