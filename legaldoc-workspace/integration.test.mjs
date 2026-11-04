import assert from 'node:assert/strict';
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
const blocked=await call('/api/docs','GET',undefined,client);assert.equal(blocked.r.status,403);
const rotate=await call('/api/change-password','POST',{currentPassword:pwd,newPassword:'Safe-Rotated-Password-2026!!!'},client);assert.equal(rotate.r.status,200,JSON.stringify(rotate.data));
const clientNew=cookies(rotate.r);
const assign=await call('/api/docs/'+id+'/assign','POST',{stage:'REVISAO_CLIENTE',userId},admin);assert.equal(assign.r.status,200,JSON.stringify(assign.data));
const clientRead=await call('/api/docs/'+id,'GET',undefined,clientNew);assert.equal(clientRead.r.status,200);
const clientApprove=await call('/api/docs/'+id+'/decision','POST',{decision:'APPROVE',note:'Revisei o documento ficticio e confirmei os dados informados.'},clientNew);
assert.equal(clientApprove.r.status,200,JSON.stringify(clientApprove.data));assert.equal(clientApprove.data.nextStage,'REVISAO_JURIDICA_1');
console.log('LegalDoc integration: setup, auth, CSRF, tenancy, documents, revisions, roles and password rotation OK');
