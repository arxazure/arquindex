"use strict";
/** Metadados Decreto 10.278/2020 - biblioteca independente (Node >=18).
 * NUNCA confiar em timestamps, ID de captura, operadores ou hash vindos do browser.
 */
const crypto = require("node:crypto");
const CAMPOS_COMUNS = Object.freeze(["assunto","autor","dataHoraDigitalizacao","localDigitalizacao","identificadorDigital","responsavelDigitalizacao","titulo","tipoDocumental","hashImagem"]);
const CAMPOS_PUBLICOS = Object.freeze(["classe","dataProducao","destinacaoPrevista","genero","prazoGuarda"]);
const ISO_TZ = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,3})?(?:Z|[+-]\d{2}:\d{2})$/;
const HEX_SHA256=/^[a-f0-9]{64}$/i;
const UUID=/^[a-f0-9]{8}-[a-f0-9]{4}-[1-8][a-f0-9]{3}-[89ab][a-f0-9]{3}-[a-f0-9]{12}$/i;
function valido(v){return typeof v === "string" ? v.trim().length>0 : Array.isArray(v)?v.some(valido):v!==null&&v!==undefined&&v!=="";}
function validarMetadados(m,{setorPublico=false,tiposPermitidos=null}={}){
 if(!m||typeof m!=="object"||Array.isArray(m))return {valido:false,erros:["metadados: objeto obrigatório"]};
 const obrigatorios=[...CAMPOS_COMUNS,...(setorPublico?CAMPOS_PUBLICOS:[])];
 const erros=obrigatorios.filter(k=>!valido(m[k])).map(k=>k+": obrigatório");
 if(valido(m.dataHoraDigitalizacao)&&(!ISO_TZ.test(m.dataHoraDigitalizacao)||Number.isNaN(Date.parse(m.dataHoraDigitalizacao))))erros.push("dataHoraDigitalizacao: ISO 8601 com fuso exigido");
 if(valido(m.identificadorDigital)&&!UUID.test(m.identificadorDigital))erros.push("identificadorDigital: UUID inválido");
 if(valido(m.hashImagem)&&!HEX_SHA256.test(m.hashImagem))erros.push("hashImagem: SHA-256 hexadecimal inválido");
 if(valido(m.algoritmoHash)&&m.algoritmoHash!=="sha256")erros.push("algoritmoHash: usar sha256");
 if(tiposPermitidos && valido(m.tipoDocumental)&&!tiposPermitidos.includes(m.tipoDocumental))erros.push("tipoDocumental: não autorizado para o cliente");
 if(typeof m.assunto==="string" && m.assunto.length>500)erros.push("assunto: excede 500 caracteres");
 if(typeof m.titulo==="string" && m.titulo.length>512)erros.push("titulo: excede 512 caracteres");
 return {valido:erros.length===0,erros};
}
/** Somente invocar em serviço autenticado, com informações obtidas no servidor. */
function registrarCaptura({arquivo,operador,empresa,unidade,local,instante=new Date(),tenantId}={}){
 if(!Buffer.isBuffer(arquivo)||!arquivo.length)throw new Error("arquivo não vazio (Buffer) obrigatório");
 if(![operador,empresa,unidade,local,tenantId].every(valido))throw new Error("identidade, tenant e local obrigatórios");
 if(!(instante instanceof Date)||Number.isNaN(instante.getTime()))throw new Error("instante inválido");
 return Object.freeze({
  tenantId,operadorId:operador,empresaResponsavel:empresa,unidadeId:unidade,
  dataHoraDigitalizacao:instante.toISOString(),localDigitalizacao:local,
  identificadorDigital:crypto.randomUUID(),
  responsavelDigitalizacao:empresa,
  hashImagem:crypto.createHash("sha256").update(arquivo).digest("hex"),
  algoritmoHash:"sha256",escopoHash:"arquivo-matriz"
 });
}
function verificarIntegridade(arquivo,hash){
 if(!Buffer.isBuffer(arquivo)||!HEX_SHA256.test(hash||""))return false;
 const a=Buffer.from(crypto.createHash("sha256").update(arquivo).digest("hex"),"hex");
 const b=Buffer.from(hash,"hex");
 return crypto.timingSafeEqual(a,b);
}
function finalizar(m,{setorPublico=false,tiposPermitidos=null,arquivo=null,aprovadoPor=null}={}){
 const r=validarMetadados(m,{setorPublico,tiposPermitidos});
 if(!valido(aprovadoPor))r.erros.push("aprovadoPor: revisão humana obrigatória");
 if(!Buffer.isBuffer(arquivo)||!verificarIntegridade(arquivo,m?.hashImagem))r.erros.push("arquivo: integridade não verificada");
 return {valido:r.erros.length===0,erros:r.erros,status:r.erros.length?"revisao":"validado"};
}
module.exports={CAMPOS_COMUNS,CAMPOS_PUBLICOS,validarMetadados,registrarCaptura,verificarIntegridade,finalizar};
