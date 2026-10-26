/**
 * Arquindex Capture Pro - integrity manifest for physical-to-digital conversion.
 * Decreto 10.278/2020 Annex II: mandatory descriptive metadata and image checksum.
 * A checksum is NOT an ICP-Brasil signature or evidence of regulatory compliance.
 * This module is side-effect free; consumers persist manifests + audit trails durably.
 */
import { createHash, randomUUID } from 'node:crypto';

export const METADATA_ALL = Object.freeze([
  'assunto', 'autor', 'dataDigitalizacao', 'localDigitalizacao',
  'identificadorDigital', 'responsavelDigitalizacao', 'titulo', 'tipoDocumental'
]);
export const METADATA_PUBLIC_BODY = Object.freeze([
  'classe', 'dataProducaoOriginal', 'destinacaoPrevista', 'genero', 'prazoGuarda'
]);

const sha256 = bytes => createHash('sha256').update(bytes).digest('hex');
const nonempty = x => typeof x === 'string' && x.trim().length > 0;

/** Input must contain actual file bytes as Buffer/Uint8Array, not a filename. */
export function checksum(bytes) {
  if (!(bytes instanceof Uint8Array)) throw new TypeError('File bytes required');
  return { algoritmo: 'SHA-256', valor: sha256(bytes), tamanhoBytes: bytes.byteLength };
}
export function validateMetadata(metadata, { publicBody = false } = {}) {
  const required = publicBody ? [...METADATA_ALL, ...METADATA_PUBLIC_BODY] : METADATA_ALL;
  const missing = required.filter(k => !nonempty(metadata?.[k]));
  if (nonempty(metadata?.dataDigitalizacao) && !Number.isFinite(Date.parse(metadata.dataDigitalizacao))) {
    missing.push('dataDigitalizacao (formato invalido)');
  }
  if (nonempty(metadata?.dataProducaoOriginal) && !Number.isFinite(Date.parse(metadata.dataProducaoOriginal))) {
    missing.push('dataProducaoOriginal (formato invalido)');
  }
  return { valid: missing.length === 0, missing };
}

/**
 * Called immediately when bytes arrive from scanner or upload.
 * Imported born-digital documents must carry origem='nato_digital' and
 * must not be described as compliant scans under Decreto 10.278/2020.
 */
export function registerInput({ bytes, metadata, origem, actorId, tenantId, publicBody = false }) {
  if (!['scanner', 'importado_fisico', 'nato_digital'].includes(origem)) throw new TypeError('Invalid origin');
  if (!nonempty(actorId) || !nonempty(tenantId)) throw new TypeError('Actor and tenant required');
  const inputHash = checksum(bytes);
  const id = metadata?.identificadorDigital || randomUUID();
  const fields = { ...metadata, identificadorDigital: id };
  const check = origem === 'nato_digital' ? { valid: true, missing: [], note: 'Fora do escopo do Decreto 10.278/2020; metadados a validar conforme politica do cliente' } : validateMetadata(fields, { publicBody });
  const timestamp = new Date().toISOString();
  return {
    documentoId: id, tenantId, origem, publicBody, capturedAt: timestamp, actorId,
    metadata: fields, metadataValidation: check,
    versions: [{ stage: 'recebido', createdAt: timestamp, actorId, ...inputHash }],
    status: check.valid ? 'aguardando_conferencia' : 'metadados_pendentes',
    assinatura: { status: 'nao_assinado' }
  };
}
/**
 * Every OCR, deskew, PDF/A or signing operation yields another immutable version.
 * Hash the signed binary AFTER signing; do not overwrite the received hash.
 */
export function appendVersion(manifest, { bytes, stage, actorId }) {
  if (!nonempty(stage) || !nonempty(actorId)) throw new TypeError('Stage and actor required');
  return { ...manifest, versions: [...manifest.versions, {
    stage, createdAt: new Date().toISOString(), actorId, ...checksum(bytes)
  }] };
}
export function verifyVersion(bytes, version) {
  return version?.algoritmo === 'SHA-256' && checksum(bytes).valor === version.valor &&
    bytes.byteLength === version.tamanhoBytes;
}
export function readyForSigning(manifest, { icpRequired = false } = {}) {
  const check = validateMetadata(manifest.metadata, { publicBody: !!manifest.publicBody });
  return { ready: check.valid, missing: check.missing, icpRequired };
}
