-- LegalDoc AI: proposed normalized catalogue schema for large-scale Brazilian template library.
-- Migration NOT applied to production; requires DB, RBAC, RLS and legal/editorial validation.
CREATE TABLE IF NOT EXISTS legaldoc_legal_sources (
 id uuid PRIMARY KEY,
 authority text NOT NULL,
 title text NOT NULL,
 official_url text NOT NULL,
 source_kind text NOT NULL CHECK (source_kind IN ('statute','regulation','guidance','technical_reference','other')),
 last_checked_at timestamptz,
 published_at timestamptz,
 effective_from date,
 effective_to date,
 content_fingerprint char(64),
 review_status text NOT NULL DEFAULT 'UNVERIFIED' CHECK (review_status IN ('UNVERIFIED','REVIEW_REQUIRED','VERIFIED','SUPERSEDED'))
);
CREATE TABLE IF NOT EXISTS legaldoc_model_families (
 id uuid PRIMARY KEY,
 sector text NOT NULL,
 document_type text NOT NULL,
 slug text NOT NULL UNIQUE,
 created_at timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS legaldoc_model_families_sector ON legaldoc_model_families(sector,document_type);
CREATE TABLE IF NOT EXISTS legaldoc_model_versions (
 id uuid PRIMARY KEY,
 family_id uuid NOT NULL REFERENCES legaldoc_model_families(id),
 version_number integer NOT NULL,
 title text NOT NULL,
 jurisdiction text NOT NULL DEFAULT 'BR',
 applicability jsonb NOT NULL DEFAULT '{}'::jsonb,
 status text NOT NULL DEFAULT 'DRAFT' CHECK (status IN ('DRAFT','LEGAL_REVIEW','APPROVED','REVOKED','SUPERSEDED')),
 body_schema jsonb NOT NULL,
 content_sha256 char(64) NOT NULL,
 reviewed_by uuid,
 reviewed_at timestamptz,
 effective_from date,
 effective_to date,
 created_at timestamptz NOT NULL DEFAULT now(),
 UNIQUE(family_id,version_number)
);
CREATE INDEX IF NOT EXISTS legaldoc_model_versions_search ON legaldoc_model_versions USING gin(to_tsvector('portuguese',title));
CREATE INDEX IF NOT EXISTS legaldoc_model_versions_applicability ON legaldoc_model_versions USING gin(applicability);
CREATE TABLE IF NOT EXISTS legaldoc_model_source_links (
 model_version_id uuid NOT NULL REFERENCES legaldoc_model_versions(id),
 source_id uuid NOT NULL REFERENCES legaldoc_legal_sources(id),
 source_section text,
 applicability_note text,
 checked_by uuid,
 checked_at timestamptz,
 PRIMARY KEY(model_version_id,source_id)
);
CREATE TABLE IF NOT EXISTS legaldoc_review_queue (
 id uuid PRIMARY KEY,
 source_id uuid REFERENCES legaldoc_legal_sources(id),
 model_version_id uuid REFERENCES legaldoc_model_versions(id),
 severity text NOT NULL CHECK (severity IN ('LOW','MEDIUM','HIGH','CRITICAL')),
 reason text NOT NULL,
 status text NOT NULL DEFAULT 'OPEN' CHECK (status IN ('OPEN','IN_REVIEW','RESOLVED','DISMISSED')),
 assigned_to uuid,
 created_at timestamptz NOT NULL DEFAULT now(),
 resolved_at timestamptz
);
CREATE INDEX IF NOT EXISTS legaldoc_review_queue_open ON legaldoc_review_queue(status,severity,created_at DESC);
-- All public documents built from DRAFT versions must carry non-final disclaimers.
-- Before running: enable RLS + service account access policy, test tenant isolation, backups,
-- immutable approved versions and audit logging. Norm text from ABNT/ISO requires licensing.
