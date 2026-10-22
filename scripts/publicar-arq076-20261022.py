import ast,ftplib,hashlib,io,os,posixpath,urllib.request,time
from pathlib import Path
from datetime import datetime,timezone
from bs4 import BeautifulSoup
from PIL import Image,ImageDraw,ImageFont
HOST="instalaralfresco.arquindex.com.br";URL="https://"+HOST+"/";STAMP=datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
TITLE="Implantação Alfresco: Aceite e Recuperação | Arquindex"
ARTICLE="<main class=\"wrap\"><p>Alfresco · Implantação e sustentação</p><h1>Como validar a recuperação de uma implantação Alfresco</h1><p>Antes do aceite, execute um teste em ambiente separado e registre se os documentos, versões, metadados, permissões e consultas necessárias foram recuperados conforme os critérios acordados. O plano deve identificar a versão, os componentes, os responsáveis e as limitações do ambiente.</p><h2>O que deve entrar no escopo</h2><p>Uma cópia de segurança precisa ser acompanhada de um procedimento de recuperação e de evidências do teste. A edição do Alfresco, as extensões, o banco de dados, o armazenamento e o mecanismo de busca devem ser identificados antes da definição técnica. Os procedimentos variam entre versões e arquiteturas.</p><p>A Arquindex avalia implantação e sustentação de GED e ECM Alfresco conforme diagnóstico. Informe versão, volume do acervo, usuários, integrações e principal dificuldade para preparar a proposta. O formato de atendimento e as responsabilidades são definidos no escopo.</p><h2>Roteiro de aceite da recuperação</h2><table><thead><tr><th>Objeto</th><th>O que conferir no teste</th><th>Evidência esperada</th></tr></thead><tbody><tr><td>Documentos</td><td>Abrir uma amostra representativa e comparar com a referência</td><td>Lista de documentos conferidos e divergências</td></tr><tr><td>Versões e metadados</td><td>Recuperar histórico e propriedades necessários ao processo</td><td>Registro dos critérios atendidos e pendências</td></tr><tr><td>Permissões</td><td>Testar perfis autorizados e restritos</td><td>Matriz de acesso validada</td></tr><tr><td>Pesquisa</td><td>Localizar os documentos pelos cenários acordados</td><td>Consultas e resultados registrados</td></tr><tr><td>Operação</td><td>Medir o tempo observado e identificar responsáveis</td><td>Relatório do ensaio e plano de correção</td></tr></tbody></table><h2>Como organizar o ensaio</h2><ol><li>Defina os objetivos e critérios de aceite com os responsáveis pelo negócio e pela infraestrutura.</li><li>Identifique componentes, configurações e dependências da versão instalada.</li><li>Prepare ambiente de teste autorizado e separado da produção.</li><li>Execute o procedimento aprovado para aquela arquitetura.</li><li>Confira a amostra, os perfis de acesso e as consultas necessárias.</li><li>Registre resultados, tempo observado, falhas e responsáveis pelas correções.</li></ol><p>Não use documentos confidenciais em demonstrações públicas. O teste deve respeitar as autorizações e os controles do cliente. Metas de tempo e perda aceitável de dados precisam ser acordadas antes do ensaio; esta página não estabelece prazos universais.</p><h2>Como solicitar uma proposta</h2><p>Informe edição e versão, tamanho atual e crescimento do acervo, usuários simultâneos, extensões, integrações, infraestrutura, rotina de cópias e último teste de recuperação. Se esses dados ainda não estiverem disponíveis, o diagnóstico pode começar por esse levantamento.</p><p>O orçamento deve esclarecer quem fornece infraestrutura, quem executa a rotina, quem valida o resultado, quais evidências serão entregues e como as pendências serão tratadas. O aceite é uma decisão documentada das partes, conforme o contrato.</p><h2>Perguntas frequentes</h2><h3>Ter backup comprova que o ambiente pode ser recuperado?</h3><p>A comprovação exige um teste documentado, com critérios e amostra definidos. A existência da cópia, isoladamente, não demonstra que os cenários de uso foram recuperados.</p><h3>Este roteiro serve para qualquer versão?</h3><p>Os critérios de negócio podem orientar o planejamento. O procedimento técnico deve seguir a documentação e as dependências da edição e versão efetivamente utilizadas.</p><h3>É necessário testar permissões?</h3><p>Sim. A recuperação deve preservar o acesso necessário e as restrições acordadas, verificadas com perfis representativos.</p><h2>Referência e serviços relacionados</h2><p>A documentação oficial <a href=\"https://docs.hyland.com/r/Alfresco/Alfresco-Content-Services-Community-Edition/23.2/Alfresco-Content-Services-Community-Edition\">Alfresco Community 23.2</a> lista tópicos de backup e restauração. Essa documentação está arquivada, com publicação em 06/05/2026; sua aplicação depende de compatibilidade. O roteiro de aceite desta página é uma orientação editorial e não substitui o procedimento técnico da versão instalada.</p><p><a href=\"https://www.arquindex.com.br/alfresco-belo-horizonte.html\">Conheça o projeto de implantação Alfresco</a> · <a class=\"cta\" href=\"https://www.arquindex.com.br/solicitar-proposta-contratacao.html?utm_source=site&amp;utm_medium=pagina_servico&amp;utm_campaign=arq076_recuperacao_20261022\">Solicitar avaliação do ambiente</a></p><p>Conteúdo institucional Arquindex · Atualizado em 22/10/2026.</p></main>"
def get(f,p):
 b=bytearray();f.retrbinary("RETR "+p,b.extend);return bytes(b)
def mkdir(f,p):
 old=f.pwd()
 try:
  f.cwd("/")
  for x in p.strip("/").split("/"):
   try:f.mkd(x)
   except ftplib.error_perm as e:
    if not str(e).startswith("550"):raise
   f.cwd(x)
 finally:f.cwd(old)
def public(url):
 with urllib.request.urlopen(urllib.request.Request(url,headers={"Cache-Control":"no-cache","User-Agent":"ArquindexPublish/1.0"}),timeout=40) as r:return r.status,r.read()
constants={}
for n in ast.parse(Path("scripts/padronizar-identidade-arquindex.py").read_text()).body:
 if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id in ["HEADER","FOOTER","CSS","JS"]:
  constants[n.targets[0].id]=ast.literal_eval(n.value)
footer=BeautifulSoup(constants["FOOTER"],"html.parser")
for p in footer.find_all("p"):p.decompose()
widget=Path("conteudo/publicacao/_atendimento-flutuante.html").read_text()
doc=BeautifulSoup('<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="index,follow"></head><body data-aq-brand="20261022"></body></html>',"html.parser")
t=doc.new_tag("title");t.string=TITLE;doc.head.append(t)
doc.head.append(doc.new_tag("link",rel="canonical",href=URL))
doc.head.append(doc.new_tag("meta",attrs={"name":"description","content":"Veja quais evidências solicitar em um teste de recuperação do Alfresco: documentos, versões, metadados, permissões e critérios de aceite."}))
for href in ["https://www.arquindex.com.br/assets/arquindex-restored/bootstrap.css","https://www.arquindex.com.br/assets/arquindex-restored/theme.css?v=3739ea98ed"]:doc.head.append(doc.new_tag("link",rel="stylesheet",href=href))
s=doc.new_tag("style");s.string=constants["CSS"]+"main.wrap{max-width:1120px}main h1{font-size:38px;color:#0b3d91}table{border-collapse:collapse;width:100%}td,th{padding:14px;border:1px solid #d9e2ef}a{overflow-wrap:anywhere}@media(max-width:760px){main h1{font-size:30px}table{display:block;overflow-x:auto}td,th{min-width:160px}}";doc.head.append(s)
for part in [constants["HEADER"],ARTICLE,str(footer),widget]:doc.body.append(BeautifulSoup(part,"html.parser"))
js=doc.new_tag("script");js.string=constants["JS"];doc.body.append(js)
new=str(doc).encode();assert len(doc.find_all("h1"))==1
with ftplib.FTP_TLS(timeout=60) as f:
 f.connect("ftp.arquindex.com.br",21);f.login("arquind2",os.environ["FTP_PASSWORD"]);f.prot_p()
 base=None
 for c in ["/public_html","/home/arquind2/public_html"]:
  try:
   if b"arquindex" in get(f,c+"/index.html").lower():base=c;break
  except ftplib.all_errors:pass
 assert base
 path=None
 for root in [base+"/subdominios/"+HOST,base+"/"+HOST,"/subdominios/"+HOST,"/"+HOST]:
  try:
   old=get(f,root+"/index.html")
   if b"<html" in old.lower():path=root+"/index.html";break
  except ftplib.all_errors:pass
 assert path,"TARGET_NOT_FOUND"
 backup="/seo-backups/arq076-"+STAMP;mkdir(f,backup)
 f.storbinary("STOR "+backup+"/.htaccess",io.BytesIO(b"Require all denied\n"))
 f.storbinary("STOR "+backup+"/index.html",io.BytesIO(old));assert get(f,backup+"/index.html")==old
 print("BACKUP_VERIFIED",backup,hashlib.sha256(old).hexdigest(),flush=True)
 assert get(f,path)==old,"CONCURRENT_CHANGE"
 f.storbinary("STOR "+path,io.BytesIO(new));assert get(f,path)==new
 try:
  status,b=public(URL+"?verify="+STAMP);assert status==200 and TITLE.encode() in b
 except Exception:
  f.storbinary("STOR "+path,io.BytesIO(old));assert get(f,path)==old
  print("ROLLBACK_VERIFIED",flush=True);raise
 print("PAGE_PUBLIC_VERIFIED",URL,hashlib.sha256(new).hexdigest(),flush=True)
 # Refresh only this subdomain's sitemap and retain existing entries.
 sm=posixpath.dirname(path)+"/sitemap.xml"
 try:sitemap=get(f,sm)
 except ftplib.error_perm:sitemap=None
 import xml.etree.ElementTree as ET
 ns="http://www.sitemaps.org/schemas/sitemap/0.9";ET.register_namespace("",ns)
 root=ET.fromstring(sitemap) if sitemap else ET.Element("{"+ns+"}urlset")
 assert root.tag=="{"+ns+"}urlset"
 found=False
 for node in root:
  loc=node.find("{"+ns+"}loc")
  if loc is not None and loc.text==URL:
   found=True
   lm=node.find("{"+ns+"}lastmod")
   if lm is None:lm=ET.SubElement(node,"{"+ns+"}lastmod")
   lm.text="2026-10-22"
 if not found:
  n=ET.SubElement(root,"{"+ns+"}url");ET.SubElement(n,"{"+ns+"}loc").text=URL;ET.SubElement(n,"{"+ns+"}lastmod").text="2026-10-22"
 if sitemap:
  f.storbinary("STOR "+backup+"/sitemap.xml",io.BytesIO(sitemap));assert get(f,backup+"/sitemap.xml")==sitemap
 updated=ET.tostring(root,encoding="utf-8",xml_declaration=True)
 f.storbinary("STOR "+sm,io.BytesIO(updated));assert get(f,sm)==updated
 status,b=public("https://"+HOST+"/sitemap.xml?verify="+STAMP);assert status==200 and URL.encode() in b
 print("SITEMAP_PUBLIC_VERIFIED",flush=True)
 # Exact text-based promotional art.
 im=Image.new("RGB",(1200,1200),"#f4f7fc");d=ImageDraw.Draw(im)
 def tx(x,y,t,z=32,c="#0c1b33",bold=False):d.text((x,y),t,font=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans"+("-Bold" if bold else "")+".ttf",z),fill=c)
 logo=Image.open(io.BytesIO(get(f,base+"/assets/arquindex-restored/arquindex-logo-oficial.webp"))).convert("RGBA");logo.thumbnail((410,140));im.paste(logo,(70,30),logo)
 tx(70,230,"ALFRESCO GED / ECM",30,bold=True);tx(70,300,"Recuperação testada.",54,bold=True);tx(70,380,"Aceite documentado.",54,bold=True)
 for i,label in enumerate(["Documentos e versões","Metadados e permissões","Consultas e evidências"]):
  y=520+i*135;d.rounded_rectangle((70,y,1130,y+106),radius=18,fill="white",outline="#cbd7e9",width=2);tx(100,y+27,label,36)
 d.rectangle((0,1050,1200,1200),fill="#0b3d91");tx(70,1080,"Veja o roteiro completo",35,"white",True);tx(70,1133,"instalaralfresco.arquindex.com.br",29,"white")
 b=io.BytesIO();im.save(b,"JPEG",quality=94);art=b.getvalue();folder=base+"/assets/social-arq076";mkdir(f,folder)
 f.storbinary("STOR "+folder+"/aceite-recuperacao-20261022.jpg",io.BytesIO(art));assert get(f,folder+"/aceite-recuperacao-20261022.jpg")==art
 photo="https://www.arquindex.com.br/assets/social-arq076/aceite-recuperacao-20261022.jpg"
 status,b=public(photo);assert status==200 and hashlib.sha256(b).digest()==hashlib.sha256(art).digest()
 print("IMAGE_PUBLIC_VERIFIED",photo,hashlib.sha256(art).hexdigest(),flush=True)
