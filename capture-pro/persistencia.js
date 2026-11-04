"use strict";
/**
 * Integracao com PostgreSQL e armazenamento de objetos.
 * Espera um pool pg compativel (pool.connect()) e storage com putImmutable(key, bytes).
 * Tenant, operador e permissoes devem vir de sessao autenticada pelo servidor.
 * Nunca expor este modulo diretamente ao navegador.
 */
const crypto = require("node:crypto");
const {registrarCaptura,validarMetadados,verificarIntegridade,finalizar} = require("./decreto10278");
function assertContexto(ctx) {
 if (!ctx || !["tenantId","projetoId","operadorId","empresaResponsavel","unidadeId","localDigitalizacao"].every(k=>typeof ctx[k]==="string" && ctx[k].trim())) throw new Error("Contexto autenticado incompleto");
}
function assertSQLTenant(tenant) {
 if (typeof tenant !== "string" || !tenant.trim() || tenant.length > 200) throw new Error("tenant invalido");
 return tenant;
}
async function transacaoTenant(pool,tenant,fn) {
 const client = await pool.connect();
 try {
  await client.query("BEGIN");
  await client.query("SELECT set_config('app.capture_tenant', $1, true)",[assertSQLTenant(tenant)]);
  const output = await fn(client);
  await client.query("COMMIT");
  return output;
 } catch(error) {
  try { await client.query("ROLLBACK"); } catch(_error) {}
  throw error;
 } finally { client.release(); }
}
async function capturarDocumento({pool,storage,contexto,arquivo,extensao="bin"}){
 assertContexto(contexto);
 if (!pool || typeof pool.connect!=="function" || !storage || typeof storage.putImmutable!=="function") throw new Error("Storage e pool obrigatorios");
 if (!Buffer.isBuffer(arquivo)||arquivo.length===0)throw new Error("Arquivo matriz vazio");
 if (!/^[a-z0-9]{1,8}$/.test(extensao))throw new Error("Extensao invalida");
 const registro=registrarCaptura({
  arquivo,operador:contexto.operadorId,empresa:contexto.empresaResponsavel,unidade:contexto.unidadeId,
  local:contexto.localDigitalizacao,tenantId:contexto.tenantId
 });
 // Nenhuma parte da chave e controlada por entrada nao autenticada.
 const tenantDigest=crypto.createHash("sha256").update(contexto.tenantId).digest("hex").slice(0,24);
 const chave=`matrizes/${tenantDigest}/${registro.identificadorDigital}.${extensao}`;
 // Storage deve recusar sobrescrita. Objeto orfao em falha de BD e tratado por reconciliacao.
 await storage.putImmutable(chave,arquivo,{sha256:registro.hashImagem,tenantId:contexto.tenantId});
 await transacaoTenant(pool,contexto.tenantId,async client=>{
  await client.query(`INSERT INTO capture_pro.documentos
    (identificador_digital,tenant_id,projeto_id,operador_id,unidade_id,criado_em,
      local_digitalizacao,responsavel_digitalizacao,hash_matriz,arquivo_matriz_chave)
     VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10)`,[
    registro.identificadorDigital,contexto.tenantId,contexto.projetoId,contexto.operadorId,
    contexto.unidadeId,registro.dataHoraDigitalizacao,registro.localDigitalizacao,
    registro.responsavelDigitalizacao,registro.hashImagem,chave]);
  await client.query(`INSERT INTO capture_pro.eventos
    (tenant_id,identificador_digital,ator_id,acao,detalhes) VALUES ($1,$2,$3,'CAPTURA',$4::jsonb)`,[
    contexto.tenantId,registro.identificadorDigital,contexto.operadorId,JSON.stringify({hash:registro.hashImagem,chave})]);
 });
 return {identificadorDigital:registro.identificadorDigital,hashImagem:registro.hashImagem,estado:"revisao"};
}
async function aprovarDocumento({pool,storage,contexto,identificadorDigital,metadados,perfilPublico=false,tiposPermitidos=[]}){
 assertContexto(contexto);
 if (!pool || typeof pool.connect!=="function" || !storage || typeof storage.get!=="function") throw new Error("Pool e storage.get obrigatorios");
 return transacaoTenant(pool,contexto.tenantId,async client=>{
  const res=await client.query(
    "SELECT * FROM capture_pro.documentos WHERE tenant_id=$1 AND identificador_digital=$2 FOR UPDATE",
    [contexto.tenantId,identificadorDigital]);
  const doc=res.rows[0];
  if(!doc)throw new Error("Documento nao encontrado");
  if(doc.estado!=="revisao")throw new Error("Documento nao esta em revisao");
  if(contexto.projetoId!==doc.projeto_id)throw new Error("Projeto nao autorizado");
  const arquivo=await storage.get(doc.arquivo_matriz_chave);
  if(!Buffer.isBuffer(arquivo)||!verificarIntegridade(arquivo,doc.hash_matriz))throw new Error("Hash da matriz diverge");
  // Valores protegidos sao sempre recuperados do BD, jamais da requisicao.
  const dados={
   ...metadados,
   identificadorDigital:doc.identificador_digital,
   dataHoraDigitalizacao:new Date(doc.criado_em).toISOString(),
   localDigitalizacao:doc.local_digitalizacao,
   responsavelDigitalizacao:doc.responsavel_digitalizacao,
   hashImagem:doc.hash_matriz,
   algoritmoHash:"sha256"
  };
  const resultado=finalizar(dados,{
   setorPublico:perfilPublico,tiposPermitidos,arquivo,aprovadoPor:contexto.operadorId});
  if(!resultado.valido)return resultado;
  await client.query(`UPDATE capture_pro.documentos SET assunto=$1,autor=$2,titulo=$3,tipo_documental=$4,
     dados_adicionais=$5::jsonb,perfil_publico=$6,estado='validado',revisado_por=$7,revisado_em=now(),
     versao=versao+1 WHERE tenant_id=$8 AND identificador_digital=$9`,[
      dados.assunto,dados.autor,dados.titulo,dados.tipoDocumental,
      JSON.stringify({classe:dados.classe||null,dataProducao:dados.dataProducao||null,destinacaoPrevista:dados.destinacaoPrevista||null,genero:dados.genero||null,prazoGuarda:dados.prazoGuarda||null}),
      perfilPublico,contexto.operadorId,contexto.tenantId,identificadorDigital
     ]);
  await client.query(`INSERT INTO capture_pro.eventos (tenant_id,identificador_digital,ator_id,acao,detalhes)
   VALUES ($1,$2,$3,'VALIDACAO',$4::jsonb)`,[
   contexto.tenantId,identificadorDigital,contexto.operadorId,JSON.stringify({perfilPublico,tipoDocumental:dados.tipoDocumental})]);
  return {valido:true,erros:[],status:"validado",identificadorDigital};
 });
}
module.exports={transacaoTenant,capturarDocumento,aprovarDocumento};
