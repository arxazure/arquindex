import test from 'node:test';
import assert from 'node:assert/strict';
import vm from 'node:vm';
import {readFileSync} from 'node:fs';
import {stripTypeScriptTypes} from 'node:module';
import {createHmac,webcrypto} from 'node:crypto';
const source=stripTypeScriptTypes(readFileSync(new URL('./capture-hub.tsx',import.meta.url),'utf8'));
function setup(){
  let handler; let calls=0;
  const secret='test-session-secret-only';
  const context={TextEncoder,Request,Response,URL,URLSearchParams,AbortSignal,Buffer,btoa,atob,escape,unescape,encodeURIComponent,decodeURIComponent,crypto:webcrypto,
    Bun:{env:{GOOGLE_CLIENT_ID:'test',GOOGLE_CLIENT_SECRET:'test',SESSION_SECRET:secret,TOP10_INTERNAL_TOKEN:'x'.repeat(48)},serve:o=>{handler=o.fetch;}},
    fetch:async(url,options)=>{calls++;assert.equal(options.headers.authorization,'Bearer '+'x'.repeat(48));assert.ok(String(url).startsWith('https://top10-google-dashboard-production.up.railway.app/'));return new Response('private-marker',{headers:{'content-type':'text/html'}});}};
  vm.runInNewContext(source,context);
  const session=(email='arquindex@gmail.com',exp=Date.now()+60000)=>{const payload=Buffer.from(JSON.stringify({email,exp})).toString('base64url');return payload+'.'+createHmac('sha256',secret).update(payload).digest('base64url');};
  return {handler,session,calls:()=>calls};
}
test('Hub protects both routes and does not forward anonymous requests',async()=>{
  const x=setup();
  for(const path of ['/admin/top10','/admin/top10/data']){
    for(const cookie of ['', 'capture_session=forged','capture_session='+x.session('other@example.com'),'capture_session='+x.session('arquindex@gmail.com',Date.now()-1)]){
      const r=await x.handler(new Request('https://hub'+path,{headers:{cookie}}));
      assert.equal(r.status,302);assert.equal(r.headers.get('location'),'/admin');
    }
  }
  assert.equal(x.calls(),0);
});
test('Hub forwards authenticated reads with private caching and no cookie forwarding',async()=>{
  const x=setup();const headers={cookie:'capture_session='+x.session()};
  for(const path of ['/admin/top10','/admin/top10/data']){
    const r=await x.handler(new Request('https://hub'+path,{headers}));
    assert.equal(r.status,200);assert.equal(await r.text(),'private-marker');assert.equal(r.headers.get('cache-control'),'no-store, private');
  }
  const rejected=await x.handler(new Request('https://hub/admin/top10',{method:'POST',headers}));
  assert.equal(rejected.status,405);assert.equal(x.calls(),2);
});
