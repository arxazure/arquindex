#!/usr/bin/env python3
"""Read-only preflight of a public social image URL.

No social API calls or publication. DNS checks and redirect refusal reduce SSRF risk;
for hostile DNS-rebinding environments, enforce egress restrictions at infrastructure.
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
    return bool(addresses) and all(
        ipaddress.ip_address(item[4][0]).is_global for item in addresses
    )

def verify_media(url):
    if not isinstance(url, str):
        raise ValueError("INVALID_MEDIA_URL")
    try:
        parts = urlsplit(url)
        port = parts.port
    except ValueError as exc:
        raise ValueError("INVALID_MEDIA_URL") from exc
    if (parts.scheme != "https" or port not in (None, 443)
            or not parts.hostname or parts.username or parts.password
            or parts.fragment):
        raise ValueError("INVALID_MEDIA_URL")
    if not _public_host(parts.hostname):
        raise ValueError("MEDIA_HOST_NOT_PUBLIC")

    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            return None

    opener = urllib.request.build_opener(NoRedirect)
    request = urllib.request.Request(
        url, headers={"User-Agent": "ArquindexMediaPreflight/1.1", "Accept": "image/*"}
    )
    try:
        with opener.open(request, timeout=TIMEOUT) as response:
            mime = response.headers.get_content_type()
            if response.status != 200 or mime not in ALLOWED_TYPES:
                raise ValueError("MEDIA_HTTP_OR_MIME_INVALID")
            length = response.headers.get("Content-Length")
            if length is not None:
                try:
                    size = int(length)
                except ValueError as exc:
                    raise ValueError("MEDIA_INVALID_LENGTH") from exc
                if size <= 0 or size > MAX_BYTES:
                    raise ValueError("MEDIA_EMPTY_OR_TOO_LARGE")
            data = response.read(MAX_BYTES + 1)
            if not data or len(data) > MAX_BYTES:
                raise ValueError("MEDIA_EMPTY_OR_TOO_LARGE")
            signatures = {
                "image/jpeg": data.startswith(bytes.fromhex("ffd8ff")),
                "image/png": data.startswith(bytes.fromhex("89504e470d0a1a0a")),
                "image/webp": data.startswith(b"RIFF") and data[8:12] == b"WEBP",
            }
            if not signatures[mime]:
                raise ValueError("MEDIA_BYTES_MISMATCH")
            # Decode entire image to catch truncation/corruption if Pillow is installed.
            try:
                from PIL import Image
            except ImportError:
                pass
            else:
                from io import BytesIO
                try:
                    with Image.open(BytesIO(data)) as image:
                        image.verify()
                except Exception as exc:
                    raise ValueError("MEDIA_DECODE_FAILED") from exc
            return {"content_type": mime, "bytes": len(data), "verified": True}
    except urllib.error.HTTPError as exc:
        raise ValueError("MEDIA_HTTP_ERROR_" + str(exc.code)) from exc
