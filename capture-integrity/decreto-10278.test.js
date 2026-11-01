import test from 'node:test';
import assert from 'node:assert/strict';
import {checksum,registerInput,appendVersion,verifyVersion,validateMetadata} from './decreto-10278.js';
const metadata={assunto:'Contrato',autor:'Emitente',dataDigitalizacao:'2026-10-26T14:00:00-03:00',localDigitalizacao:'BH',identificadorDigital:'e2ea8a45-4381-43a6-9366-cd1a5ead507a',responsavelDigitalizacao:'Arquindex',titulo:'Contrato de teste',tipoDocumental:'Contrato'};
test('SHA-256 is deterministic and sensitive to byte changes',()=>{
 const a=Buffer.from('first'),b=Buffer.from('second');
 assert.equal(checksum(a).valor,checksum(a).valor);
 assert.notEqual(checksum(a).valor,checksum(b).valor);
});
test('missing mandatory metadata prevents readiness',()=>{
 assert.equal(validateMetadata({}).valid,false);
 assert.equal(validateMetadata(metadata).valid,true);
 assert.equal(validateMetadata(metadata,{publicBody:true}).valid,false);
});
test('version hashes remain unchanged after processing',()=>{
 const raw=Buffer.from('original'),processed=Buffer.from('processed');
 const m=registerInput({bytes:raw,metadata,origem:'scanner',actorId:'operator',tenantId:'company'});
 const n=appendVersion(m,{bytes:processed,stage:'ocr',actorId:'operator'});
 assert.equal(n.versions.length,2);
 assert.equal(n.versions[0].valor,m.versions[0].valor);
 assert.equal(verifyVersion(raw,n.versions[0]),true);
 assert.equal(verifyVersion(processed,n.versions[0]),false);
 assert.equal(verifyVersion(processed,n.versions[1]),true);
});
test('born digital imports are not certified scans',()=>{
 const m=registerInput({bytes:Buffer.from('a'),metadata:{},origem:'nato_digital',actorId:'operator',tenantId:'company'});
 assert.match(m.metadataValidation.note,/Fora do escopo/);
});
