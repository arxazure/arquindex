import test from 'node:test';
import assert from 'node:assert/strict';
import {legalCatalog,legalSources,modelById,selectedClauses,reviewIssues} from './legal-catalog.js';
test('catalogue IDs are unique and source refs resolve',()=>{
 assert.ok(legalCatalog.length>=12);
 assert.equal(new Set(legalCatalog.map(m=>m.id)).size,legalCatalog.length);
 for(const m of legalCatalog){assert.equal(m.status,'DRAFT_UNREVIEWED');assert.ok(m.sections.length);for(const source of m.sources)assert.ok(legalSources[source]);}
});
test('core clauses are selected even when unchecked',()=>{
 const m=modelById('contrato-servicos');const s=selectedClauses(m,{parties:false,privacy:false});
 assert.ok(s.some(x=>x.id==='parties'));assert.ok(!s.some(x=>x.id==='privacy'));
});
test('conditional and missing data block unsupported readiness',()=>{
 const m=modelById('contrato-servicos');const warnings=reviewIssues(m,{},{ });
 assert.ok(warnings.some(w=>w.includes('não homologado')));
 assert.ok(warnings.some(w=>w.includes('condicional')));
 assert.ok(warnings.some(w=>w.includes('Campo pendente')));
});
