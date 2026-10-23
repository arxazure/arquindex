import ftplib,hashlib,io,os,posixpath,time,urllib.request,xml.etree.ElementTree as ET
from datetime import datetime,timezone
from pathlib import Path
from bs4 import BeautifulSoup
from PIL import Image,ImageDraw,ImageFont
STAMP=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ');TODAY='2026-10-23'
TARGETS=[
{'id':'ARQ-095','host':'digitalizar-ocr-empresas.arquindex.com.br','file':'index.html','url':'https://digitalizar-ocr-empresas.arquindex.com.br/','title':'OCR Corporativo: Teste, Revisão e Critérios de Aceite | Arquindex','h1':'OCR corporativo: como testar, revisar e aceitar a entrega','description':'Entenda quando o OCR torna documentos pesquisáveis, quais páginas exigem revisão e como testar busca, campos críticos e qualidade antes do aceite.','art':'ocr-corporativo-aceite-20261023.jpg','art_title':['OCR CORPORATIVO','Teste antes','de aceitar.'],'bullets':['Amostra representativa','Campos críticos revisados','Busca e entrega verificadas'],'section':'''<section class="aq-aeo-answer" data-aq-aeo="ARQ-095"><h2>Quando o OCR torna o documento pesquisável e quando precisa de revisão?</h2><p><strong>Resposta direta:</strong> o OCR cria uma camada de texto que permite localizar palavras em imagens digitalizadas, mas a qualidade depende do original, resolução, contraste, orientação, tipografia e idioma. Carimbos, manuscritos, páginas inclinadas, fundos ruidosos e documentos degradados devem entrar em uma amostra de teste e podem exigir revisão humana.</p><table><thead><tr><th>Teste</th><th>Como verificar</th><th>Critério de aceite</th></tr></thead><tbody><tr><td>Amostra</td><td>Inclua tipos, períodos e qualidades diferentes</td><td>Amostra representa o lote real</td></tr><tr><td>Pesquisa</td><td>Busque nomes, números e termos conhecidos</td><td>Resultados localizam os documentos esperados</td></tr><tr><td>Campos críticos</td><td>Compare OCR e imagem nos dados usados para indexar</td><td>Erros são registrados e corrigidos conforme o escopo</td></tr><tr><td>Imagem</td><td>Confira corte, orientação, ordem e legibilidade</td><td>Páginas completas e na sequência correta</td></tr><tr><td>Entrega</td><td>Abra os PDFs e teste busca, metadados e exportação</td><td>Arquivos e índice correspondem ao inventário</td></tr></tbody></table><p>Não existe precisão universal de OCR. O percentual aceitável, a revisão e o tratamento de exceções devem ser definidos no escopo a partir de uma amostra representativa.</p><p class="aq-review">Revisão editorial Arquindex: 23/10/2026. Referências: <a href="https://www.gov.br/conarq/pt-br">CONARQ</a> e <a href="https://www.arquindex.com.br/digitalizacao-com-ocr.html">guia de digitalização com OCR</a>.</p><p><a href="https://www.arquindex.com.br/digitalizacao.html">Digitalização de documentos</a> · <a href="https://www.arquindex.com.br/digitalizacao-com-ocr.html">OCR e PDF pesquisável</a> · <a href="https://www.arquindex.com.br/solicitar-proposta-contratacao.html?utm_source=site&amp;utm_medium=guia_ocr&amp;utm_campaign=arq095_ocr_aceite_20261023">Solicitar teste com amostra</a></p></section>'''},
{'id':'ARQ-096','host':'empresas-digitalizacao-documentos-regiao.arquindex.com.br','file':'como-escolher.html','url':'https://empresas-digitalizacao-documentos-regiao.arquindex.com.br/como-escolher.html','title':'Como Comparar Empresas de Digitalização | Arquindex','h1':'Como comparar empresas de digitalização de documentos','description':'Compare fornecedores de digitalização pelo inventário, amostra, captura, OCR, indexação, segurança, conferência, formato de entrega e custo total.','art':'comparar-empresas-digitalizacao-20261023.jpg','art_title':['DIGITALIZAÇÃO','Compare escopo,','não só preço.'],'bullets':['Inventário e amostra','Qualidade e segurança','Entrega e custo total'],'section':'''<section class="aq-aeo-answer" data-aq-aeo="ARQ-096"><h2>Como comparar empresas de digitalização de documentos?</h2><p><strong>Resposta direta:</strong> envie o mesmo inventário e a mesma amostra a todos os fornecedores. Compare preparação, captura, OCR, indexação, conferência, tratamento de exceções, segurança, logística, formato de entrega e custo total. Um preço por página sem unidade de medição e exclusões claras não permite comparação confiável.</p><table><thead><tr><th>Critério</th><th>Pergunta ao fornecedor</th><th>Evidência</th></tr></thead><tbody><tr><td>Inventário</td><td>Como volumes, formatos e estado físico serão medidos?</td><td>Planilha de escopo e exceções</td></tr><tr><td>Amostra</td><td>O teste usa documentos representativos?</td><td>Arquivos de teste e relatório</td></tr><tr><td>Qualidade</td><td>Como corte, orientação, ordem, OCR e campos serão conferidos?</td><td>Checklist e critérios de aceite</td></tr><tr><td>Segurança</td><td>Como coleta, acesso e movimentação serão registrados?</td><td>Protocolo e perfis de acesso</td></tr><tr><td>Entrega</td><td>Quais formatos, metadados e meios de exportação serão fornecidos?</td><td>Layout de índice e pacote final</td></tr><tr><td>Custo total</td><td>O que está incluído e o que gera cobrança adicional?</td><td>Preço, unidade, premissas e exclusões</td></tr></tbody></table><p>A escolha depende do acervo e do uso futuro. Validade jurídica, descarte e prazos de guarda exigem requisitos próprios; digitalizar não autoriza eliminar originais automaticamente.</p><p class="aq-review">Revisão editorial Arquindex: 23/10/2026. Referências: <a href="https://www.gov.br/conarq/pt-br">CONARQ</a> e <a href="https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2020/decreto/d10278.htm">Decreto 10.278/2020</a>.</p><p><a href="https://www.arquindex.com.br/digitalizacao.html">Serviço de digitalização</a> · <a href="https://www.arquindex.com.br/digitalizacao-certificada.html">Digitalização e requisitos legais</a> · <a href="https://www.arquindex.com.br/solicitar-proposta-contratacao.html?utm_source=site&amp;utm_medium=checklist_fornecedor&amp;utm_campaign=arq096_comparar_digitalizacao_20261023">Solicitar avaliação do acervo</a></p></section>'''},
{'id':'ARQ-098','host':'digitalizardocumentos.arquindex.com.br','file':'o-que-e.html','url':'https://digitalizardocumentos.arquindex.com.br/o-que-e.html','title':'Como Preparar Documentos para Digitalização | Arquindex','h1':'Como preparar documentos para digitalização e conferir a entrega','description':'Veja como inventariar, ordenar, higienizar, identificar exceções e definir captura, OCR, metadados e critérios de conferência antes da digitalização.','art':'preparar-documentos-digitalizacao-20261023.jpg','art_title':['PREPARAÇÃO','Organize antes','de digitalizar.'],'bullets':['Inventário e ordem','Exceções identificadas','Aceite documentado'],'section':'''<section class="aq-aeo-answer" data-aq-aeo="ARQ-098"><h2>Como preparar documentos para digitalização e conferir a entrega?</h2><p><strong>Resposta direta:</strong> comece por inventário e amostragem; defina a ordem documental, identifique grampos, dobras, rasgos, formatos especiais, páginas em branco e anexos; depois estabeleça resolução, cor, OCR, nomes, metadados, formato de saída e critérios de aceite. A preparação deve preservar contexto e sequência, não apenas acelerar o scanner.</p><table><thead><tr><th>Fase</th><th>Decisão</th><th>Controle</th></tr></thead><tbody><tr><td>Inventário</td><td>Volumes, tipos, períodos, suportes e estado</td><td>Planilha e amostra representativa</td></tr><tr><td>Preparação</td><td>Ordem, retirada de fixadores e tratamento de exceções</td><td>Regras por tipo documental</td></tr><tr><td>Captura</td><td>Resolução, cor, frente/verso e grandes formatos</td><td>Perfil aprovado no teste</td></tr><tr><td>Indexação</td><td>Nomes, campos, vocabulários e obrigatoriedade</td><td>Layout de metadados validado</td></tr><tr><td>Conferência</td><td>Legibilidade, completude, sequência, OCR e duplicidades</td><td>Checklist, amostra e registro de correções</td></tr><tr><td>Entrega</td><td>PDF/PDF-A/TIFF, estrutura de pastas e exportação</td><td>Inventário conciliado com arquivos</td></tr></tbody></table><p>O formato e o nível de revisão devem seguir a finalidade do acervo. A eliminação de originais depende de classificação, temporalidade, autorização e requisitos aplicáveis; não decorre apenas da criação de uma cópia digital.</p><p class="aq-review">Revisão editorial Arquindex: 23/10/2026. Referências: <a href="https://www.gov.br/conarq/pt-br">CONARQ</a> e <a href="https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2020/decreto/d10278.htm">Decreto 10.278/2020</a>.</p><p><a href="https://www.arquindex.com.br/digitalizacao.html">Digitalização de documentos</a> · <a href="https://www.arquindex.com.br/gestao_documental_documentos.html">Gestão documental</a> · <a href="https://www.arquindex.com.br/solicitar-proposta-contratacao.html?utm_source=site&amp;utm_medium=guia_preparacao&amp;utm_campaign=arq098_preparar_digitalizacao_20261023">Planejar a digitalização</a></p></section>'''}]
STYLE='<style id="arquindex-aeo-20261023-noite">.aq-aeo-answer{max-width:1120px;margin:36px auto;padding:28px;border:1px solid #d9e2ef;border-radius:16px;background:#fff;color:#0c1b33;box-sizing:border-box;overflow-wrap:anywhere}.aq-aeo-answer h2{color:#0b3d91}.aq-aeo-answer table{width:100%;border-collapse:collapse;margin:18px 0}.aq-aeo-answer th,.aq-aeo-answer td{padding:12px;border:1px solid #d9e2ef;text-align:left;vertical-align:top}.aq-aeo-answer th{background:#eaf0f8}.aq-review{font-size:.94rem;color:#42536b}@media(max-width:760px){.aq-aeo-answer{margin:24px 16px;padding:20px}.aq-aeo-answer table{display:block;overflow-x:auto}.aq-aeo-answer th,.aq-aeo-answer td{min-width:145px}}</style>'
WIDGET=Path('conteudo/publicacao/_atendimento-flutuante.html').read_text('utf-8')
def get(f,p): b=bytearray();f.retrbinary('RETR '+p,b.extend);return bytes(b)
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
 d,n=posixpath.dirname(p),posixpath.basename(p);tmp=d+'/.tmp-'+n+'-'+label
 f.storbinary('STOR '+tmp,io.BytesIO(b));assert get(f,tmp)==b
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
 s=BeautifulSoup(b.decode('utf-8','ignore'),'html.parser');assert s.head and s.body
 for old in s.select('[data-aq-aeo="'+t['id']+'"],#arquindex-aeo-20261023-noite'):old.decompose()
 if s.title:s.title.string=t['title']
 else:n=s.new_tag('title');n.string=t['title'];s.head.append(n)
 desc=s.find('meta',attrs={'name':lambda v:v and v.lower()=='description'})
 if not desc:desc=s.new_tag('meta',attrs={'name':'description'});s.head.append(desc)
 desc['content']=t['description']
 h1s=s.find_all('h1');assert h1s;h1s[0].clear();h1s[0].append(t['h1'])
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
 sec=BeautifulSoup(t['section'],'html.parser');footer=s.find('footer');footer.insert_before(sec) if footer else s.body.append(sec)
 out=str(s).encode();assert out.count(b'id="arq-floating"')==1 and t['id'].encode() in out and t['url'].encode() in out;return out
def public(url):
 req=urllib.request.Request(url+('&' if '?' in url else '?')+'verify='+STAMP,headers={'User-Agent':'ArquindexSEO/1.0','Cache-Control':'no-cache'})
 with urllib.request.urlopen(req,timeout=40) as r:return r.status,r.read(10000000)
def art_bytes(t):
 im=Image.new('RGB',(1200,1200),'#f4f7fc');d=ImageDraw.Draw(im)
 def tx(x,y,s,z=32,c='#0c1b33',bold=False):
  font='/usr/share/fonts/truetype/dejavu/DejaVuSans'+('-Bold' if bold else '')+'.ttf';d.text((x,y),s,font=ImageFont.truetype(font,z),fill=c)
 tx(70,70,'ARQUINDEX',48,'#0b3d91',True);tx(70,210,t['art_title'][0],30,'#0b3d91',True);tx(70,290,t['art_title'][1],52,'#0c1b33',True);tx(70,365,t['art_title'][2],52,'#0c1b33',True)
 for i,label in enumerate(t['bullets']):
  y=530+i*135;d.rounded_rectangle((70,y,1130,y+106),radius=18,fill='white',outline='#cbd7e9',width=2);tx(100,y+27,label,34)
 d.rectangle((0,1050,1200,1200),fill='#0b3d91');tx(70,1080,'Veja o guia completo',35,'white',True);tx(70,1133,t['host'],24,'white')
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
 backup='/seo-backups/rodada-20261023-noite-'+STAMP;mkdir(f,backup);f.storbinary('STOR '+backup+'/.htaccess',io.BytesIO(b'Options -Indexes\nRequire all denied\n'))
 for t,p,o,u in rec:
  bp=backup+'/'+t['id'].lower()+'.html';f.storbinary('STOR '+bp,io.BytesIO(o));assert get(f,bp)==o;print('BACKUP_VERIFIED',t['id'],bp,hashlib.sha256(o).hexdigest(),flush=True)
 written=[]
 try:
  for t,p,o,u in rec:assert get(f,p)==o,'CONCURRENT_CHANGE '+t['id']
  for t,p,o,u in rec:put(f,p,u,STAMP);written.append((p,o));print('FTP_PUBLISHED_VERIFIED',t['id'],hashlib.sha256(u).hexdigest(),flush=True)
  time.sleep(2)
  for t,p,o,u in rec:
   st,body=public(t['url']);assert st==200 and t['id'].encode() in body and t['title'].encode() in body and t['url'].encode() in body and b'noindex' not in body.lower()
   print('PUBLIC_SOURCE_VERIFIED',t['id'],t['url'],hashlib.sha256(body).hexdigest(),flush=True)
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
  folder=base+'/assets/social-arq095-100';mkdir(f,folder)
  for t,p,o,u in rec:
   art=art_bytes(t);ap=folder+'/'+t['art'];f.storbinary('STOR '+ap,io.BytesIO(art));assert get(f,ap)==art
   photo='https://www.arquindex.com.br/assets/social-arq095-100/'+t['art'];st,b=public(photo);assert st==200 and hashlib.sha256(b).digest()==hashlib.sha256(art).digest();print('IMAGE_PUBLIC_VERIFIED',t['id'],photo,hashlib.sha256(art).hexdigest(),flush=True)
 except Exception:
  for p,o in reversed(written):put(f,p,o,'rollback-'+STAMP)
  print('ROLLBACK_COMPLETED',flush=True);raise
