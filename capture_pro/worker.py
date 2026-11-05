"""OCR job runner for a dedicated, private worker.

No public API, no arbitrary shell, no client-supplied tenant scope.
Requirements: schema.sql applied, worker DB role with narrowly scoped
privileges; dedicated job-claim function/security model must be reviewed
before giving this worker production credentials.
"""
from __future__ import annotations
import hashlib
import json
import os
import tempfile
import time
from pathlib import Path
from uuid import UUID
import boto3
import psycopg
from botocore.config import Config
from capture_pro.ocr_pipeline import pipeline
from capture_pro.storage import object_key

REQUIRED = ("DATABASE_URL", "S3_ENDPOINT", "S3_BUCKET", "S3_ACCESS_KEY", "S3_SECRET_KEY")

def configuration():
    missing=[n for n in REQUIRED if not os.getenv(n)]
    if missing:
        raise RuntimeError("Missing required environment variables: " + ", ".join(missing))
    if not os.environ["S3_ENDPOINT"].startswith("https://"):
        raise ValueError("HTTPS S3 endpoint required")
    return {n:os.environ[n] for n in REQUIRED}

def client(cfg):
    return boto3.client("s3",endpoint_url=cfg["S3_ENDPOINT"],
        aws_access_key_id=cfg["S3_ACCESS_KEY"],
        aws_secret_access_key=cfg["S3_SECRET_KEY"],
        config=Config(signature_version="s3v4"))

def sha256(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for block in iter(lambda:f.read(1024*1024),b""):
            h.update(block)
    return h.hexdigest()

def run_once(conn, s3, cfg):
    # Only jobs owned by this tenant are visible under RLS. A dedicated
    # role should be granted access to exactly the tenant it serves.
    tenant = os.environ.get("WORKER_TENANT_ID")
    if not tenant:
        raise RuntimeError("WORKER_TENANT_ID required; do not use global RLS bypass")
    tenant=str(UUID(tenant))
    with conn.transaction():
        conn.execute("SELECT set_config('app.tenant_id', %s, true)",(tenant,))
        job=conn.execute("""
            SELECT j.id, j.document_id, v.number, v.storage_key
            FROM capture.jobs j
            JOIN LATERAL (
              SELECT number,storage_key FROM capture.versions v
              WHERE v.tenant_id=j.tenant_id AND v.document_id=j.document_id
                AND v.kind='original'
              ORDER BY number DESC LIMIT 1
            ) v ON true
            WHERE j.tenant_id=%s AND j.type='ocr' AND j.status='queued'
            ORDER BY j.created_at FOR UPDATE OF j SKIP LOCKED LIMIT 1
        """,(tenant,)).fetchone()
        if not job:
            return False
        job_id, doc_id, number, key=job
        expected=object_key(tenant,str(doc_id),number,"original")
        if key!=expected:
            conn.execute("UPDATE capture.jobs SET status='failed', error_message=%s, finished_at=now() WHERE id=%s",
                ("Original key does not match expected tenant-scoped key",job_id))
            return True
        conn.execute("UPDATE capture.jobs SET status='running',started_at=now(),attempts=attempts+1 WHERE id=%s",(job_id,))
        conn.execute("UPDATE capture.documents SET status='ocr_running' WHERE id=%s AND tenant_id=%s",(doc_id,tenant))
    try:
        with tempfile.TemporaryDirectory() as scratch:
            source=Path(scratch)/"source.pdf"
            output=Path(scratch)/"searchable.pdf"
            s3.download_file(cfg["S3_BUCKET"],key,str(source))
            result=pipeline(source,output)
            if result["status"]!="aguardando_revisao":
                raise RuntimeError(result["status"])
            output_key=object_key(tenant,str(doc_id),number,"ocr")
            # S3 preconditions are not supported uniformly by upload_file:
            # prevent duplicate workers via DB row lock; require immutable version policy.
            s3.upload_file(str(output),cfg["S3_BUCKET"],output_key,
                ExtraArgs={"ContentType":"application/pdf","Metadata":{"sha256":result["pdfa_sha256"]}})
            with conn.transaction():
                conn.execute("SELECT set_config('app.tenant_id', %s, true)",(tenant,))
                existing=conn.execute("SELECT id FROM capture.versions WHERE tenant_id=%s AND document_id=%s AND number=%s AND kind='ocr'",(tenant,doc_id,number)).fetchone()
                if existing:
                    raise RuntimeError("OCR version already registered; manual reconciliation required")
                from uuid import uuid4
                conn.execute("""INSERT INTO capture.versions (id,tenant_id,document_id,number,kind,storage_key,sha256,byte_size)
                    VALUES (%s,%s,%s,%s,'ocr',%s,%s,%s)""",
                    (str(uuid4()),tenant,doc_id,number,output_key,result["pdfa_sha256"],output.stat().st_size))
                conn.execute("UPDATE capture.documents SET status='ocr_review' WHERE id=%s AND tenant_id=%s",(doc_id,tenant))
                conn.execute("UPDATE capture.jobs SET status='review',finished_at=now(),error_message=NULL WHERE id=%s",(job_id,))
                conn.execute("INSERT INTO capture.audit_events (tenant_id,document_id,action,details) VALUES (%s,%s,'ocr_completed',%s::jsonb)",
                    (tenant,doc_id,json.dumps({"job_id":str(job_id),"sha256":result["pdfa_sha256"]})))
    except Exception as exc:
        with conn.transaction():
            conn.execute("SELECT set_config('app.tenant_id', %s, true)",(tenant,))
            conn.execute("UPDATE capture.jobs SET status='failed',finished_at=now(),error_message=%s WHERE id=%s",
                (str(exc)[:500],job_id))
            conn.execute("UPDATE capture.documents SET status='failed' WHERE id=%s AND tenant_id=%s",(doc_id,tenant))
        return True
    return True

def main():
    cfg=configuration()
    tenant=os.environ.get("WORKER_TENANT_ID")
    UUID(tenant) if tenant else (_ for _ in ()).throw(RuntimeError("WORKER_TENANT_ID is required"))
    s3=client(cfg)
    while True:
        try:
            with psycopg.connect(cfg["DATABASE_URL"],autocommit=False) as conn:
                worked=run_once(conn,s3,cfg)
            if not worked: time.sleep(5)
        except KeyboardInterrupt:
            return
        except Exception as exc:
            print(json.dumps({"event":"worker_error","error":str(exc)[:500]}),flush=True)
            time.sleep(10)

if __name__=="__main__":
    main()
