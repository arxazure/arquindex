import test from 'node:test';
import assert from 'node:assert/strict';
import {qualityForCompany,dossierForCompany,safeCorrections} from '../quality.js';
const company='7ebfb6d6-cee7-4649-ac25-fb6bdfb42a95';
const recs=[
 {id:company,company_id:company,section:'company',payload:{company_name:'MINAS MOTOS',company_cnpj:'01.566.501/0001-00',company_city:'Belo Horizonte',company_state:'MF',company_email:'',company_dpo:'Marina Lopes'}},
 {id:'branch1',company_id:company,section:'branch',parent_id:company,payload:{name:'MINAS MOTOS MATRIZ CNPJ nº 01.566.501/0001-00',city:'Belo Horizonte',address:'Avenida do Contorno'}},
 {id:'policy1',company_id:company,section:'policy',payload:{name:'Minuta Política de Privacidade',text:'RASCUNHO - Política em fase de revisão para aprovação. '+('Texto documental. '.repeat(20)),status:'Publicado',version:'1.0'}},
 {id:'policy2',company_id:company,section:'policy',payload:{name:'Política de Privacidade - Dossiê 1.0',text:'Texto em validação. '+('Texto. '.repeat(35)),status:'Rascunho'}}
];
test('Identifies published drafts, missing contact, invalid UF and missing modules',()=>{
 const q=qualityForCompany(recs);
 assert.ok(q.issues.some(x=>x.severity==='critical'&&x.section==='policy'));
 assert.ok(q.issues.some(x=>x.field==='company_email'));
 assert.ok(q.issues.some(x=>x.field==='company_state'));
 assert.ok(q.issues.some(x=>x.section==='process'));
});
test('Deterministic reconciliation only copies source facts and revokes draft publication',()=>{
 const fixes=safeCorrections(recs);
 assert.ok(fixes.some(x=>x.field==='company_state'&&x.after==='MG'));
 assert.ok(fixes.some(x=>x.field==='branch_cnpj'&&x.after==='01.566.501/0001-00'));
 assert.ok(fixes.some(x=>x.field==='branch_type'&&x.after==='Matriz'));
 assert.ok(fixes.some(x=>x.field==='status'&&x.after==='Rascunho'));
 assert.equal(fixes.some(x=>x.field==='company_email'),false);
});
test('Dossier preserves full original policy text and marks draft',()=>{
 const doc=dossierForCompany(recs,new Date('2026-11-11T14:00:00Z'));
 assert.equal(doc.status,'RASCUNHO');
 assert.ok(doc.blocks.some(x=>x.kind==='paragraph'&&x.text.startsWith('RASCUNHO - Política')));
 assert.ok(doc.blocks.some(x=>x.kind==='table'));
 assert.ok(doc.blocks.some(x=>x.kind==='section'&&x.text.includes('Políticas')));
});
test('Safe corrections idempotent after applying them in memory',()=>{
 const fixes=safeCorrections(recs);
 const updated=recs.map(r=>({...r,payload:{...r.payload}}));
 for(const f of fixes)updated.find(r=>r.id===f.id).payload[f.field]=f.after;
 assert.equal(safeCorrections(updated).length,0);
});
