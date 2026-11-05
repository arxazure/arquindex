import test from 'node:test';
import assert from 'node:assert/strict';
import {evaluateDecision,applyDecision,roleFor,hasVerifiedRole,hasConsistentApprovals} from './decision-policy.js';
const hash='a'.repeat(64);
test('role and hash are required for documented decisions',()=>{
 const base={stage:'REVISAO_JURIDICA_1',decision:'approve',actorRole:'legal',note:'Texto revisado e conferido.',documentHash:hash};
 assert.equal(evaluateDecision(base).ok,true);
 assert.equal(evaluateDecision({...base,actorRole:'requester'}).ok,false);
 assert.equal(evaluateDecision({...base,documentHash:'invalid'}).ok,false);
 assert.equal(evaluateDecision({...base,note:'ok'}).ok,false);
});
test('author cannot approve or homologate own document',()=>{
 const base={stage:'APROVACAO',decision:'approve',actorRole:'approver',note:'Conferência completa e adequada.',documentHash:hash,authorId:'user-1',actorId:'user-1'};
 assert.equal(evaluateDecision(base).ok,false);
 assert.equal(evaluateDecision({...base,actorId:'user-2'}).ok,true);
});
test('signed and published outcomes require real integrations',()=>{
 const q={stage:'AGUARDANDO_ASSINATURA',decision:'approve',actorRole:'signer',note:'Documento completo e revisado.',documentHash:hash};
 assert.equal(evaluateDecision(q).ok,false);
 assert.equal(roleFor('AGUARDANDO_PUBLICACAO'),'publisher');
});
test('request changes returns to draft preparation stage',()=>{
 const stages=['SOLICITACAO','MINUTA','REVISAO_CLIENTE','REVISAO_JURIDICA_1','REVISAO_TECNICA','APROVACAO'];
 assert.deepEqual(applyDecision({stages,index:3,decision:'request_changes'}),{ok:true,index:1,state:'REWORK_REQUIRED'});
 assert.equal(applyDecision({stages,index:5,decision:'approve'}).ok,false);
});

test('requires verified role membership and matching approved document versions',()=>{
 assert.equal(hasVerifiedRole({verified:true,roles:['legal','technical']},'legal'),true);
 assert.equal(hasVerifiedRole({verified:false,role:'legal'},'legal'),false);
 const h='b'.repeat(64);
 const stages=[{status:'APPROVED'},{status:'APPROVED',document_version_hash:h},{status:'ACTIVE'}];
 assert.equal(hasConsistentApprovals(stages,2,h),true);
 assert.equal(hasConsistentApprovals(stages,2,'a'.repeat(64)),false);
 assert.equal(hasConsistentApprovals([{status:'APPROVED'},{status:'PENDING',document_version_hash:h},{status:'ACTIVE'}],2,h),false);
});
