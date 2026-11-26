import test from 'node:test';
import assert from 'node:assert/strict';
import {validObservations,summarizeObservations} from './observations.mjs';
import {importSnapshot} from './import-snapshot.mjs';
import {handle,render} from './server.mjs';
const row={kind:'ranking',key:'query · device · country',source:'authorized export',account:'test property',observedAt:'2026-10-27T12:00:00Z',evidenceId:'fixture-only',status:'observed',url:'https://example.org/',value:4};
const snapshot={schemaVersion:1,collectedAt:row.observedAt,metrics:[],observations:[row]};
test('observations require traceability and safe URLs without coercing ranks',()=>{
 assert.ok(validObservations([row]));
 for(const patch of [{kind:'other'},{source:''},{account:''},{evidenceId:''},{observedAt:'bad'},{url:'javascript:alert(1)'},{url:'https://user:pass@example.org/'},{value:0},{value:'4'},{status:'published'}])assert.equal(validObservations([{...row,...patch}]),false);
 assert.equal(summarizeObservations([])[0].observed,null);
 const result=summarizeObservations([row,{...row,status:'error',value:null,observedAt:'2026-10-28T12:00:00Z'}]);
 assert.equal(result[0].observed,0);assert.equal(result[0].entries.length,1);
});
test('offline import validates snapshots and private endpoint rejects malformed evidence',()=>{
 assert.deepEqual(JSON.parse(importSnapshot(JSON.stringify(snapshot))),snapshot);
 assert.throws(()=>importSnapshot(JSON.stringify({...snapshot,observations:[{...row,account:''}]})));
 const token='x'.repeat(48);
 const response=handle(new Request('https://test/api/snapshot',{headers:{authorization:'Bearer '+token}}),{TOP10_INTERNAL_TOKEN:token,TOP10_SNAPSHOT_JSON:JSON.stringify({...snapshot,observations:[null]})});
 assert.equal(response.status,503);
});
test('evidence output escapes text, preserves goals and discloses sample limits',()=>{
 const html=render({...snapshot,observations:[{...row,key:'<script>bad</script>'}]});
 assert.ok(!html.includes('<script>'));assert.ok(html.includes('&lt;script&gt;'));
 assert.ok(html.includes('não é total de produção'));assert.ok(html.includes('Meta planejada'));
 assert.ok(html.includes('Sem dados fornecidos'));
});

test('AI citation observations distinguish cited, unlinked mentions and absent results',()=>{
 const base={...row,kind:'ai_citations',key:'ChatGPT | digitalização certificada em BH | pt-BR | sessão controlada'};
 for(const value of ['cited','mentioned_without_link','not_cited']) assert.ok(validObservations([{...base,value}]));
 for(const value of [1,'yes','ranking','']) assert.equal(validObservations([{...base,value}]),false);
 const html=render({...snapshot,observations:[{...base,value:'not_cited'}]});
 assert.ok(html.includes('Citações em respostas de IA'));assert.ok(html.includes('not_cited'));
 assert.equal(summarizeObservations([{...base,status:'unavailable',value:null}]).at(-1).observed,0);
});
