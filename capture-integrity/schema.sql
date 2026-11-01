-- Capture Pro integrity manifest: additive schema, no deletions.
CREATE TABLE IF NOT EXISTS capture_integrity_documents (
  tenant_id TEXT NOT NULL,
  document_id UUID NOT NULL,
  origin TEXT NOT NULL CHECK (origin IN ('scanner','importado_fisico','nato_digital')),
  metadata JSONB NOT NULL,
  metadata_valid BOOLEAN NOT NULL DEFAULT FALSE,
  metadata_missing JSONB NOT NULL DEFAULT '[]'::jsonb,
  public_body BOOLEAN NOT NULL DEFAULT FALSE,
  status TEXT NOT NULL,
  created_by TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (tenant_id,document_id)
);
CREATE TABLE IF NOT EXISTS capture_integrity_versions (
  tenant_id TEXT NOT NULL,
  document_id UUID NOT NULL,
  version_number INTEGER NOT NULL CHECK (version_number > 0),
  stage TEXT NOT NULL,
  algorithm TEXT NOT NULL CHECK (algorithm='SHA-256'),
  hash_hex TEXT NOT NULL CHECK (hash_hex ~ '^[a-f0-9]{64}$'),
  size_bytes BIGINT NOT NULL CHECK(size_bytes >= 0),
  object_key TEXT NOT NULL,
  created_by TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY(tenant_id,document_id,version_number),
  FOREIGN KEY(tenant_id,document_id) REFERENCES capture_integrity_documents(tenant_id,document_id)
);
CREATE TABLE IF NOT EXISTS capture_integrity_audit (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  tenant_id TEXT NOT NULL,
  document_id UUID NOT NULL,
  action TEXT NOT NULL,
  actor_id TEXT NOT NULL,
  details JSONB NOT NULL DEFAULT '{}'::jsonb,
  recorded_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  FOREIGN KEY(tenant_id,document_id) REFERENCES capture_integrity_documents(tenant_id,document_id)
);
CREATE INDEX IF NOT EXISTS capture_integrity_audit_doc_idx ON capture_integrity_audit(tenant_id,document_id,recorded_at);
-- Recommended in deployment: deny UPDATE/DELETE on versions/audit to the application role.
-- Object storage must also use immutable retention/versioning and server-side encryption.
