"""Idempotent HomeHost IndexNow key setup with FTP TLS + public HTTP verification."""
import ftplib
import io
import json
import os
import re
import time
import uuid
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

HOST = "www.arquindex.com.br"
ROOT = "/public_html"
REPORT = Path("publish-report/indexnow-key-status.json")
REPORT.parent.mkdir(parents=True, exist_ok=True)
state = {"host": HOST, "checked_at": datetime.now(timezone.utc).isoformat(),
         "status": "blocked", "key_file_url": None, "created": [], "reason": None}

def record():
    REPORT.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def read(ftp, name):
    data = bytearray()
    try:
        ftp.retrbinary("RETR " + name, data.extend)
    except ftplib.error_perm as err:
        if str(err).startswith("550"):
            return None
        raise
    return bytes(data)

def write_new(ftp, name, content):
    if read(ftp, name) is not None:
        raise RuntimeError("ALREADY_EXISTS_CONFLICT: " + name)
    ftp.storbinary("STOR " + name, io.BytesIO(content))
    if read(ftp, name) != content:
        raise RuntimeError("FTP_READBACK_MISMATCH: " + name)
    state["created"].append(name)

def verify_public(url, key):
    req = urllib.request.Request(url, headers={
        "User-Agent": "ArquindexIndexNowVerification/1.0",
        "Cache-Control": "no-cache"
    })
    with urllib.request.urlopen(req, timeout=35) as res:
        body = res.read(256)
        if res.status != 200 or res.geturl().split("/")[2].lower() != HOST:
            raise RuntimeError("PUBLIC_HTTP_OR_HOST_NOT_VALID")
        if body.decode("ascii").strip() != key:
            raise RuntimeError("PUBLIC_KEY_CONTENT_MISMATCH")

def main():
    password = os.environ.get("FTP_PASSWORD", "")
    if not password:
        raise RuntimeError("FTP_PASSWORD secret missing: GitHub Settings > Secrets and variables > Actions")
    with ftplib.FTP_TLS(timeout=45) as ftp:
        ftp.connect("ftp.arquindex.com.br", 21)
        ftp.login("arquind2", password)
        ftp.prot_p()
        ftp.set_pasv(True)
        ftp.cwd(ROOT)
        if read(ftp, "sitemap.xml") is None and read(ftp, "index.html") is None:
            raise RuntimeError("FTP_ROOT_NOT_CONFIRMED: neither sitemap.xml nor index.html in /public_html")
        existing = read(ftp, "indexnow-key.txt")
        if existing is not None:
            key = existing.decode("ascii").strip()
            if not re.fullmatch(r"[A-Za-z0-9-]{8,128}", key):
                raise RuntimeError("EXISTING_KEY_INVALID_FORMAT; no overwrite")
            state["mode"] = "reuse-existing"
        else:
            key = uuid.uuid4().hex
            state["mode"] = "new-key"
        filename = key + ".txt"
        current = read(ftp, filename)
        if current is None:
            write_new(ftp, filename, (key + "\n").encode("ascii"))
        elif current.decode("ascii").strip() != key:
            raise RuntimeError("ROOT_KEY_FILE_CONFLICT; no overwrite")
        if existing is None:
            write_new(ftp, "indexnow-key.txt", (key + "\n").encode("ascii"))
        state["key_file_url"] = "https://" + HOST + "/" + filename
        state["status"] = "ftp-readback-ok-public-pending"
        record()
    last = None
    for attempt in range(3):
        try:
            verify_public(state["key_file_url"], key)
            state["status"] = "verified-public-http-200"
            state["reason"] = None
            record()
            print("INDEXNOW_KEY_PUBLIC_HTTP_200_VERIFIED", state["key_file_url"])
            return
        except Exception as err:
            last = str(err)
            if attempt < 2:
                time.sleep(5)
    state["status"] = "ftp-readback-ok-public-verification-blocked"
    state["reason"] = last
    record()
    raise RuntimeError("INDEXNOW_NOT_PUBLICLY_VERIFIED: " + str(last))

if __name__ == "__main__":
    try:
        main()
    except Exception as err:
        state["reason"] = state.get("reason") or str(err)
        record()
        raise
