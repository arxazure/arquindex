/**
 * Arquindex Alfresco: temporalidade e relatório de produção.
 * Módulo puro: NÃO altera nós, não chama Alfresco nem executa eliminação.
 * Integração deve fornecer os eventos reais e verificar persistência no Alfresco.
 */
export type TemporalRule = {
  codigo: string; tipo: string; eventoInicial: string;
  anosAposEvento: number | null; acesso: string; destinacao: string;
};
export type TemporalResult = {
  codigo: string; tipo: string; evento: string; dataEvento: string | null;
  anosAposEvento: number | null; dataAvaliacao: string | null;
  situacao: "AGUARDANDO_EVENTO" | "EM_RETENCAO" | "REVISAO_DESTINACAO" | "REGRA_PENDENTE";
  motivo: string | null; podeEliminarAutomaticamente: false;
};
const DATE_ONLY = /^\d{4}-\d{2}-\d{2}$/;
function parseDate(value: string): Date {
  if (!DATE_ONLY.test(value)) throw new Error("Data deve usar AAAA-MM-DD");
  const date = new Date(value + "T00:00:00.000Z");
  if (Number.isNaN(date.getTime()) || date.toISOString().slice(0,10) !== value)
    throw new Error("Data inválida");
  return date;
}
export function addYearsClamped(dateISO: string, years: number): string {
  if (!Number.isSafeInteger(years) || years < 0) throw new Error("Prazo inválido");
  const d = parseDate(dateISO);
  const targetYear = d.getUTCFullYear() + years;
  const lastDay = new Date(Date.UTC(targetYear, d.getUTCMonth()+1, 0)).getUTCDate();
  return new Date(Date.UTC(targetYear, d.getUTCMonth(), Math.min(lastDay, d.getUTCDate())))
    .toISOString().slice(0,10);
}
export const SMS_ATM_RULE: TemporalRule = Object.freeze({
  codigo:"01.20.006.001",tipo:"Atestado Médico",
  eventoInicial:"Desligamento do empregado",anosAposEvento:10,
  acesso:"Restrito - dados pessoais sensíveis",
  destinacao:"Eliminação condicionada à revisão e autorização"
});
export function avaliarTemporalidade(
  regra: TemporalRule | null, dataEvento: string | null,
  hoje: string
): TemporalResult {
  parseDate(hoje);
  if (!regra || regra.anosAposEvento === null) {
    return {codigo:regra?.codigo ?? "",tipo:regra?.tipo ?? "",evento:regra?.eventoInicial ?? "",
      dataEvento:null,anosAposEvento:null,dataAvaliacao:null,
      situacao:"REGRA_PENDENTE",motivo:"Regra formal não aprovada",
      podeEliminarAutomaticamente:false};
  }
  if (!Number.isSafeInteger(regra.anosAposEvento) || regra.anosAposEvento < 0)
    throw new Error("Prazo inválido");
  if (!dataEvento) return {
    codigo:regra.codigo,tipo:regra.tipo,evento:regra.eventoInicial,dataEvento:null,
    anosAposEvento:regra.anosAposEvento,dataAvaliacao:null,
    situacao:"AGUARDANDO_EVENTO",motivo:"Evento inicial ainda não ocorreu ou não foi confirmado",
    podeEliminarAutomaticamente:false
  };
  if (dataEvento > hoje) throw new Error("Evento futuro exige revisão");
  const dataAvaliacao = addYearsClamped(dataEvento,regra.anosAposEvento);
  return {codigo:regra.codigo,tipo:regra.tipo,evento:regra.eventoInicial,dataEvento,
    anosAposEvento:regra.anosAposEvento,dataAvaliacao,
    situacao:dataAvaliacao <= hoje ? "REVISAO_DESTINACAO" : "EM_RETENCAO",
    motivo:null,podeEliminarAutomaticamente:false};
}
export type ProducaoEvento = {
  eventoId:string; documentoId:string; loteId:string;
  empresa:string; departamento:string; tipoDocumental:string; codigo:string;
  nomeArquivo:string; operador:string; enviadoEm:string;
  paginas:number | null; bytes:number | null;
  status:"RECEBIDO"|"ENVIANDO"|"GRAVADO"|"VALIDADO"|"FALHA"|"DUPLICADO";
  temporalidade:"APLICADA"|"PENDENTE"|"NAO_VERIFICADA";
  alfrescoNodeId:string | null; erro:string | null;
};
export function consolidarProducao(eventos: ProducaoEvento[]) {
  // Um documento pode gerar múltiplos eventos; contar somente o último evento de cada documento.
  const ultimos = new Map<string,ProducaoEvento>();
  for (const e of eventos) {
    if (!e.documentoId || !e.eventoId) throw new Error("Identificação obrigatória");
    if (e.paginas !== null && (!Number.isSafeInteger(e.paginas) || e.paginas < 0))
      throw new Error("Contagem de páginas inválida");
    if (e.bytes !== null && (!Number.isSafeInteger(e.bytes) || e.bytes < 0))
      throw new Error("Contagem de bytes inválida");
    if (!Number.isFinite(Date.parse(e.enviadoEm))) throw new Error("Data do envio inválida");
    const old=ultimos.get(e.documentoId);
    if (!old || e.enviadoEm > old.enviadoEm ||
      (e.enviadoEm === old.enviadoEm && e.eventoId > old.eventoId))
      ultimos.set(e.documentoId,e);
  }
  const docs=[...ultimos.values()];
  const resumo=(items:ProducaoEvento[])=>({
    documentos:items.length,
    recebidos:items.filter(e=>e.status==="RECEBIDO").length,
    gravados:items.filter(e=>e.status==="GRAVADO").length,
    validados:items.filter(e=>e.status==="VALIDADO").length,
    falhas:items.filter(e=>e.status==="FALHA").length,
    duplicados:items.filter(e=>e.status==="DUPLICADO").length,
    pendentes:items.filter(e=>["RECEBIDO","ENVIANDO"].includes(e.status)).length,
    temporalidadeAplicada:items.filter(e=>e.temporalidade==="APLICADA").length,
    temporalidadePendente:items.filter(e=>e.temporalidade==="PENDENTE").length,
    paginasConhecidas:items.reduce((n,e)=>n+(e.paginas??0),0),
    tamanhoBytesConhecido:items.reduce((n,e)=>n+(e.bytes??0),0),
    paginasNaoInformadas:items.filter(e=>e.paginas===null).length,
    tamanhoNaoInformado:items.filter(e=>e.bytes===null).length
  });
  const por=(campo:keyof Pick<ProducaoEvento,"empresa"|"departamento"|"tipoDocumental"|"operador"|"loteId"|"codigo">)=>
    Object.entries(Object.groupBy(docs,e=>e[campo]||"Não informado"))
      .map(([chave,items])=>({chave,...resumo(items??[])})).sort((a,b)=>b.documentos-a.documentos);
  return {geradoEm:new Date().toISOString(),resumo:resumo(docs),
    porEmpresa:por("empresa"),porDepartamento:por("departamento"),
    porTipoDocumental:por("tipoDocumental"),porCodigo:por("codigo"),
    porOperador:por("operador"),porLote:por("loteId"),
    documentos:docs.sort((a,b)=>b.enviadoEm.localeCompare(a.enviadoEm))};
}
export function validarConfirmacaoAlfresco(registro:ProducaoEvento): boolean {
  return registro.status==="VALIDADO" && !!registro.alfrescoNodeId &&
    registro.temporalidade==="APLICADA";
}
