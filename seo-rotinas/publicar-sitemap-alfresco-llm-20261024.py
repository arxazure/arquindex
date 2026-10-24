#!/usr/bin/env python3
"""Sitemap Alfresco: atualização existing-first + IndexNow, com TLS, backup e validação."""
import ftplib, hashlib, io, json, os, re, socket, ssl, time, urllib.request, xml.etree.ElementTree as ET
from datetime import datetime, timezone
NS="http://www.sitemaps.org/schemas/sitemap/0.9"
ET.register_namespace("",NS)
FILE="sitemap-alfresco-cloud-20261021.xml"
ROOT="https://www.arquindex.com.br/"
CHANGED={
ROOT+"blog/alfresco-cloud-ocr-inteligencia-documental/":"2026-10-24",
ROOT+"blog/tco-alfresco-cloud-versus-saas/":"2026-10-24",
ROOT+"blog/ocr-inteligente-vs-busca-ecm/":"2026-10-22",
}
def sha(x):return hashlib.sha256(x).hexdigest()
def get(ftp,p):
 b=io.BytesIO();ftp.retrbinary("RETR "+p,b.write);return b.getvalue()
def put(ftp,p,b):ftp.storbinary("STOR "+p,io.BytesIO(b))
def fetch(u):
 req=urllib.request.Request(u+"?review="+str(int(time.time())),headers={"User-Agent":"ArquindexSitemap/1.0","Cache-Control":"no-cache"})
 with urllib.request.urlopen(req,timeout=30) as res:return res.status,res.read()
def parse(b):
 root=ET.fromstring(b)
 assert root.tag=="{"+NS+"}urlset","UNEXPECTED_SITEMAP_SCHEMA"
 urls={}
 for item in root.findall("{"+NS+"}url"):
  loc=item.findtext("{"+NS+"}loc")
  assert loc and loc.startswith(ROOT),"INVALID_HOST"
  assert loc not in urls,"DUPLICATE_URL"
  urls[loc]=item
 return root,urls
def main():
 pw=os.environ.get("FTP_PASSWORD")
 assert pw,"FTP_PASSWORD_MISSING"
 host=(os.environ.get("FTP_TLS_HOST") or "h59.servidorhh.com").strip()
 directory=(os.environ.get("FTP_REMOTE_DIR") or "public_html").strip("/")
 assert re.fullmatch("[A-Za-z0-9._-]+",directory),"INVALID_DIRECTORY"
 expected=set(socket.gethostbyname_ex("ftp.arquindex.com.br")[2])
 assert expected.intersection(socket.gethostbyname_ex(host)[2]),"HOST_MISMATCH"
 ctx=ssl.create_default_context();ctx.minimum_version=ssl.TLSVersion.TLSv1_2
 with ftplib.FTP_TLS(timeout=50,context=ctx) as ftp:
  ftp.connect(host,21);assert ftp.sock.getpeername()[0] in expected,"REMOTE_IP_MISMATCH"
  ftp.auth();ftp.login("arquind2",pw);ftp.prot_p();ftp.cwd(directory)
  old=get(ftp,FILE)
  root,urls=parse(old)
  assert len(urls)>=10,"UNEXPECTED_SITEMAP"
  for url,lastmod in CHANGED.items():
   if url in urls:
    lm=urls[url].find("{"+NS+"}lastmod")
    if lm is None:lm=ET.SubElement(urls[url],"{"+NS+"}lastmod")
    lm.text=lastmod
   else:
    el=ET.SubElement(root,"{"+NS+"}url")
    ET.SubElement(el,"{"+NS+"}loc").text=url
    ET.SubElement(el,"{"+NS+"}lastmod").text=lastmod
  new=ET.tostring(root,encoding="utf-8",xml_declaration=True)
  assert set(parse(new)[1])==set(urls)|set(CHANGED),"URL_SET_MISMATCH"
  if new!=old:
   backup=FILE+".backup."+datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
   put(ftp,backup,old);assert get(ftp,backup)==old,"BACKUP_FAILED"
   assert get(ftp,FILE)==old,"CONCURRENT_CHANGE"
   try:
    put(ftp,FILE,new);assert get(ftp,FILE)==new,"UPLOAD_FAILED"
   except Exception:
    if get(ftp,FILE)==new:put(ftp,FILE,old)
    raise
   print("SITEMAP_BACKUP_AND_FTPS_UPLOAD_VERIFIED",len(CHANGED),sha(new))
  else:print("SITEMAP_ALREADY_CURRENT")
  keybytes=None
  try:keybytes=get(ftp,"indexnow-key.txt")
  except ftplib.error_perm:pass
 status,public=fetch(ROOT+FILE)
 assert status==200,"SITEMAP_HTTP_NOT_200"
 assert set(CHANGED).issubset(parse(public)[1]),"SITEMAP_PUBLIC_URLS_MISSING"
 print("SITEMAP_PUBLIC_HTTP200_URLS_VERIFIED",len(parse(public)[1]))
 if not keybytes:
  print("INDEXNOW_SKIPPED_KEY_MISSING");return
 key=keybytes.decode("ascii").strip()
 assert re.fullmatch("[A-Za-z0-9-]{8,128}",key),"INDEXNOW_KEY_FORMAT_INVALID"
 keyurl=ROOT+key+".txt"
 code,publickey=fetch(keyurl)
 assert code==200 and publickey.decode("ascii").strip()==key,"INDEXNOW_KEY_NOT_PUBLIC"
 payload=json.dumps({"host":"www.arquindex.com.br","key":key,"keyLocation":keyurl,"urlList":list(CHANGED)}).encode("utf-8")
 request=urllib.request.Request("https://api.indexnow.org/indexnow",data=payload,headers={"Content-Type":"application/json","User-Agent":"ArquindexIndexNow/1.0"},method="POST")
 try:
  with urllib.request.urlopen(request,timeout=30) as res:
   print("INDEXNOW_RESPONSE",res.status,"URL_COUNT",len(CHANGED),"ACCEPTED_NOT_INDEXED")
 except urllib.error.HTTPError as exc:
  print("INDEXNOW_NOT_ACCEPTED_HTTP",exc.code)
  raise
if __name__=="__main__":main()
