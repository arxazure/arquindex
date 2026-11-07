"use strict";
const test = require("node:test");
const assert = require("node:assert/strict");
const {createHash} = require("node:crypto");
const {criarAdaptador} = require("./adapter");
const ID = "00000000-0000-4000-8000-000000000001";
function setup() {
  // Explicit unit doubles: not a PostgreSQL/RLS or OpenArch integration test.
  const bytes = Buffer.from("ARQUINDEX SYNTHETIC FIXTURE / tenant A / no personal data\n");
  const hash = createHash("sha256").update(bytes).digest("hex");
  const calls = [];
  const doc = {identificador_digital:ID,tenant_id:"a",projeto_id:"p",estado:"validado",versao:2,
    revisado_por:"reviewer-synthetic",revisado_em:"2026-11-06T08:00:00Z",perfil_publico:false,
    criado_em:"2026-11-06T07:00:00Z",local_digitalizacao:"Synthetic lab",responsavel_digitalizacao:"Synthetic entity",
    hash_matriz:hash,arquivo_matriz_chave:"synthetic/a/matrix.txt",assunto:"Synthetic",autor:"Synthetic author",
    titulo:"Synthetic title",tipo_documental:"teste",dados_adicionais:{}};
  const ctx = {tenantId:"a",projetoId:"p",operadorId:"test-user",permissoes:["openarch:pilot"]};
  const bindings = [{tenantId:"a",projetoId:"p",instanceId:"isolated-a",syntheticSha256:[hash],tiposPermitidos:["teste"],setorPublico:false}];
  const client = {async query(sql,params) { calls.push({sql,params}); return {rows:sql.startsWith("SELECT *") ? [doc] : []}; },release(){calls.push({sql:"RELEASE"});}};
  const options = {env:{CAPTURE_OPENARCH_PILOT_ENABLED:"true"},bindings,
    resolverSessao:async token => token === "synthetic-session" ? ctx : null,
    pool:{async connect(){calls.push({sql:"CONNECT"});return client;}},
    storage:{async get(key){calls.push({sql:"STORAGE",key});return bytes;}}};
  return {bytes,doc,ctx,bindings,calls,options,request:{sessao:"synthetic-session",identificadorDigital:ID}};
}
async function rejects(s,code) { await assert.rejects(()=>criarAdaptador(s.options).preparar(s.request),{code}); }
test("disabled by default and exact flag only; no dependency touched",async()=>{
  for (const value of [undefined,"false","1",true,"TRUE"]) {
    const s=setup();s.options.env={CAPTURE_OPENARCH_PILOT_ENABLED:value};
    await rejects(s,"OPENARCH_DISABLED");assert.equal(s.calls.length,0);
  }
});
test("prepares metadata only using pinned 0.2.1 command; scoped SQL and stable job key",async()=>{
  const s=setup(),a=criarAdaptador(s.options);
  const result=await a.preparar(s.request),again=await a.preparar(s.request);
  assert.equal(result.status,"prepared_not_sent");assert.equal(result.idempotencyKey,again.idempotencyKey);
  assert.equal(result.document.sys_primaryType,"SysFolder");
  assert.equal(JSON.parse(result.document.sys_description).metadata.hashImagem,s.doc.hash_matriz);
  assert.equal(result.command.stdin,JSON.stringify(result.document));
  assert.deepEqual(result.command.args.slice(0,2),["documents","create"]);
  const q=s.calls.find(x=>x.sql.startsWith("SELECT *"));
  assert.deepEqual(q.params,["a","p",ID]);assert.match(q.sql,/tenant_id=\$1 AND projeto_id=\$2/);
  assert.ok(s.calls.some(x=>x.sql.includes("set_config")));
  assert.ok(s.calls.some(x=>x.sql==="COMMIT"));
  assert.equal(s.calls.some(x=>/^(INSERT|UPDATE|DELETE)/.test(x.sql)),false);
});
test("session and permission required before database access",async()=>{
  const s=setup();s.request.sessao="invalid";await rejects(s,"FORBIDDEN");assert.equal(s.calls.length,0);
  s.request.sessao="synthetic-session";s.ctx.permissoes=[];await rejects(s,"FORBIDDEN");assert.equal(s.calls.length,0);
});
test("caller identity fields cannot override server session",async()=>{
  const s=setup();Object.assign(s.request,{tenantId:"b",projetoId:"other",permissoes:["admin"]});
  const r=await criarAdaptador(s.options).preparar(s.request);assert.equal(r.instanceId,"isolated-a");
});
test("cross-tenant and cross-project rows rejected even if a faulty DB returns them",async()=>{
  for(const key of ["tenant_id","projeto_id","identificador_digital"]) {
    const s=setup();s.doc[key]="other";await rejects(s,"DOCUMENT_NOT_FOUND");
    assert.equal(s.calls.some(x=>x.sql==="STORAGE"),false);
    assert.ok(s.calls.some(x=>x.sql==="ROLLBACK"));assert.equal(s.calls.at(-1).sql,"RELEASE");
  }
});
test("one OpenArch instance cannot be assigned to two tenants",async()=>{
  const s=setup();s.bindings.push({...s.bindings[0],tenantId:"b"});
  await rejects(s,"SHARED_INSTANCE_FORBIDDEN");assert.equal(s.calls.length,0);
});
test("two authorized synthetic tenants get distinct instance, path and job key",async()=>{
  const a=setup(),b=setup();
  Object.assign(b.ctx,{tenantId:"b"});b.doc.tenant_id="b";
  Object.assign(b.bindings[0],{tenantId:"b",instanceId:"isolated-b"});
  const ra=await criarAdaptador(a.options).preparar(a.request);
  const rb=await criarAdaptador(b.options).preparar(b.request);
  assert.notEqual(ra.instanceId,rb.instanceId);assert.notEqual(ra.parent,rb.parent);
  assert.notEqual(ra.idempotencyKey,rb.idempotencyKey);
});
test("project binding and known synthetic bytes are mandatory",async()=>{
  const s=setup();s.ctx.projetoId="unknown";await rejects(s,"BINDING_REQUIRED");
  const t=setup();t.doc.hash_matriz="a".repeat(64);await rejects(t,"SYNTHETIC_ONLY");
  assert.equal(t.calls.some(x=>x.sql==="STORAGE"),false);
});
test("hash mismatch rolls back and releases connection",async()=>{
  const s=setup();s.options.storage.get=async()=>Buffer.from("changed");
  await rejects(s,"INTEGRITY_FAILED");assert.ok(s.calls.some(x=>x.sql==="ROLLBACK"));
  assert.equal(s.calls.at(-1).sql,"RELEASE");
});
test("rejects unapproved document, missing metadata and forbidden type",async()=>{
  const s=setup();s.doc.estado="revisao";await rejects(s,"DOCUMENT_NOT_APPROVED");
  const t=setup();t.doc.autor="";await rejects(t,"INVALID_METADATA");
  const u=setup();u.doc.tipo_documental="outro";await rejects(u,"INVALID_METADATA");
});
test("public profile requires trusted policy and extended metadata",async()=>{
  const s=setup();s.doc.perfil_publico=true;await rejects(s,"PROJECT_POLICY_MISMATCH");
  s.bindings[0].setorPublico=true;await rejects(s,"INVALID_METADATA");
});
test("storage failures propagate with transaction rollback",async()=>{
  const s=setup();s.options.storage.get=async()=>{throw Error("storage unavailable");};
  await assert.rejects(()=>criarAdaptador(s.options).preparar(s.request),/storage unavailable/);
  assert.ok(s.calls.some(x=>x.sql==="ROLLBACK"));assert.equal(s.calls.at(-1).sql,"RELEASE");
});
test("remote execution always fails closed pending real runtime validation",()=>{
  const s=setup();assert.throws(()=>criarAdaptador(s.options).executar(),{code:"OPENARCH_RUNTIME_NOT_VALIDATED"});
});
