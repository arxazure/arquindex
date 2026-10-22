import ftplib,hashlib,io,os,posixpath,time,urllib.request
from datetime import datetime,timezone
from pathlib import Path
from bs4 import BeautifulSoup
STAMP=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
TARGETS=[
{'id':'ARQ-070','host':'ocr-maua.arquindex.com.br','file':'index.html','url':'https://ocr-maua.arquindex.com.br/','title':'OCR em Mauá: Pesquisa e Conferência Documental | Arquindex','h1':'Digitalização com OCR em Mauá','description':'Entenda quando o OCR torna documentos pesquisáveis, quais materiais exigem revisão e como definir amostra, indexação e critérios de aceite em Mauá.','section':'''<section class="aq-aeo-answer" data-aq-aeo="ARQ-070"><h2>Quando o OCR torna um documento pesquisável e quando precisa de revisão?</h2><p><strong>Resposta direta:</strong> o OCR cria uma camada de texto para pesquisa, mas a qualidade depende da imagem, do idioma, da tipografia e do estado do original. Documentos com carimbos, manuscritos, baixo contraste, dobras ou páginas degradadas precisam de amostra e conferência proporcional ao uso do dado.</p><table><thead><tr><th>Situação</th><th>Procedimento</th><th>Critério de aceite</th></tr></thead><tbody><tr><td>Texto impresso e imagem limpa</td><td>OCR com idioma e orientação definidos</td><td>Pesquisa por termos da amostra</td></tr><tr><td>Carimbos, tabelas ou baixo contraste</td><td>Ajuste de captura e revisão dirigida</td><td>Campos críticos conferidos</td></tr><tr><td>Manuscritos ou páginas degradadas</td><td>Indexação manual ou revisão ampliada</td><td>Exceções registradas e aprovadas</td></tr><tr><td>Entrega</td><td>PDF pesquisável e metadados combinados</td><td>Busca, abertura e exportação testadas</td></tr></tbody></table><p>Atendimento e logística em Mauá são confirmados no escopo; a página não declara unidade física local nem precisão universal.</p><p class="aq-review">Revisão editorial Arquindex: 22/10/2026. Fonte primária: <a href="https://www.gov.br/conarq/pt-br">CONARQ</a>.</p><p><a href="https://www.arquindex.com.br/digitalizacao-com-ocr.html">Digitalização com OCR</a> · <a href="https://www.arquindex.com.br/digitalizacao.html">Digitalização de documentos</a> · <a href="https://www.arquindex.com.br/solicitar-proposta-contratacao.html?utm_source=site&amp;utm_medium=pagina_local&amp;utm_campaign=arq070_ocr_maua_20261022">Avaliar uma amostra</a></p></section>'''},
{'id':'ARQ-073','host':'mapeamento-educacao.arquindex.com.br','file':'index.html','url':'https://mapeamento-educacao.arquindex.com.br/','title':'Mapeamento Documental para Educação | Arquindex','h1':'Mapeamento documental para instituições de ensino','description':'Mapeie repositórios, responsáveis, acessos, retenção e riscos de documentos acadêmicos e administrativos sem expor dados pessoais.','section':'''<section class="aq-aeo-answer" data-aq-aeo="ARQ-073"><h2>Como iniciar o mapeamento de informações em uma instituição de ensino?</h2><p><strong>Resposta direta:</strong> comece pelos processos — matrícula, vida acadêmica, contratos, RH e financeiro — e registre onde cada documento está, quem responde por ele, quem pode acessar, por quanto tempo deve ser mantido e qual risco precisa ser tratado primeiro.</p><table><thead><tr><th>Objeto</th><th>Pergunta de mapeamento</th><th>Saída útil</th></tr></thead><tbody><tr><td>Processo</td><td>Qual tarefa gera ou usa o documento?</td><td>Fluxo e finalidade documentados</td></tr><tr><td>Repositório</td><td>Onde está o original e qual é a cópia de trabalho?</td><td>Inventário físico e digital</td></tr><tr><td>Responsabilidade</td><td>Quem cria, aprova, consulta e administra?</td><td>Matriz de papéis e acessos</td></tr><tr><td>Ciclo de vida</td><td>Qual regra orienta guarda e destinação?</td><td>Prazo, fundamento e ação</td></tr><tr><td>Risco</td><td>O que ocorre em perda, indisponibilidade ou acesso indevido?</td><td>Prioridade, responsável e prazo</td></tr></tbody></table><p>O diagnóstico pode usar categorias e exemplos anonimizados; não é necessário expor prontuários, dados de alunos ou documentos de colaboradores para desenhar controles.</p><p class="aq-review">Revisão editorial Arquindex: 22/10/2026. Fontes primárias: <a href="https://www.gov.br/anpd/pt-br">ANPD</a> e <a href="https://www.gov.br/conarq/pt-br">CONARQ</a>.</p><p><a href="https://www.arquindex.com.br/gestao_documental_documentos.html">Gestão documental</a> · <a href="https://www.arquindex.com.br/lgpd-consultoria.html">Consultoria LGPD</a> · <a href="https://www.arquindex.com.br/solicitar-proposta-contratacao.html?utm_source=site&amp;utm_medium=pagina_vertical&amp;utm_campaign=arq073_mapeamento_educacao_20261022">Solicitar diagnóstico</a></p></section>'''},
{'id':'ARQ-075','host':'digitalizar-lgpd-solucao.arquindex.com.br','file':'empresas.html','url':'https://digitalizar-lgpd-solucao.arquindex.com.br/empresas.html','title':'Consultoria LGPD: Escopo e Entregáveis | Arquindex','h1':'O que uma consultoria de adequação à LGPD entrega','description':'Compare diagnóstico, inventário de tratamentos, responsabilidades, plano de ação e entregáveis antes de contratar consultoria de adequação à LGPD.','section':'''<section class="aq-aeo-answer" data-aq-aeo="ARQ-075"><h2>Como definir o escopo de uma consultoria de adequação à LGPD?</h2><p><strong>Resposta direta:</strong> o escopo deve partir do diagnóstico dos tratamentos de dados, sistemas, fornecedores e riscos. Inventário, registros, políticas, RIPD, contratos, treinamentos e apoio ao encarregado só entram quando forem pertinentes ao contexto e às responsabilidades apuradas.</p><table><thead><tr><th>Frente</th><th>Decisão de escopo</th><th>Evidência esperada</th></tr></thead><tbody><tr><td>Diagnóstico</td><td>Unidades, processos e sistemas abrangidos</td><td>Achados, lacunas e prioridades</td></tr><tr><td>Inventário</td><td>Tratamentos, finalidades, titulares e agentes</td><td>Registro conferido pelos responsáveis</td></tr><tr><td>Riscos</td><td>Critérios e situações que exigem análise adicional</td><td>Plano de ação e RIPD quando aplicável</td></tr><tr><td>Governança</td><td>Papéis, políticas, contratos e rotina de revisão</td><td>Responsáveis, prazos e versões aprovadas</td></tr><tr><td>Transferência</td><td>Treinamento e continuidade após o projeto</td><td>Materiais, registro e pendências entregues</td></tr></tbody></table><p>A consultoria organiza evidências e decisões; não substitui avaliação jurídica específica nem garante conformidade automática. Entregáveis e prazos são confirmados após diagnóstico.</p><p class="aq-review">Revisão editorial Arquindex: 22/10/2026. Fonte primária: <a href="https://www.gov.br/anpd/pt-br">Autoridade Nacional de Proteção de Dados</a>.</p><p><a href="https://www.arquindex.com.br/lgpd-consultoria.html">Consultoria LGPD</a> · <a href="https://www.arquindex.com.br/dpo-terceirizado.html">DPO terceirizado</a> · <a href="https://www.arquindex.com.br/solicitar-proposta-contratacao.html?utm_source=site&amp;utm_medium=pagina_comercial&amp;utm_campaign=arq075_escopo_lgpd_20261022">Definir o escopo</a></p></section>'''}]
STYLE='<style id="arquindex-aeo-20261022-tarde">.aq-aeo-answer{max-width:1120px;margin:36px auto;padding:28px;border:1px solid #d9e2ef;border-radius:16px;background:#fff;color:#0c1b33;box-sizing:border-box;overflow-wrap:anywhere}.aq-aeo-answer h2{color:#0b3d91}.aq-aeo-answer table{width:100%;border-collapse:collapse;margin:18px 0}.aq-aeo-answer th,.aq-aeo-answer td{padding:12px;border:1px solid #d9e2ef;text-align:left;vertical-align:top}.aq-aeo-answer th{background:#eaf0f8}.aq-review{font-size:.94rem;color:#42536b}@media(max-width:760px){.aq-aeo-answer{margin:24px 16px;padding:20px}.aq-aeo-answer table{display:block;overflow-x:auto}.aq-aeo-answer th,.aq-aeo-answer td{min-width:145px}}</style>'
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
 backup='/seo-backups/rodada-20261022-tarde-'+STAMP;mkdir(f,backup);f.storbinary('STOR '+backup+'/.htaccess',io.BytesIO(b'Options -Indexes\nRequire all denied\n'))
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
