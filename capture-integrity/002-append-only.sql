-- Additive migration. Run with schema owner; application must be a separate,
-- non-owner, non-superuser role. No document/file deletion or data rewrite.
CREATE OR REPLACE FUNCTION capture_integrity_no_mutation() RETURNS trigger
LANGUAGE plpgsql AS $$ BEGIN
  RAISE EXCEPTION 'Capture integrity records are append-only';
END $$;
DROP TRIGGER IF EXISTS capture_versions_append_only ON capture_integrity_versions;
CREATE TRIGGER capture_versions_append_only BEFORE UPDATE OR DELETE OR TRUNCATE
ON capture_integrity_versions FOR EACH STATEMENT EXECUTE FUNCTION capture_integrity_no_mutation();
DROP TRIGGER IF EXISTS capture_audit_append_only ON capture_integrity_audit;
CREATE TRIGGER capture_audit_append_only BEFORE UPDATE OR DELETE OR TRUNCATE
ON capture_integrity_audit FOR EACH STATEMENT EXECUTE FUNCTION capture_integrity_no_mutation();
