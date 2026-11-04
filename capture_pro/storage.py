"""Storage adapter for Arquindex's private S3 bucket.
No HTTP endpoints. Caller must resolve tenant from an authenticated server session.
"""
from __future__ import annotations
import hashlib
import re
from pathlib import Path
from uuid import UUID
import boto3
from botocore.config import Config

SAFE_ID = re.compile(r"^[a-zA-Z0-9_-]{1,64}$")
def checked_tenant(tenant_id: str) -> str:
    # Tenant ID must be server-side resolved, never copied from user parameters.
    if not SAFE_ID.fullmatch(tenant_id):
        raise ValueError("Invalid tenant identifier")
    return tenant_id

def object_key(tenant_id: str, document_id: str, version: int, kind: str) -> str:
    checked_tenant(tenant_id)
    UUID(document_id)
    if not 1 <= version <= 1000000 or kind not in ("original", "ocr", "signed"):
        raise ValueError("Invalid document version/type")
    return f"tenants/{tenant_id}/documents/{document_id}/v{version}/{kind}.pdf"

class PrivateDocumentStore:
    def __init__(self, *, endpoint: str, bucket: str, access_key: str, secret_key: str, region: str = "auto"):
        if not endpoint.startswith("https://"):
            raise ValueError("Storage endpoint must use HTTPS")
        self.bucket = bucket
        self.client = boto3.client("s3", endpoint_url=endpoint,
            aws_access_key_id=access_key, aws_secret_access_key=secret_key,
            region_name=region, config=Config(signature_version="s3v4"))

    def upload_pdf(self, tenant_id: str, document_id: str, version: int, kind: str, file: Path) -> dict:
        key = object_key(tenant_id, document_id, version, kind)
        if not file.is_file() or file.suffix.lower() != ".pdf":
            raise ValueError("PDF file required")
        digest = hashlib.sha256()
        with file.open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(chunk)
        # Do not overwrite existing objects. Explicit versioning required for edits.
        try:
            self.client.head_object(Bucket=self.bucket, Key=key)
        except self.client.exceptions.ClientError as exc:
            if exc.response.get("ResponseMetadata", {}).get("HTTPStatusCode") != 404:
                raise
        else:
            raise FileExistsError("Object version already exists")
        self.client.upload_file(str(file), self.bucket, key,
            ExtraArgs={"ContentType": "application/pdf",
                       "Metadata": {"sha256": digest.hexdigest()}})
        return {"key": key, "sha256": digest.hexdigest(), "bytes": file.stat().st_size}

    def download(self, tenant_id: str, document_id: str, version: int, kind: str, target: Path) -> None:
        key = object_key(tenant_id, document_id, version, kind)
        if target.exists():
            raise FileExistsError(target)
        self.client.download_file(self.bucket, key, str(target))
