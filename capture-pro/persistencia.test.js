"use strict";
const test=require("node:test");
const assert=require("node:assert/strict");
const {capturarDocumento,aprovarDocumento}=require("./persistencia");

function setup() {
 const events=[],stored=new Map(),rows=new Map();
 const storage={
  async putImmutable(key,buf){if(stored.has(key))throw Error("overwrite");stored.set(key,Buffer.from(buf));},
  async get(key){return stored.get(key);}
 };
 const conn={
  async query(sql,values=[]){
   events.push({sql,values});
   if(sql.includes("INSERT INTO capture_pro.documentos")){
    rows.set(values[0],{
     identificador_digital:values[0],tenant_id:values[1],projeto_id:values[2],
     operador_id:values[3],unidade_id:values[4],criado_em:values[5],local_digitalizacao:values[6],
     responsavel_digitalizacao:values[7],hash_matriz:values[8],arquivo_matriz_chave:values[9],estado:"revisao"
    });
   }
   if(sql.includes("SELECT * FROM capture_pro.documentos")){
    const row=rows.get(values[1]);
    return {rows:row&&row.tenant_id===values[0]?[row]:[]};
   }
   if(sql.includes("UPDATE capture_pro.documentos")){
    const row=rows.get(values[8]); if(row)row.estado="validado";
   }
   return {rows:[]};
  },
  release(){events.push({sql:"RELEASE"});}
 };
 const pool={async connect(){return conn;}};
 const contexto={tenantId:"cliente-1",projetoId:"prj1",operadorId:"op-1",empresaResponsavel:"Arquindex",unidadeId:"BH",localDigitalizacao:"BH"};
 return {storage,pool,contexto,events,rows,stored};
}
test("captura persiste com isolamento transacional e objeto imutavel",async()=>{
 const s=setup();
 const r=await capturarDocumento({...s,arquivo:Buffer.from("matriz"),extensao:"pdf"});
 assert.equal(r.estado,"revisao");
 assert.equal(s.rows.size,1);
 assert.equal(s.events.some(e=>e.sql.startsWith("SELECT set_config(")),true);
 assert.equal(s.events.some(e=>e.sql==="COMMIT"),true);
 assert.equal(s.stored.size,1);
});
test("revisao aprova apenas se valida, hash confere e projeto corresponde",async()=>{
 const s=setup();
 const r=await capturarDocumento({...s,arquivo:Buffer.from("matriz"),extensao:"pdf"});
 const m={assunto:"Contrato",autor:"Empresa emissora",titulo:"Documento",tipoDocumental:"contrato"};
 let result=await aprovarDocumento({...s,identificadorDigital:r.identificadorDigital,metadados:m,tiposPermitidos:["contrato"]});
 assert.equal(result.valido,true);
 assert.equal(s.rows.get(r.identificadorDigital).estado,"validado");
});
test("revisao rejeita arquivo alterado",async()=>{
 const s=setup();
 const r=await capturarDocumento({...s,arquivo:Buffer.from("matriz")});
 const key=s.rows.get(r.identificadorDigital).arquivo_matriz_chave;
 s.stored.set(key,Buffer.from("adulterado"));
 await assert.rejects(()=>aprovarDocumento({...s,identificadorDigital:r.identificadorDigital,metadados:{},tiposPermitidos:["contrato"]}),/Hash da matriz diverge/);
 assert.equal(s.events.some(e=>e.sql==="ROLLBACK"),true);
});
test("rejeita tenant ausente",async()=>{
 const s=setup();s.contexto.tenantId="";
 await assert.rejects(()=>capturarDocumento({...s,arquivo:Buffer.from("matriz")}),/Contexto autenticado incompleto/);
});
test("revisao rejeita projeto diferente",async()=>{
 const s=setup();
 const r=await capturarDocumento({...s,arquivo:Buffer.from("matriz")});
 const contexto={...s.contexto,projetoId:"outro"};
 await assert.rejects(()=>aprovarDocumento({...s,contexto,identificadorDigital:r.identificadorDigital,metadados:{}}),/Projeto nao autorizado/);
});
