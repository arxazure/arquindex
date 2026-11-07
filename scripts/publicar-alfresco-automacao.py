"""Read-only FTPS preflight for Arquindex. No deployment capability in Phase A."""
import argparse
import ftplib
import hashlib
import json
import os
from pathlib import Path
import ssl
import sys
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "publish-report/alfresco-automacao/diagnostic.json"
MANIFEST = ROOT / "seo/alfresco-automacao-manifest.json"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def safe_path(path):
    p = Path(path)
    if p.is_absolute() or ".." in p.parts or not path or "\\" in path:
        raise ValueError("UNSAFE_MANIFEST_PATH")
    return p.as_posix()


def inventory():
    rows = json.loads(MANIFEST.read_text(encoding="utf-8"))
    files = {}
    for row in rows:
        path = safe_path(row["path"])
        if not row["url"].startswith("https://www.arquindex.com.br/") or row["url"].split("?", 1)[0].split("#", 1)[0].rstrip("/") != ("https://www.arquindex.com.br/" + path.removesuffix("index.html")).rstrip("/"):
            raise ValueError("NON_CANONICAL_URL")
        files[path] = digest((ROOT / path).read_bytes())
    path = "sitemap-alfresco-automacao.xml"
    files[path] = digest((ROOT / path).read_bytes())
    return files


def validate_config(host, user, password, public_root):
    if not all((host, user, password, public_root)):
        raise ValueError("FTPS_CONFIG_MISSING")
    if any(c in host for c in "/:@ \\t\\n\\r") or host.startswith(".") or host.endswith("."):
        raise ValueError("INVALID_FTPS_HOST")
    if (not public_root.startswith("/") or public_root == "/"
            or any(part in ("", ".", "..") for part in public_root[1:].split("/"))
            or "\\\\" in public_root):
        raise ValueError("INVALID_PUBLIC_ROOT")
    return True


def preflight(host, user, password, public_root, factory=ftplib.FTP_TLS):
    validate_config(host, user, password, public_root)
    # Explicit FTPS, verified server certificate, encrypted data channel.
    with factory(context=ssl.create_default_context(), timeout=25) as ftp:
        ftp.connect(host, 21)
        ftp.login(user, password)
        ftp.prot_p()
        original = ftp.pwd()
        ftp.cwd(public_root)
        confirmed = ftp.pwd()
        ftp.cwd(original)
        # No STOR, MKD, DELE, RNFR/RNTO or site-changing commands.
        return {"tls_verified": True, "login_verified": True,
                "remote_root_readable": True, "remote_pwd": confirmed,
                "public_http_mapping_verified": False,
                "backup_restoration_verified": False}


def diagnose():
    result = {"mode": "read_only", "timestamp_utc": datetime.now(timezone.utc).isoformat(),
              "ftps_verified": False, "public_http_verified": False,
              "sitemap_submitted": False, "indexed": False}
    try:
        result["local_sha256"] = inventory()
        result.update(preflight(os.getenv("FTP_TLS_HOST", ""),
                                os.getenv("FTP_USER", ""),
                                os.getenv("FTP_PASSWORD", ""),
                                os.getenv("FTP_PUBLIC_ROOT", "")))
        result["ftps_verified"] = True
    except (ValueError, OSError, ftplib.Error, ssl.SSLError) as exc:
        result["error_type"] = type(exc).__name__
        # Do not expose server response strings, usernames, passwords or paths.
        result["error_code"] = (
            "TLS_CERTIFICATE_INVALID" if isinstance(exc, ssl.SSLCertVerificationError)
            else "FTPS_PREFLIGHT_FAILED" if isinstance(exc, (OSError, ftplib.Error, ssl.SSLError))
            else str(exc))
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print("FTPS_DIAGNOSTIC:", result.get("error_code", "READ_ONLY_OK"))
    return 0 if result["ftps_verified"] else 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--diagnose", action="store_true")
    args = parser.parse_args()
    if not args.diagnose:
        parser.error("Deployment disabled in Phase A. Use --diagnose only.")
    sys.exit(diagnose())
