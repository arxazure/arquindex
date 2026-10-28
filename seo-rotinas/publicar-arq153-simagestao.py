#!/usr/bin/env python3
import ftplib, hashlib, io, json, os, posixpath, socket, ssl, time, urllib.request
from datetime import datetime, timezone
from pathlib import Path

HOSTNAME="simagestao.arquindex.com.br"
PUBLIC="https://"+HOSTNAME+"/"
FILES={
 "index.html":Path("staging/seo/arq153-simagestao/index.html").read_bytes(),
 "robots.txt":Path("staging/seo/arq153-simagestao/robots.txt").read_bytes(),
 "sitemap.xml":Path("staging/seo/arq153-simagestao/sitemap.xml").read_bytes(),
}
STAMP=datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

def mlsd(ftp,path):
 return [(n,{k.lower():v for k,v in f.items()}) for n,f in ftp.mlsd(path,facts=["type","size","modify"]) if n not in {".",".."}]

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

def get(ftp,path):
 out=bytearray(); ftp.retrbinary("RETR "+path,out.extend); return bytes(out)

def exists(ftp,path):
 try: ftp.size(path); return True
 except ftplib.all_errors: return False

def locate(ftp):
 candidates=[
  "/public_html/subdominios/"+HOSTNAME,
  "/public_html/"+HOSTNAME,
  "/subdominios/"+HOSTNAME,
  "/"+HOSTNAME,
 ]
 for path in candidates:
  try:
   ftp.cwd(path); names={n.lower() for n,_ in mlsd(ftp,path)}
   if "index.html" not in names and "index.php" not in names:
    return path,names
  except ftplib.all_errors: pass
 raise RuntimeError("EMPTY_SUBDOMAIN_ROOT_NOT_FOUND")

def public_get(path):
 req=urllib.request.Request(PUBLIC+path+("?verify="+STAMP if path=="" else "?verify="+STAMP),headers={"User-Agent":"ArquindexSEO/1.0","Cache-Control":"no-cache"})
 with urllib.request.urlopen(req,timeout=45) as r: return r.status,r.read(4_000_000)

pw=os.environ.get("FTP_PASSWORD")
if not pw: raise RuntimeError("FTP_PASSWORD_MISSING")
host=(os.environ.get("FTP_TLS_HOST") or "h59.servidorhh.com").strip()
user=(os.environ.get("FTP_USER") or "arquind2").strip()
expected=set(socket.gethostbyname_ex("ftp.arquindex.com.br")[2])
resolved=set(socket.gethostbyname_ex(host)[2])
if not expected.intersection(resolved): raise RuntimeError("HOST_IP_MISMATCH")
ctx=ssl.create_default_context(); ctx.minimum_version=ssl.TLSVersion.TLSv1_2
created=[]
with ftplib.FTP_TLS(timeout=60,context=ctx) as ftp:
 ftp.connect(host,21)
 if ftp.sock.getpeername()[0] not in expected: raise RuntimeError("SERVER_IP_CHANGED")
 ftp.auth(); ftp.login(user,pw); ftp.prot_p(); ftp.set_pasv(True)
 root,names=locate(ftp)
 for name in FILES:
  if name.lower() in names or exists(ftp,posixpath.join(root,name)):
   raise RuntimeError("CONCURRENT_FILE_EXISTS "+name)
 backup="/seo-backups/reconstrucoes/arq153-"+STAMP
 mkdirs(ftp,backup)
 inventory={"target":root,"observed_before":sorted(names),"created_at":STAMP,"source_commit":os.environ.get("GITHUB_SHA","")}
 inv=json.dumps(inventory,ensure_ascii=False,indent=2).encode()
 ftp.storbinary("STOR "+backup+"/inventory.json",io.BytesIO(inv))
 ftp.storbinary("STOR "+backup+"/.htaccess",io.BytesIO(b"Options -Indexes\nRequire all denied\n"))
 if get(ftp,backup+"/inventory.json")!=inv: raise RuntimeError("INVENTORY_BACKUP_MISMATCH")
 print("INVENTORY_BACKUP_VERIFIED",backup,hashlib.sha256(inv).hexdigest(),flush=True)
 try:
  for name,data in FILES.items():
   temp=posixpath.join(root,".upload-"+name+"-"+STAMP)
   final=posixpath.join(root,name)
   ftp.storbinary("STOR "+temp,io.BytesIO(data))
   if get(ftp,temp)!=data: raise RuntimeError("TEMP_VERIFY_FAILED "+name)
   ftp.rename(temp,final)
   if get(ftp,final)!=data: raise RuntimeError("FINAL_VERIFY_FAILED "+name)
   created.append((final,data))
   print("FTP_CREATED_VERIFIED",name,hashlib.sha256(data).hexdigest(),flush=True)
 except Exception:
  for path,data in reversed(created):
   try:
    if get(ftp,path)==data: ftp.delete(path)
   except ftplib.all_errors: pass
  print("ROLLBACK_CREATED_FILES_COMPLETED",flush=True)
  raise

last=None
for attempt in range(3):
 try:
  status,body=public_get("")
  text=body.decode("utf-8","replace")
  if status!=200 or "Index of /" in text or '<link rel="canonical" href="'+PUBLIC+'">' not in text or 'data-aq-aeo="ARQ-153"' not in text or 'id="arq-floating"' not in text:
   raise RuntimeError("PUBLIC_HTML_INVALID")
  for name,needle in [("robots.txt","Sitemap: "+PUBLIC+"sitemap.xml"),("sitemap.xml","<loc>"+PUBLIC+"</loc>")]:
   st,b=public_get(name)
   if st!=200 or needle not in b.decode("utf-8","replace"): raise RuntimeError("PUBLIC_"+name+"_INVALID")
  print("PUBLIC_VERIFIED",PUBLIC,hashlib.sha256(body).hexdigest(),flush=True); last=None; break
 except Exception as exc:
  last=exc
  if attempt<2: time.sleep(8)
if last: raise last

key=(os.environ.get("INDEXNOW_KEY") or "").strip()
if not key:
 print("INDEXNOW_SKIPPED_KEY_EMPTY",flush=True)
else:
 try:
  st,keybody=public_get(key+".txt")
  if st!=200 or keybody.decode().strip()!=key: raise RuntimeError("INDEXNOW_PUBLIC_KEY_INVALID")
  payload=json.dumps({"host":HOSTNAME,"key":key,"keyLocation":PUBLIC+key+".txt","urlList":[PUBLIC]}).encode()
  req=urllib.request.Request("https://api.indexnow.org/indexnow",data=payload,headers={"Content-Type":"application/json","User-Agent":"ArquindexSEO/1.0"},method="POST")
  with urllib.request.urlopen(req,timeout=30) as r: print("INDEXNOW_RESPONSE",r.status,flush=True)
 except Exception as exc:
  print("INDEXNOW_NOT_CONFIRMED",type(exc).__name__,str(exc),flush=True)
