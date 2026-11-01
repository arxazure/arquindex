#!/usr/bin/env python3
"""Image media preflight for Arquindex social publishing (read-only HTTP).

Call verify_media(media_url) before any API create-image-post call.
No post creation and no remote mutations occur here.
"""
import ipaddress
import socket
import urllib.error
import urllib.request
from urllib.parse import urlsplit

ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp"}
MAX_BYTES = 10 * 1024 * 1024
TIMEOUT = 12

def _public_host(host):
    if not host:
        return False
    try:
        addresses = socket.getaddrinfo(host, 443, type=socket.SOCK_STREAM)
    except OSError:
        return False
    if not addresses:
        return False
    for item in addresses:
        ip = ipaddress.ip_address(item[4][0])
        if not ip.is_global:
            return False
    return True

def verify_media(url):
    parts = urlsplit(url)
    if parts.scheme != "https" or parts.port not in (None, 443) or parts.username or parts.password:
        raise ValueError("INVALID_MEDIA_URL")
    if not _public_host(parts.hostname):
        raise ValueError("MEDIA_HOST_NOT_PUBLIC")
    # Do not follow redirects; each new destination must be validated separately.
    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            return None
    opener = urllib.request.build_opener(NoRedirect)
    req = urllib.request.Request(url, headers={"User-Agent": "ArquindexMediaPreflight/1.0", "Accept": "image/*"})
    try:
        with opener.open(req, timeout=TIMEOUT) as response:
            mime = response.headers.get_content_type()
            if response.status != 200 or mime not in ALLOWED_TYPES:
                raise ValueError("MEDIA_HTTP_OR_MIME_INVALID")
            length = response.headers.get("Content-Length")
            if length and int(length) > MAX_BYTES:
                raise ValueError("MEDIA_TOO_LARGE")
            data = response.read(MAX_BYTES + 1)
            if not data or len(data) > MAX_BYTES:
                raise ValueError("MEDIA_EMPTY_OR_TOO_LARGE")
            if mime == "image/jpeg" and not data.startswith(bytes.fromhex("ffd8ff")):
                raise ValueError("MEDIA_BYTES_MISMATCH")
            if mime == "image/png" and not data.startswith(bytes.fromhex("89504e470d0a1a0a")):
                raise ValueError("MEDIA_BYTES_MISMATCH")
            if mime == "image/webp" and not (data.startswith(b"RIFF") and data[8:12] == b"WEBP"):
                raise ValueError("MEDIA_BYTES_MISMATCH")
            return {"content_type": mime, "bytes": len(data), "verified": True}
    except urllib.error.HTTPError as e:
        raise ValueError("MEDIA_HTTP_ERROR_" + str(e.code)) from e
