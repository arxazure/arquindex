import test from 'node:test';
import assert from 'node:assert/strict';
import {compare,handle,render} from './server.mjs';
test('colors respect direction, missing values and a zero baseline',()=>{
  assert.equal(compare(78,76).color,'green');
  assert.equal(compare(1,4).color,'red');
  assert.equal(compare(19.8,18.8,true).color,'red');
  assert.equal(compare(10,20,true).color,'green');
  for(const v of [null,undefined,NaN,'2']) assert.equal(compare(v,0).color,'gray');
  assert.equal(compare(1,0).percent,null);
  assert.equal(compare(0,0).color,'gray');
});
test('backend fails closed; only authenticated read routes expose snapshots',async()=>{
  const snapshot={schemaVersion:1,collectedAt:'2026-10-24T22:00:00Z',metrics:[]};
  const env={TOP10_INTERNAL_TOKEN:'x'.repeat(48),TOP10_SNAPSHOT_JSON:JSON.stringify(snapshot)};
  assert.equal(handle(new Request('https://test/api/snapshot'),env).status,401);
  assert.equal(handle(new Request('https://test/dashboard',{headers:{authorization:'Bearer wrong'}}),env).status,401);
  const req=(path,method='GET')=>new Request('https://test'+path,{method,headers:{authorization:'Bearer '+env.TOP10_INTERNAL_TOKEN}});
  assert.equal(handle(req('/api/snapshot'),{}).status,401);
  assert.equal(handle(req('/api/snapshot','POST'),env).status,405);
  assert.equal(handle(req('/api/snapshot'),{...env,TOP10_SNAPSHOT_JSON:'bad'}).status,503);
  const res=handle(req('/api/snapshot'),env);
  assert.equal(res.status,200);assert.equal(res.headers.get('cache-control'),'no-store, private');
  assert.deepEqual(await res.json(),snapshot);
  assert.equal(handle(new Request('https://test/'),env).headers.get('location'),'https://capture-hub-production.up.railway.app/admin/top10');
});
test('provider strings cannot inject HTML or unsafe links',()=>{
  const html=render({collectedAt:'2026-10-24T22:00:00Z',metrics:[{label:'<script>alert(1)</script>',current:null,previous:null}],receipts:[{url:'javascript:alert(1)',id:'link'}]});
  assert.ok(!html.includes('<script>'));assert.ok(!html.includes('href="javascript:'));assert.ok(html.includes('Sem dados comparáveis'));
});
