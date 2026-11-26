import {test,expect} from "bun:test";
import {SMS_ATM_RULE,avaliarTemporalidade,addYearsClamped,consolidarProducao,validarConfirmacaoAlfresco,type ProducaoEvento} from "./temporalidade-producao";
test("atestado classificado enquanto aguarda desligamento",()=>{
 const v=avaliarTemporalidade(SMS_ATM_RULE,null,"2026-10-29");
 expect(v.anosAposEvento).toBe(10);expect(v.situacao).toBe("AGUARDANDO_EVENTO");
 expect(v.dataAvaliacao).toBeNull();expect(v.podeEliminarAutomaticamente).toBe(false);
});
test("desligamento gera data futura e revisão, não eliminação automática",()=>{
 expect(avaliarTemporalidade(SMS_ATM_RULE,"2025-02-01","2026-10-29").dataAvaliacao).toBe("2035-02-01");
 const v=avaliarTemporalidade(SMS_ATM_RULE,"2015-02-01","2026-10-29");
 expect(v.situacao).toBe("REVISAO_DESTINACAO");expect(v.podeEliminarAutomaticamente).toBe(false);
});
test("data bissexta tem cálculo determinístico",()=>expect(addYearsClamped("2024-02-29",10)).toBe("2034-02-28"));
test("regra ausente não adota prazo fictício",()=>expect(avaliarTemporalidade(null,null,"2026-10-29").situacao).toBe("REGRA_PENDENTE"));
const item=(diff:Partial<ProducaoEvento>):ProducaoEvento=>({
 eventoId:"1",documentoId:"id-1",loteId:"lote-1",empresa:"SMS",departamento:"DP",
 tipoDocumental:"Atestado Médico",codigo:"01.20.006.001",nomeArquivo:"atestado.pdf",operador:"operador",
 enviadoEm:"2026-10-29T11:00:00Z",paginas:2,bytes:100,status:"RECEBIDO",
 temporalidade:"NAO_VERIFICADA",alfrescoNodeId:null,erro:null,...diff
});
test("evita contagem duplicada entre eventos, preserva última situação",()=>{
 const r=consolidarProducao([item({}),item({eventoId:"2",status:"VALIDADO",temporalidade:"APLICADA",alfrescoNodeId:"node-1",enviadoEm:"2026-10-29T11:01:00Z"})]);
 expect(r.resumo.documentos).toBe(1);expect(r.resumo.validados).toBe(1);
 expect(r.porDepartamento[0].chave).toBe("DP");expect(validarConfirmacaoAlfresco(r.documentos[0])).toBe(true);
});
test("gravado sem temporalidade não conta como validado",()=>{
 const r=consolidarProducao([item({status:"GRAVADO",temporalidade:"PENDENTE",alfrescoNodeId:"node-1"})]);
 expect(r.resumo.validados).toBe(0);expect(validarConfirmacaoAlfresco(r.documentos[0])).toBe(false);
});
