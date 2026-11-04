-- Arquindex Capture Pro: application data model (review before migration).
-- Execute using a dedicated least-privilege database role in a separate schema.
CREATE SCHEMA IF NOT EXISTS capture;
CREATE TABLE IF NOT EXISTS capture.tenants (
    id uuid PRIMARY KEY, name text NOT NULL, created_at timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE IF NOT EXISTS capture.memberships (
    tenant_id uuid NOT NULL REFERENCES capture.tenants(id),
    user_id uuid NOT NULL,
    role text NOT NULL CHECK (role IN ('admin','manager','operator','reviewer','client')),
    PRIMARY KEY (tenant_id, user_id)
);
CREATE TABLE IF NOT EXISTS capture.models (
    id uuid PRIMARY KEY, tenant_id uuid NOT NULL REFERENCES capture.tenants(id),
    name text NOT NULL, version integer NOT NULL DEFAULT 1,
    rules jsonb NOT NULL, approved_by uuid, created_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE(tenant_id,id)
);
CREATE TABLE IF NOT EXISTS capture.documents (
    id uuid PRIMARY KEY, tenant_id uuid NOT NULL REFERENCES capture.tenants(id),
    model_id uuid, filename text NOT NULL, status text NOT NULL
      CHECK (status IN ('uploaded','ocr_running','ocr_review','classification','qa_pending','qa_rejected','approved','signing','signed','delivered','failed')),
    created_by uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE(tenant_id,id),
    FOREIGN KEY (tenant_id,model_id) REFERENCES capture.models(tenant_id,id)
);
CREATE TABLE IF NOT EXISTS capture.versions (
    id uuid PRIMARY KEY, tenant_id uuid NOT NULL, document_id uuid NOT NULL,
    number integer NOT NULL CHECK(number>0), kind text NOT NULL
      CHECK(kind IN ('original','ocr','signed')),
    storage_key text NOT NULL, sha256 char(64) NOT NULL, byte_size bigint NOT NULL CHECK(byte_size>=0),
    created_at timestamptz NOT NULL DEFAULT now(), UNIQUE(tenant_id,document_id,number,kind),
    FOREIGN KEY (tenant_id,document_id) REFERENCES capture.documents(tenant_id,id)
);
CREATE TABLE IF NOT EXISTS capture.jobs (
    id uuid PRIMARY KEY, tenant_id uuid NOT NULL, document_id uuid NOT NULL,
    type text NOT NULL CHECK(type IN ('ocr','split','qa','sign','export','backup')),
    status text NOT NULL CHECK(status IN ('queued','running','succeeded','failed','review')),
    attempts integer NOT NULL DEFAULT 0 CHECK(attempts>=0),
    requested_by uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(),
    started_at timestamptz, finished_at timestamptz, error_message text,
    FOREIGN KEY (tenant_id,document_id) REFERENCES capture.documents(tenant_id,id)
);
CREATE TABLE IF NOT EXISTS capture.audit_events (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY, tenant_id uuid NOT NULL,
    document_id uuid, actor_id uuid, action text NOT NULL,
    details jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS jobs_pending_idx ON capture.jobs (created_at) WHERE status='queued';
CREATE INDEX IF NOT EXISTS documents_tenant_status_idx ON capture.documents (tenant_id,status);
-- Defense in depth: enable and FORCE RLS, then establish connection-local tenant claims.
-- Tenant application role must not own these tables or have BYPASSRLS.
ALTER TABLE capture.memberships ENABLE ROW LEVEL SECURITY;
ALTER TABLE capture.models ENABLE ROW LEVEL SECURITY;
ALTER TABLE capture.documents ENABLE ROW LEVEL SECURITY;
ALTER TABLE capture.versions ENABLE ROW LEVEL SECURITY;
ALTER TABLE capture.jobs ENABLE ROW LEVEL SECURITY;
ALTER TABLE capture.audit_events ENABLE ROW LEVEL SECURITY;
ALTER TABLE capture.memberships FORCE ROW LEVEL SECURITY;
ALTER TABLE capture.models FORCE ROW LEVEL SECURITY;
ALTER TABLE capture.documents FORCE ROW LEVEL SECURITY;
ALTER TABLE capture.versions FORCE ROW LEVEL SECURITY;
ALTER TABLE capture.jobs FORCE ROW LEVEL SECURITY;
ALTER TABLE capture.audit_events FORCE ROW LEVEL SECURITY;
CREATE POLICY tenant_scope_memberships ON capture.memberships
 USING (tenant_id::text = current_setting('app.tenant_id',true))
 WITH CHECK (tenant_id::text = current_setting('app.tenant_id',true));
CREATE POLICY tenant_scope_models ON capture.models
 USING (tenant_id::text = current_setting('app.tenant_id',true))
 WITH CHECK (tenant_id::text = current_setting('app.tenant_id',true));
CREATE POLICY tenant_scope_documents ON capture.documents
 USING (tenant_id::text = current_setting('app.tenant_id',true))
 WITH CHECK (tenant_id::text = current_setting('app.tenant_id',true));
CREATE POLICY tenant_scope_versions ON capture.versions
 USING (tenant_id::text = current_setting('app.tenant_id',true))
 WITH CHECK (tenant_id::text = current_setting('app.tenant_id',true));
CREATE POLICY tenant_scope_jobs ON capture.jobs
 USING (tenant_id::text = current_setting('app.tenant_id',true))
 WITH CHECK (tenant_id::text = current_setting('app.tenant_id',true));
CREATE POLICY tenant_scope_audit ON capture.audit_events
 USING (tenant_id::text = current_setting('app.tenant_id',true))
 WITH CHECK (tenant_id::text = current_setting('app.tenant_id',true));
-- Before using, ensure tenant context is derived from authorized membership and SET LOCAL within transaction.
