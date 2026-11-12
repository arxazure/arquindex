-- Proposed schema, NOT executed. Tenant isolation/RLS, verified identities and audit policies required.
CREATE TABLE IF NOT EXISTS legaldoc_requests (
 id uuid PRIMARY KEY,
 company_id uuid NOT NULL,
 requested_by uuid NOT NULL,
 document_type text NOT NULL,
 instructions text NOT NULL,
 status text NOT NULL DEFAULT 'DRAFT' CHECK(status IN
 ('DRAFT','INTAKE','DRAFTING','CLIENT_REVIEW','LEGAL_REVIEW_1','LEGAL_REVIEW_2',
  'TECHNICAL_REVIEW','APPROVAL','HOMOLOGATION','SIGNATURE_PENDING','PUBLICATION_PENDING','COMPLETED','CANCELLED')),
 legal_review_rounds integer NOT NULL CHECK(legal_review_rounds IN (1,2)),
 outcome text NOT NULL CHECK(outcome IN ('SIGN','PUBLISH')),
 current_revision integer NOT NULL DEFAULT 1,
 current_document_hash char(64),
 created_at timestamptz NOT NULL DEFAULT now(),
 updated_at timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS legaldoc_requests_tenant ON legaldoc_requests(company_id,status,created_at DESC);
CREATE TABLE IF NOT EXISTS legaldoc_request_reviewers (
 id uuid PRIMARY KEY,
 company_id uuid NOT NULL,
 request_id uuid NOT NULL REFERENCES legaldoc_requests(id),
 email_normalized text NOT NULL,
 user_id uuid,
 role text NOT NULL CHECK(role IN ('LEGAL','TECHNICAL','APPROVER','HOMOLOGATOR','SIGNER')),
 verified_at timestamptz,
 invited_at timestamptz,
 invite_token_hash char(64),
 invite_expires_at timestamptz,
 UNIQUE(request_id,email_normalized,role)
);
CREATE TABLE IF NOT EXISTS legaldoc_request_reviews (
 id uuid PRIMARY KEY,
 company_id uuid NOT NULL,
 request_id uuid NOT NULL REFERENCES legaldoc_requests(id),
 reviewer_id uuid NOT NULL REFERENCES legaldoc_request_reviewers(id),
 revision integer NOT NULL,
 round integer NOT NULL CHECK(round IN (0,1,2)),
 kind text NOT NULL CHECK(kind IN ('CLIENT','LEGAL','TECHNICAL','APPROVAL','HOMOLOGATION')),
 verdict text NOT NULL CHECK(verdict IN ('CHANGES_REQUESTED','ACCEPTED','REJECTED')),
 remarks text,
 document_sha256 char(64) NOT NULL,
 reviewed_at timestamptz NOT NULL DEFAULT now(),
 UNIQUE(request_id,revision,reviewer_id,kind,round)
);
CREATE INDEX IF NOT EXISTS legaldoc_reviews_request ON legaldoc_request_reviews(company_id,request_id,revision);
CREATE TABLE IF NOT EXISTS legaldoc_request_events (
 id uuid PRIMARY KEY,
 company_id uuid NOT NULL,
 request_id uuid NOT NULL REFERENCES legaldoc_requests(id),
 actor_user_id uuid,
 action text NOT NULL,
 from_state text,
 to_state text,
 revision integer NOT NULL,
 document_sha256 char(64),
 detail jsonb NOT NULL DEFAULT '{}'::jsonb,
 occurred_at timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS legaldoc_request_events_tenant ON legaldoc_request_events(company_id,request_id,occurred_at);
-- Safeguards for the actual API:
-- 1. All writes in transactions with SELECT ... FOR UPDATE on the request.
-- 2. Enforce tenant access and distinct reviewer identity server-side; reject owner self-approval.
-- 3. Client review / legal reviews (1 or 2) / technical review / approval / homologation
--    bind decisions to the exact revision and SHA-256 digest.
-- 4. Any requested change creates a new revision and invalidates prior downstream approvals.
-- 5. No auto-emails to unverified addresses; rate limit invitations and confirm domains.
-- 6. Only authenticated signature-provider callbacks may advance to signed.
-- 7. Publishing needs authorized destination, explicit release approval and immutable snapshots.
-- 8. Exclude raw document content, personal data and legal email addresses from public logs.
