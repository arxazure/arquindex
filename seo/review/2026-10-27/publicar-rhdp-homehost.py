#!/usr/bin/env python3
"""Integracao RH/DP no HomeHost com backup e validacao. DRY RUN por padrao.

Uso no runner autorizado, com FTP_PASSWORD configurada:
 python seo/review/2026-10-27/publicar-rhdp-homehost.py
 python seo/review/2026-10-27/publicar-rhdp-homehost.py --publish --backup-confirmed

Publicacao exige backup integral previamente validado pelo operador.
Nunca exclui arquivos; cria backup remoto do HTML original antes do STOR.
"""
import argparse
import ftplib
import hashlib
import io
import os
from pathlib import Path
import re
import ssl
from datetime import datetime, timezone
from html.parser import HTMLParser

NAME = "gestao_de_colaboradores_documentos.html"
FRAGMENT = Path(__file__).with_name("rhdp-dossies-bloco-editorial.html")
MARK_START = "<!-- ARQ_RHDP_UPDATE_START -->"
MARK_END = "<!-- ARQ_RHDP_UPDATE_END -->"

class Structure(HTMLParser):
    def __init__(self):
        super().__init__()
        self.h1 = 0
        self.canonical = []
    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == "h1": self.h1 += 1
        if tag == "link" and "canonical" in d.get("rel", "").lower().split():
            self.canonical.append(d.get("href", ""))

def validate(html):
    p = Structure()
    p.feed(html)
    expected = "https://www.arquindex.com.br/" + NAME
    if p.h1 != 1 or p.canonical != [expected]:
        raise RuntimeError("HTML_STRUCTURE_REVIEW_REQUIRED: H1 or canonical unexpected")
    if len(re.findall(r"</body\s*>", html, re.I)) != 1:
        raise RuntimeError("HTML_BODY_REVIEW_REQUIRED")

def integrate(html, fragment):
    if MARK_START in html or MARK_END in html:
        if html.count(MARK_START) != 1 or html.count(MARK_END) != 1:
            raise RuntimeError("AMBIGUOUS_EXISTING_MARKERS")
        pattern = re.escape(MARK_START) + r".*?" + re.escape(MARK_END)
        return re.sub(pattern, lambda _: MARK_START + "\n" + fragment + "\n" + MARK_END, html, flags=re.S)
    return re.sub(r"</body\s*>", lambda m: MARK_START + "\n" + fragment + "\n" + MARK_END + "\n" + m.group(), html, count=1, flags=re.I)

def read(ftp, name):
    data = bytearray()
    ftp.retrbinary("RETR " + name, data.extend)
    return bytes(data)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--publish", action="store_true")
    parser.add_argument("--backup-confirmed", action="store_true")
    args = parser.parse_args()
    if args.publish and not args.backup_confirmed:
        raise SystemExit("BLOCKED: confirm full backup before publication")
    password = os.environ.get("FTP_PASSWORD")
    if not password:
        raise SystemExit("FTP_PASSWORD_MISSING")
    fragment = FRAGMENT.read_text(encoding="utf-8").strip()
    if fragment.count('<section id="arquindex-dossies-rhdp"') != 1:
        raise SystemExit("INVALID_FRAGMENT")
    ctx = ssl.create_default_context()
    ctx.minimum_version = ssl.TLSVersion.TLSv1_2
    with ftplib.FTP_TLS(timeout=60, context=ctx) as ftp:
        ftp.connect(os.getenv("FTP_TLS_HOST", "h59.servidorhh.com"), 21)
        ftp.login(os.getenv("FTP_USER", "arquind2"), password)
        ftp.prot_p()
        for root in ("/public_html", "/home/arquind2/public_html"):
            try:
                ftp.cwd(root)
                original = read(ftp, NAME)
                break
            except ftplib.all_errors:
                continue
        else:
            raise RuntimeError("SOURCE_HTML_NOT_FOUND")
        text = original.decode("utf-8")
        validate(text)
        updated = integrate(text, fragment)
        validate(updated)
        if updated == text:
            print("UNCHANGED: target already current")
            return
        old_hash = hashlib.sha256(original).hexdigest()
        print("PREVIEW:", NAME, "original_sha256=", old_hash, "updated_sha256=", hashlib.sha256(updated.encode()).hexdigest(), "bytes=", len(updated.encode()))
        if not args.publish:
            print("DRY_RUN: no remote changes")
            return
        # Re-read immediately before writing to prevent overwriting a concurrent edit.
        if hashlib.sha256(read(ftp, NAME)).hexdigest() != old_hash:
            raise RuntimeError("SOURCE_CHANGED_ABORT")
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        backup_name = NAME + ".backup-rhdp-" + stamp
        ftp.storbinary("STOR " + backup_name, io.BytesIO(original))
        if hashlib.sha256(read(ftp, backup_name)).digest() != hashlib.sha256(original).digest():
            raise RuntimeError("BACKUP_READBACK_MISMATCH: original untouched")
        try:
            ftp.storbinary("STOR " + NAME, io.BytesIO(updated.encode("utf-8")))
            if hashlib.sha256(read(ftp, NAME)).hexdigest() != hashlib.sha256(updated.encode()).hexdigest():
                raise RuntimeError("DEPLOY_READBACK_MISMATCH")
        except Exception:
            # Restore the exact bytes captured before the update.
            ftp.storbinary("STOR " + NAME, io.BytesIO(original))
            raise
        print("PUBLISHED", NAME, "BACKUP", backup_name)

if __name__ == "__main__":
    main()
