-- LegalDoc AI: migracao ADITIVA; nao executar antes de homologar controle de acesso.
CREATE TABLE IF NOT EXISTS legaldoc_templates (
 id uuid PRIMARY KEY, company_id uuid NOT NULL, title text NOT NULL,
 body text NOT NULL, version integer NOT NULL DEFAULT 1,
 status text NOT NULL DEFAULT 'DRAFT' CHECK(status IN ('DRAFT','APPROVED','REVOKED')),
 created_by uuid NOT NULL, approved_by uuid, approved_at timestamptz,
 body_sha256 char(64) NOT NULL, created_at timestamptz NOT NULL DEFAULT now(),
 updated_at timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS legaldoc_templates_tenant ON legaldoc_templates(company_id,status);
CREATE TABLE IF NOT EXISTS legaldoc_documents (
 id uuid PRIMARY KEY, company_id uuid NOT NULL, template_id uuid NOT NULL REFERENCES legaldoc_templates(id),
 title text NOT NULL, content text NOT NULL, content_sha256 char(64) NOT NULL,
 state text NOT NULL DEFAULT 'DRAFT' CHECK(state IN ('DRAFT','REVIEW','APPROVED','SIGNATURE_PENDING','SIGNED','ARCHIVED','REJECTED')),
 created_by uuid NOT NULL, reviewer_id uuid, approved_by uuid, created_at timestamptz NOT NULL DEFAULT now(),
 updated_at timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS legaldoc_documents_tenant ON legaldoc_documents(company_id,state);
CREATE TABLE IF NOT EXISTS legaldoc_audit (
 id uuid PRIMARY KEY, company_id uuid NOT NULL, document_id uuid,
 template_id uuid, actor_id uuid NOT NULL, event text NOT NULL, detail jsonb NOT NULL DEFAULT '{}'::jsonb,
 occurred_at timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS legaldoc_audit_tenant ON legaldoc_audit(company_id,occurred_at DESC);
