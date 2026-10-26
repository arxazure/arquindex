import {registerInput,appendVersion,verifyVersion} from './decreto-10278.js';

/**
 * Transactional metadata registration. Caller must save bytes first in durable storage
 * under an immutable objectKey and verify storage ETag/size before committing metadata.
 * pool: pg Pool. No file bytes or document contents are logged.
 */
export async function persistInitial(pool, {bytes,metadata,origem,actorId,tenantId,publicBody=false,objectKey}) {
 if(typeof objectKey!=='string'||!objectKey) throw new Error('Immutable object key required');
 const m=registerInput({bytes,metadata,origem,actorId,tenantId,publicBody});
 const v=m.versions[0];
 const db=await pool.connect();
 try{
  await db.query('BEGIN');
  await db.query(`INSERT INTO capture_integrity_documents
   (tenant_id,document_id,origin,metadata,metadata_valid,metadata_missing,public_body,status,created_by)
   VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9)`,
   [tenantId,m.documentoId,origem,JSON.stringify(m.metadata),m.metadataValidation.valid,JSON.stringify(m.metadataValidation.missing),publicBody,m.status,actorId]);
  await db.query(`INSERT INTO capture_integrity_versions
   (tenant_id,document_id,version_number,stage,algorithm,hash_hex,size_bytes,object_key,created_by)
   VALUES ($1,$2,1,$3,$4,$5,$6,$7,$8)`,[tenantId,m.documentoId,v.stage,v.algoritmo,v.valor,v.tamanhoBytes,objectKey,actorId]);
  await db.query(`INSERT INTO capture_integrity_audit(tenant_id,document_id,action,actor_id,details)
  VALUES ($1,$2,'received',$3,$4)`,[tenantId,m.documentoId,actorId,JSON.stringify({origem,version:1})]);
  await db.query('COMMIT');
  return {documentoId:m.documentoId,status:m.status,hash:v.valor};
 } catch(e){await db.query('ROLLBACK');throw e;}finally{db.release();}
}
export async function persistDerived(pool,{tenantId,documentId,bytes,stage,actorId,objectKey}) {
 if(!objectKey)throw new Error('Immutable object key required');
 const db=await pool.connect();
 try{
  await db.query('BEGIN');
  const doc=await db.query('SELECT document_id FROM capture_integrity_documents WHERE tenant_id=$1 AND document_id=$2 FOR UPDATE',[tenantId,documentId]);
  if(doc.rowCount!==1)throw new Error('Document not found in tenant');
  const prior=await db.query('SELECT COALESCE(MAX(version_number),0) AS n FROM capture_integrity_versions WHERE tenant_id=$1 AND document_id=$2',[tenantId,documentId]);
  const n=Number(prior.rows[0].n)+1;
  const v=appendVersion({versions:[]},{bytes,stage,actorId}).versions[0];
  await db.query(`INSERT INTO capture_integrity_versions
  (tenant_id,document_id,version_number,stage,algorithm,hash_hex,size_bytes,object_key,created_by)
  VALUES($1,$2,$3,$4,$5,$6,$7,$8,$9)`,[tenantId,documentId,n,stage,v.algoritmo,v.valor,v.tamanhoBytes,objectKey,actorId]);
  await db.query(`INSERT INTO capture_integrity_audit(tenant_id,document_id,action,actor_id,details)
  VALUES($1,$2,'version_added',$3,$4)`,[tenantId,documentId,actorId,JSON.stringify({stage,version:n})]);
  await db.query('COMMIT');return {version:n,hash:v.valor};
 }catch(e){await db.query('ROLLBACK');throw e;}finally{db.release();}
}
export async function verifyStoredVersion(pool,{tenantId,documentId,version,loadObject}) {
 const q=await pool.query('SELECT algorithm,hash_hex,size_bytes,object_key FROM capture_integrity_versions WHERE tenant_id=$1 AND document_id=$2 AND version_number=$3',[tenantId,documentId,version]);
 if(!q.rowCount)return {ok:false,reason:'not_found'};
 const v=q.rows[0],bytes=await loadObject(v.object_key);
 const ok=verifyVersion(bytes,{algoritmo:v.algorithm,valor:v.hash_hex,tamanhoBytes:Number(v.size_bytes)});
 return {ok,reason:ok?'integrity_ok':'hash_mismatch'};
}
