import {randomUUID} from 'node:crypto';
import {checksum} from './decreto-10278.js';
import {persistInitial,persistDerived} from './persistence.js';

/**
 * Reference adapter for scanner/PaperStream output and uploaded files.
 *
 * storage.putImmutable(key, bytes) MUST reject overwrite and durably write bytes.
 * storage.get(key) MUST return exact binary bytes and enforce tenant access.
 * This adapter validates stored bytes before committing the manifest.
 * Files placed in storage without a committed database record must be reconciled
 * by a separate, audited orphan cleanup job (not deleted automatically here).
 */
export async function ingestDocument({pool,storage,tenantId,actorId,bytes,metadata,origem,publicBody=false}) {
 if(!(bytes instanceof Uint8Array) || bytes.byteLength===0) throw new TypeError('Nonempty file required');
 if(!tenantId || !actorId) throw new TypeError('Authenticated tenant and actor required');
 const key=tenantId+'/capture/'+randomUUID()+'/received';
 await storage.putImmutable(key,bytes);
 const stored=await storage.get(key);
 if(checksum(stored).valor!==checksum(bytes).valor) throw new Error('Stored bytes differ from input');
 return persistInitial(pool,{tenantId,actorId,bytes,metadata,origem,publicBody,objectKey:key});
}
export async function createProcessingVersion({pool,storage,tenantId,documentId,actorId,stage,bytes}) {
 if(!(bytes instanceof Uint8Array) || bytes.byteLength===0) throw new TypeError('Nonempty file required');
 if(!['conferencia','ocr','pdfa','assinado','entrega'].includes(stage)) throw new TypeError('Invalid stage');
 const key=tenantId+'/capture/'+documentId+'/'+stage+'/'+randomUUID();
 await storage.putImmutable(key,bytes);
 const stored=await storage.get(key);
 if(checksum(stored).valor!==checksum(bytes).valor)throw new Error('Storage integrity validation failed');
 return persistDerived(pool,{tenantId,documentId,actorId,stage,bytes,objectKey:key});
}
