-- LegalDoc AI: proposed secure intake workflow. NOT applied on public landing.
CREATE TABLE IF NOT EXISTS legaldoc_requests (
 id uuid PRIMARY KEY, company_id uuid NOT NULL, created_by uuid NOT NULL,
 client_organisation_label text NOT NULL,
 technical_role_label text NOT NULL,
 approver_role_label text NOT NULL,
 document_type text NOT NULL, description text NOT NULL,
 review_rounds smallint NOT NULL CHECK(review_rounds IN (1,2)),
 outcome text NOT NULL CHECK(outcome IN ('PUBLISH','SIGN')),
 status text NOT NULL DEFAULT 'DRAFT',
 created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE IF NOT EXISTS legaldoc_request_reviewers (
 request_id uuid NOT NULL REFERENCES legaldoc_requests(id), company_id uuid NOT NULL,
 reviewer_user_id uuid, email text NOT NULL,
 role text NOT NULL CHECK(role IN ('CLIENT','LEGAL','TECHNICAL','APPROVER','HOMOLOGATOR','SIGNATORY')),
 verified_at timestamptz, accepted_at timestamptz,
 PRIMARY KEY(request_id,email,role)
);
CREATE TABLE IF NOT EXISTS legaldoc_request_stages (
 id uuid PRIMARY KEY, request_id uuid NOT NULL REFERENCES legaldoc_requests(id),
 company_id uuid NOT NULL, step_number integer NOT NULL, stage text NOT NULL,
 status text NOT NULL DEFAULT 'PENDING' CHECK(status IN ('PENDING','ACTIVE','APPROVED','REJECTED','CANCELLED')),
 assigned_user_id uuid, completed_by uuid, completed_at timestamptz,
 document_version_hash char(64), review_notes text,
 UNIQUE(request_id,step_number)
);
CREATE INDEX IF NOT EXISTS legaldoc_request_stages_tenant ON legaldoc_request_stages(company_id,request_id,status);
-- Production gate: tenant isolation/RLS, invite token with expiry, verified email ownership,
-- CSRF/session auth, per-stage authorization, two-review limits, distinct reviewer/approver,
-- tamper evident append-only events, document version hash and signatures provider callback.

CREATE TABLE IF NOT EXISTS legaldoc_request_events (
 id uuid PRIMARY KEY,
 request_id uuid NOT NULL REFERENCES legaldoc_requests(id),
 company_id uuid NOT NULL,
 actor_id uuid NOT NULL,
 event text NOT NULL,
 detail jsonb NOT NULL DEFAULT '{}'::jsonb,
 occurred_at timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS legaldoc_request_events_tenant ON legaldoc_request_events(company_id,request_id,occurred_at);
-- Configure INSERT-only privilege for this audit table; revoke UPDATE/DELETE.
-- All tenant tables require RLS policies before any migration is deployed.

CREATE TABLE IF NOT EXISTS legaldoc_reviewer_invites (
 id uuid PRIMARY KEY,
 company_id uuid NOT NULL,
 request_id uuid NOT NULL REFERENCES legaldoc_requests(id),
 invited_email text NOT NULL,
 role text NOT NULL,
 token_hash char(64) NOT NULL UNIQUE,
 invited_by uuid NOT NULL,
 expires_at timestamptz NOT NULL,
 consumed_at timestamptz,
 revoked_at timestamptz,
 created_at timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS legaldoc_reviewer_invites_pending
 ON legaldoc_reviewer_invites(company_id,request_id,expires_at)
 WHERE consumed_at IS NULL AND revoked_at IS NULL;
-- Before real invitation dispatch:
-- * authenticate client, rate limit invite creation and enforce per-tenant roles
-- * store only token hash, send raw token through approved mail service, never logs
-- * require recipient email ownership/verified identity before linking reviewer_user_id
-- * consume atomically, check expiry/revocation and require re-authentication for decisions
