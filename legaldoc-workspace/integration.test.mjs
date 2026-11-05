import assert from 'node:assert/strict';
import pg from 'pg';
import {randomUUID} from 'node:crypto';
if(process.env.LEGALDOC_DISPOSABLE_TEST!=='true')throw new Error('Requires LEGALDOC_DISPOSABLE_TEST=true and a disposable PostgreSQL database');
const base='http://localhost:3001',origin=base;
async function call(path,method='GET',body,session){
 const headers={Origin:origin};
 if(body!==undefined)headers['Content-Type']='application/json';
 if(session){headers.Cookie=session.cookie;if(method!=='GET')headers['X-CSRF-Token']=session.csrf;}
 const r=await fetch(base+path,{method,headers,body:body===undefined?undefined:JSON.stringify(body)});
 const data=await r.json();
 return {r,data};
}
function cookies(res){
 const list=res.headers.getSetCookie();
 const cookie=list.map(x=>x.split(';')[0]).join('; ');
 const csrf=/ldw_csrf=([^;]+)/.exec(cookie)?.[1];
 assert.ok(csrf,'CSRF cookie required');
 return {cookie,csrf};
}
const status=await call('/api/setup-status');assert.equal(status.r.status,200);assert.equal(status.data.needsSetup,true);
const setup=await call('/api/setup','POST',{setupToken:process.env.ADMIN_SETUP_TOKEN,company:'Arquindex QA',email:'admin@example.org',password:'Strong-Test-Pass-2026!!!'});
assert.equal(setup.r.status,200,JSON.stringify(setup.data));
const admin=cookies(setup.r);
const noSetup=await call('/api/setup-status');assert.equal(noSetup.data.needsSetup,false);
const fail=await call('/api/docs','POST',{title:'Unsafe'});assert.equal(fail.r.status,401);
const create=await call('/api/docs','POST',{title:'Termo de Confidencialidade Teste',kind:'NDA de teste',description:'Proteger informacoes ficticias da empresa QA.',legalEmails:['legal@example.org'],rounds:2,destination:'SIGN'},admin);
assert.equal(create.r.status,201,JSON.stringify(create.data));
const id=create.data.doc.id;
const edit=await call('/api/docs/'+id+'/body','PUT',{body:'TERMO DE CONFIDENCIALIDADE — TEXTO FICTICIO. A empresa QA preservara segredos industriais exclusivamente para avaliacao documental, com prazo, responsabilidades e procedimentos previstos nas clausulas aprovadas pelas partes. Documento nao valido juridicamente.'},admin);
assert.equal(edit.r.status,200,JSON.stringify(edit.data));
const version=await call('/api/docs/'+id,'GET',undefined,admin);assert.equal(version.data.doc.version,2);
const approve=await call('/api/docs/'+id+'/decision','POST',{decision:'APPROVE',note:'Minuta de teste completada e submetida a revisao.'},admin);
assert.equal(approve.r.status,200,JSON.stringify(approve.data));assert.equal(approve.data.nextStage,'REVISAO_CLIENTE');
const cannot=await call('/api/docs/'+id+'/decision','POST',{decision:'APPROVE',note:'Admin tentou aprovar como cliente.'},admin);assert.equal(cannot.r.status,403);
const user=await call('/api/users','POST',{email:'client@example.org',role:'client'},admin);assert.equal(user.r.status,201);
const userId=user.data.id,pwd=user.data.temporaryPassword;
const verify=await call('/api/users/'+userId+'/verify','POST',{justification:'Identidade confirmada por procedimento de auditoria interno.'},admin);assert.equal(verify.r.status,200);
const login=await call('/api/login','POST',{email:'client@example.org',password:pwd});assert.equal(login.data.mustChangePassword,true);
const client=cookies(login.r);
const me=await call('/api/me','GET',undefined,client);assert.equal(me.data.mustChangePassword,true);
for(const [path,method,body] of [
 ['/api/docs','GET'],['/api/docs','POST',{}],['/api/docs/'+id,'GET'],
 ['/api/docs/'+id+'/body','PUT',{body:'x'.repeat(100)}],
 ['/api/docs/'+id+'/assign','POST',{stage:'REVISAO_CLIENTE',userId}],
 ['/api/docs/'+id+'/decision','POST',{decision:'APPROVE',note:'Teste de bloqueio obrigatório.'}],
 ['/api/users','GET'],['/api/users','POST',{}],['/api/users/'+userId+'/verify','POST',{}],
 ['/api/future-feature','GET']
]){const denied=await call(path,method,body,client);assert.equal(denied.r.status,403,path);assert.match(denied.data.error,/senha temporária/);}
async function raw(path,method,session,extra={},body={}){
 return fetch(base+path,{method,headers:{Origin:origin,Cookie:session.cookie,'Content-Type':'application/json',...extra},body:JSON.stringify(body)});
}
assert.equal((await raw('/api/change-password','POST',client,{}, {currentPassword:pwd,newPassword:'Safe-Rotated-Password-2026!!!'})).status,403);
assert.equal((await raw('/api/logout','POST',client,{'X-CSRF-Token':'wrong'})).status,403);
assert.equal((await raw('/api/logout','POST',client,{'X-CSRF-Token':client.csrf,Origin:'https://attacker.example'})).status,403);
const wrongPassword=await call('/api/change-password','POST',{currentPassword:'incorrect',newPassword:'Safe-Rotated-Password-2026!!!'},client);assert.equal(wrongPassword.r.status,403);
const stillBlocked=await call('/api/docs','GET',undefined,client);assert.equal(stillBlocked.r.status,403);
const secondLogin=await call('/api/login','POST',{email:'client@example.org',password:pwd});
const otherSession=cookies(secondLogin.r);
const logout=await call('/api/logout','POST',{},otherSession);assert.equal(logout.r.status,200);
assert.equal((await call('/api/me','GET',undefined,otherSession)).r.status,401);
const concurrentSession=cookies((await call('/api/login','POST',{email:'client@example.org',password:pwd})).r);

const rotate=await call('/api/change-password','POST',{currentPassword:pwd,newPassword:'Safe-Rotated-Password-2026!!!'},client);assert.equal(rotate.r.status,200,JSON.stringify(rotate.data));
const clientNew=cookies(rotate.r);
assert.notEqual(clientNew.cookie,client.cookie);
for(const stale of [client,concurrentSession])assert.equal((await call('/api/docs','GET',undefined,stale)).r.status,401);
assert.equal((await call('/api/login','POST',{email:'client@example.org',password:pwd})).r.status,401);
assert.equal((await call('/api/me','GET',undefined,clientNew)).data.mustChangePassword,false);
assert.equal((await call('/api/docs','GET',undefined,clientNew)).r.status,200);
assert.equal((await call('/api/docs/'+id,'GET',undefined,clientNew)).r.status,403,'unassigned client cannot read');
assert.equal((await raw('/api/docs','POST',admin)).status,403);
assert.equal((await raw('/api/docs','POST',admin,{'X-CSRF-Token':admin.csrf,Origin:'https://attacker.example'})).status,403);

const assign=await call('/api/docs/'+id+'/assign','POST',{stage:'REVISAO_CLIENTE',userId},admin);assert.equal(assign.r.status,200,JSON.stringify(assign.data));
const clientRead=await call('/api/docs/'+id,'GET',undefined,clientNew);assert.equal(clientRead.r.status,200);
const clientApprove=await call('/api/docs/'+id+'/decision','POST',{decision:'APPROVE',note:'Revisei o documento ficticio e confirmei os dados informados.'},clientNew);
assert.equal(clientApprove.r.status,200,JSON.stringify(clientApprove.data));assert.equal(clientApprove.data.nextStage,'REVISAO_JURIDICA_1');
// Test-only fixture access: never point this suite at a persistent/production database.
const db=new pg.Pool({connectionString:process.env.DATABASE_URL});
try{
 const tenant=randomUUID(),foreignDoc=randomUUID(),foreignUser=randomUUID();
 await db.query('INSERT INTO ldw_tenants(id,name) VALUES($1,$2)',[tenant,'Empresa fictícia B']);
 await db.query(`INSERT INTO ldw_users(id,tenant_id,email,password_hash,role,verified,must_change_password)
 SELECT $1,$2,'foreign@example.org',password_hash,'admin',true,false FROM ldw_users WHERE id=$3`,[foreignUser,tenant,userId]);
 await db.query(`INSERT INTO ldw_docs(id,tenant_id,created_by,title,kind,description,legal_emails,rounds,destination,stages,body,body_hash)
 SELECT $1,$2,$3,title,kind,description,legal_emails,rounds,destination,stages,body,body_hash FROM ldw_docs WHERE id=$4`,[foreignDoc,tenant,foreignUser,id]);
 const foreign=cookies((await call('/api/login','POST',{email:'foreign@example.org',password:'Safe-Rotated-Password-2026!!!'})).r);
 for(const [sess,target] of [[admin,foreignDoc],[foreign,id]]){
  const listing=await call('/api/docs','GET',undefined,sess);assert.ok(!listing.data.docs.some(d=>d.id===target));
  for(const [suffix,method,body] of [['','GET'],['/body','PUT',{body:'x'.repeat(100)}],['/assign','POST',{stage:'REVISAO_CLIENTE',userId}],['/decision','POST',{decision:'APPROVE',note:'Teste isolamento entre empresas.'}]]){
   assert.equal((await call('/api/docs/'+target+suffix,method,body,sess)).r.status,404);
  }
 }
 assert.equal((await call('/api/users/'+userId+'/verify','POST',{justification:'Teste de isolamento entre empresas fictícias.'},foreign)).r.status,404);
 assert.equal((await call('/api/docs/'+id+'/assign','POST',{stage:'REVISAO_CLIENTE',userId:foreignUser},admin)).r.status,403);
 // Exercise each independent review profile and require its explicit assignment.
 for(const [role,stages] of [['legal',['REVISAO_JURIDICA_1','REVISAO_JURIDICA_2']],['technical',['REVISAO_TECNICA']],['approver',['APROVACAO']],['homologator',['HOMOLOGACAO']]]){
  const email=role==='legal'?'legal@example.org':role+'@example.org';
  const made=await call('/api/users','POST',{email,role},admin);assert.equal(made.r.status,201);
  const uid=made.data.id,temp=made.data.temporaryPassword;
  const logged=cookies((await call('/api/login','POST',{email,password:temp})).r);
  const rotated=await call('/api/change-password','POST',{currentPassword:temp,newPassword:'Profile-Password-2026!!!'},logged);assert.equal(rotated.r.status,200);
  const reviewer=cookies(rotated.r);
  assert.equal((await call('/api/docs/'+id+'/assign','POST',{stage:stages[0],userId:uid},admin)).r.status,403,'unverified reviewer');
  await call('/api/users/'+uid+'/verify','POST',{justification:'Perfil fictício conferido para teste de integração.'},admin);
  assert.equal((await call('/api/docs/'+id+'/decision','POST',{decision:'APPROVE',note:'Revisor ainda não atribuído.'},reviewer)).r.status,403);
  for(const stage of stages){
   assert.equal((await call('/api/docs/'+id+'/assign','POST',{stage,userId:uid},admin)).r.status,200);
   assert.equal((await call('/api/docs/'+id+'/decision','POST',{decision:'APPROVE',note:'Perfil incorreto nesta etapa.'},clientNew)).r.status,403);
   const decision=await call('/api/docs/'+id+'/decision','POST',{decision:'APPROVE',note:'Revisão fictícia aprovada pelo perfil atribuído.'},reviewer);
   assert.equal(decision.r.status,200,JSON.stringify(decision.data));
  }
 }
 assert.equal((await call('/api/docs/'+id,'GET',undefined,admin)).data.doc.stage,'AGUARDANDO_ASSINATURA');
 assert.equal((await call('/api/docs/'+id+'/decision','POST',{decision:'APPROVE',note:'Não pode assinar automaticamente.'},admin)).r.status,409);
 // Server-side expiry and active-account checks, independent of client cookies.
 await db.query("UPDATE ldw_sessions SET expires_at=now()-interval '1 second' WHERE user_id=$1",[userId]);
 assert.equal((await call('/api/me','GET',undefined,clientNew)).r.status,401);
 const active=cookies((await call('/api/login','POST',{email:'client@example.org',password:'Safe-Rotated-Password-2026!!!'})).r);
 await db.query('UPDATE ldw_users SET active=false WHERE id=$1',[userId]);
 assert.equal((await call('/api/me','GET',undefined,active)).r.status,401);
}finally{await db.end();}
console.log('LegalDoc integration: setup, auth, CSRF, tenancy, documents, revisions, roles and password rotation OK');
