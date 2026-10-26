import {createHash,randomUUID} from 'node:crypto';
const sha256=bytes=>createHash('sha256').update(bytes).digest('hex');
const required=['subject','author','digitized_at','digitized_location','responsible','title','document_type'];
const publicRequired=['classification','original_produced_at','planned_destination','genre','retention_period'];
export function inspectDocument(bytes,metadata={},options={}){
 if(!Buffer.isBuffer(bytes)||bytes.length===0)throw Error('Arquivo vazio');
 const missing=[...required,...(options.publicBody?publicRequired:[])].filter(k=>!String(metadata[k]??'').trim());
 const digest=sha256(bytes);
 return {id:randomUUID(),algorithm:'SHA-256',sourceHash:digest,sourceBytes:bytes.length,metadata:{...metadata,digital_identifier:randomUUID(),image_hash:digest,imported_at:new Date().toISOString()},missing,status:missing.length?'pending_metadata':'pending_validation',legalDisclaimer:'Hash isolado não substitui assinatura ICP-Brasil ou conferência exigida pelo Decreto 10.278/2020'};
}
export function verifyDocument(bytes,expected){if(!/^[a-f0-9]{64}$/i.test(expected||''))throw Error('Hash inválido');return sha256(bytes)===expected.toLowerCase();}
export function recordDerivative(originalRecord,derivedBytes,processing){return {sourceId:originalRecord.id,sourceHash:originalRecord.sourceHash,derivativeHash:sha256(derivedBytes),operation:processing,processedAt:new Date().toISOString()};}
