// Arquindex LegalDoc AI — seed catalog: editorial drafts, NOT approved legal instruments.
// Source metadata is for human verification; never infer legal obligation just from a title.
export const legalSources = Object.freeze({
 lgpd:{title:"Lei 13.709/2018 e atos da ANPD",url:"https://www.gov.br/anpd/pt-br/centrais-de-conteudo/legislacao",authority:"ANPD"},
 anpd:{title:"Regulamentações da ANPD",url:"https://www.gov.br/anpd/pt-br/acesso-a-informacao/institucional/atos-normativos/regulamentacoes_anpd",authority:"ANPD"},
 nr:{title:"Normas Regulamentadoras vigentes",url:"https://www.gov.br/trabalho-e-emprego/pt-br/assuntos/inspecao-do-trabalho/seguranca-e-saude-no-trabalho/ctpp-nrs/normas-regulamentadoras-nrs",authority:"MTE"},
 pgr:{title:"Orientações oficiais PGR",url:"https://www.gov.br/trabalho-e-emprego/pt-br/assuntos/inspecao-do-trabalho/pgr/",authority:"MTE"},
 assinatura:{title:"Lei 14.063/2020 — assinaturas eletrônicas",url:"https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2020/lei/l14063.htm",authority:"Planalto"},
 cc:{title:"Código Civil — Lei 10.406/2002",url:"https://www.planalto.gov.br/ccivil_03/leis/2002/l10406compilada.htm",authority:"Planalto"},
 clt:{title:"CLT — Decreto-Lei 5.452/1943",url:"https://www.planalto.gov.br/ccivil_03/decreto-lei/del5452.htm",authority:"Planalto"}
});
const clause=(id,title,body,requirement="optional",condition="")=>({id,title,body,requirement,condition});
const party=clause("parties","Identificação e qualificação","{{razao_social}}, CNPJ {{cnpj}}, sede {{endereco}}, representada por {{representante}}, e {{outra_parte}} celebram o presente instrumento.","core");
const object=clause("object","Objeto e escopo","As partes definem como objeto {{objeto}}. O escopo, entregáveis e os critérios de aceite devem ser detalhados e revisados pelas partes.","core");
const signing=clause("signing","Assinaturas e responsáveis","Local e data: {{local_data}}\n\nRepresentante da primeira parte: __________________\n\nRepresentante da segunda parte: __________________","core");
const term=clause("term","Vigência e revisão","A vigência será de {{vigencia}}. A prorrogação, alteração e revisão deverão ser formalizadas pelas partes.","conditional","Aplicar conforme o instrumento e o enquadramento.");
const privacy=clause("privacy","Proteção de dados pessoais","As partes descreverão finalidades, papéis, base legal, compartilhamentos e medidas de proteção apropriadas à operação. Texto sujeito a avaliação de aderência à LGPD.","conditional","Quando houver tratamento de dados pessoais.");
const security=clause("security","Medidas de segurança","As partes estabelecerão controles de acesso, confidencialidade, registro de incidentes e procedimentos proporcionais aos riscos.","optional");
const remuneration=clause("remuneration","Remuneração e faturamento","O valor e as condições de pagamento serão: {{valor_e_condicoes}}. Eventuais encargos e índices deverão ser revisados.","conditional","Quando houver contraprestação financeira.");
const termination=clause("termination","Rescisão e consequências","A rescisão, prazos de comunicação e efeitos sobre obrigações pendentes serão definidos segundo o negócio e a legislação aplicável.","optional");
const confidentiality=clause("confidentiality","Informações confidenciais","As informações identificadas como confidenciais serão usadas apenas para {{finalidade}} e protegidas segundo os limites contratuais e legais.","core");
const disposition=clause("disposition","Destinação de informações","Ao término da relação, a devolução, retenção ou eliminação de informações observará as hipóteses e prazos legais aplicáveis.","conditional","Conferir hipóteses de retenção e preservação de prova.");
const risks=clause("risks","Inventário de perigos e riscos","Registrar estabelecimento, funções, processos, perigos identificados, trabalhadores expostos, avaliação e medidas de prevenção. Dados exigem levantamento técnico em campo.","core");
const actions=clause("actions","Plano de ação","Relacionar medidas preventivas, prioridade, responsáveis, cronograma, evidências de implementação e acompanhamento técnico.","core");
const legalBasis=clause("legal_basis","Finalidades e hipóteses legais","Para cada tratamento, indicar finalidade, categorias de titulares e dados, hipótese legal proposta, agentes envolvidos, retenção e comprovação.","core");
const incidents=clause("incidents","Incidentes e comunicação","Descrever critérios de avaliação de incidentes, canais internos, responsabilidades, evidências e obrigações de comunicação conforme normas aplicáveis.","conditional","Avaliar contexto regulatório e natureza dos dados.");
const retention=clause("retention","Retenção, descarte e revisão","Estabelecer períodos por categoria documental conforme requisitos legais e necessidades demonstradas; prever eliminação segura e exceções justificadas.","core");
const isoControls=clause("iso_controls","Controle de documentos e versões","Definir responsável, classificação, código, revisão, aprovação, distribuição, acesso, retenção e tratamento de versões obsoletas.","core");
const label=(id,title,sector,sources,sections,owner="Revisão jurídica ou técnica habilitada")=>({id,title,sector,sources,sections,owner,status:"DRAFT_UNREVIEWED",version:"0.1.0",lastReviewed:null,legalReviewRequired:true});
export const legalCatalog = Object.freeze([
 label("contrato-servicos","Contrato de prestação de serviços","Contratos",["cc","lgpd","assinatura"],[party,object,remuneration,term,privacy,security,termination,signing]),
 label("acordo-confidencialidade","Acordo de confidencialidade (NDA)","Contratos",["cc","lgpd"],[party,confidentiality,disposition,term,signing]),
 label("aditivo-contratual","Aditivo contratual","Contratos",["cc","assinatura"],[party,clause("amendment","Alterações pactuadas","As partes acordam a alteração das cláusulas {{clausulas_alteradas}}, preservadas as demais disposições não alteradas.","core"),term,signing]),
 label("termo-entrega-documentos","Termo de entrega de documentos","Gestão Documental",["cc","lgpd"],[party,clause("delivery","Relação de documentos","Descrição, quantidade, estado, protocolo de recebimento, data, responsável e finalidade: {{relacao_documentos}}.","core"),privacy,retention,signing]),
 label("aviso-privacidade","Aviso de privacidade","LGPD",["lgpd","anpd"],[clause("controller","Identificação do controlador","Identificar controlador {{razao_social}}, contatos {{contato_privacidade}} e canais do titular.","core"),legalBasis,retention,clause("rights","Direitos dos titulares","Descrever de forma acessível os direitos previstos na legislação e o procedimento de exercício.","core"),incidents]),
 label("ropa","Registro de operações de tratamento (ROPA)","LGPD",["lgpd","anpd"],[clause("operation","Operação documentada","Processo {{processo}}, unidade {{unidade}}, finalidade {{finalidade}} e responsável {{responsavel}}.","core"),legalBasis,privacy,retention]),
 label("ripd","Relatório de impacto à proteção de dados (RIPD) — estrutura","LGPD",["lgpd","anpd"],[clause("context","Descrição do tratamento","Contexto, natureza, escopo, finalidade e necessidade: {{contexto_tratamento}}.","core"),clause("risk","Avaliação de riscos","Identificar cenários, probabilidade, gravidade, titulares afetados e impactos. Exige avaliação específica e revisão humana.","core"),clause("mitigations","Salvaguardas e medidas","Indicar controles existentes, plano de mitigação, riscos residuais e responsáveis.","core"),incidents]),
 label("politica-seguranca","Política de segurança da informação","Governança/ISO",["lgpd","anpd"],[clause("commitment","Objetivos e abrangência","Descrever objetivos, âmbito, responsabilidades e aprovação da direção: {{escopo_politica}}.","core"),security,isoControls,incidents,retention]),
 label("controle-documentos","Procedimento de controle de informação documentada","Governança/ISO",[],[isoControls,clause("review","Revisão, aprovação e distribuição","Definir elaboração, verificação, aprovação, distribuição controlada e mudança de versões.","core"),retention]),
 label("codigo-conduta","Código de conduta e ética","Governança",["clt","lgpd"],[clause("values","Valores e aplicação","Descrever princípios, público abrangido e compromissos: {{principios}}.","core"),clause("integrity","Conflitos de interesse","Definir declaração, prevenção, investigação e consequências proporcionais e lícitas.","optional"),privacy,clause("report","Canal de relato e proteção","Informar fluxo de comunicação, confidencialidade, apuração e proteção contra retaliações.","conditional","Conforme organização e normas aplicáveis.")]),
 label("termo-epi","Ficha/termo de entrega de EPI","SESMT/SST",["nr","clt"],[clause("worker","Identificação do trabalhador","Nome {{colaborador}}, matrícula {{matricula}}, função {{funcao}} e estabelecimento {{unidade}}.","core"),clause("equipment","Equipamentos entregues","Discriminar EPI, quantidade, CA quando aplicável, data de fornecimento, orientação e substituição.","core"),clause("receipt","Ciência e recebimento","Registrar ciência do trabalhador, orientações recebidas e assinatura conforme método válido.","core"),signing]),
 label("pgr-estrutura","PGR — estrutura de elaboração técnica","SESMT/SST",["nr","pgr"],[clause("scope","Caracterização da organização","Estabelecimento {{unidade}}, atividades, processos, funções e responsáveis técnicos.","core"),risks,actions,clause("review","Monitoramento e revisão","Acompanhar implementação e revisão da avaliação de riscos conforme critérios aplicáveis.","core")],"Profissional técnico competente"),
 label("pc mso".replace(" ",""),"PCMSO — estrutura de elaboração médica","SESMT/SST",["nr","clt"],[clause("medical","Planejamento médico ocupacional","Identificar riscos ocupacionais, população exposta, exames e periodicidades definidos por médico responsável.","core"),clause("reporting","Relatório analítico e acompanhamento","Organizar os indicadores, avaliação de resultados e recomendações conforme requisitos aplicáveis.","core")],"Médico responsável"),
 label("ordem-servico-sst","Ordem de serviço de segurança e saúde","SESMT/SST",["nr","clt"],[clause("task","Atividade e condições de execução","Atividade {{atividade}}, local {{local}}, função {{funcao}} e condições observadas.","core"),risks,clause("precautions","Instruções de prevenção","Definir procedimentos, EPI/EPC, permissões e respostas a emergências conforme avaliação específica.","core"),signing]),
 label("termo-teletrabalho","Aditivo de teletrabalho","Trabalhista/RH",["clt","lgpd"],[party,clause("workplace","Regime e local de execução","Definir modalidade, local de trabalho, equipamentos, despesas e comunicação nos limites legais.","core"),privacy,security,term,signing]),
 label("autorizacao-imagem","Autorização de uso de imagem — minuta","RH/Marketing",["cc","lgpd"],[clause("subject","Identificação do titular","Nome {{nome_titular}}, finalidade declarada {{finalidade}} e contato {{contato}}.","core"),clause("scope","Uso, finalidade e canais","Descrever imagens, canais, período, território, condições e eventuais limitações do uso.","core"),privacy,signing])
]);
export const catalogSectors = [...new Set(legalCatalog.map(x=>x.sector))];
export function modelById(id){return legalCatalog.find(x=>x.id===id)||null;}
export function selectedClauses(model,choices){
 if(!model||!choices||typeof choices!=="object")throw Error("Modelo ou seleção inválidos");
 return model.sections.filter(c=>c.requirement==="core"||choices[c.id]===true).map(c=>({...c}));
}
export function reviewIssues(model,choices,fields={}){
 if(!model)return ["Modelo não encontrado"];
 const issues=[];
 if(model.status!=="APPROVED")issues.push("Modelo editorial não homologado para uso jurídico.");
 for(const c of model.sections){
  if(c.requirement==="conditional"&&choices[c.id]!==true)issues.push('Verificar aplicação da seção condicional: '+c.title);
  if(c.requirement==="core"&&choices[c.id]===false)issues.push('Seção essencial do modelo excluída: '+c.title);
 }
 const sections=selectedClauses(model,choices);
 for(const c of sections)for(const m of c.body.matchAll(/\{\{\s*([A-Za-z][A-Za-z0-9_]{0,63})\s*\}\}/g))if(!String(fields[m[1]]??"").trim())issues.push("Campo pendente: "+m[1]);
 return [...new Set(issues)];
}
