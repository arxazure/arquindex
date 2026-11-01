#!/usr/bin/env python3
"""Validador de publicacoes Arquindex: bloquear posts sem imagem.

Uso: python scripts/validar-postagem-com-imagem.py post.json
Entrada: {"channel":"linkedin|instagram|google","title":"...","body":"...","media":"https://...jpg"}
Nao faz publicacao; executa apenas verificacoes locais. O agendador deve usar
esta validacao antes de criar/encaminhar cada post e registrar o recibo remoto.
"""
import json
import re
import sys
from urllib.parse import urlsplit

CHANNELS = {"linkedin", "instagram", "google"}
MEDIA_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}

def validate(post):
    errors = []
    channel = str(post.get("channel", "")).strip().lower()
    if channel not in CHANNELS:
        errors.append("INVALID_CHANNEL")
    if not str(post.get("body", "")).strip():
        errors.append("EMPTY_BODY")
    media = post.get("media")
    if not isinstance(media, str) or not media.strip():
        errors.append("MISSING_IMAGE")
    else:
        url = urlsplit(media.strip())
        if url.scheme != "https" or not url.netloc or url.username or url.password:
            errors.append("INVALID_IMAGE_URL")
        if not any(url.path.lower().endswith(ext) for ext in MEDIA_EXTENSIONS):
            errors.append("UNSUPPORTED_IMAGE_FORMAT")
    if post.get("state") in {"unknown", "accepted", "published"}:
        errors.append("REQUIRES_REMOTE_STATUS_RECONCILIATION")
    return errors

def main():
    if len(sys.argv) != 2:
        raise SystemExit("Usage: validar-postagem-com-imagem.py post.json")
    with open(sys.argv[1], encoding="utf-8") as f:
        data = json.load(f)
    errors = validate(data)
    if errors:
        print("BLOCKED:", ",".join(errors))
        raise SystemExit(1)
    print("PRECHECK_OK: image URL declared; remote reachability and platform rendering still require verification")

if __name__ == "__main__":
    main()
