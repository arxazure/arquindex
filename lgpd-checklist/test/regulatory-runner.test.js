import test from 'node:test';
import assert from 'node:assert/strict';
import {runRegulatoryCheck} from '../regulatory-runner.js';
import {runOfficialChecks} from '../regulatory-monitor.js';
import {regulatorySources} from '../regulatory-catalog.js';

function fake({done=[],busy=false,failAudit=false}={}){
 const calls=[];let held=busy;
 const pool={async connect(){return {async query(sql,args){calls.push([sql,args]);if(sql.includes('pg_try_advisory_lock')){const locked=!held;held=true;return {rows:[{locked}]};}if(sql.includes('pg_advisory_unlock'))held=false;if(sql.startsWith('SELECT DISTINCT'))return {rows:done.map(source_id=>({source_id}))};if(failAudit&&sql.startsWith('INSERT INTO lgpd_audit'))throw Error('audit unavailable');return {rows:[]};},release(destroy){calls.push(['release',destroy]);}};}};
 return {pool,calls};
}
test('manual and scheduled checks share lock across connections',async()=>{
 const f=fake();let finish;const wait=new Promise(r=>finish=r);let started;const ready=new Promise(r=>started=r);
 const first=runRegulatoryCheck(f.pool,{check:async()=>{started();await wait;return [];}});await ready;
 assert.equal((await runRegulatoryCheck(f.pool,{trigger:'manual'})).status,'busy');finish();await first;
 assert(f.calls.some(x=>x[0].includes('pg_advisory_unlock')));
});
test('successful sources skipped, failed/missing sources retried',async()=>{
 const f=fake({done:[regulatorySources[0].id]});let selected;
 const result=await runRegulatoryCheck(f.pool,{check:async(db,sources)=>{selected=sources;return sources.map(s=>({source_id:s.id,state:'error'}));}});
 assert.equal(selected.length,3);assert.equal(result.status,'partial_failure');assert(f.calls.some(x=>x[0]==='COMMIT'));
});
test('full daily success skips network and inserts',async()=>{
 const f=fake({done:regulatorySources.map(x=>x.id)});
 assert.equal((await runRegulatoryCheck(f.pool,{check:()=>assert.fail('unexpected fetch')})).status,'already_checked');
 assert(!f.calls.some(x=>x[0]==='BEGIN'));
});
test('audit failure rolls back and releases lock',async()=>{
 const f=fake({failAudit:true});await assert.rejects(runRegulatoryCheck(f.pool,{check:async()=>[]}),/audit unavailable/);
 assert(f.calls.some(x=>x[0]==='ROLLBACK'));assert(f.calls.some(x=>x[0].includes('pg_advisory_unlock')));
});
test('manual audit includes actor and source outcomes',async()=>{
 const f=fake();await runRegulatoryCheck(f.pool,{userId:'actor',trigger:'manual',check:async()=>[{source_id:'anpd-materiais',state:'baseline'}]});
 const audit=f.calls.find(x=>x[0].startsWith('INSERT INTO lgpd_audit'));assert.equal(audit[1][0],'actor');assert.equal(audit[1][1],'regulatory_check_manual');assert.match(audit[1][2],/baseline/);
});
test('collector records HTTP and timeout failures and continues',async()=>{
 const original=globalThis.fetch;let n=0;const inserts=[];
 try{
 globalThis.fetch=async()=>{if(n++===0)throw new DOMException('timeout','TimeoutError');return new Response('',{status:503});};
 const db={async query(sql,args){if(sql.startsWith('SELECT'))return {rowCount:0,rows:[]};inserts.push(args);return {};}};
 const result=await runOfficialChecks(db,regulatorySources.slice(0,2));assert.equal(result.length,2);assert(result.every(x=>x.state==='error'));assert.equal(inserts.length,2);
 }finally{globalThis.fetch=original;}
});
