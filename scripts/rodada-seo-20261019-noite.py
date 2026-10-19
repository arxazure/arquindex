import ftplib,io,os,posixpath,hashlib,json,time,urllib.request
from datetime import datetime,timezone
STAMP=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
TARGETS=[
 dict(id='ARQ-022',host='digitalizar-arquivos-corporativo.arquindex.com.br',file='custo.html',slug='sharepoint-ou-alfresco',article='SharePoint ou Alfresco? Qual faz mais sentido',section='''<section class="aq-aeo-answer" data-aq-aeo="ARQ-022"><h2>Como dimensionar e validar uma implantação Alfresco?</h2><p><strong>Resposta direta:</strong> dimensione pelo volume atual e crescimento, usuários simultâneos, formatos, integrações, metadados, permissões e requisitos de recuperação. Antes da migração integral, valide um piloto com documentos reais anonimizados, busca, perfis de acesso, restauração e critérios de aceite.</p><table><thead><tr><th>Frente</th><th>Evidência do piloto</th></tr></thead><tbody><tr><td>Capacidade</td><td>Volume inicial, crescimento, usuários e janela de processamento</td></tr><tr><td>Governança</td><td>Metadados, perfis, versionamento, retenção e trilha de auditoria</td></tr><tr><td>Recuperação</td><td>Backup executado, restauração testada e tempo registrado</td></tr></tbody></table><p>Defina a versão e a arquitetura somente após conferir a documentação compatível com o ambiente planejado.</p><p><a href="https://docs.alfresco.com/content-services/latest/">Documentação oficial do Alfresco Content Services</a> · <a href="https://www.arquindex.com.br/alfresco-belo-horizonte.html">Implantação Alfresco e ECM</a> · <a href="https://www.arquindex.com.br/solicitar-proposta-contratacao.html?utm_source=site&amp;utm_medium=artigo&amp;utm_campaign=arq022_alfresco_20261019">Solicitar diagnóstico técnico</a></p></section>'''),
 dict(id='ARQ-024',host='ecm.arquindex.com.br',file='custo.html',slug='mapeamento-de-repositorios-de-dados-lgpd',article='Mapeamento de repositórios de dados LGPD',section='''<section class="aq-aeo-answer" data-aq-aeo="ARQ-024"><h2>Como mapear repositórios de dados para um projeto LGPD?</h2><p><strong>Resposta direta:</strong> comece pelos processos de negócio e registre onde os dados pessoais entram, ficam armazenados, circulam, são compartilhados e descartados. O inventário precisa relacionar finalidade, base legal, responsáveis, acessos, retenção e riscos; uma lista isolada de servidores ou sistemas não descreve o tratamento.</p><table><thead><tr><th>Campo</th><th>Pergunta de validação</th></tr></thead><tbody><tr><td>Processo e finalidade</td><td>Por que o dado é tratado e qual atividade depende dele?</td></tr><tr><td>Repositório e acesso</td><td>Onde está, quem acessa e quais terceiros participam?</td></tr><tr><td>Retenção e descarte</td><td>Por quanto tempo permanece e qual evidência encerra o ciclo?</td></tr></tbody></table><p>O artigo 37 da LGPD exige que controlador e operador mantenham registro das operações de tratamento, especialmente quando baseado em legítimo interesse.</p><p><a href="https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm#art37">LGPD — registro das operações</a> · <a href="https://www.arquindex.com.br/lgpd-consultoria.html">Consultoria de adequação LGPD</a> · <a href="https://www.arquindex.com.br/solicitar-proposta-contratacao.html?utm_source=site&amp;utm_medium=artigo&amp;utm_campaign=arq024_mapeamento_20261019">Definir o escopo</a></p></section>'''),
 dict(id='ARQ-025',host='empresas-adequacao-lgpd-paulo.arquindex.com.br',file='diagnostico.html',slug='como-digitalizar-prontuarios-medicos',article='Como digitalizar prontuários médicos com segurança',section='''<section class="aq-aeo-answer" data-aq-aeo="ARQ-025"><h2>Como preparar prontuários médicos para digitalização e conferir a entrega?</h2><p><strong>Resposta direta:</strong> inventarie o lote, preserve a ordem documental, restrinja o acesso, defina resolução, formato, indexação e amostragem de qualidade antes da captura. A entrega deve comprovar completude, legibilidade, vínculo correto ao paciente, controle de acesso e tratamento das exceções.</p><table><thead><tr><th>Etapa</th><th>Controle mínimo</th></tr></thead><tbody><tr><td>Preparação</td><td>Inventário, ordem, retirada de grampos e registro de documentos sensíveis</td></tr><tr><td>Captura</td><td>Imagem completa, orientação correta, legibilidade e identificação</td></tr><tr><td>Conferência</td><td>Amostra documentada, exceções corrigidas e aceite do responsável</td></tr><tr><td>Entrega</td><td>Formato acordado, índice validado, acesso restrito e cópia de segurança</td></tr></tbody></table><p>A Lei nº 13.787/2018 trata especificamente da digitalização e guarda informatizada de prontuários. O descarte do papel não deve ser presumido: depende dos requisitos legais, arquivísticos e profissionais aplicáveis.</p><p><a href="https://www.gov.br/conarq/pt-br/legislacao-arquivistica/leis-e-decretos-leis/lei-no13-787-de-27-de-dezembro-de-2018">Lei nº 13.787/2018</a> · <a href="https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2020/decreto/d10278.htm">Decreto nº 10.278/2020</a> · <a href="https://www.arquindex.com.br/digitalizacao.html">Digitalização de documentos</a> · <a href="https://www.arquindex.com.br/solicitar-proposta-contratacao.html?utm_source=site&amp;utm_medium=artigo&amp;utm_campaign=arq025_prontuarios_20261019">Solicitar avaliação do acervo</a></p></section>''')
]
def get(f,p):
 b=bytearray();f.retrbinary('RETR '+p,b.extend);return bytes(b)
def put_atomic(f,p,data,label):
 d=posixpath.dirname(p);n=posixpath.basename(p);tmp=d+'/.tmp-'+n+'-'+label
 f.storbinary('STOR '+tmp,io.BytesIO(data));assert get(f,tmp)==data
 try:f.delete(p)
 except ftplib.error_perm as e:
  if not str(e).startswith('550'):raise
 f.rename(tmp,p);assert get(f,p)==data
def mkdir(f,p):
 cur=f.pwd()
 try:
  f.cwd('/')
  for part in p.strip('/').split('/'):
   if not part:continue
   try:f.mkd(part)
   except ftplib.error_perm as e:
    if not str(e).startswith('550'):raise
   f.cwd(part)
 finally:f.cwd(cur)
def locate(f,base,t):
 for root in [base+'/subdominios/'+t['host'],base+'/'+t['host'],'/subdominios/'+t['host'],'/'+t['host']]:
  p=root+'/'+t['file']
  try:
   b=get(f,p)
   if b'<html' in b.lower():return p,b
  except ftplib.all_errors:pass
 raise RuntimeError('TARGET_NOT_FOUND '+t['id'])
def public(url):
 sep='&' if '?' in url else '?'
 req=urllib.request.Request(url+sep+'verify='+STAMP,headers={'User-Agent':'ArquindexSEO/1.0','Cache-Control':'no-cache'})
 with urllib.request.urlopen(req,timeout=40) as r:return r.status,r.read(6000000)
with ftplib.FTP_TLS(timeout=60) as f:
 f.connect('ftp.arquindex.com.br',21);f.login('arquind2',os.environ['FTP_PASSWORD']);f.prot_p();f.set_pasv(True)
 base=None
 for cand in ['/public_html','/home/arquind2/public_html']:
  try:
   if b'arquindex' in get(f,cand+'/index.html').lower():base=cand;break
  except ftplib.all_errors:pass
 assert base,'PUBLIC_ROOT_NOT_FOUND'
 rec=[]
 for t in TARGETS:
  path,old=locate(f,base,t);text=old.decode('utf-8')
  marker='arquindex-aeo-'+t['id'].lower()+'-20261019'
  assert marker not in text,'ALREADY_UPDATED '+t['id']
  payload=json.dumps(dict(slug=t['slug'],article=t['article'],canonical='https://'+t['host']+'/'+t['file']+'?post='+t['slug'],section=t['section']),ensure_ascii=False)
  js=f'''<script id="{marker}">
(function(c){{
 function apply(){{
  if(new URLSearchParams(location.search).get("post")!==c.slug)return;
  var blog=document.getElementById("soro-blog");if(!blog)return;
  var article=Array.from(blog.querySelectorAll("h1")).find(function(h){{return h.textContent.trim()===c.article;}});
  if(!article)return;
  Array.from(document.querySelectorAll("h1")).forEach(function(h){{if(h===article||blog.contains(h))return;var p=document.createElement("p");p.className=(h.className?h.className+" ":"")+"aq-context-title";p.innerHTML=h.innerHTML;h.replaceWith(p);}});
  var cans=Array.from(document.querySelectorAll('link[rel="canonical"]'));var can=cans.shift();if(!can){{can=document.createElement("link");can.rel="canonical";document.head.appendChild(can);}}can.href=c.canonical;cans.forEach(function(x){{x.remove();}});
  if(!document.querySelector('[data-aq-aeo="{t['id']}"]'))article.closest("article,section,div").insertAdjacentHTML("beforeend",c.section);
 }}
 function start(){{apply();new MutationObserver(apply).observe(document.documentElement,{{childList:true,subtree:true}});}}
 if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",start,{{once:true}});else start();
}})({payload});
</script>'''
  i=text.lower().rindex('</body>');new=(text[:i]+js+'\n'+text[i:]).encode('utf-8')
  rec.append((t,path,old,new))
 backup='/seo-backups/rodada-20261019-noite-'+STAMP;mkdir(f,backup)
 f.storbinary('STOR '+backup+'/.htaccess',io.BytesIO(b'Options -Indexes\nRequire all denied\n'))
 for t,path,old,new in rec:
  bp=backup+'/'+t['id'].lower()+'-'+hashlib.sha256(path.encode()).hexdigest()[:12]+'.html'
  f.storbinary('STOR '+bp,io.BytesIO(old));assert get(f,bp)==old
  print('BACKUP_VERIFIED',t['id'],bp,hashlib.sha256(old).hexdigest(),flush=True)
 written=[]
 try:
  for t,path,old,new in rec:assert get(f,path)==old,'CONCURRENT_CHANGE '+t['id']
  for t,path,old,new in rec:
   put_atomic(f,path,new,STAMP);written.append((path,old))
   print('FTP_PUBLISHED_VERIFIED',t['id'],hashlib.sha256(new).hexdigest(),flush=True)
  for t,path,old,new in rec:
   url='https://'+t['host']+'/'+t['file']+'?post='+t['slug'];last=None
   for attempt in range(3):
    try:
     code,body=public(url)
     assert code==200 and ('arquindex-aeo-'+t['id'].lower()+'-20261019').encode() in body
     assert b'id="arq-floating"' in body and b'arquindex-logo-oficial.webp' in body
     assert b'noindex' not in body.lower()
     print('PUBLIC_SOURCE_VERIFIED',t['id'],url,hashlib.sha256(body).hexdigest(),flush=True)
     last=None;break
    except Exception as e:
     last=e
     if attempt<2:time.sleep(5)
   if last:raise last
 except Exception:
  for path,old in reversed(written):put_atomic(f,path,old,'rollback-'+STAMP)
  print('ROLLBACK_COMPLETED',flush=True);raise
