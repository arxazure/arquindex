import ftplib,hashlib,io,os,posixpath,time,urllib.request
from datetime import datetime,timezone
from pathlib import Path
from bs4 import BeautifulSoup
STAMP=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
TARGETS=[
{'id':'ARQ-043','file':'alfresco-belo-horizonte.html','url':'https://www.arquindex.com.br/alfresco-belo-horizonte.html','section':'''<section class="aq-aeo-answer" data-aq-aeo="ARQ-043"><h2>Como dimensionar e validar uma implantação Alfresco?</h2><p><strong>Resposta direta:</strong> defina usuários simultâneos, volume inicial e crescimento, tipos documentais, permissões, integrações, migração, backup e recuperação; depois valide tudo em um piloto com critérios de aceite mensuráveis.</p><table><thead><tr><th>Decisão</th><th>Teste de aceite</th></tr></thead><tbody><tr><td>Metadados</td><td>Localizar documentos reais pelos campos definidos, sem depender apenas do nome do arquivo</td></tr><tr><td>Permissões</td><td>Confirmar acesso, restrição e auditoria para perfis representativos</td></tr><tr><td>Migração</td><td>Conferir quantidade, versões, propriedades e exceções da amostra</td></tr><tr><td>Continuidade</td><td>Executar cópia de segurança e teste documentado de recuperação</td></tr></tbody></table><p>A versão, os componentes e o dimensionamento devem ser confirmados para cada ambiente antes da proposta técnica.</p><p><a href="https://docs.alfresco.com/content-services/latest/">Documentação oficial Alfresco Content Services</a> · <a href="https://www.arquindex.com.br/alfresco-incloud-gestao-arquivos.html">Soluções Alfresco da Arquindex</a> · <a href="https://www.arquindex.com.br/solicitar-proposta-contratacao.html?utm_source=site&amp;utm_medium=pagina_local&amp;utm_campaign=arq043_alfresco_bh_20261020">Definir um piloto</a></p></section>'''},
{'id':'ARQ-044','file':'gestao-documental-belo-horizonte.html','url':'https://www.arquindex.com.br/gestao-documental-belo-horizonte.html','section':'''<section class="aq-aeo-answer" data-aq-aeo="ARQ-044"><h2>Como escolher entre organizar arquivos, implantar GED e adotar ECM?</h2><p><strong>Resposta direta:</strong> organize primeiro quando o problema é classificação e localização; use GED quando precisa de captura, índice, acesso e versões; avance para ECM quando conteúdo, processos e integrações precisam de governança conjunta.</p><table><thead><tr><th>Necessidade</th><th>Entrega inicial</th><th>Evidência</th></tr></thead><tbody><tr><td>Acervo físico disperso</td><td>Inventário, classificação e protocolo</td><td>Documento recuperado e movimentação registrada</td></tr><tr><td>Arquivos digitais sem padrão</td><td>GED com índice e permissões</td><td>Busca, versão, acesso e restauração testados</td></tr><tr><td>Fluxos entre áreas</td><td>ECM e integração gradual</td><td>Piloto com regras, responsáveis e auditoria</td></tr></tbody></table><p>A temporalidade e o descarte dependem do tipo documental e das obrigações aplicáveis; tecnologia não substitui a decisão arquivística.</p><p><a href="https://www.gov.br/conarq/pt-br">Conselho Nacional de Arquivos</a> · <a href="https://www.arquindex.com.br/gestao_documental_documentos.html">Gestão documental</a> · <a href="https://www.arquindex.com.br/solicitar-proposta-contratacao.html?utm_source=site&amp;utm_medium=pagina_local&amp;utm_campaign=arq044_gestao_bh_20261020">Avaliar o acervo</a></p></section>'''},
{'id':'ARQ-045','file':'consultoria-lgpd-belo-horizonte.html','url':'https://www.arquindex.com.br/consultoria-lgpd-belo-horizonte.html','section':'''<section class="aq-aeo-answer" data-aq-aeo="ARQ-045"><h2>O que uma consultoria LGPD entrega e como definir o escopo?</h2><p><strong>Resposta direta:</strong> o escopo começa pelos processos e riscos prioritários e normalmente combina diagnóstico, inventário das operações, responsáveis, bases legais, contratos, atendimento aos titulares e plano de ação. ROPA, RIPD e políticas são definidos conforme a necessidade apurada, não como pacote automático.</p><table><thead><tr><th>Fase</th><th>Entregável verificável</th></tr></thead><tbody><tr><td>Diagnóstico</td><td>Escopo, áreas, responsáveis, lacunas e critérios de prioridade</td></tr><tr><td>Mapeamento</td><td>Fluxos, finalidades, titulares, dados, acessos, compartilhamentos e retenção</td></tr><tr><td>Plano de ação</td><td>Medidas, responsável, prazo, evidência e risco residual</td></tr><tr><td>Governança</td><td>Rotina de atualização, incidentes, titulares, contratos e treinamento</td></tr></tbody></table><p>O artigo 37 da LGPD prevê o registro das operações de tratamento. O trabalho precisa refletir os processos reais, inclusive arquivos físicos e fornecedores.</p><p><a href="https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm#art37">LGPD — artigo 37</a> · <a href="https://www.arquindex.com.br/lgpd-consultoria.html">Consultoria LGPD</a> · <a href="https://www.arquindex.com.br/solicitar-proposta-contratacao.html?utm_source=site&amp;utm_medium=pagina_local&amp;utm_campaign=arq045_lgpd_bh_20261020">Definir o escopo</a></p></section>'''}]
STYLE='<style id="arquindex-aeo-20261020-noite">.aq-aeo-answer{max-width:1120px;margin:36px auto;padding:28px;border:1px solid #d9e2ef;border-radius:16px;background:#fff;color:#0c1b33;box-sizing:border-box}.aq-aeo-answer h2{color:#0b3d91}.aq-aeo-answer table{width:100%;border-collapse:collapse;margin:18px 0}.aq-aeo-answer th,.aq-aeo-answer td{padding:12px;border:1px solid #d9e2ef;text-align:left;vertical-align:top}.aq-aeo-answer th{background:#eaf0f8}@media(max-width:760px){.aq-aeo-answer{margin:24px 16px;padding:20px}.aq-aeo-answer table{display:block;overflow-x:auto}.aq-aeo-answer th,.aq-aeo-answer td{min-width:145px}}</style>'
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
 with urllib.request.urlopen(req,timeout=40) as r:return r.status,r.read(6000000)
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
 backup='/seo-backups/rodada-20261020-noite-'+STAMP;mkdir(f,backup);f.storbinary('STOR '+backup+'/.htaccess',io.BytesIO(b'Options -Indexes\nRequire all denied\n'))
 for t,p,o,u in rec:
  bp=backup+'/'+t['id'].lower()+'.html';f.storbinary('STOR '+bp,io.BytesIO(o));assert get(f,bp)==o;print('BACKUP_VERIFIED',t['id'],bp,hashlib.sha256(o).hexdigest(),flush=True)
 written=[]
 try:
  for t,p,o,u in rec:assert get(f,p)==o,'CONCURRENT_CHANGE '+t['id']
  for t,p,o,u in rec:put(f,p,u,STAMP);written.append((p,o));print('FTP_PUBLISHED_VERIFIED',t['id'],hashlib.sha256(u).hexdigest(),flush=True)
  for t,p,o,u in rec:
   st,body=public(t['url']);assert st==200 and t['id'].encode() in body and b'id="arq-floating"' in body and b'noindex' not in body.lower();print('PUBLIC_SOURCE_VERIFIED',t['id'],t['url'],hashlib.sha256(body).hexdigest(),flush=True)
 except Exception:
  for p,o in reversed(written):put(f,p,o,'rollback-'+STAMP)
  print('ROLLBACK_COMPLETED',flush=True);raise
