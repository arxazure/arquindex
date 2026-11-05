-- Arquindex LegalDoc AI / knowledge and milestone management, PROPOSED migration.
-- Never run on the public static marketing service. Requires secure backend and tenant-aware RBAC/RLS.
CREATE TABLE IF NOT EXISTS legaldoc_knowledge_submissions (
 id uuid PRIMARY KEY,
 company_id uuid NOT NULL,
 submitted_by uuid NOT NULL,
 sector text NOT NULL,
 title text NOT NULL,
 body text NOT NULL,
 source_url text,
 source_kind text NOT NULL DEFAULT 'USER_EXPERIENCE',
 confidentiality text NOT NULL DEFAULT 'PRIVATE' CHECK(confidentiality IN ('PRIVATE','SHARED_WITH_CONSENT')),
 state text NOT NULL DEFAULT 'PENDING_REVIEW' CHECK(state IN ('PENDING_REVIEW','TRIAGE','LEGAL_REVIEW','TECHNICAL_REVIEW','APPROVED','REJECTED')),
 reviewed_by uuid,
 reviewed_at timestamptz,
 created_at timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS legaldoc_knowledge_tenant ON legaldoc_knowledge_submissions(company_id,state,created_at DESC);
CREATE TABLE IF NOT EXISTS legaldoc_audit_controls (
 id uuid PRIMARY KEY,
 company_id uuid NOT NULL,
 template_version_id uuid,
 code text NOT NULL,
 title text NOT NULL,
 applicability jsonb NOT NULL DEFAULT '{}'::jsonb,
 source_references jsonb NOT NULL DEFAULT '[]'::jsonb,
 mandatory_evidence jsonb NOT NULL DEFAULT '[]'::jsonb,
 state text NOT NULL DEFAULT 'DRAFT' CHECK(state IN ('DRAFT','APPROVED','RETIRED')),
 reviewed_by uuid,
 reviewed_at timestamptz
);
CREATE INDEX IF NOT EXISTS legaldoc_audit_controls_tenant ON legaldoc_audit_controls(company_id,state);
CREATE TABLE IF NOT EXISTS legaldoc_audit_executions (
 id uuid PRIMARY KEY,
 company_id uuid NOT NULL,
 control_id uuid NOT NULL REFERENCES legaldoc_audit_controls(id),
 document_id uuid,
 evaluator_id uuid NOT NULL,
 verification text NOT NULL CHECK(verification IN ('CONFORMING','NONCONFORMING','NOT_APPLICABLE','NOT_VERIFIED')),
 evidence_ref text,
 justification text,
 checked_at timestamptz NOT NULL DEFAULT now(),
 approved_by uuid,
 approved_at timestamptz
);
CREATE INDEX IF NOT EXISTS legaldoc_audit_executions_tenant ON legaldoc_audit_executions(company_id,checked_at DESC);
CREATE TABLE IF NOT EXISTS legaldoc_document_milestones (
 id uuid PRIMARY KEY,
 company_id uuid NOT NULL,
 document_id uuid,
 contractual_obligation_id uuid,
 title text NOT NULL,
 kind text NOT NULL,
 responsible_user_id uuid,
 responsible_role text,
 due_at timestamptz NOT NULL,
 status text NOT NULL DEFAULT 'OPEN' CHECK(status IN ('OPEN','IN_PROGRESS','COMPLETED','CANCELLED')),
 completed_at timestamptz,
 evidence_ref text,
 created_at timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS legaldoc_document_milestones_tenant ON legaldoc_document_milestones(company_id,status,due_at);
-- Production prerequisites: RLS isolation, authenticated access policies, audit/event log,
-- retention and deletion requests, backup, evidence storage, source-review queue and DPO approval.
