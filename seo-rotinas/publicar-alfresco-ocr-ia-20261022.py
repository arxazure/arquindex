#!/usr/bin/env python3
"""Atualização idempotente de URLs existentes com FTPS TLS, backup, verificação e rollback."""
import ftplib, hashlib, io, json, os, re, socket, ssl, time, urllib.request
from datetime import datetime, timezone
from pathlib import Path
from bs4 import BeautifulSoup

ROOT="https://www.arquindex.com.br/"
DATA=json.loads(Path("seo-rotinas/alfresco-ocr-ia-existing-first-20261022.json").read_text(encoding="utf-8"))
BLOCKS=DATA["blocks"]
STAMP=datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
MARKER="arq-ia-leitura-documental-20261022"
def sha(b):return hashlib.sha256(b).hexdigest()
def get(f,p):
    buf=io.BytesIO();f.retrbinary("RETR "+p,buf.write);return buf.getvalue()
def put(f,p,b):f.storbinary("STOR "+p,io.BytesIO(b))
def check_html(b,path,with_marker):
    soup=BeautifulSoup(b.decode("utf-8"),"html.parser")
    assert soup.find("main"),("MISSING_MAIN",path)
    assert len(soup.find_all("h1"))>=1,("MISSING_H1",path)
    assert soup.find("title"),("MISSING_TITLE",path)
    assert not any("noindex" in (x.get("content") or "").lower() for x in soup.find_all("meta",attrs={"name":re.compile(r"^(robots|googlebot)$",re.I)})),("NOINDEX",path)
    if with_marker:
        assert len(soup.find_all(id=MARKER))==1,("DUPLICATE_MARKER",path)
    return soup
def patch(b,path,block):
    old=check_html(b,path,False)
    text=b.decode("utf-8")
    soupblock=BeautifulSoup(block,"html.parser")
    assert soupblock.find("section",id=MARKER),"BLOCK_MARKER_MISSING"
    if old.find(id=MARKER):
        pattern=r'<section\b[^>]*\bid=["\x27]'+MARKER+r'["\x27][^>]*>.*?</section>'
        text,n=re.subn(pattern,lambda _:block,text,count=1,flags=re.S|re.I)
        assert n==1,("REPLACE_FAILED",path)
    else:
        ends=list(re.finditer(r"</main\s*>",text,re.I))
        assert ends,("MAIN_END_NOT_FOUND",path)
        at=ends[-1].start()
        text=text[:at]+"\n"+block+"\n"+text[at:]
    result=text.encode("utf-8")
    new=check_html(result,path,True)
    assert [str(x) for x in old.find_all("script")]==[str(x) for x in new.find_all("script")],("SCRIPT_CHANGED",path)
    assert [str(x) for x in old.find_all("form")]==[str(x) for x in new.find_all("form")],("FORM_CHANGED",path)
    assert [x.get_text(" ",strip=True) for x in old.find_all("h1")]==[x.get_text(" ",strip=True) for x in new.find_all("h1")],("H1_CHANGED",path)
    assert [str(x) for x in old.find_all("link",rel="canonical")]==[str(x) for x in new.find_all("link",rel="canonical")],("CANONICAL_CHANGED",path)
    return result
def http(path):
    url=ROOT+path[:-10] if path.endswith("/index.html") else ROOT+path
    req=urllib.request.Request(url+"?iareview="+str(int(time.time())),headers={"User-Agent":"ArquindexAIExistingFirst/1.0","Cache-Control":"no-cache"})
    with urllib.request.urlopen(req,timeout=30) as resp:return url,resp.status,resp.headers,resp.read()
def main():
    assert len(BLOCKS)==12,"UNEXPECTED_TARGET_COUNT"
    pw=os.environ.get("FTP_PASSWORD")
    assert pw,"FTP_PASSWORD_MISSING"
    host=(os.environ.get("FTP_TLS_HOST") or "h59.servidorhh.com").strip()
    remote=(os.environ.get("FTP_REMOTE_DIR") or "public_html").strip("/")
    assert re.fullmatch(r"[A-Za-z0-9._-]+",remote),"UNSAFE_REMOTE_ROOT"
    expected=set(socket.gethostbyname_ex("ftp.arquindex.com.br")[2])
    assert expected.intersection(socket.gethostbyname_ex(host)[2]),"HOST_IP_MISMATCH"
    context=ssl.create_default_context();context.minimum_version=ssl.TLSVersion.TLSv1_2
    with ftplib.FTP_TLS(timeout=50,context=context) as ftp:
        ftp.connect(host,21)
        assert ftp.sock.getpeername()[0] in expected,"SERVER_IP_CHANGED"
        ftp.auth()
        print("FTPS_TLS_VERIFIED",host,flush=True)
        ftp.login("arquind2",pw);ftp.prot_p();ftp.cwd(remote)
        before={};after={}
        for path,block in BLOCKS.items():
            assert ".." not in path and path.endswith("/index.html"),("UNSAFE_PATH",path)
            try:before[path]=get(ftp,path)
            except ftplib.error_perm as e:raise RuntimeError("EXISTING_FIRST_MISSING "+path) from e
            after[path]=patch(before[path],path,block)
        print("ALL_TWELVE_EXISTING_FILES_PREFLIGHT_VALIDATED",flush=True)
        backups={};changed=[]
        for path in BLOCKS:
            if before[path]==after[path]:continue
            backup=path+".backup."+STAMP
            put(ftp,backup,before[path])
            assert get(ftp,backup)==before[path],("BACKUP_INVALID",path)
            backups[path]=backup
        print("ALL_BACKUPS_VERIFIED",len(backups),flush=True)
        try:
            for path in BLOCKS:
                if before[path]==after[path]:continue
                assert get(ftp,path)==before[path],("CONCURRENT_CHANGE",path)
                put(ftp,path,after[path]);changed.append(path)
                assert get(ftp,path)==after[path],("FTP_UPLOAD_INVALID",path)
            for path in BLOCKS:
                last=None
                for attempt in range(5):
                    try:
                        url,status,headers,body=http(path)
                        assert status==200,("HTTP",url,status)
                        assert MARKER.encode() in body,("MARKER_ABSENT",url)
                        assert "noindex" not in headers.get("X-Robots-Tag","").lower(),("NOINDEX_HEADER",url)
                        check_html(body,path,True)
                        print("PUBLIC_HTTP200_MARKER_VALIDATED",url,sha(body),flush=True)
                        last=None;break
                    except Exception as exc:
                        last=exc
                        if attempt<4:time.sleep(6)
                if last:raise last
            print("ALL_TWELVE_UPDATES_PUBLIC_CONFIRMED",flush=True)
        except Exception:
            print("ERROR_ROLLBACK_STARTED",flush=True)
            for path in reversed(changed):
                if get(ftp,path)==after[path]:
                    put(ftp,path,before[path])
                    assert get(ftp,path)==before[path],("ROLLBACK_FAILED",path)
                    print("ROLLBACK_VERIFIED",path,flush=True)
            raise
if __name__=="__main__":main()
