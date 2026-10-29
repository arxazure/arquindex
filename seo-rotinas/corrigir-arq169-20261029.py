#!/usr/bin/env python3
import ftplib, hashlib, io, os, posixpath, re, socket, ssl, time, urllib.request
from datetime import datetime, timezone

HOST="decreto10278-educacao.arquindex.com.br"
URL="https://"+HOST+"/custo.html"
TITLE="Custo de digitalização certificada para educação | Arquindex"
CANONICAL=URL
STAMP=datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

def get(f,p):
 out=bytearray(); f.retrbinary("RETR "+p,out.extend); return bytes(out)
def put(f,p,b):
 f.storbinary("STOR "+p,io.BytesIO(b))
 if get(f,p)!=b: raise RuntimeError("FTP_VERIFY_FAILED "+p)
def mkdirs(f,p):
 old=f.pwd(); f.cwd("/")
 try:
  for part in p.strip("/").split("/"):
   try: f.mkd(part)
   except ftplib.error_perm: pass
   f.cwd(part)
 finally: f.cwd(old)
def public():
 req=urllib.request.Request(URL+"?verify="+STAMP,headers={"User-Agent":"ArquindexSEO/1.0","Cache-Control":"no-cache"})
 with urllib.request.urlopen(req,timeout=45) as r:return r.status,r.read(5_000_000)
pw=os.environ.get("FTP_PASSWORD")
if not pw: raise RuntimeError("FTP_PASSWORD_MISSING")
server=(os.environ.get("FTP_TLS_HOST") or "h59.servidorhh.com").strip()
user=(os.environ.get("FTP_USER") or "arquind2").strip()
expected=set(socket.gethostbyname_ex("ftp.arquindex.com.br")[2]); resolved=set(socket.gethostbyname_ex(server)[2])
if not expected.intersection(resolved): raise RuntimeError("HOST_IP_MISMATCH")
ctx=ssl.create_default_context();ctx.minimum_version=ssl.TLSVersion.TLSv1_2
with ftplib.FTP_TLS(timeout=60,context=ctx) as f:
 f.connect(server,21)
 if f.sock.getpeername()[0] not in expected: raise RuntimeError("SERVER_IP_CHANGED")
 f.auth();f.login(user,pw);f.prot_p();f.set_pasv(True)
 candidates=["/public_html/subdominios/"+HOST+"/custo.html","/public_html/"+HOST+"/custo.html","/subdominios/"+HOST+"/custo.html","/"+HOST+"/custo.html","/public_html/subdominios/decreto10278-educacao/custo.html","/public_html/decreto10278-educacao/custo.html"]
 path=None; original=None
 for p in candidates:
  try:
   b=get(f,p)
   if b"<html" in b.lower(): path=p;original=b;break
  except ftplib.all_errors: pass
 if not path: raise RuntimeError("TARGET_NOT_FOUND")
 text=original.decode("utf-8")
 old_title=re.search(r"<title[^>]*>(.*?)</title>",text,re.I|re.S)
 old_canonical=re.search(r"<link\b[^>]*rel=[\"']canonical[\"'][^>]*>",text,re.I)
 if not old_title or not old_canonical: raise RuntimeError("SEO_TAGS_NOT_FOUND")
 text=re.sub(r"<title[^>]*>.*?</title>","<title>"+TITLE+"</title>",text,count=1,flags=re.I|re.S)
 text=re.sub(r"<link\b[^>]*rel=[\"']canonical[\"'][^>]*>",'<link rel="canonical" href="'+CANONICAL+'">',text,count=1,flags=re.I)
 new=text.encode("utf-8")
 if new==original: raise RuntimeError("NO_CHANGE")
 backup="/seo-backups/seo-arq169-"+STAMP;mkdirs(f,backup)
 put(f,backup+"/custo.html",original);put(f,backup+"/.htaccess",b"Options -Indexes\nRequire all denied\n")
 print("BACKUP_VERIFIED",backup,hashlib.sha256(original).hexdigest(),flush=True)
 if get(f,path)!=original: raise RuntimeError("CONCURRENT_CHANGE")
 temp=path+".upload-"+STAMP;put(f,temp,new);f.rename(temp,path)
 if get(f,path)!=new: raise RuntimeError("FINAL_VERIFY_FAILED")
 print("FTP_UPDATED_VERIFIED",path,hashlib.sha256(new).hexdigest(),flush=True)
last=None
for i in range(3):
 try:
  st,b=public(); t=b.decode("utf-8","replace")
  if st!=200 or "<title>"+TITLE+"</title>" not in t or '<link rel="canonical" href="'+CANONICAL+'">' not in t: raise RuntimeError("PUBLIC_SEO_VERIFY_FAILED")
  if t.lower().count("<h1")!=1: raise RuntimeError("H1_CHANGED_OR_INVALID")
  print("PUBLIC_SEO_VERIFIED",URL,hashlib.sha256(b).hexdigest(),flush=True);last=None;break
 except Exception as e:
  last=e
  if i<2: time.sleep(8)
if last:
 with ftplib.FTP_TLS(timeout=60,context=ctx) as f:
  f.connect(server,21);f.auth();f.login(user,pw);f.prot_p();put(f,path,original)
 print("ROLLBACK_COMPLETED",flush=True)
 raise last
