import test from 'node:test';
import assert from 'node:assert/strict';
import {classify,recommend} from './semantic-editorial-export.mjs';

test('recognizes real editorial cluster',()=>{
 assert.equal(classify({title:'Adequação LGPD para empresas'}),'lgpd');
});
test('keeps all recommendations unpublished',()=>{
 const result=recommend({slug:'a',title:'Alfresco ECM',lead:'Gestão documental'});
 assert.equal(result.approvedForPublish,false);
 assert.equal(result.suggestedBlock?.status,'requires_human_review');
});
test('does not force unrelated topics',()=>{
 assert.equal(classify({title:'Tema sem correspondência'}),null);
 assert.equal(recommend({slug:'x',title:'Tema sem correspondência'}).suggestedBlock,null);
});
