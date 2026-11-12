# ANPD monitor: validation and rollout

This change is prepared for review only. Do not merge/deploy, restart Railway or change variables before the owner approves the concrete rollout.

## Behavior

Manual and scheduled checks use the same dedicated PostgreSQL session and advisory lock (987643203), across replicas. Successful source checks are skipped for the current UTC day; failed or missing sources remain eligible at the next hourly/manual attempt. Existing rows are preserved. Each attempted batch and its audit event commit in one transaction; database/audit failures roll back. The lock is released on success and failure; an unlock failure destroys the pooled connection. No schema migration or client-document update is introduced.

Scheduled audit action: regulatory_check_scheduled (system actor). Manual: regulatory_check_manual (authenticated actor). record_id stores the source/status summary. Existing audit events remain unchanged.

## Verification performed

Six Node tests with simulated database/network: shared lock contention; retries of failed/missing sources; daily success skip; rollback on audit failure; manual actor/outcome audit; HTTP/timeout failure continuation. Syntax checks: server.js and inline app script. These do not substitute for a real PostgreSQL concurrency/transaction test or authenticated UI validation.

Prior live read-only inspection confirmed Railway deployment 0c2c1d44-b468-42f8-b32d-f03091fde0a3 at merge commit 04d78d683ba120c1f2207c705a0eb8c475467e54, health connected, and ANPD_DAILY_CHECK with four baseline results at 2026-11-04T04:00:43Z. That evidence concerns the previous deployed version, not this proposed change.

## Approval-gated rollout

1. Review and merge this PR to railway-production-2026, which can trigger Railway deployment of lgpd-checklist-app in the staging environment used by the live domain.
2. Preserve existing variables. ANPD_AUTO_CHECK must equal the literal true to enable startup/hourly checks. It was already active in the observed deployment; OAuth hides its current value. No variable change is proposed.
3. Validate health and deployment SHA, read the authenticated regulatory history/audit, and inspect Atualizar. A runtime check may add regulatory results/audit events, never client documents.
4. Validate concurrent manual/scheduled checks against real PostgreSQL in an isolated test environment before scaling replicas. Roll back to the previous successful deployment if validation fails, with owner approval.

## Interpretation and human review

The monitor stores hashes and metadata, not the complete source text. A changed hash is not a confirmed regulatory amendment. The UI distinguishes collection, hash changes, static catalog templates and document review status. Actual policy/ROPA/RIPD review is explicitly unverified by this monitor; do not infer it from imports or collection success. Templates are drafts. Human review and approval remain mandatory for all compliance document changes.
