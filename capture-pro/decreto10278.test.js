"use strict";
const test=require("node:test");
const assert=require("node:assert/strict");
const {registrarCaptura,validarMetadados,verificarIntegridade,finalizar}=require("./decreto10278");
const arquivo=Buffer.from("documento de teste");
function fixture(){
 const auto=registrarCaptura({arquivo,operador:"op-1",empresa:"Arquindex",unidade:"BH",local:"BH / unidade 01",tenantId:"cliente-1"});
 return {...auto,assunto:"Contrato",autor:"Empresa emissora",titulo:"Contrato de prestação de serviços",tipoDocumental:"contrato"};
}
test("captura define UUID, data e hash automaticamente",()=>{const a=fixture();assert.equal(a.hashImagem.length,64);assert.match(a.dataHoraDigitalizacao,/Z$/);assert.equal(verificarIntegridade(arquivo,a.hashImagem),true);assert.equal(verificarIntegridade(Buffer.from("adulterado"),a.hashImagem),false)});
test("privado: oito grupos presentes",()=>assert.equal(validarMetadados(fixture()).valido,true));
test("público: exige cinco grupos adicionais",()=>{const f=fixture();assert.equal(validarMetadados(f,{setorPublico:true}).erros.length,5);Object.assign(f,{classe:"02",dataProducao:"2025-01-01",destinacaoPrevista:"guarda permanente",genero:"textual",prazoGuarda:"permanente"});assert.equal(validarMetadados(f,{setorPublico:true}).valido,true)});
test("finalização exige arquivo original, revisão e catálogo",()=>{const f=fixture();assert.equal(finalizar(f,{arquivo,aprovadoPor:"revisor",tiposPermitidos:["contrato"]}).valido,true);assert.equal(finalizar(f,{arquivo:Buffer.from("outro"),aprovadoPor:"revisor"}).valido,false);assert.equal(finalizar(f,{arquivo,tiposPermitidos:["prontuario"]}).valido,false)});
test("falha em metadados ausentes e fuso omitido",()=>{const f=fixture();delete f.autor;f.dataHoraDigitalizacao="2026-10-26T13:00:00";assert.equal(validarMetadados(f).valido,false)});
test("não cria captura sem tenant/operador",()=>assert.throws(()=>registrarCaptura({arquivo,operador:"a",empresa:"b",unidade:"c",local:"d"})));
