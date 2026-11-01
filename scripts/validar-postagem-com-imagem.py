#!/usr/bin/env python3
"""Structural gate for Arquindex image posts; does not publish."""
import json
import sys
from urllib.parse import urlsplit

LIMITS = {"linkedin": 3000, "instagram": 2200, "google": 1500}
MEDIA_EXTENSIONS = (".jpg", ".jpeg", ".png", ".webp")
RECONCILE = {"unknown", "accepted", "published"}

def validate(post):
    errors = []
    if not isinstance(post, dict):
        return ["INVALID_POST"]
    channel = str(post.get("channel", "")).strip().lower()
    if channel not in LIMITS:
        errors.append("INVALID_CHANNEL")
    body = post.get("body")
    if not isinstance(body, str) or not body.strip():
        errors.append("EMPTY_BODY")
    elif channel in LIMITS and len(body) > LIMITS[channel]:
        errors.append("BODY_TOO_LONG")
    media = post.get("media")
    if not isinstance(media, str) or not media.strip():
        errors.append("MISSING_IMAGE")
    else:
        try:
            url = urlsplit(media.strip())
            port = url.port
            if (url.scheme != "https" or not url.hostname or port not in (None, 443)
                    or url.username or url.password or url.fragment):
                errors.append("INVALID_IMAGE_URL")
            if not url.path.lower().endswith(MEDIA_EXTENSIONS):
                errors.append("UNSUPPORTED_IMAGE_FORMAT")
        except ValueError:
            errors.append("INVALID_IMAGE_URL")
    if post.get("state") in RECONCILE:
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
    print("PRECHECK_OK: verify media HTTP and platform rendering before publishing")

if __name__ == "__main__":
    main()
