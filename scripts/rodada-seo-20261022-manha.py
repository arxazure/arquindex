import ftplib,hashlib,io,os,posixpath,time,urllib.request
from datetime import datetime,timezone
from pathlib import Path
from bs4 import BeautifulSoup
STAMP=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
TARGETS=[
{'id':'ARQ-064','host':'digitalizar-arquivos-sp.arquindex.com.br','file':'index.html','url':'https://digitalizar-arquivos-sp.arquindex.com.br/','title':'Digitalização de Arquivos Empresariais em São Paulo | Arquindex','h1':'Digitalização de arquivos empresariais em São Paulo','description':'Planeje a digitalização de arquivos empresariais em São Paulo com inventário, amostra, captura, OCR, indexação e critérios objetivos de aceite.','section':'''<section class="aq-aeo-answer" data-aq-aeo="ARQ-064"><h2>Como preparar um lote para digitalização e conferir a entrega em São Paulo?</h2><p><strong>Resposta direta:</strong> inventarie caixas, séries e formatos; separe documentos frágeis ou restritos; aprove uma amostra; e defina como serão testados legibilidade, ordem, OCR, metadados e exceções antes da produção completa.</p><table><thead><tr><th>Etapa</th><th>Decisão necessária</th><th>Evidência de aceite</th></tr></thead><tbody><tr><td>Inventário</td><td>Volume, tipos, tamanhos e restrições</td><td>Relação conciliada com o lote recebido</td></tr><tr><td>Amostra</td><td>Resolução, cor, formato e separação</td><td>Imagem completa, orientada e legível</td></tr><tr><td>OCR e índice</td><td>Idioma, campos e nomenclatura</td><td>Busca por termos e campos críticos conferidos</td></tr><tr><td>Entrega</td><td>Estrutura, acesso e exceções</td><td>Checklist e aceite registrados</td></tr></tbody></table><p>Coleta, atendimento e condições logísticas em São Paulo são confirmados no escopo; a página não pressupõe uma unidade física no endereço do cliente.</p><p><a href="https://www.gov.br/conarq/pt-br">Conselho Nacional de Arquivos</a> · <a href="https://www.arquindex.com.br/digitalizacao.html">Digitalização de documentos</a> · <a href="https://www.arquindex.com.br/digitalizacao-com-ocr.html">Digitalização com OCR</a> · <a href="https://www.arquindex.com.br/solicitar-proposta-contratacao.html?utm_source=site&amp;utm_medium=pagina_local&amp;utm_campaign=arq064_digitalizacao_sp_20261022">Avaliar o lote</a></p></section>'''},
{'id':'ARQ-066','host':'seguranca.arquindex.com.br','file':'index.html','url':'https://seguranca.arquindex.com.br/','title':'Segurança da Informação e Documentos | Arquindex','h1':'Segurança da informação e governança documental','description':'Organize repositórios, responsáveis, acessos, retenção e evidências para reduzir riscos na gestão de documentos físicos e digitais.','section':'''<section class="aq-aeo-answer" data-aq-aeo="ARQ-066"><h2>Como iniciar o mapeamento de documentos e definir responsáveis?</h2><p><strong>Resposta direta:</strong> liste repositórios físicos e digitais, identifique responsáveis e finalidades, classifique criticidade e acesso, registre prazos de retenção e priorize os riscos com maior impacto e menor controle.</p><table><thead><tr><th>Objeto</th><th>Pergunta de controle</th><th>Evidência mínima</th></tr></thead><tbody><tr><td>Repositório</td><td>Onde a informação está e quem administra?</td><td>Inventário com responsável e localização</td></tr><tr><td>Acesso</td><td>Quem precisa consultar, alterar ou exportar?</td><td>Perfis, autorizações e registros de acesso</td></tr><tr><td>Ciclo de vida</td><td>Por quanto tempo manter e como destinar?</td><td>Regra aprovada e descarte documentado</td></tr><tr><td>Risco</td><td>Qual impacto de perda, acesso indevido ou indisponibilidade?</td><td>Prioridade, ação, responsável e prazo</td></tr></tbody></table><p>O mapa deve usar categorias e exemplos anonimizados; não é necessário expor dados pessoais para definir controles e responsabilidades.</p><p><a href="https://www.gov.br/anpd/pt-br">Autoridade Nacional de Proteção de Dados</a> · <a href="https://www.arquindex.com.br/gestao_documental_documentos.html">Gestão documental</a> · <a href="https://www.arquindex.com.br/lgpd-consultoria.html">Consultoria LGPD</a> · <a href="https://www.arquindex.com.br/solicitar-proposta-contratacao.html?utm_source=site&amp;utm_medium=pagina_servico&amp;utm_campaign=arq066_seguranca_governanca_20261022">Solicitar diagnóstico</a></p></section>'''},
{'id':'ARQ-067','host':'contratar-servicos-digitalizacao-documentos-com-armazenamento.arquindex.com.br','file':'index.html','url':'https://contratar-servicos-digitalizacao-documentos-com-armazenamento.arquindex.com.br/','title':'Digitalização com Armazenamento: Como Contratar | Arquindex','h1':'Como contratar digitalização de documentos com armazenamento','description':'Compare escopo de captura, OCR, indexação, armazenamento, acesso e suporte antes de contratar digitalização de documentos para sua empresa.','section':'''<section class="aq-aeo-answer" data-aq-aeo="ARQ-067"><h2>O que comparar ao contratar digitalização com armazenamento?</h2><p><strong>Resposta direta:</strong> separe no orçamento a preparação e captura, o OCR e a indexação, a entrega dos arquivos e o repositório. Defina usuários, permissões, pesquisa, exportação, backup, suporte, prazo de retenção e como os dados serão devolvidos ao término do contrato.</p><table><thead><tr><th>Componente</th><th>Definir no escopo</th><th>Teste de aceite</th></tr></thead><tbody><tr><td>Digitalização</td><td>Volume, resolução, cor, formato e exceções</td><td>Completude, ordem e legibilidade por amostra</td></tr><tr><td>OCR e índice</td><td>Idioma, campos e regra de nomenclatura</td><td>Busca e conferência de campos críticos</td></tr><tr><td>Armazenamento</td><td>Usuários, permissões, backup e exportação</td><td>Acesso por perfil, recuperação e cópia de saída</td></tr><tr><td>Operação</td><td>Suporte, níveis de serviço e término</td><td>Chamados, prazos e plano de devolução</td></tr></tbody></table><p>Preço por página não resume o custo total: preparação, indexação, qualidade do acervo e requisitos do repositório alteram o escopo. Valores só devem ser confirmados após avaliar uma amostra real.</p><p><a href="https://www.arquindex.com.br/digitalizacao.html">Digitalização de documentos</a> · <a href="https://www.arquindex.com.br/guarda_de_documentos.html">Guarda documental</a> · <a href="https://www.arquindex.com.br/solicitar-proposta-contratacao.html?utm_source=site&amp;utm_medium=pagina_comercial&amp;utm_campaign=arq067_digitalizacao_armazenamento_20261022">Solicitar proposta</a></p></section>'''}]
STYLE='<style id="arquindex-aeo-20261022-manha">.aq-aeo-answer{max-width:1120px;margin:36px auto;padding:28px;border:1px solid #d9e2ef;border-radius:16px;background:#fff;color:#0c1b33;box-sizing:border-box;overflow-wrap:anywhere}.aq-aeo-answer h2{color:#0b3d91}.aq-aeo-answer table{width:100%;border-collapse:collapse;margin:18px 0}.aq-aeo-answer th,.aq-aeo-answer td{padding:12px;border:1px solid #d9e2ef;text-align:left;vertical-align:top}.aq-aeo-answer th{background:#eaf0f8}@media(max-width:760px){.aq-aeo-answer{margin:24px 16px;padding:20px}.aq-aeo-answer table{display:block;overflow-x:auto}.aq-aeo-answer th,.aq-aeo-answer td{min-width:145px}}</style>'
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
 backup='/seo-backups/rodada-20261022-manha-'+STAMP;mkdir(f,backup);f.storbinary('STOR '+backup+'/.htaccess',io.BytesIO(b'Options -Indexes\nRequire all denied\n'))
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
