# Alfresco + AI — Secure open-source architecture

**Audience:** AI Solutions Architects, ECM Architects and Tech Leads.

## End-to-end reference
```text
User -> authenticated API -> Alfresco ACL checked retrieval
                            -> isolated OCR/Tika worker
                            -> normalized text + metadata + SHA-256
                            -> tenant-separated embeddings/search
                            -> local LLM (Ollama) -> answer + citations/audit log
```

## Implementation guide
1. Select and pin officially supported Alfresco Community deployment versions; validate infrastructure and backups before installation.
2. Use minimally privileged service credentials and TLS. The Alfresco REST API accesses repository documents only within the requesting principal's permissions.
3. Extract document text asynchronously with Apache Tika and Tesseract OCR. Retain original files separately from derivatives.
4. Store content IDs, version IDs, parent folders, source hash, OCR quality score and classification.
5. Create tenant-scoped vector indexes and invalidate indexed chunks after access revocation.
6. Retrieve document chunks only after permission checks; reject missing tenant context.
7. Treat document text as untrusted input. Never execute embedded instructions or allow prompt injection to override access control.
8. Log trace IDs, metadata references, decisions and model versions, with configurable retention.

## Acceptance tests
- A user in tenant A cannot obtain tenant B's chunks.
- Revoked Alfresco access prevents subsequent AI retrieval.
- Document text reading "ignore your instructions" cannot alter security controls.
- Changes to OCR derivatives do not overwrite original hashes.
- Responses must cite source document identifiers, or abstain.

**Design principle:** AI does not replace ECM governance. This document is a reference design, not proof of a deployed integration.

[Academy index](README.md) · [PostgreSQL lab](02-fastapi-postgresql.md) · [Integrity lab](03-digital-evidence.md)
