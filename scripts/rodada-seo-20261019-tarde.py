import ftplib,io,os,posixpath,hashlib,json,time,urllib.request
from datetime import datetime,timezone
from bs4 import BeautifulSoup
STAMP=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
TARGETS=[
  dict(id='ARQ-016',host='cedoc-compras-maua.arquindex.com.br',file='custo.html',slug='ocr-para-documentos-corporativos-na-pratica',article='OCR para documentos corporativos na prática',section='''<section class="aq-aeo-answer" data-aq-aeo="ARQ-016"><h2>Quando o OCR torna o documento pesquisável e quando precisa de revisão?</h2><p><strong>Resposta direta:</strong> o OCR cria uma camada de texto pesquisável, mas a conferência continua necessária quando há carimbos, manuscritos, imagens degradadas, baixo contraste ou campos críticos. O aceite deve combinar teste de busca, amostragem visual e validação dos campos acordados.</p><table><thead><tr><th>Etapa</th><th>Critério de aceite</th></tr></thead><tbody><tr><td>Captura</td><td>Imagem legível, orientação correta e páginas completas</td></tr><tr><td>OCR</td><td>Pesquisa por termos da amostra e registro das exceções</td></tr><tr><td>Indexação</td><td>Campos críticos conferidos conforme regra do projeto</td></tr></tbody></table><p><a href="https://www.arquindex.com.br/digitalizacao-com-ocr.html">Conheça a digitalização com OCR</a> · <a href="https://www.arquindex.com.br/solicitar-proposta-contratacao.html?utm_source=site&amp;utm_medium=artigo&amp;utm_campaign=arq016_ocr_20261019">Solicite uma amostra técnica</a></p></section>'''),
  dict(id='ARQ-017',host='ia.arquindex.com.br',file='custo.html',slug='relatorio-de-impacto-o-que-e',article='Relatório de impacto: o que é e quando fazer',section='''<section class="aq-aeo-answer" data-aq-aeo="ARQ-017"><h2>O que uma consultoria LGPD entrega e como definir o escopo?</h2><p><strong>Resposta direta:</strong> o escopo começa pelo inventário dos tratamentos e pela avaliação de riscos. O RIPD documenta operações que possam gerar alto risco, as medidas de segurança e os mecanismos de mitigação; não substitui ROPA, políticas ou plano de ação.</p><table><thead><tr><th>Entregável</th><th>Pergunta que responde</th></tr></thead><tbody><tr><td>Inventário/ROPA</td><td>Quais dados são tratados, por quem e para qual finalidade?</td></tr><tr><td>RIPD</td><td>Quais riscos relevantes existem e como serão mitigados?</td></tr><tr><td>Plano de ação</td><td>Quem fará cada correção, com qual prioridade e evidência?</td></tr></tbody></table><p><a href="https://www.gov.br/anpd/pt-br/canais_atendimento/agente-de-tratamento/relatorio-de-impacto-a-protecao-de-dados-pessoais-ripd">Orientação oficial da ANPD sobre RIPD</a> · <a href="https://www.arquindex.com.br/lgpd-consultoria.html">Consultoria LGPD</a> · <a href="https://www.arquindex.com.br/solicitar-proposta-contratacao.html?utm_source=site&amp;utm_medium=artigo&amp;utm_campaign=arq017_ripd_20261019">Definir o escopo</a></p></section>'''),
  dict(id='ARQ-021',host='digitalizacao-documentos-beneficios.arquindex.com.br',file='passo-a-passo.html',slug='organizacao-de-arquivo-morto',article='Organização de arquivo morto sem risco',section='''<section class="aq-aeo-answer" data-aq-aeo="ARQ-021"><h2>Como localizar, solicitar e devolver documentos guardados?</h2><p><strong>Resposta direta:</strong> cada caixa e documento precisa de identificador, localização controlada e registro de movimentação. A solicitação deve gerar protocolo; retirada, consulta e devolução precisam manter responsável, data, motivo e posição final.</p><table><thead><tr><th>Movimento</th><th>Evidência mínima</th></tr></thead><tbody><tr><td>Entrada</td><td>Inventário, identificador da caixa e posição de guarda</td></tr><tr><td>Consulta</td><td>Solicitante, autorização, data e item movimentado</td></tr><tr><td>Devolução</td><td>Conferência, data e localização restabelecida</td></tr></tbody></table><p>Temporalidade e destinação devem seguir critérios documentados; “arquivo morto” não significa descarte automático.</p><p><a href="https://www.arquindex.com.br/guarda_de_documentos.html">Conheça a guarda documental</a> · <a href="https://www.arquindex.com.br/solicitar-proposta-contratacao.html?utm_source=site&amp;utm_medium=artigo&amp;utm_campaign=arq021_guarda_20261019">Solicite avaliação do acervo</a></p></section>''')
]
def get(f,p):
  b=bytearray();f.retrbinary('RETR '+p,b.extend);return bytes(b)
def put_atomic(f,p,data,label):
  d=posixpath.dirname(p);n=posixpath.basename(p);t=d+'/.tmp-'+n+'-'+label
  f.storbinary('STOR '+t,io.BytesIO(data));assert get(f,t)==data
  try:f.delete(p)
  except ftplib.error_perm as e:
    if not str(e).startswith('550'):raise
  f.rename(t,p);assert get(f,p)==data
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
    path,old=locate(f,base,t)
    text=old.decode('utf-8')
    marker='arquindex-aeo-'+t['id'].lower()+'-20261019'
    text=text.replace("var can=document.querySelector('link[rel=\\\"canonical\\\"]');if(can)can.href=c.canonical;","var cans=Array.from(document.querySelectorAll('link[rel=\\\"canonical\\\"]'));var can=cans.shift();if(can)can.href=c.canonical;cans.forEach(function(x){x.remove();});")
    if marker not in text:
      payload=json.dumps(dict(slug=t['slug'],article=t['article'],canonical='https://'+t['host']+'/'+t['file']+'?post='+t['slug'],section=t['section']),ensure_ascii=False)
      script=f'''<script id="{marker}">
(function(c){{
 function apply(){{
  if(new URLSearchParams(location.search).get("post")!==c.slug)return;
  var blog=document.getElementById("soro-blog");if(!blog)return;
  var article=Array.from(blog.querySelectorAll("h1")).find(function(h){{return h.textContent.trim()===c.article;}});
  if(!article)return;
  Array.from(document.querySelectorAll("h1")).forEach(function(h){{if(h===article||blog.contains(h))return;var p=document.createElement("p");p.className=(h.className?h.className+" ":"")+"aq-context-title";p.innerHTML=h.innerHTML;h.replaceWith(p);}});
  var cans=Array.from(document.querySelectorAll('link[rel="canonical"]'));var can=cans.shift();if(can)can.href=c.canonical;cans.forEach(function(x){{x.remove();}});
  if(!document.querySelector('[data-aq-aeo="{t['id']}"]'))article.closest("article,section,div").insertAdjacentHTML("beforeend",c.section);
 }}
 function start(){{apply();new MutationObserver(apply).observe(document.documentElement,{{childList:true,subtree:true}});}}
 if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",start,{{once:true}});else start();
}})({payload});
</script>'''
      i=text.lower().rindex('</body>');text=text[:i]+script+'\n'+text[i:]
    rec.append((t,path,old,text.encode('utf-8')))
  backup='/seo-backups/rodada-20261019-tarde-'+STAMP;mkdir(f,backup)
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
          code,body=public(url);s=BeautifulSoup(body,'html.parser')
          assert code==200 and ('arquindex-aeo-'+t['id'].lower()+'-20261019').encode() in body
          assert 'noindex' not in body.decode('utf-8','ignore').lower()
          print('PUBLIC_SOURCE_VERIFIED',t['id'],url,hashlib.sha256(body).hexdigest(),flush=True)
          last=None;break
        except Exception as e:
          last=e
          if attempt<2:time.sleep(5)
      if last:raise last
  except Exception:
    for path,old in reversed(written):put_atomic(f,path,old,'rollback-'+STAMP)
    print('ROLLBACK_COMPLETED',flush=True);raise
