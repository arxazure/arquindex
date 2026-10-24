const {test}=require('node:test');
const assert=require('node:assert/strict');
const {readFileSync}=require('node:fs');
const {randomUUID}=require('node:crypto');
const source=readFileSync(__dirname+'/server.js','utf8');
const block=source.slice(source.indexOf('const bootstrapEmail='),source.indexOf("\napp.get('/health'"));
const run=new (Object.getPrototypeOf(async function(){}).constructor)('process','Q','bcrypt','db','randomUUID','console',block);
async function scenario(env,existing={id:randomUUID(),password_hash:'hash',role:'admin'},matches=true,failInsert=false){
 const writes=[],logs=[];let released=false;
 const Q=async(sql,args)=>{if(sql.startsWith('select'))return {rowCount:existing?1:0,rows:existing?[existing]:[]};writes.push({sql,args});return {rowCount:1}};
 const bcrypt={compare:async(p,h)=>{assert.equal(h,'hash');return matches},hash:async(p)=>'new:'+p};
 const db={connect:async()=>({query:async(sql,args)=>{writes.push({sql,args});if(failInsert&&sql.startsWith('insert into users'))throw Error('insert failed')},release:()=>{released=true}})};
 await run({env},Q,bcrypt,db,randomUUID,{log:x=>logs.push(x)});
 return {writes,logs,released};
}
const env={BOOTSTRAP_ADMIN_EMAIL:' ADMIN@example.test ',BOOTSTRAP_ADMIN_PASSWORD:'long-test-password-12345'};
test('existing account ignores unused short bootstrap password',async()=>{const r=await scenario({...env,BOOTSTRAP_ADMIN_PASSWORD:'short'});assert.equal(r.writes.length,0)});
test('missing bootstrap leaves accounts unchanged',async()=>{assert.equal((await scenario({})).writes.length,0)});
test('reset false preserves stored hash',async()=>{assert.equal((await scenario({...env,BOOTSTRAP_ADMIN_RESET:'false'},undefined,false)).writes.length,0)});
test('same password does not rehash on restart',async()=>{assert.equal((await scenario({...env,BOOTSTRAP_ADMIN_RESET:'true'})).writes.length,0)});
test('explicit reset accepts exact supported flag variants',async()=>{for(const flag of ['true',' TRUE ','"true"',"'true'"]){const r=await scenario({...env,BOOTSTRAP_ADMIN_RESET:flag},undefined,false);assert.equal(r.writes.length,1);assert.match(r.writes[0].sql,/update users/)}});
test('false or malformed legacy flag never resets',async()=>{for(const flag of ['false','','untrue','!true!'])assert.equal((await scenario({...env,'BOOTSTRAP_ADMIN_RESET=true':flag},undefined,false)).writes.length,0)});
test('legacy true is supported and canonical false takes priority',async()=>{assert.equal((await scenario({...env,'BOOTSTRAP_ADMIN_RESET=true':'true'},undefined,false)).writes.length,1);assert.equal((await scenario({...env,'BOOTSTRAP_ADMIN_RESET=true':'true',BOOTSTRAP_ADMIN_RESET:'false'},undefined,false)).writes.length,0)});
test('reset rejects short and bcrypt-truncated passwords',async()=>{for(const pw of ['short','á'.repeat(37)])await assert.rejects(scenario({...env,BOOTSTRAP_ADMIN_PASSWORD:pw,BOOTSTRAP_ADMIN_RESET:'true'}),/Bootstrap password/)});
test('password whitespace is preserved and secrets are absent from logs',async()=>{const pw='  long-test-password-12345  ';const r=await scenario({...env,BOOTSTRAP_ADMIN_PASSWORD:pw,BOOTSTRAP_ADMIN_RESET:'true'},undefined,false);assert.equal(r.writes[0].args[0],'new:'+pw);assert.ok(!r.logs.join().includes(pw));assert.ok(!r.logs.join().includes('example.test'))});
test('bootstrap never changes non-admin credentials',async()=>{await assert.rejects(scenario({...env,BOOTSTRAP_ADMIN_RESET:'true'},{id:randomUUID(),role:'viewer'},false),/non-admin/)});
test('new admin creation commits and releases connection',async()=>{const r=await scenario(env,null);assert.equal(r.writes[0].sql,'BEGIN');assert.equal(r.writes.at(-1).sql,'COMMIT');assert.equal(r.released,true);assert.equal(r.writes.find(x=>x.sql.startsWith('insert into users')).args[2],'admin@example.test')});
test('new admin failure rolls back and releases connection',async()=>{await assert.rejects(scenario(env,null,true,true),/insert failed/)});
