#!/usr/bin/env python3
import ftplib, hashlib, html, io, json, os, posixpath, re, socket, ssl, time, urllib.request
from datetime import datetime, timezone

STAMP=datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
LOGO="https://www.arquindex.com.br/assets/arquindex-restored/arquindex-logo-oficial.webp"
WA="https://wa.me/5531973632725?text=Ol%C3%A1%2C%20Arquindex!%20Gostaria%20de%20avaliar%20um%20projeto%20documental."
HEAD_STYLE="""<style data-aq-brand="20261029">
.aq-brandbar{box-sizing:border-box;display:flex;align-items:center;justify-content:space-between;gap:20px;padding:12px max(20px,calc((100% - 1180px)/2));background:#fff;border-bottom:1px solid #e5e7eb;font:600 15px Arial,sans-serif;position:relative;z-index:1000}.aq-brandbar img{width:190px;max-width:46vw;height:auto}.aq-brandbar nav{display:flex;gap:18px;flex-wrap:wrap}.aq-brandbar a{color:#12395b;text-decoration:none}.aq-brandbar .aq-cta{background:#0b7a56;color:#fff;padding:10px 14px;border-radius:8px}.aq-brand-wa{position:fixed;right:18px;bottom:18px;z-index:9999;background:#087f5b;color:#fff!important;padding:13px 16px;border-radius:999px;text-decoration:none;font:700 14px Arial,sans-serif;box-shadow:0 8px 22px #0003}@media(max-width:760px){.aq-brandbar{align-items:flex-start}.aq-brandbar nav a:not(.aq-cta){display:none}.aq-brandbar img{width:150px}}
</style>"""
BAR=f"""<header class="aq-brandbar" aria-label="Cabeçalho Arquindex"><a href="https://www.arquindex.com.br/" aria-label="Arquindex - início"><img src="{LOGO}" alt="Arquindex"></a><nav aria-label="Navegação Arquindex"><a href="https://www.arquindex.com.br/servicos/">Soluções</a><a href="https://www.arquindex.com.br/blog/">Artigos</a><a class="aq-cta" href="{WA}">Solicitar avaliação</a></nav></header>"""
FLOAT=f"""<a id="arq-floating" class="aq-brand-wa" href="{WA}" aria-label="Falar com a Arquindex no WhatsApp">WhatsApp · 31 97363-2725</a>"""

def get(ftp,path):
 out=bytearray(); ftp.retrbinary("RETR "+path,out.extend); return bytes(out)
def exists(ftp,path):
 try: ftp.size(path); return True
 except ftplib.all_errors: return False
def mkdirs(ftp,path):
 old=ftp.pwd(); ftp.cwd("/")
 try:
  for part in path.strip("/").split("/"):
   if not part: continue
   try: ftp.mkd(part)
   except ftplib.error_perm as e:
    if not str(e).startswith("550"): raise
   ftp.cwd(part)
 finally: ftp.cwd(old)
def list_names(ftp,path):
 try: return {n.lower() for n,_ in ftp.mlsd(path) if n not in {".",".."}}
 except ftplib.all_errors: return set()
def candidates(host):
 slug=host.split(".")[0]
 return ["/public_html/subdominios/"+host,"/public_html/"+host,"/subdominios/"+host,"/"+host,
         "/public_html/subdominios/"+slug,"/public_html/"+slug,"/subdominios/"+slug,"/"+slug]
def locate_existing(ftp,host,name):
 for root in candidates(host):
  if exists(ftp,posixpath.join(root,name)): return root
 raise RuntimeError("TARGET_NOT_FOUND "+host+"/"+name)
def locate_empty(ftp,host):
 for root in candidates(host):
  try:
   ftp.cwd(root); names=list_names(ftp,root)
   if "index.html" not in names and "index.php" not in names: return root,names
  except ftplib.all_errors: pass
 raise RuntimeError("EMPTY_SUBDOMAIN_ROOT_NOT_FOUND "+host)
def put_verified(ftp,path,data):
 temp=path+".upload-"+STAMP
 ftp.storbinary("STOR "+temp,io.BytesIO(data))
 if get(ftp,temp)!=data: raise RuntimeError("TEMP_MISMATCH "+path)
 if exists(ftp,path): ftp.delete(path)
 ftp.rename(temp,path)
 if get(ftp,path)!=data: raise RuntimeError("FINAL_MISMATCH "+path)
def public(url):
 req=urllib.request.Request(url+("?verify="+STAMP if "?" not in url else "&verify="+STAMP),headers={"User-Agent":"ArquindexSEO/1.0","Cache-Control":"no-cache"})
 with urllib.request.urlopen(req,timeout=45) as r: return r.status,r.read(6_000_000)
def backup(ftp,id,path,data):
 b="/seo-backups/seo-"+id.lower()+"-"+STAMP
 mkdirs(ftp,b)
 meta=json.dumps({"id":id,"target":path,"created_at":STAMP,"sha256":hashlib.sha256(data).hexdigest(),"source_commit":os.environ.get("GITHUB_SHA","")},ensure_ascii=False,indent=2).encode()
 for name,blob in [("original.html",data),("manifest.json",meta),(".htaccess",b"Options -Indexes\nRequire all denied\n")]:
  put_verified(ftp,b+"/"+name,blob)
 print("BACKUP_VERIFIED",id,b,hashlib.sha256(data).hexdigest(),flush=True)
 return b
def patch_html(raw,title,desc,canonical):
 text=raw.decode("utf-8","replace")
 text=re.sub(r"<title\b[^>]*>.*?</title>","<title>"+html.escape(title)+"</title>",text,count=1,flags=re.I|re.S)
 if re.search(r'<meta\b[^>]*name=["\']description["\'][^>]*>',text,re.I):
  text=re.sub(r'<meta\b[^>]*name=["\']description["\'][^>]*>',f'<meta name="description" content="{html.escape(desc,quote=True)}">',text,count=1,flags=re.I)
 else: text=re.sub(r"</head>",f'<meta name="description" content="{html.escape(desc,quote=True)}">\n</head>',text,count=1,flags=re.I)
 if re.search(r'<link\b[^>]*rel=["\']canonical["\'][^>]*>',text,re.I):
  text=re.sub(r'<link\b[^>]*rel=["\']canonical["\'][^>]*>',f'<link rel="canonical" href="{canonical}">',text,count=1,flags=re.I)
 else: text=re.sub(r"</head>",f'<link rel="canonical" href="{canonical}">\n</head>',text,count=1,flags=re.I)
 if not re.search(r'<meta\b[^>]*name=["\']robots["\']',text,re.I):
  text=re.sub(r"</head>",'<meta name="robots" content="index,follow,max-image-preview:large">\n</head>',text,count=1,flags=re.I)
 if 'data-aq-brand="20261029"' not in text:
  text=re.sub(r"</head>",HEAD_STYLE+"\n</head>",text,count=1,flags=re.I)
  text=re.sub(r"<body([^>]*)>","<body\\1>"+BAR,text,count=1,flags=re.I)
  text=re.sub(r"</body>",FLOAT+"</body>",text,count=1,flags=re.I)
 return text.encode("utf-8")

D178="""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Assinaturas eletrônicas e gestão de documentos | Arquindex</title><meta name="description" content="Guia independente sobre assinaturas eletrônicas, documentos digitalizados, evidências, guarda e integração com gestão documental."><meta name="robots" content="index,follow,max-image-preview:large"><link rel="canonical" href="https://docusign.arquindex.com.br/">"""+HEAD_STYLE+"""<style>body{margin:0;color:#17324d;background:#f6f8fb;font:17px/1.65 Arial,sans-serif}main{max-width:1060px;margin:auto;padding:46px 22px}h1{font-size:clamp(2rem,5vw,3.4rem);line-height:1.12;color:#0d3457}h2{margin-top:38px;color:#135e6b}.hero,.card,.notice{background:#fff;padding:28px;border-radius:16px;box-shadow:0 8px 28px #15324d12}.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}.notice{border-left:5px solid #d19a2d;margin:22px 0}table{width:100%;border-collapse:collapse;background:#fff}th,td{padding:14px;border:1px solid #d9e2ea;text-align:left;vertical-align:top}footer{background:#0d3457;color:#fff;padding:30px 22px;text-align:center}a{color:#075f8f}@media(max-width:760px){.grid{grid-template-columns:1fr}table{font-size:14px}th,td{padding:9px}}</style><script type="application/ld+json">{"@context":"https://schema.org","@type":"WebPage","name":"Assinaturas eletrônicas e gestão de documentos","url":"https://docusign.arquindex.com.br/","publisher":{"@type":"Organization","name":"Arquindex","url":"https://www.arquindex.com.br/"}}</script></head><body>"""+BAR+"""<main data-aq-aeo="ARQ-178"><section class="hero"><p>GUIA INDEPENDENTE · GESTÃO DOCUMENTAL</p><h1>Assinaturas eletrônicas e gestão de documentos</h1><p><strong>Resposta direta:</strong> assinar eletronicamente resolve a manifestação de vontade e a evidência da assinatura; gerir o documento exige também classificação, controle de versão, acesso, retenção, descarte e capacidade de auditoria. São camadas complementares.</p><p><a href="#checklist">Ver checklist</a> · <a href="https://www.arquindex.com.br/gestao-documental.html">Conhecer gestão documental</a></p></section><div class="notice"><strong>Transparência:</strong> este é conteúdo informativo da Arquindex. “DocuSign” é marca de terceiro; esta página não declara parceria, representação, integração homologada ou afiliação.</div><h2>O que conferir antes de contratar</h2><div class="grid"><article class="card"><h3>Identidade e consentimento</h3><p>Defina como o signatário será identificado, quais fatores de autenticação serão usados e como o consentimento será registrado.</p></article><article class="card"><h3>Integridade e evidências</h3><p>Verifique trilha de auditoria, carimbo de tempo quando aplicável, hash, registro de eventos e forma de exportar as evidências.</p></article><article class="card"><h3>Ciclo de vida</h3><p>Planeje onde o documento final será classificado, quem acessa, por quanto tempo será guardado e como ocorrerá a destinação.</p></article></div><h2>Assinatura eletrônica não é a mesma coisa que digitalização</h2><table><thead><tr><th>Etapa</th><th>Objetivo</th><th>Pergunta prática</th></tr></thead><tbody><tr><td>Digitalização</td><td>Converter o suporte físico em arquivo digital com critérios de captura e controle.</td><td>O arquivo representa o original com qualidade e metadados adequados?</td></tr><tr><td>Assinatura eletrônica</td><td>Registrar autoria, manifestação de vontade e evidências do ato.</td><td>A identificação e a trilha de auditoria são proporcionais ao risco?</td></tr><tr><td>Gestão documental</td><td>Controlar classificação, acesso, versão, temporalidade e destinação.</td><td>O documento será localizado, preservado e descartado com governança?</td></tr></tbody></table><h2 id="checklist">Checklist de implantação</h2><ol><li>Mapeie os tipos documentais, signatários, riscos e requisitos regulatórios.</li><li>Defina níveis de assinatura e autenticação conforme o caso de uso, com validação jurídica própria.</li><li>Teste a exportação do documento e das evidências antes de contratar em escala.</li><li>Integre o resultado ao repositório documental sem perder metadados ou histórico.</li><li>Documente perfis de acesso, retenção, continuidade e saída do fornecedor.</li><li>Meça tempo de assinatura, retrabalho, falhas de autenticação e localização posterior.</li></ol><h2>Fontes primárias para avaliação</h2><ul><li><a href="https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2020/lei/l14063.htm">Lei nº 14.063/2020 — assinaturas eletrônicas</a></li><li><a href="https://www.planalto.gov.br/ccivil_03/mpv/antigas_2001/2200-2.htm">MP nº 2.200-2/2001 — ICP-Brasil</a></li><li><a href="https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2020/decreto/d10278.htm">Decreto nº 10.278/2020 — digitalização de documentos</a></li></ul><h2>Próximos passos</h2><p>A Arquindex pode avaliar a organização, digitalização e governança do acervo que antecede ou sucede a assinatura. A disponibilidade de integração com qualquer plataforma deve ser confirmada no escopo.</p><p><a href="https://www.arquindex.com.br/digitalizacao.html">Digitalização de documentos</a> · <a href="https://www.arquindex.com.br/gestao-documental.html">Gestão documental</a> · <a href="https://www.arquindex.com.br/lgpd-consultoria.html">Consultoria LGPD</a></p><p><a class="aq-brand-wa" style="position:static;display:inline-block" href=\""""+WA+"""\">Solicitar avaliação no WhatsApp</a></p><p><small>Autoria institucional: Arquindex · Revisão editorial: 29/10/2026.</small></p></main><footer>Arquindex · Belo Horizonte · WhatsApp +55 31 97363-2725</footer>"""+FLOAT+"""</body></html>"""

targets=[
 ("ARQ-174","digitalizar-arquivos-corporativo.arquindex.com.br","vantagens.html","Vantagens da gestão de arquivos físicos e digitais | Arquindex","Veja critérios e benefícios da gestão integrada de arquivos físicos e digitais, com rastreabilidade, acesso, OCR e governança documental."),
 ("ARQ-176","digitalizar-mapeamento-mg.arquindex.com.br","o-que-e.html","O que é mapeamento de dados para governança documental | Arquindex","Entenda o mapeamento de dados aplicado à governança documental, com etapas, responsáveis, acessos, riscos e apoio à adequação LGPD.")
]
pw=os.environ.get("FTP_PASSWORD")
if not pw: raise RuntimeError("FTP_PASSWORD_MISSING")
host=(os.environ.get("FTP_TLS_HOST") or "h59.servidorhh.com").strip(); user=(os.environ.get("FTP_USER") or "arquind2").strip()
expected=set(socket.gethostbyname_ex("ftp.arquindex.com.br")[2]); resolved=set(socket.gethostbyname_ex(host)[2])
if not expected.intersection(resolved): raise RuntimeError("HOST_IP_MISMATCH")
ctx=ssl.create_default_context(); ctx.minimum_version=ssl.TLSVersion.TLSv1_2
with ftplib.FTP_TLS(timeout=70,context=ctx) as ftp:
 ftp.connect(host,21)
 if ftp.sock.getpeername()[0] not in expected: raise RuntimeError("SERVER_IP_CHANGED")
 ftp.auth(); ftp.login(user,pw); ftp.prot_p(); ftp.set_pasv(True)
 for id,hostname,name,title,desc in targets:
  root=locate_existing(ftp,hostname,name); path=posixpath.join(root,name); old=get(ftp,path)
  backup(ftp,id,path,old); new=patch_html(old,title,desc,"https://"+hostname+"/"+name)
  try:
   put_verified(ftp,path,new); print("FTP_UPDATED_VERIFIED",id,path,hashlib.sha256(new).hexdigest(),flush=True)
  except Exception:
   put_verified(ftp,path,old); print("ROLLBACK_COMPLETED",id,flush=True); raise
 root,names=locate_empty(ftp,"docusign.arquindex.com.br")
 b="/seo-backups/reconstrucoes/arq178-"+STAMP; mkdirs(ftp,b)
 inv=json.dumps({"id":"ARQ-178","target":root,"observed_before":sorted(names),"created_at":STAMP,"source_commit":os.environ.get("GITHUB_SHA","")},indent=2).encode()
 for n,d in [("inventory.json",inv),(".htaccess",b"Options -Indexes\nRequire all denied\n")]: put_verified(ftp,b+"/"+n,d)
 print("INVENTORY_BACKUP_VERIFIED","ARQ-178",b,hashlib.sha256(inv).hexdigest(),flush=True)
 created=[]
 try:
  files={"index.html":D178.encode(),"robots.txt":b"User-agent: *\nAllow: /\nSitemap: https://docusign.arquindex.com.br/sitemap.xml\n","sitemap.xml":b'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>https://docusign.arquindex.com.br/</loc><lastmod>2026-10-29</lastmod></url></urlset>\n'}
  for n,d in files.items():
   p=posixpath.join(root,n)
   if exists(ftp,p): raise RuntimeError("CONCURRENT_FILE_EXISTS "+p)
   put_verified(ftp,p,d); created.append((p,d)); print("FTP_CREATED_VERIFIED","ARQ-178",n,hashlib.sha256(d).hexdigest(),flush=True)
 except Exception:
  for p,d in reversed(created):
   try:
    if get(ftp,p)==d: ftp.delete(p)
   except ftplib.all_errors: pass
  print("ROLLBACK_CREATED_FILES_COMPLETED ARQ-178",flush=True); raise

checks=[
 ("ARQ-174","https://digitalizar-arquivos-corporativo.arquindex.com.br/vantagens.html","https://digitalizar-arquivos-corporativo.arquindex.com.br/vantagens.html","Vantagens da gestão de arquivos físicos e digitais | Arquindex"),
 ("ARQ-176","https://digitalizar-mapeamento-mg.arquindex.com.br/o-que-e.html","https://digitalizar-mapeamento-mg.arquindex.com.br/o-que-e.html","O que é mapeamento de dados para governança documental | Arquindex"),
 ("ARQ-178","https://docusign.arquindex.com.br/","https://docusign.arquindex.com.br/","Assinaturas eletrônicas e gestão de documentos | Arquindex")
]
for id,url,canonical,title in checks:
 last=None
 for attempt in range(4):
  try:
   st,body=public(url); text=body.decode("utf-8","replace")
   required=[title,'rel="canonical" href="'+canonical+'"',"arquindex-logo-oficial.webp","31 97363-2725"]
   if st!=200 or any(x not in text for x in required) or "Index of /" in text: raise RuntimeError("PUBLIC_HTML_INVALID")
   print("PUBLIC_VERIFIED",id,url,hashlib.sha256(body).hexdigest(),flush=True); last=None; break
  except Exception as e:
   last=e
   if attempt<3: time.sleep(10)
 if last: raise last
for p,needle in [("https://docusign.arquindex.com.br/robots.txt","Sitemap: https://docusign.arquindex.com.br/sitemap.xml"),("https://docusign.arquindex.com.br/sitemap.xml","<loc>https://docusign.arquindex.com.br/</loc>")]:
 st,b=public(p)
 if st!=200 or needle not in b.decode("utf-8","replace"): raise RuntimeError("ARQ178_DISCOVERY_INVALID")
 print("DISCOVERY_VERIFIED",p,st,flush=True)
print("INDEXNOW_SKIPPED_KEY_EMPTY" if not (os.environ.get("INDEXNOW_KEY") or "").strip() else "INDEXNOW_NOT_RUN_NO_VALIDATED_KEY_FILE",flush=True)
