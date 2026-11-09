"use strict";
// Preparation-only pilot. No network, subprocess, database writes or binary upload.
const {createHash} = require("node:crypto");
const {transacaoTenant} = require("../persistencia");
const {validarMetadados, verificarIntegridade} = require("../decreto10278");
const UUID = /^[a-f0-9]{8}-[a-f0-9]{4}-[1-8][a-f0-9]{3}-[89ab][a-f0-9]{3}-[a-f0-9]{12}$/i;
function fail(code) { const e = new Error(code); e.code = code; throw e; }
function digest(bytes) { return createHash("sha256").update(bytes).digest("hex"); }
function criarAdaptador({env = {}, pool, storage, resolverSessao, bindings = []} = {}) {
  // Copy trusted server configuration once; never accept bindings or identity from a request.
  const enabled = env.CAPTURE_OPENARCH_PILOT_ENABLED === "true";
  const config = structuredClone(bindings);
  function ready() { if (!enabled) fail("OPENARCH_DISABLED"); }
  async function preparar({sessao, identificadorDigital} = {}) {
    ready();
    if (typeof resolverSessao !== "function") fail("AUTH_RESOLVER_REQUIRED");
    const ctx = await resolverSessao(sessao);
    if (!ctx || ![ctx.tenantId,ctx.projetoId,ctx.operadorId].every(v => typeof v === "string" && v.trim()) ||
        !Array.isArray(ctx.permissoes) || !ctx.permissoes.includes("openarch:pilot")) fail("FORBIDDEN");
    if (!UUID.test(identificadorDigital || "")) fail("INVALID_DOCUMENT_ID");
    const matches = config.filter(b => b.tenantId === ctx.tenantId && b.projetoId === ctx.projetoId);
    if (matches.length !== 1) fail("BINDING_REQUIRED");
    const binding = matches[0];
    // Separate OpenArch instance per tenant: paths/metadata alone are not access controls.
    if (typeof binding.instanceId !== "string" || !binding.instanceId ||
        config.some(b => b.instanceId === binding.instanceId && b.tenantId !== ctx.tenantId)) fail("SHARED_INSTANCE_FORBIDDEN");
    if (!Array.isArray(binding.syntheticSha256) || !binding.syntheticSha256.length ||
        !Array.isArray(binding.tiposPermitidos) || !binding.tiposPermitidos.length ||
        typeof binding.setorPublico !== "boolean") fail("INVALID_PROJECT_POLICY");
    if (!pool || typeof pool.connect !== "function" || !storage || typeof storage.get !== "function") fail("DEPENDENCY_REQUIRED");
    return transacaoTenant(pool,ctx.tenantId,async client => {
      const res = await client.query(
        "SELECT * FROM capture_pro.documentos WHERE tenant_id=$1 AND projeto_id=$2 AND identificador_digital=$3 FOR SHARE",
        [ctx.tenantId,ctx.projetoId,identificadorDigital]);
      const doc = res.rows[0];
      if (!doc || doc.tenant_id !== ctx.tenantId || doc.projeto_id !== ctx.projetoId ||
          doc.identificador_digital !== identificadorDigital) fail("DOCUMENT_NOT_FOUND");
      if (doc.estado !== "validado" || !doc.revisado_por || !doc.revisado_em ||
          !Number.isSafeInteger(doc.versao) || doc.versao < 1) fail("DOCUMENT_NOT_APPROVED");
      if (doc.perfil_publico !== binding.setorPublico) fail("PROJECT_POLICY_MISMATCH");
      // Allowlist established by the server from known synthetic fixtures, not a payload boolean.
      if (!binding.syntheticSha256.includes(doc.hash_matriz)) fail("SYNTHETIC_ONLY");
      const bytes = await storage.get(doc.arquivo_matriz_chave);
      if (!verificarIntegridade(bytes,doc.hash_matriz)) fail("INTEGRITY_FAILED");
      const extra = doc.dados_adicionais || {};
      const metadata = {
        assunto:doc.assunto,autor:doc.autor,titulo:doc.titulo,tipoDocumental:doc.tipo_documental,
        identificadorDigital:doc.identificador_digital,
        dataHoraDigitalizacao:new Date(doc.criado_em).toISOString(),
        localDigitalizacao:doc.local_digitalizacao,responsavelDigitalizacao:doc.responsavel_digitalizacao,
        hashImagem:doc.hash_matriz,algoritmoHash:"sha256",
        classe:extra.classe,dataProducao:extra.dataProducao,destinacaoPrevista:extra.destinacaoPrevista,
        genero:extra.genero,prazoGuarda:extra.prazoGuarda
      };
      if (!validarMetadados(metadata,{setorPublico:binding.setorPublico,tiposPermitidos:binding.tiposPermitidos}).valido) fail("INVALID_METADATA");
      const tenantKey = digest(ctx.tenantId);
      const projectKey = digest(ctx.projetoId);
      const parent = `/capture-pilot/${tenantKey}/${projectKey}`;
      const name = `${doc.identificador_digital}-v${doc.versao}`;
      // SysFolder is documented in v0.2.1; this is a metadata envelope, not a stored PDF.
      // Keep app fields inside sys_description until a custom type is tested on a real server.
      const envelope = {schemaVersion:1,synthetic:true,tenantKey,projectKey,version:doc.versao,metadata};
      const document = {sys_primaryType:"SysFolder",sys_name:name,sys_title:metadata.titulo,
        sys_description:JSON.stringify(envelope)};
      return {status:"prepared_not_sent",cliVersion:"0.2.1",instanceId:binding.instanceId,
        idempotencyKey:digest(JSON.stringify([ctx.tenantId,ctx.projetoId,identificadorDigital,doc.versao,doc.hash_matriz])),
        parent,document,
        command:{executable:"openarch",args:["documents","create","--parent",parent,"--file","-","--output","json","--non-interactive"],
          stdin:JSON.stringify(document)},
        limitations:["metadata_only","parent_must_exist","server_schema_unverified","no_remote_idempotency_guarantee"]};
    });
  }
  function executar() { ready(); fail("OPENARCH_RUNTIME_NOT_VALIDATED"); }
  return Object.freeze({preparar,executar});
}
module.exports = {criarAdaptador};
