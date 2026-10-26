import test from 'node:test';
import assert from 'node:assert/strict';
import {ingestDocument} from './ingestion.js';
const meta={assunto:'Ficha',autor:'Emitente',dataDigitalizacao:'2026-10-26T15:30:00-03:00',localDigitalizacao:'Belo Horizonte',responsavelDigitalizacao:'Arquindex',titulo:'Ficha teste',tipoDocumental:'Ficha'};
test('input is persisted only after storage readback hash matches',async()=>{
 const events=[]; const bytes=Buffer.from('documento de teste');
 const store=new Map();
 const storage={async putImmutable(key,value){assert.equal(store.has(key),false);store.set(key,Buffer.from(value));events.push('stored');},async get(key){events.push('verified');return store.get(key);}};
 const client={async query(sql,args){if(sql==='BEGIN'||sql==='COMMIT'||sql==='ROLLBACK'){events.push(sql);return {rows:[],rowCount:0};}events.push('sql');return {rows:[],rowCount:1};},release(){}};
 const pool={async connect(){return client;}};
 const result=await ingestDocument({pool,storage,tenantId:'cliente-a',actorId:'operador',bytes,metadata:meta,origem:'scanner'});
 assert.equal(result.status,'aguardando_conferencia');
 assert.deepEqual(events.slice(0,3),['stored','verified','BEGIN']);
 assert.ok(events.includes('COMMIT'));
});
test('tampered storage prevents database insert',async()=>{
 const pool={async connect(){throw Error('Database should not be accessed');}};
 const storage={async putImmutable(){},async get(){return Buffer.from('alterado');}};
 await assert.rejects(ingestDocument({pool,storage,tenantId:'cliente-a',actorId:'operador',bytes:Buffer.from('documento'),metadata:meta,origem:'scanner'}),/differ/);
});
