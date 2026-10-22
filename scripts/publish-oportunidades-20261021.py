"""Publish scoped campaign assets and useful pages through verified HomeHost FTPS."""
import ftplib,io,json,os,re,ssl,socket,hashlib,time
from pathlib import Path
from datetime import datetime,timezone
from urllib.request import Request,urlopen
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'campanhas/oportunidades-20261021'
BASE='https://www.arquindex.com.br/'
MARKER='ARQ-OPORTUNIDADES-20261021'
manifest=json.loads((SOURCE/'manifest.json').read_text())
planned={s['target']:(ROOT/s['source']).read_bytes() for s in manifest}
for name in ['guarda','ocr','alfresco','databooks']:
 p=SOURCE/'campanha-oportunidades-20261021'/f'{name}.jpg'
 assert p.stat().st_size>10000
 planned['/public_html/campanha-oportunidades-20261021/'+p.name]=p.read_bytes()
for s in manifest:
 text=(ROOT/s['source']).read_text()
 assert text.count('<h1>')==1 and MARKER in text
 assert 'rel="canonical" href="'+s['url']+'"' in text
 assert 'name="robots" content="index,follow"' in text
 for value in re.findall(r'<script type="application/ld\+json">(.*?)</script>',text,re.S):json.loads(value)
if '--check' in __import__('sys').argv:print('LOCAL_CHECK_OK',len(planned));raise SystemExit

def get(f,p):
 b=bytearray()
 try:f.retrbinary('RETR '+p,b.extend)
 except ftplib.error_perm as e:
  if str(e).startswith('550'):return None
  raise
 return bytes(b)
def mkdir(f,path):
 current=''
 for part in path.strip('/').split('/'):
  current+='/'+part
  try:f.cwd(current)
  except ftplib.error_perm as e:
   if not str(e).startswith('550'):raise
   f.mkd(current)
def put(f,p,data):
 mkdir(f,p.rsplit('/',1)[0]);f.storbinary('STOR '+p,io.BytesIO(data));assert get(f,p)==data
def http(url):
 with urlopen(Request(url,headers={'User-Agent':'ArquindexCampaign/2026.10','Cache-Control':'no-cache'}),timeout=35) as r:
  return r.status,r.url,r.headers,r.read()
def sha(b):return hashlib.sha256(b).hexdigest()

style='style="max-width:1100px;margin:32px auto;padding:clamp(18px,4vw,36px);background:#eff6fc;color:#142d43;box-sizing:border-box;font:18px/1.7 system-ui,sans-serif;border-radius:12px;clear:both"'
shared='<p><a href="/blog/alfresco-cloud-ocr-inteligencia-documental/">Como integrar Alfresco, OCR e metadados</a> · <a href="/blog/tco-alfresco-cloud-versus-saas/">Compare o custo total de GED</a></p><p><a href="https://wa.me/5531973632725">Solicitar avaliação: (31) 97363-2725</a></p>'
blocks={
 '/public_html/guarda_de_documentos.html':f'''<section id="arquindex-guarda-controle-20261021" {style}><!-- {MARKER} --><h2>Como comparar propostas de guarda documental</h2><img src="/campanha-oportunidades-20261021/guarda.jpg" width="1122" height="1402" alt="Guarda documental: classificação, localização e rastreabilidade" style="width:100%;max-width:320px;height:auto;display:block;margin:20px auto"><p>Uma proposta deve esclarecer como os documentos serão identificados, localizados, consultados e devolvidos. Compare o custo do serviço completo: preparação do acervo, transporte, inventário, armazenamento, consultas, digitalização sob demanda e encerramento contratual.</p><h3>Informações para dimensionar seu acervo</h3><ul><li>Quantidade, dimensões e condição das caixas; tipos de documentos e intervalo de datas.</li><li>Unidades envolvidas, localização da retirada e necessidade de preparação ou reembalagem.</li><li>Frequência de consultas, pessoas autorizadas e forma de entrega: caixa, documento ou cópia digital.</li><li>Regras de movimentação, responsabilidade por aprovação e registro da devolução.</li><li>Critérios para retenção e destinação, incluindo impedimentos de descarte e autorização formal.</li></ul><h3>O que conferir antes da primeira coleta</h3><p>Valide uma relação de volumes e identificadores, registre o responsável pela entrega e defina como serão tratadas divergências. O inventário deve permitir reconciliar o que saiu da empresa com o que foi recebido e armazenado. Para cada solicitação posterior, registre quem pediu, qual documento foi movimentado e quando ele retornou.</p><h3>Guarda física substitui a gestão dos prazos?</h3><p>Não. Prazos de retenção dependem da classificação, do contexto e das obrigações aplicáveis. A eliminação precisa de análise e autorização; o vencimento de uma data não deve causar descarte automático. Atendimento, coleta, prazos de consulta e condições comerciais são confirmados em proposta.</p>{shared}</section>''',
 '/public_html/digitalizacao-com-ocr.html':f'''<section id="arquindex-ocr-controle-20261021" {style}><!-- {MARKER} --><h2>Como conferir o OCR antes de aceitar um lote</h2><img src="/campanha-oportunidades-20261021/ocr.jpg" width="1122" height="1402" alt="OCR e indexação: nomes, datas e tipos documentais" style="width:100%;max-width:320px;height:auto;display:block;margin:20px auto"><p>PDF pesquisável e extração de campos são entregas diferentes. O primeiro permite buscar palavras na camada de texto; a segunda organiza valores em campos definidos para uso em índices, planilhas ou sistemas. Um teste deve confirmar separadamente essas duas necessidades.</p><h3>Defina a amostra e os campos críticos</h3><p>Inclua páginas de formatos, épocas e estados de conservação diferentes. Teste termos conhecidos e confira nomes, datas, identificadores e valores. Combine a unidade de medição, a tolerância de erro e quem decide se o lote foi aceito. Não há taxa universal de acerto para qualquer acervo.</p><h3>Separe as causas do retrabalho</h3><ul><li><strong>Imagem inclinada ou com fundo irregular:</strong> avaliar tratamento em uma cópia e comparar com a imagem preservada.</li><li><strong>Borda cortada ou conteúdo ausente:</strong> verificar o original e considerar nova captura; o OCR não recupera informação que não foi digitalizada.</li><li><strong>Campo reconhecido incorretamente:</strong> conferir no original e registrar correção, arquivo, página e responsável.</li><li><strong>Tabela sem estrutura:</strong> validar o vínculo entre linha, coluna e valor; reconhecer caracteres não reconstrói automaticamente o significado da tabela.</li></ul><p>A documentação oficial do <a href="https://tesseract-ocr.github.io/tessdoc/ImproveQuality.html" rel="noopener">Tesseract sobre qualidade da imagem</a>, consultada em 21/10/2026, descreve limitações de ruído, inclinação, bordas e tabelas. É referência técnica; o projeto da Arquindex deve definir as ferramentas efetivamente usadas.</p><h3>Registro de exceções e aceite</h3><p>Para cada exceção, mantenha o identificador do lote, arquivo e página, tipo de falha, ação aplicada, resultado e responsável pela conferência. Preserve a ordem e o conjunto dos documentos. Antes de ampliar o processamento, valide com a equipe se o arquivo pode ser encontrado e usado na rotina.</p>{shared}</section>'''
}
report={'published':False,'pages':[],'assets':[]};previous={};applied=[]
out=ROOT/'publish-report';out.mkdir(exist_ok=True)
ips=set(socket.gethostbyname_ex('ftp.arquindex.com.br')[2]);assert ips & set(socket.gethostbyname_ex('h59.servidorhh.com')[2])
with ftplib.FTP_TLS(context=ssl.create_default_context(),timeout=55) as f:
 f.connect('h59.servidorhh.com',21);assert f.sock.getpeername()[0] in ips
 f.login('arquind2',os.environ['FTP_PASSWORD']);f.prot_p();f.set_pasv(True)
 home=get(f,'/public_html/index.html');assert home and b'arquindex' in home.lower()
 for s in manifest:
  old=get(f,s['target']);assert old is None or MARKER.encode() in old,('EXISTING_URL_REQUIRES_REVIEW',s['url'])
 for target,block in blocks.items():
  old=get(f,target);assert old and b'<html' in old.lower(),('MISSING_EXISTING_PAGE',target)
  text=old.decode('utf-8-sig');assert not re.search(r'name=["\']robots["\'][^>]+noindex',text,re.I)
  if MARKER not in text:
   closing='</main>' if '</main>' in text else '</body>'
   assert closing in text;planned[target]=text.replace(closing,block+closing,1).encode()
  else:planned[target]=old
 sitemap_path='/public_html/sitemap.xml';raw=get(f,sitemap_path);assert raw
 ns='http://www.sitemaps.org/schemas/sitemap/0.9';ET.register_namespace('',ns)
 tree=ET.fromstring(raw);child=ET.Element('{'+ns+'}urlset')
 for url in [s['url'] for s in manifest]+[BASE+p.removeprefix('/public_html/') for p in blocks]:
  u=ET.SubElement(child,'{'+ns+'}url');ET.SubElement(u,'{'+ns+'}loc').text=url;ET.SubElement(u,'{'+ns+'}lastmod').text='2026-10-21'
 childname='sitemap-oportunidades-20261021.xml';planned['/public_html/'+childname]=ET.tostring(child,encoding='utf-8',xml_declaration=True)
 locs={n.text for n in tree.iter('{'+ns+'}loc')}
 if tree.tag=='{'+ns+'}sitemapindex':
  if BASE+childname not in locs:
   n=ET.SubElement(tree,'{'+ns+'}sitemap');ET.SubElement(n,'{'+ns+'}loc').text=BASE+childname
 elif tree.tag=='{'+ns+'}urlset':
  for s in manifest:
   if s['url'] not in locs:
    n=ET.SubElement(tree,'{'+ns+'}url');ET.SubElement(n,'{'+ns+'}loc').text=s['url'];ET.SubElement(n,'{'+ns+'}lastmod').text='2026-10-21'
 else:raise RuntimeError('Unexpected sitemap root')
 planned[sitemap_path]=ET.tostring(tree,encoding='utf-8',xml_declaration=True)
 backup='/seo-backups/oportunidades-'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ');mkdir(f,backup)
 put(f,backup+'/.htaccess',b'Require all denied\n')
 for target in planned:
  old=get(f,target);previous[target]=old
  if old is not None:put(f,backup+'/'+sha(target.encode())+'.bak',old)
 put(f,backup+'/manifest.json',json.dumps({p:{'backup':sha(p.encode())+'.bak','sha256':sha(v)} for p,v in previous.items() if v is not None},indent=2).encode())
 report['backup']=backup
 try:
  for target,content in planned.items():
   if previous[target]==content:continue
   assert get(f,target)==previous[target],('CONCURRENT_CHANGE',target)
   applied.append(target);put(f,target,content)
  for target,content in planned.items():
   url=BASE+target.removeprefix('/public_html/')
   if url.endswith('/index.html'):url=url[:-10]
   last=None
   for attempt in range(4):
    try:
     status,final,headers,data=http(url);assert status==200 and data==content,('PUBLIC_MISMATCH',url,status)
     assert 'noindex' not in headers.get('X-Robots-Tag','').lower()
     last=(status,final);break
    except Exception:
     if attempt==3:raise
     time.sleep(4)
   row={'url':url,'http':last[0],'sha256':sha(content)}
   report['assets' if target.endswith('.jpg') else 'pages'].append(row)
   print('PUBLIC_VERIFIED',url,sha(content),flush=True)
  assert get(f,'/public_html/index.html')==home,'UNEXPECTED_HOMEPAGE_CHANGE'
  report['published']=True
 except Exception:
  for target in reversed(applied):
   if get(f,target)!=planned[target]:continue
   if previous[target] is None:f.delete(target)
   else:put(f,target,previous[target])
  report['rolled_back']=applied
  raise
 finally:
  (out/'oportunidades-20261021.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
  print(json.dumps(report,ensure_ascii=False),flush=True)
