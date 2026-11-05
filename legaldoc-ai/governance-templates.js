// Original Arquindex checklist prompts — require professional verification of applicability.
export const auditTemplates = Object.freeze([
{id:'contract',title:'Gestão de contratos e marcos',sources:['Código Civil'],items:[
{id:'parties',question:'Partes, representantes e poderes de assinatura estão identificados?'},
{id:'scope',question:'Objeto, escopo, entregáveis e critérios de aceite foram definidos?'},
{id:'term',question:'Datas de início, término, renovação e aviso prévio estão registradas?'},
{id:'payments',question:'Valores, reajustes, faturamento e eventuais garantias foram conferidos?'},
{id:'privacy',question:'Foram avaliadas obrigações de privacidade e confidencialidade?'},
{id:'evidence',question:'Assinaturas, anexos e versões possuem trilha de evidências?'}]},
{id:'sst',title:'SST / SESMT — controles gerais',sources:['NR-1','NR-6','NR-7'],items:[
{id:'risks',question:'Riscos e perigos foram avaliados conforme as atividades reais?'},
{id:'pgr',question:'Foi conferida a aplicabilidade e a documentação de GRO/PGR?'},
{id:'medical',question:'O planejamento médico ocupacional foi revisado pelo responsável técnico?'},
{id:'epi',question:'Há registro rastreável de entrega, substituição e orientações de EPI?'},
{id:'training',question:'Treinamentos aplicáveis têm responsáveis, evidências e controle de vencimento?'},
{id:'actions',question:'Há plano de ação com responsáveis, prazos e verificação de eficácia?'}]},
{id:'integrity',title:'Integridade e anticorrupção',sources:['Lei 12.846/2013','Decreto 11.129/2022','CGU'],items:[
{id:'tone',question:'A direção demonstra compromisso formal com integridade?'},
{id:'risk',question:'Riscos de integridade foram identificados e priorizados?'},
{id:'conduct',question:'Existe código de ética e conduta submetido a revisão?'},
{id:'thirdparty',question:'Parceiros e terceiros são avaliados segundo riscos relevantes?'},
{id:'report',question:'Existem canais de denúncia e tratamento de relatos com proteção apropriada?'},
{id:'monitor',question:'Existem evidências de treinamento, monitoramento e melhoria contínua?'}]},
{id:'lgpd',title:'LGPD e privacidade',sources:['Lei 13.709/2018','ANPD'],items:[
{id:'ropa',question:'Operações de tratamento, finalidades e bases legais estão registradas?'},
{id:'access',question:'Controles de acesso e compartilhamento foram avaliados?'},
{id:'retention',question:'Prazos de retenção, descarte e exceções foram documentados?'},
{id:'rights',question:'Canal e processo de direitos dos titulares foram definidos?'},
{id:'incident',question:'Plano de resposta a incidentes e critérios de comunicação foram revisados?'},
{id:'review',question:'Há revisão jurídica e registros de versões das políticas?'}]},
{id:'documented',title:'Gestão de informação documentada / ISO',sources:['Normas ISO/ABNT aplicáveis sob licença'],items:[
{id:'approval',question:'Informações documentadas são aprovadas antes de emissão?'},
{id:'version',question:'Identificação, revisão, responsáveis e datas estão controlados?'},
{id:'access',question:'Distribuição e acesso estão adequados ao uso?'},
{id:'retention',question:'Retenção, armazenamento e descarte têm controles definidos?'},
{id:'obsolete',question:'Versões obsoletas são identificadas e protegidas contra uso indevido?'},
{id:'audit',question:'Não conformidades e ações corretivas são acompanhadas?'}]}
]);