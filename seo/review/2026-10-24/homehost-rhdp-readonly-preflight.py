#!/usr/bin/env python3
"""Preflight read-only para a pagina institucional RH/DP no HomeHost.

Nao faz upload, exclusao ou alteracao no servidor.
Requer FTP_PASSWORD no ambiente seguro do executor.
"""
import ftplib
import hashlib
import json
import os
import re
import ssl
from datetime import datetime, timezone
from html.parser import HTMLParser

TARGET = "gestao_de_colaboradores_documentos.html"
HOST = os.getenv("FTP_TLS_HOST", "h59.servidorhh.com")
USER = os.getenv("FTP_USER", "arquind2")
ROOTS = ("/public_html", "/home/arquind2/public_html")

class Metadata(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = ""
        self.h1_count = 0
        self.canonicals = []
        self._title = False
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "title": self._title = True
        if tag == "h1": self.h1_count += 1
        if tag == "link" and a.get("rel", "").lower() == "canonical":
            self.canonicals.append(a.get("href", ""))
    def handle_endtag(self, tag):
        if tag == "title": self._title = False
    def handle_data(self, data):
        if self._title: self.title += data

def main():
    password = os.environ.get("FTP_PASSWORD")
    if not password: raise SystemExit("FTP_PASSWORD_MISSING: use GitHub Actions secret")
    ctx = ssl.create_default_context()
    ctx.minimum_version = ssl.TLSVersion.TLSv1_2
    with ftplib.FTP_TLS(timeout=45, context=ctx) as ftp:
        ftp.connect(HOST, 21)
        ftp.login(USER, password)
        ftp.prot_p()
        ftp.set_pasv(True)
        chosen = None
        raw = None
        for root in ROOTS:
            try:
                ftp.cwd(root)
                data = bytearray()
                ftp.retrbinary("RETR " + TARGET, data.extend)
                if b"<html" in data.lower():
                    chosen, raw = root, bytes(data)
                    break
            except ftplib.all_errors:
                continue
        if raw is None: raise SystemExit("TARGET_NOT_FOUND: no changes made")
    html = raw.decode("utf-8")
    p = Metadata()
    p.feed(html)
    expected = "https://www.arquindex.com.br/" + TARGET
    report = {
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "state": "read_only_no_deploy",
        "server": HOST,
        "root": chosen,
        "filename": TARGET,
        "size_bytes": len(raw),
        "sha256": hashlib.sha256(raw).hexdigest(),
        "title": p.title.strip(),
        "h1_count": p.h1_count,
        "canonical": p.canonicals,
        "canonical_expected": expected,
        "canonical_matches": p.canonicals == [expected],
        "has_body_close": bool(re.search(r"</body\s*>", html, re.I)),
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if not report["has_body_close"] or report["h1_count"] != 1 or not report["canonical_matches"]:
        raise SystemExit("PREFLIGHT_REVIEW_REQUIRED: no changes made")

if __name__ == "__main__":
    main()
