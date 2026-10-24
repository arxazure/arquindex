#!/usr/bin/env python3
"""Backup integral e inventário seguro do conteúdo público da Arquindex.

Não remove nem move arquivos. O relatório fica fora de public_html.
"""

import collections
import ftplib
import hashlib
import io
import json
import os
import posixpath
import re
import socket
import ssl
import tarfile
import tempfile
from datetime import datetime, timezone


STAMP = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
BACKUP_DIR = "seo-backups"
MAX_FILES = 200_000
MAX_BYTES = 8 * 1024 * 1024 * 1024
SYSTEM_ROOTS = {
    ".cpanel", ".trash", "etc", "logs", "mail", "tmp", "ssl",
    "public_ftp", BACKUP_DIR,
}
TEMP_RE = re.compile(r"(?:^|/)(?:cache|tmp|temp)(?:/|$)|(?:\.tmp|\.temp|\.swp|~)$", re.I)
ARCHIVE_RE = re.compile(r"\.(?:zip|tar|tgz|tar\.gz|7z|rar)$", re.I)
BACKUP_RE = re.compile(r"(?:\.bak|\.backup(?:\.|$)|\.old|\.orig|copy|copia)", re.I)
LOG_RE = re.compile(r"\.(?:log|out)$", re.I)


def ensure_dir(ftp: ftplib.FTP_TLS, path: str) -> None:
    current = ftp.pwd()
    ftp.cwd("/")
    for part in path.strip("/").split("/"):
        if not part:
            continue
        try:
            ftp.mkd(part)
        except ftplib.error_perm as exc:
            if not str(exc).startswith("550"):
                raise
        ftp.cwd(part)
    ftp.cwd(current)


def mlsd(ftp: ftplib.FTP_TLS, path: str):
    rows = []
    for name, facts in ftp.mlsd(path, facts=["type", "size", "modify"]):
        if name in {".", ".."}:
            continue
        rows.append((name, {k.lower(): v for k, v in facts.items()}))
    return rows


def has_site_signature(ftp: ftplib.FTP_TLS, root: str) -> bool:
    try:
        names = {name.lower() for name, _ in mlsd(ftp, root)}
    except ftplib.all_errors:
        return False
    return bool(names.intersection({"index.html", "index.php", "robots.txt", "sitemap.xml"}))


def classify(path: str):
    kinds = []
    if TEMP_RE.search(path): kinds.append("temporary_or_cache")
    if ARCHIVE_RE.search(path): kinds.append("archive_or_installer")
    if BACKUP_RE.search(path): kinds.append("backup_or_old_copy")
    if LOG_RE.search(path): kinds.append("log")
    return kinds


def main() -> None:
    password = os.environ.get("FTP_PASSWORD")
    if not password:
        raise RuntimeError("FTP_PASSWORD_MISSING")
    host = (os.environ.get("FTP_TLS_HOST") or "h59.servidorhh.com").strip()
    user = (os.environ.get("FTP_USER") or "arquind2").strip()
    expected = set(socket.gethostbyname_ex("ftp.arquindex.com.br")[2])
    resolved = set(socket.gethostbyname_ex(host)[2])
    if not expected.intersection(resolved):
        raise RuntimeError("HOST_IP_MISMATCH")

    context = ssl.create_default_context()
    context.minimum_version = ssl.TLSVersion.TLSv1_2
    report = {
        "run": STAMP,
        "state": "started",
        "roots": [],
        "files": 0,
        "bytes": 0,
        "extensions": {},
        "empty_directories": [],
        "candidates": [],
        "cleanup": {
            "deleted": 0,
            "moved_to_quarantine": 0,
            "bytes_freed": 0,
            "state": "held_no_gsc_evidence",
            "reason": "GSC read returned INVALID_ARGUMENT; no file is proven unused.",
        },
    }

    with ftplib.FTP_TLS(timeout=60, context=context) as ftp:
        ftp.connect(host, 21)
        if ftp.sock.getpeername()[0] not in expected:
            raise RuntimeError("SERVER_IP_CHANGED")
        ftp.auth()
        ftp.login(user, password)
        ftp.prot_p()
        ftp.cwd("/")
        print("FTPS_TLS_VERIFIED", host, flush=True)

        root_rows = mlsd(ftp, "/")
        root_dirs = [n for n, f in root_rows if f.get("type") == "dir"]
        roots = []
        if "public_html" in root_dirs:
            roots.append("public_html")
        for name in root_dirs:
            if name in SYSTEM_ROOTS or name.startswith(".") or name == "public_html":
                continue
            if has_site_signature(ftp, name):
                roots.append(name)
        if not roots:
            raise RuntimeError("NO_PUBLIC_ROOT_FOUND")
        report["roots"] = sorted(roots)

        fd, local_tar = tempfile.mkstemp(prefix="arquindex-weekly-", suffix=".tar.gz")
        os.close(fd)
        try:
            with tarfile.open(local_tar, "w:gz") as archive:
                stack = list(reversed(sorted(roots)))
                while stack:
                    directory = stack.pop()
                    rows = mlsd(ftp, directory)
                    visible = [(n, f) for n, f in rows if not n.startswith(".upload-")]
                    if not visible:
                        report["empty_directories"].append(directory)
                    for name, facts in visible:
                        path = posixpath.join(directory, name)
                        kind = facts.get("type")
                        if kind == "dir":
                            if path.startswith("public_html/seo-backups"):
                                continue
                            stack.append(path)
                            continue
                        if kind != "file":
                            continue
                        size = int(facts.get("size") or 0)
                        report["files"] += 1
                        report["bytes"] += size
                        if report["files"] > MAX_FILES:
                            raise RuntimeError("FILE_LIMIT_EXCEEDED")
                        if report["bytes"] > MAX_BYTES:
                            raise RuntimeError("BYTE_LIMIT_EXCEEDED")
                        suffix = posixpath.basename(path).lower().rsplit(".", 1)
                        ext = "." + suffix[-1] if len(suffix) == 2 else "[none]"
                        report["extensions"][ext] = report["extensions"].get(ext, 0) + 1
                        kinds = classify(path)
                        if kinds:
                            report["candidates"].append({
                                "path": path,
                                "bytes": size,
                                "modified": facts.get("modify"),
                                "classes": kinds,
                                "action": "review_only",
                            })

                        with tempfile.SpooledTemporaryFile(max_size=8 * 1024 * 1024) as tmp:
                            ftp.retrbinary("RETR " + path, tmp.write)
                            tmp.seek(0, io.SEEK_END)
                            actual = tmp.tell()
                            if size and actual != size:
                                raise RuntimeError("SIZE_MISMATCH " + path)
                            tmp.seek(0)
                            info = tarfile.TarInfo(path)
                            info.size = actual
                            info.mtime = int(datetime.now(timezone.utc).timestamp())
                            archive.addfile(info, tmp)

            local_size = os.path.getsize(local_tar)
            digest = hashlib.sha256()
            with open(local_tar, "rb") as src:
                for block in iter(lambda: src.read(1024 * 1024), b""):
                    digest.update(block)
            local_sha = digest.hexdigest()

            ensure_dir(ftp, BACKUP_DIR)
            remote = f"/{BACKUP_DIR}/weekly-full-{STAMP}.tar.gz"
            temp_remote = remote + ".upload"
            ftp.cwd("/")
            with open(local_tar, "rb") as src:
                ftp.storbinary("STOR " + temp_remote, src)
            if ftp.size(temp_remote) != local_size:
                raise RuntimeError("BACKUP_UPLOAD_SIZE_MISMATCH")
            try:
                ftp.delete(remote)
            except ftplib.error_perm:
                pass
            ftp.rename(temp_remote, remote)

            remote_sha = hashlib.sha256()
            ftp.retrbinary("RETR " + remote, remote_sha.update)
            if remote_sha.hexdigest() != local_sha:
                raise RuntimeError("BACKUP_UPLOAD_HASH_MISMATCH")

            report["backup"] = {
                "path": remote,
                "bytes": local_size,
                "sha256": local_sha,
                "outside_public_html": True,
                "verified_by_full_readback": True,
            }
            report["extensions"] = dict(sorted(report["extensions"].items()))
            report["candidates"].sort(key=lambda x: (-x["bytes"], x["path"]))
            report["state"] = "backup_verified_inventory_complete_cleanup_held"
            payload = (json.dumps(report, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
            report_path = f"/{BACKUP_DIR}/weekly-inventory-{STAMP}.json"
            ftp.storbinary("STOR " + report_path, io.BytesIO(payload))
            if ftp.size(report_path) != len(payload):
                raise RuntimeError("REPORT_UPLOAD_SIZE_MISMATCH")
            print("WEEKLY_AUDIT_RESULT", json.dumps({
                "state": report["state"],
                "roots": report["roots"],
                "files": report["files"],
                "bytes": report["bytes"],
                "candidates": len(report["candidates"]),
                "empty_directories": len(report["empty_directories"]),
                "backup": report["backup"],
                "report": report_path,
                "deleted": 0,
                "moved": 0,
                "bytes_freed": 0,
            }, ensure_ascii=False), flush=True)
        finally:
            try:
                os.unlink(local_tar)
            except FileNotFoundError:
                pass


if __name__ == "__main__":
    main()
