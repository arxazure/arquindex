#!/usr/bin/env python3
"""Publish Arquindex editorial pages to HomeHost via FTPS, with dry-run by default.
Never overwrites an existing different file. Pass --publish intentionally.
Requires FTP_PASSWORD only in publish mode; verifies HTTPS after upload.
"""
import argparse
import ftplib
import hashlib
import io
import os
import pathlib
import ssl
import sys
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent
SLUGS = (
    "custo-total-ecm-alfresco",
    "digitalizacao-decreto-10278-metadados",
    "bpo-documental-departamento-pessoal",
    "guarda-documental-ou-digitalizacao",
)
PUBLIC_BASE = "https://www.arquindex.com.br/guias/"

def validate_page(path, slug):
    data = path.read_bytes()
    text = data.decode("utf-8")
    expected = PUBLIC_BASE + slug + "/"
    assert '<html lang="pt-BR">' in text, path
    assert 'rel="canonical" href="' + expected + '"' in text, path
    assert '<meta name="robots" content="index,follow">' in text, path
    assert '"@type": "Article"' in text, path
    assert 'noindex' not in text.lower(), path
    return data

def ensure_dir(ftp, name):
    try:
        ftp.cwd(name)
    except ftplib.error_perm as exc:
        if not str(exc).startswith("550"):
            raise
        ftp.mkd(name)
        ftp.cwd(name)

def publish(ftp, slug, data):
    ftp.cwd("/public_html")
    ensure_dir(ftp, "guias")
    ensure_dir(ftp, slug)
    previous = io.BytesIO()
    try:
        ftp.retrbinary("RETR index.html", previous.write)
    except ftplib.error_perm as exc:
        if not str(exc).startswith("550"):
            raise
    if previous.getvalue() and previous.getvalue() != data:
        raise RuntimeError("ABORT: target already exists with different content: " + slug)
    if previous.getvalue() != data:
        ftp.storbinary("STOR index.html", io.BytesIO(data))
    check = io.BytesIO()
    ftp.retrbinary("RETR index.html", check.write)
    if check.getvalue() != data:
        raise RuntimeError("Remote bytes mismatch: " + slug)

def check_http(slug, expected):
    url = PUBLIC_BASE + slug + "/"
    req = urllib.request.Request(url, headers={"User-Agent": "Arquindex-SEO-Release-Check/1.0"})
    with urllib.request.urlopen(req, timeout=35) as res:
        body = res.read()
        if res.status != 200 or hashlib.sha256(body).digest() != hashlib.sha256(expected).digest():
            raise RuntimeError("Public HTTP verification failed: " + url)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--publish", action="store_true", help="Explicitly deploy files using FTPS")
    args = parser.parse_args()
    pages = [(s, validate_page(ROOT / "guias" / s / "index.html", s)) for s in SLUGS]
    for slug, data in pages:
        print("VALIDATED", slug, "sha256=" + hashlib.sha256(data).hexdigest())
    if not args.publish:
        print("DRY_RUN_ONLY: no connection or changes; use --publish after editorial approval")
        return
    password = os.environ.get("FTP_PASSWORD")
    if not password:
        raise RuntimeError("FTP_PASSWORD is required for --publish; never commit credentials")
    with ftplib.FTP_TLS(context=ssl.create_default_context(), timeout=40) as ftp:
        ftp.connect(os.environ.get("FTP_HOST", "h59.servidorhh.com"), 21)
        ftp.login(os.environ.get("FTP_USER", "arquind2"), password)
        ftp.prot_p()
        for slug, data in pages:
            publish(ftp, slug, data)
            print("FTPS_VERIFIED", slug)
    for slug, data in pages:
        check_http(slug, data)
        print("PUBLIC_HTTP200_VERIFIED", PUBLIC_BASE + slug + "/")

if __name__ == "__main__":
    main()
