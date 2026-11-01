import {ingestDocument, createProcessingVersion} from './ingestion.js';
import {verifyVersion} from './decreto-10278.js';
import {tenantKey} from './storage.js';

/** Bind ONLY a server-verified identity, never req.body, filenames or headers
 * forwarded by an untrusted client. Host authorization must validate membership,
 * project access and CSRF before constructing this service. No HTTP route is
 * automatically mounted; production auth/source code is not accessible yet.
 */
export function captureService({pool, storage, identity}) {
  const {tenantId, actorId, canCapture} = identity || {};
  tenantKey(tenantId, `${tenantId}/capture/check`);
  if (!actorId || canCapture !== true) throw new Error('Capture permission required');
  const context = {pool, storage, tenantId, actorId};
  return {
    async receive({bytes, metadata, origem, publicBody = false, channel}) {
      if (!['scanner', 'watched_folder', 'upload'].includes(channel)) throw new TypeError('Invalid channel');
      return ingestDocument({...context, bytes, metadata, origem, publicBody, channel});
    },
    async readVersion(documentId, version) {
      const result = await pool.query(`SELECT algorithm,hash_hex,size_bytes,object_key FROM capture_integrity_versions
        WHERE tenant_id=$1 AND document_id=$2 AND version_number=$3`, [tenantId, documentId, version]);
      if (result.rowCount !== 1) throw new Error('Document version not found in tenant');
      const row = result.rows[0];
      const bytes = await storage.get(tenantKey(tenantId, row.object_key));
      if (!verifyVersion(bytes, {algoritmo: row.algorithm, valor: row.hash_hex, tamanhoBytes: Number(row.size_bytes)})) {
        await audit(documentId, 'integrity_failed', {version});
        throw new Error('Stored version integrity failed');
      }
      await audit(documentId, 'integrity_verified', {version});
      return bytes;
    },
    async process({documentId, sourceVersion, stage, processor}) {
      if (!['ocr', 'pdfa'].includes(stage) || typeof processor !== 'function') throw new TypeError('Invalid processor');
      // Verify the committed source before any processing or writes.
      const input = await this.readVersion(documentId, sourceVersion);
      try {
        const output = await processor(Buffer.from(input));
        // A PDF/A claim requires an independent validator report, not XMP alone.
        if (stage === 'pdfa' && (output?.validation?.valid !== true || !output.validation.validator)) {
          throw new Error('PDF/A validation evidence required');
        }
        // Detect source corruption during processing; never overwrite it.
        await this.readVersion(documentId, sourceVersion);
        return await createProcessingVersion({...context, documentId, stage, bytes: output?.bytes,
          sourceVersion, evidence: output?.validation || {}});
      } catch (error) {
        await audit(documentId, 'processing_failed', {stage, sourceVersion});
        throw error;
      }
    }
  };
  async function audit(documentId, action, details) {
    await pool.query(`INSERT INTO capture_integrity_audit(tenant_id,document_id,action,actor_id,details)
      VALUES($1,$2,$3,$4,$5)`, [tenantId, documentId, action, actorId, JSON.stringify(details)]);
  }
}
