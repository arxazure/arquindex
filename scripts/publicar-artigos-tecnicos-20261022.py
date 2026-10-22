"""Publica os artigos de 22/10/2026 com backup, rollback e validação pública."""
import ftplib, hashlib, io, json, os, pathlib, re, socket, ssl, time
import urllib.request, urllib.robotparser
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from html.parser import HTMLParser

ROOT="https://www.arquindex.com.br/"; DATE="2026-10-22"; SITEMAP="/public_html/sitemap-artigos.xml"
ARTICLES=[
 {"source":pathlib.Path("artigos-tecnicos/2026-10-22/pdfa-nao-basta-decreto-10278-validacao/index.html"),"target":"/public_html/blog/pdfa-nao-basta-decreto-10278-validacao/index.html","url":ROOT+"blog/pdfa-nao-basta-decreto-10278-validacao/","marker":"ARQ-ARTICLE-20261022-PDFA-VALIDACAO-10278"},
 {"source":pathlib.Path("artigos-tecnicos/2026-10-22/prontuario-ocupacional-digital-rh-lgpd-nr7/index.html"),"target":"/public_html/blog/prontuario-ocupacional-digital-rh-lgpd-nr7/index.html","url":ROOT+"blog/prontuario-ocupacional-digital-rh-lgpd-nr7/","marker":"ARQ-ARTICLE-20261022-PRONTUARIO-OCUPACIONAL-NR7-LGPD"},
]

class Page(HTMLParser):
 def __init__(self): super().__init__(); self.h1=0; self.canonical=[]; self.robots=[]; self.article=0; self.skip=0; self.text=[]; self.ld=0; self.json=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=="h1": self.h1+=1
  if tag=="link" and a.get("rel")=="canonical": self.canonical.append(a.get("href"))
  if tag=="meta" and a.get("name","").lower()=="robots": self.robots.append(a.get("content",""))
  if tag=="article": self.article+=1
  if tag in {"script","style","nav","footer","aside"}: self.skip+=1
  if tag=="script" and a.get("type")=="application/ld+json": self.ld+=1
 def handle_endtag(self,tag):
  if tag=="article": self.article=max(0,self.article-1)
  if tag in {"script","style","nav","footer","aside"}: self.skip=max(0,self.skip-1)
  if tag=="script" and self.ld: self.ld-=1
 def handle_data(self,data):
  if self.article and not self.skip: self.text.append(data)
  if self.ld: self.json.append(data)

def sha(data): return hashlib.sha256(data).hexdigest()
def validate(data,spec):
 text=data.decode("utf-8"); p=Page(); p.feed(text)
 words=re.findall(r"\b[\wÀ-ÿ][\wÀ-ÿ’'-]*\b"," ".join(p.text))
 assert p.h1==1 and p.canonical==[spec["url"]]
 assert len(p.robots)==1 and "index" in p.robots[0].lower() and "follow" in p.robots[0].lower()
 assert len(words)>=1500 and spec["marker"] in text
 assert "comercial@arquindex.com.br" in text and "5531973632725" in text and 'datePublished":"'+DATE in text
 assert json.loads("".join(p.json))["@context"]=="https://schema.org"
 return len(words)
def http(url):
 req=urllib.request.Request(url,headers={"User-Agent":"ArquindexEditorialVerification/2026.10","Cache-Control":"no-cache"})
 with urllib.request.urlopen(req,timeout=45) as r: return r.status,r.url,r.headers,r.read()
def get(ftp,path):
 out=bytearray(); ftp.retrbinary("RETR "+path,out.extend); return bytes(out)
def put(ftp,path,data):
 ftp.storbinary("STOR "+path,io.BytesIO(data)); assert get(ftp,path)==data,("FTPS_READBACK",path)
def ensure(ftp,path):
 here=ftp.pwd()
 try:
  ftp.cwd("/"); current=""
  for part in path.strip("/").split("/"):
   current+="/"+part
   try: ftp.cwd(current)
   except ftplib.error_perm as exc:
    if not str(exc).startswith("550"): raise
    ftp.mkd(current); ftp.cwd(current)
 finally: ftp.cwd(here)

planned={}; previous={}; applied=[]
for article in ARTICLES:
 data=article["source"].read_bytes(); article["words"]=validate(data,article); article["sha256"]=sha(data); planned[article["target"]]=data
report={"date":DATE,"started_at":datetime.now(timezone.utc).isoformat(),"published":False,"articles":[{k:a[k] for k in ("url","target","marker","words","sha256")} for a in ARTICLES]}
pathlib.Path("publish-report").mkdir(exist_ok=True)
expected=set(socket.gethostbyname_ex("ftp.arquindex.com.br")[2]); provider=set(socket.gethostbyname_ex("h59.servidorhh.com")[2]); assert expected & provider
stamp=datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
try:
 with ftplib.FTP_TLS(context=ssl.create_default_context(),timeout=60) as ftp:
  ftp.connect("h59.servidorhh.com",21); assert ftp.sock.getpeername()[0] in expected
  ftp.login("arquind2",os.environ["FTP_PASSWORD"]); ftp.prot_p(); ftp.set_pasv(True)
  homepage=get(ftp,"/public_html/index.html"); assert b"arquindex" in homepage.lower()
  for a in ARTICLES:
   ensure(ftp,a["target"].rsplit("/",1)[0])
   try: previous[a["target"]]=get(ftp,a["target"])
   except ftplib.error_perm as exc:
    if not str(exc).startswith("550"): raise
    previous[a["target"]]=None
   assert previous[a["target"]] in (None,planned[a["target"]]),("DESTINATION_CONFLICT",a["target"])
  sitemap_before=get(ftp,SITEMAP); previous[SITEMAP]=sitemap_before
  ns="http://www.sitemaps.org/schemas/sitemap/0.9"; ET.register_namespace("",ns); root=ET.fromstring(sitemap_before); assert root.tag=="{"+ns+"}urlset"
  existing={n.text for n in root.iter("{"+ns+"}loc")}
  for a in ARTICLES:
   if a["url"] not in existing:
    e=ET.SubElement(root,"{"+ns+"}url"); ET.SubElement(e,"{"+ns+"}loc").text=a["url"]; ET.SubElement(e,"{"+ns+"}lastmod").text=DATE
  planned[SITEMAP]=ET.tostring(root,encoding="utf-8",xml_declaration=True)
  backup="/seo-backups/artigos-20261022-"+stamp; ensure(ftp,"/seo-backups"); ftp.mkd(backup); put(ftp,backup+"/.htaccess",b"Require all denied\n")
  manifest={}
  for path,old in previous.items():
   if old is not None:
    name=hashlib.sha256(path.encode()).hexdigest()+".bak"; put(ftp,backup+"/"+name,old); manifest[path]={"backup":name,"sha256":sha(old)}
  put(ftp,backup+"/manifest.json",json.dumps(manifest,indent=2).encode()); report["backup"]=backup
  status,_,_,body=http(ROOT+"robots.txt"); assert status==200; robot=urllib.robotparser.RobotFileParser(); robot.parse(body.decode().splitlines())
  assert all(robot.can_fetch("Googlebot",a["url"]) for a in ARTICLES)
  try:
   for path,data in planned.items():
    old=previous[path]
    if old==data: continue
    if old is not None: assert get(ftp,path)==old,("CONCURRENT_CHANGE",path)
    applied.append(path); put(ftp,path,data)
   for a in ARTICLES:
    result=None
    for _ in range(8):
     try:
      candidate=http(a["url"])
      if candidate[0]==200 and candidate[1]==a["url"] and a["marker"].encode() in candidate[3]: result=candidate; break
     except Exception: pass
     time.sleep(5)
    assert result,("PUBLIC_ARTICLE_NOT_VISIBLE",a["url"])
    words=validate(result[3],a); assert sha(result[3])==a["sha256"] and "noindex" not in result[2].get("X-Robots-Tag","").lower()
    a["http"]=result[0]; a["verified_words"]=words
   status,final,_,body=http(ROOT+"sitemap-artigos.xml"); assert status==200 and final==ROOT+"sitemap-artigos.xml"
   urls={n.text for n in ET.fromstring(body).iter("{"+ns+"}loc")}; assert all(a["url"] in urls for a in ARTICLES)
   assert get(ftp,"/public_html/index.html")==homepage
   report.update({"published":True,"sitemap":ROOT+"sitemap-artigos.xml","completed_at":datetime.now(timezone.utc).isoformat(),"articles":[{k:a[k] for k in ("url","target","marker","words","sha256","http","verified_words")} for a in ARTICLES]})
   print("ARTIGOS_20261022_HTTP200_CANONICAL_ROBOTS_SITEMAP_VERIFIED",flush=True)
  except Exception:
   rolled=[]
   for path in reversed(applied):
    if get(ftp,path)!=planned[path]: continue
    if previous[path] is None: ftp.delete(path)
    else: put(ftp,path,previous[path])
    rolled.append(path)
   report["rolled_back"]=rolled; raise
finally:
 pathlib.Path("publish-report/artigos-20261022.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
 print(json.dumps(report,ensure_ascii=False),flush=True)
