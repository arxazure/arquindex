/**
 * Adaptador de indexação OCR para importação do Conector Alfresco e digitalização Arquindex.
 * É obrigatório confirmar os dados antes da gravação. Sem gravação direta no ECM.
 */
export const tiposSms = Object.freeze({
 "Atestado Médico": {codigo:"01.20.006.001",evento:"Desligamento do empregado",anos:10,sensivel:true},
 "ASO Admissional":{codigo:"01.20.005.001",evento:"Desligamento do empregado",anos:20,sensivel:true},
 "ASO Periódico":{codigo:"01.20.005.002",evento:"Desligamento do empregado",anos:20,sensivel:true},
 "ASO Demissional":{codigo:"01.20.005.003",evento:"Desligamento do empregado",anos:20,sensivel:true},
 "Declaração de Comparecimento":{codigo:"01.20.006.004",evento:"Desligamento do empregado",anos:10,sensivel:true}
});
export function validarIndexacaoAprovada(r,usuario) {
 if(!usuario?.id) throw Error("Aprovação requer identidade autenticada");
 if(!r || r.status!=="APROVADO_MANUALMENTE_PARA_INTEGRACAO")throw Error("Aguardando aprovação humana");
 const colaborador=String(r.colaborador||"").trim(),titulo=String(r.titulo||"").trim();
 if(!colaborador||!titulo||!r.dataDocumento||!r.departamento)throw Error("Indexação incompleta");
 if(!/^\d{4}-\d{2}-\d{2}$/.test(r.dataDocumento) || Number.isNaN(Date.parse(r.dataDocumento+"T00:00:00Z")))throw Error("Data inválida");
 const rule=tiposSms[r.tipoDocumental];
 if(!rule || (r.codigo&&r.codigo!==rule.codigo))throw Error("Tipo ou código não validado pela tabela");
 return {colaborador,titulo,tipoDocumental:r.tipoDocumental,codigo:rule.codigo,
 dataDocumento:r.dataDocumento,departamento:r.departamento,eventoInicial:rule.evento,
 anosAposEvento:rule.anos,dataEvento:null,dataAvaliacao:null,
 situacao:"AGUARDANDO_EVENTO",acesso:"RESTRITO_DADOS_SENSIVEIS",
 revisadoPor:usuario.id,revisadoEm:new Date().toISOString(),origem:"OCR_REVISADO",
 // O backend deve mapear propriedades para os QName registrados no modelo Alfresco.
 gravacaoPendente:true};
}
export function statusAposGravacao(local,alfresco) {
 if(!alfresco?.id||!Array.isArray(alfresco.aspectNames))return {status:"FALHA_VALIDACAO",motivo:"Nó Alfresco não retornado"};
 // Os QName e propriedades exigidos vêm de configuração aprovada no backend, não desta rotina.
 const expected=local.requiredAspects||[];
 const missing=expected.filter(x=>!alfresco.aspectNames.includes(x));
 return missing.length?{status:"ASPECTOS_PENDENTES",missing}:{status:"VERIFICAR_PROPRIEDADES",motivo:"Confirmar propriedades em leitura independente"};
}
