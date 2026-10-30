#!/usr/bin/env python3
import ftplib, hashlib, html, io, json, os, posixpath, re, socket, ssl, time, urllib.request
from datetime import datetime, timezone

ID="ARQ-172"
HOSTNAME="digitalizaca.arquindex.com.br"
URL="https://digitalizaca.arquindex.com.br/"
STAMP=datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
TITLE="Checklist para orçamento de digitalização de documentos | Arquindex"
DESC="Saiba como preparar inventário, amostra, requisitos de OCR, formatos e critérios de aceite antes de pedir orçamento de digitalização."
LOGO="https://www.arquindex.com.br/assets/arquindex-restored/arquindex-logo-oficial.webp"
WA="https://wa.me/5531973632725?text=Ol%C3%A1%2C%20Arquindex!%20Gostaria%20de%20avaliar%20um%20projeto%20de%20digitaliza%C3%A7%C3%A3o."
STYLE="""<style data-aq-brand="20261030">.aq-brandbar{box-sizing:border-box;display:flex;align-items:center;justify-content:space-between;gap:20px;padding:12px max(20px,calc((100% - 1180px)/2));background:#fff;border-bottom:1px solid #e5e7eb;font:600 15px Arial,sans-serif;position:relative;z-index:1000}.aq-brandbar img{width:190px;max-width:46vw;height:auto}.aq-brandbar nav{display:flex;gap:18px;flex-wrap:wrap}.aq-brandbar a{color:#12395b;text-decoration:none}.aq-brandbar .aq-cta,.aq-brand-wa{background:#0b7a56;color:#fff!important;padding:10px 14px;border-radius:8px}.aq-brand-wa{position:fixed;right:18px;bottom:18px;z-index:9999;text-decoration:none;font:700 14px Arial,sans-serif;box-shadow:0 8px 22px #0003}.aq172{max-width:1100px;margin:34px auto;padding:28px;background:#fff;border:1px solid #dce5ed;border-radius:16px;color:#17324d;font:17px/1.65 Arial,sans-serif}.aq172 h2,.aq172 h3{color:#0d4f69}.aq172 table{width:100%;border-collapse:collapse}.aq172 th,.aq172 td{border:1px solid #d9e2ea;padding:12px;text-align:left;vertical-align:top}.aq172 .answer{border-left:5px solid #0b7a56;padding:14px 18px;background:#f1faf7}.aq172 a{color:#075f8f}@media(max-width:760px){.aq-brandbar{align-items:flex-start}.aq-brandbar nav a:not(.aq-cta){display:none}.aq-brandbar img{width:150px}.aq172{margin:20px 12px;padding:20px;overflow-wrap:anywhere}.aq172 table{font-size:14px}.aq172 th,.aq172 td{padding:8px}}</style>"""
BAR=f"""<header class="aq-brandbar" aria-label="Cabeçalho Arquindex"><a href="https://www.arquindex.com.br/" aria-label="Arquindex - início"><img src="{LOGO}" alt="Arquindex"></a><nav aria-label="Navegação Arquindex"><a href="https://www.arquindex.com.br/digitalizacao.html">Digitalização</a><a href="https://www.arquindex.com.br/digitalizacao-com-ocr.html">OCR</a><a class="aq-cta" href="{WA}">Solicitar avaliação</a></nav></header>"""
FLOAT=f"""<a id="arq-floating" class="aq-brand-wa" href="{WA}" aria-label="Falar com a Arquindex no WhatsApp">WhatsApp · 31 97363-2725</a>"""
BLOCK=f"""<section class="aq172" id="checklist-orcamento" data-aq-aeo="ARQ-172"><h2>Como preparar um orçamento de digitalização sem comparar escopos diferentes</h2><p class="answer"><strong>Resposta direta:</strong> informe tipos documentais, volumes e tamanhos; forneça uma amostra representativa; defina OCR e campos de indexação; combine formato de entrega, segurança e critérios de aceite. Sem esses itens, propostas com preços parecidos podem cobrir entregas diferentes.</p><h3>Checklist de entrada</h3><ol><li><strong>Inventário:</strong> relacione caixas, pastas, páginas estimadas, A4/A3 e itens especiais sem enviar dados pessoais desnecessários.</li><li><strong>Amostra:</strong> inclua documentos claros, frágeis, grampeados, frente e verso e páginas com carimbos ou anotações.</li><li><strong>Uso do arquivo:</strong> diga se a necessidade é consulta, carga em GED, extração de campos ou preservação.</li><li><strong>Aceite:</strong> defina legibilidade, orientação, páginas ausentes, nomenclatura, pesquisa por OCR e tratamento de exceções.</li></ol><h3>O que muda o escopo</h3><table><thead><tr><th>Decisão</th><th>O que confirmar</th></tr></thead><tbody><tr><td>Captura</td><td>Preparação, retirada de grampos, tamanhos, frente e verso e necessidade de recaptura.</td></tr><tr><td>OCR e indexação</td><td>PDF pesquisável não é igual à extração validada de nomes, datas, valores ou códigos.</td></tr><tr><td>Entrega</td><td>Estrutura de pastas, PDF/PDF-A/TIFF conforme o uso, mídia, transferência e carga em sistema.</td></tr><tr><td>Segurança</td><td>Transporte, acesso, ambiente de processamento, devolução e descarte de cópias temporárias.</td></tr></tbody></table><h3>Próximo passo</h3><p>Consulte a página de <a href="https://www.arquindex.com.br/digitalizacao.html">digitalização de documentos</a> e os critérios de <a href="https://www.arquindex.com.br/digitalizacao-com-ocr.html">OCR e controle de qualidade</a>. A Arquindex confirma disponibilidade, método, prazo e condições comerciais na proposta; esta página não publica preço sem escopo.</p><p><a class="aq-brand-wa" style="position:static;display:inline-block" href="{WA}">Enviar informações para avaliação</a></p><p><small>Autoria institucional: Arquindex · Revisão editorial: 30/10/2026.</small></p></section>"""

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
def candidates(host):
 slug=host.split(".")[0]
 return ["/public_html/subdominios/"+host,"/public_html/"+host,"/subdominios/"+host,"/"+host,
         "/public_html/subdominios/"+slug,"/public_html/"+slug,"/subdominios/"+slug,"/"+slug]
def locate_existing(ftp,host,name):
 for root in candidates(host):
  if exists(ftp,posixpath.join(root,name)): return root
 raise RuntimeError("TARGET_NOT_FOUND "+host+"/"+name)
def put_verified(ftp,path,data):
 temp=path+".upload-"+STAMP
 ftp.storbinary("STOR "+temp,io.BytesIO(data))
 if get(ftp,temp)!=data: raise RuntimeError("TEMP_MISMATCH "+path)
 if exists(ftp,path): ftp.delete(path)
 ftp.rename(temp,path)
 if get(ftp,path)!=data: raise RuntimeError("FINAL_MISMATCH "+path)
def public(url):
 req=urllib.request.Request(url+("?verify="+STAMP if "?" not in url else "&verify="+STAMP),headers={"User-Agent":"ArquindexSEO/1.0","Cache-Control":"no-cache"})
 with urllib.request.urlopen(req,timeout=45) as r:return r.status,r.read(6_000_000)

pw=os.environ.get("FTP_PASSWORD")
if not pw: raise RuntimeError("FTP_PASSWORD_MISSING")
cert_host="h59.servidorhh.com"; connect_host=(os.environ.get("FTP_IP") or "177.234.150.42").strip(); user=(os.environ.get("FTP_USER") or "arquind2").strip()
ctx=ssl.create_default_context(); ctx.minimum_version=ssl.TLSVersion.TLSv1_2
with ftplib.FTP_TLS(timeout=70,context=ctx) as ftp:
 ftp.connect(connect_host,21)
 if ftp.sock.getpeername()[0] != connect_host: raise RuntimeError("SERVER_IP_CHANGED")
 ftp.host=cert_host
 ftp.auth(); ftp.login(user,pw); ftp.prot_p(); ftp.set_pasv(True)
 root=locate_existing(ftp,HOSTNAME,"index.html"); path=posixpath.join(root,"index.html"); old=get(ftp,path)
 backup_root="/seo-backups/seo-arq172-"+STAMP; mkdirs(ftp,backup_root)
 meta=json.dumps({"id":ID,"target":path,"created_at":STAMP,"sha256":hashlib.sha256(old).hexdigest(),"source_commit":os.environ.get("GITHUB_SHA","")},ensure_ascii=False,indent=2).encode()
 for n,d in [("original.html",old),("manifest.json",meta),(".htaccess",b"Options -Indexes\nRequire all denied\n")]: put_verified(ftp,backup_root+"/"+n,d)
 print("BACKUP_VERIFIED",ID,backup_root,hashlib.sha256(old).hexdigest(),flush=True)
 text=old.decode("utf-8","replace")
 text=re.sub(r"<title\b[^>]*>.*?</title>","<title>"+html.escape(TITLE)+"</title>",text,count=1,flags=re.I|re.S)
 if re.search(r'<meta\b[^>]*name=["\']description["\'][^>]*>',text,re.I):
  text=re.sub(r'<meta\b[^>]*name=["\']description["\'][^>]*>',f'<meta name="description" content="{html.escape(DESC,quote=True)}">',text,count=1,flags=re.I)
 else:text=re.sub(r"</head>",f'<meta name="description" content="{html.escape(DESC,quote=True)}">\n</head>',text,count=1,flags=re.I)
 if not re.search(r'<meta\b[^>]*name=["\']robots["\']',text,re.I):text=re.sub(r"</head>",'<meta name="robots" content="index,follow,max-image-preview:large">\n</head>',text,count=1,flags=re.I)
 text=re.sub(r"<h1\b([^>]*)>\s*(?:<[^>]+>\s*)*</h1>",r'<h1\1>Checklist para orçamento de digitalização de documentos</h1>',text,count=1,flags=re.I|re.S)
 if not re.search(r"<h1\b[^>]*>\s*[^<\s]",text,re.I): raise RuntimeError("H1_TEXT_NOT_FIXED")
 if 'data-aq-brand="20261030"' not in text:
  text=re.sub(r"</head>",STYLE+"\n</head>",text,count=1,flags=re.I)
  text=re.sub(r"<body([^>]*)>","<body\\1>"+BAR,text,count=1,flags=re.I)
 if 'data-aq-aeo="ARQ-172"' not in text:
  text=re.sub(r"</main>",BLOCK+"</main>",text,count=1,flags=re.I) if re.search(r"</main>",text,re.I) else re.sub(r"</body>",BLOCK+"</body>",text,count=1,flags=re.I)
 if 'id="arq-floating"' not in text:text=re.sub(r"</body>",FLOAT+"</body>",text,count=1,flags=re.I)
 new=text.encode("utf-8")
 try:
  put_verified(ftp,path,new)
  robots=posixpath.join(root,"robots.txt")
  if not exists(ftp,robots):
   put_verified(ftp,robots,("User-agent: *\nAllow: /\nSitemap: "+URL+"sitemap.xml\n").encode())
   print("ROBOTS_CREATED_VERIFIED",ID,robots,flush=True)
  print("FTP_UPDATED_VERIFIED",ID,path,hashlib.sha256(new).hexdigest(),flush=True)
 except Exception:
  put_verified(ftp,path,old); print("ROLLBACK_COMPLETED",ID,flush=True); raise

last=None
for attempt in range(4):
 try:
  st,body=public(URL); text=body.decode("utf-8","replace")
  required=[TITLE,'rel="canonical" href="'+URL+'"',"Checklist para orçamento de digitalização de documentos","arquindex-logo-oficial.webp","31 97363-2725",'data-aq-aeo="ARQ-172"']
  if st!=200 or any(x not in text for x in required) or "melhor empresa" in text.lower(): raise RuntimeError("PUBLIC_HTML_INVALID")
  print("PUBLIC_VERIFIED",ID,URL,hashlib.sha256(body).hexdigest(),flush=True); last=None; break
 except Exception as e:
  last=e
  if attempt<3: time.sleep(10)
if last: raise last
st,rb=public(URL+"robots.txt")
if st!=200 or "Sitemap: "+URL+"sitemap.xml" not in rb.decode("utf-8","replace"): raise RuntimeError("ROBOTS_PUBLIC_INVALID")
print("DISCOVERY_VERIFIED",URL+"robots.txt",st,flush=True)
print("SITEMAP_EXISTING_NOT_RESUBMITTED",URL+"sitemap.xml",flush=True)
print("INDEXNOW_SKIPPED_KEY_EMPTY" if not (os.environ.get("INDEXNOW_KEY") or "").strip() else "INDEXNOW_NOT_RUN_NO_VALIDATED_KEY_FILE",flush=True)
