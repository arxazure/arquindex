const solutions=[
["digitalizacao-documentos","Digitalização de documentos","OCR, PDF/A, indexação, controle de qualidade e rastreabilidade"],
["gestao-documental","Gestão documental","classificação, temporalidade, organização, governança e acesso"],
["organizacao-arquivos","Organização de arquivos","inventário, endereçamento, padronização, empréstimos e localização"],
["consultoria-lgpd","Adequação LGPD","mapeamento, ROPA, políticas, contratos, direitos dos titulares e governança"],
["dpo-terceirizado","DPO terceirizado","rotina de privacidade, atendimento a titulares, registros e orientação"],
["alfresco-incloud","Alfresco ECM em nuvem","repositório, permissões, metadados, versionamento, workflows e auditoria"],
["databook","Databook de engenharia","índices, volumes, capítulos, conferência documental e entrega"],
["guarda-documental","Guarda documental","custódia, rastreabilidade, consultas, movimentação e temporalidade"],
["incineracao-segura","Descarte e incineração segura","validação de temporalidade, autorização, rastreabilidade e certificado"],
["seguranca-informacao","Segurança da informação documental","controles de acesso, incidentes, políticas e proteção de documentos"]
];
const sectors=[
["rh-departamento-pessoal","RH e Departamento Pessoal","dossiês de colaboradores, admissões, folhas, benefícios, treinamentos e documentos trabalhistas","reduzir tempo de busca, controlar acesso e aplicar retenção adequada"],
["juridico","Jurídico e escritórios de advocacia","processos, contratos, pareceres, procurações, provas e documentos de clientes","preservar histórico, localizar versões e manter confidencialidade"],
["saude","Clínicas, hospitais e saúde ocupacional","prontuários, exames, laudos, ASOs, fichas clínicas e documentos sensíveis","separar por paciente, restringir acesso e manter rastreabilidade"],
["engenharia","Engenharia e construção","projetos, desenhos, memoriais, relatórios, databooks, certificados e revisões","controlar versões, disciplinas, fornecedores e entregáveis"],
["industria","Indústria e manufatura","qualidade, manutenção, produção, segurança, contratos, RH e documentação técnica","padronizar acervo e acelerar auditorias e inspeções"],
["mineracao","Mineração e siderurgia","engenharia, meio ambiente, qualidade, segurança, contratos e documentação operacional","integrar acervos extensos e facilitar evidências para auditorias"],
["farmaceutico","Farmacêutico e laboratórios","qualidade, produção, validações, treinamentos, regulatórios e documentação administrativa","melhorar disponibilidade de evidências e controlar versões"],
["educacao","Educação e instituições de ensino","documentos acadêmicos, contratos, RH, financeiro, alunos e registros institucionais","organizar históricos e permitir acesso controlado por área"],
["cartorios","Cartórios e registros","livros, atos, índices, documentos históricos e acervos de consulta","preservar legibilidade, facilitar localização e apoiar continuidade do acervo"],
["financeiro","Financeiro, contábil e administrativo","notas, comprovantes, contratos, conciliações, cadastros e documentos fiscais","reduzir dispersão, melhorar busca e apoiar retenção e auditoria"]
];
const benefits={
"digitalizacao-documentos":["preparação física e conferência do acervo","captura adequada ao formato documental","OCR para pesquisa de texto","indexação por campos relevantes","entrega estruturada e controle de qualidade"],
"gestao-documental":["diagnóstico do acervo","plano de classificação","tabela de temporalidade","regras de acesso e movimentação","destinação e descarte controlado"],
"organizacao-arquivos":["inventário inicial","padronização de caixas e pastas","endereçamento físico","controle de empréstimos","estrutura digital correspondente"],
"consultoria-lgpd":["mapeamento das operações","identificação de bases legais","ROPA e registros","políticas e contratos","plano de adequação e governança"],
"dpo-terceirizado":["canal de titulares","rotina de decisões e registros","orientação a áreas internas","acompanhamento de incidentes","revisão periódica de controles"],
"alfresco-incloud":["estrutura por sites e departamentos","perfis e permissões","metadados e busca","versionamento e workflows","auditoria, backup e suporte"],
"databook":["índice contratual","organização por volumes e capítulos","conferência de documentos","controle de pendências","entrega final rastreável"],
"guarda-documental":["inventário de entrada","endereçamento de caixas","solicitações e devoluções","controle de movimentações","temporalidade e destinação"],
"incineracao-segura":["validação de autorização","segregação do material","cadeia de custódia","destruição controlada","registro e certificado"],
"seguranca-informacao":["matriz de acessos","políticas e procedimentos","proteção de dados e documentos","resposta a incidentes","auditoria e melhoria contínua"]
};
function slug(s){return s.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g,"").replace(/[^a-z0-9]+/g,"-").replace(/^-|-$/g,"")}
export const landingPages=[];
for(const sol of solutions){
 for(const sec of sectors){
  const [serviceSlug,service,scope]=sol;
  const [sectorSlug,sector,docs,goal]=sec;
  const title=`${service} para ${sector}`;
  const lead=`Como estruturar ${service.toLowerCase()} em operações de ${sector.toLowerCase()} com foco em ${goal}.`;
  const checklist=benefits[serviceSlug];
  landingPages.push({
   slug:`${serviceSlug}-para-${sectorSlug}`,
   title,serviceSlug,service,sector,lead,
   description:`${service} para ${sector}: ${scope}. Guia prático da Arquindex para projetos corporativos.`,
   docs,goal,scope,checklist,
   sections:[
    ["O desafio documental do setor",`Em ${sector.toLowerCase()}, o acervo costuma reunir ${docs}. Quando arquivos físicos, pastas de rede, e-mails e sistemas ficam separados, localizar a informação certa pode exigir tempo excessivo e aumentar o risco de uso de versões incorretas.`],
    ["Como estruturar o projeto",`O desenho deve partir do volume, dos tipos documentais, de quem consulta o acervo e dos prazos de retenção. Para ${service.toLowerCase()}, a Arquindex combina ${scope}, adaptando etapas ao ambiente e às prioridades do cliente.`],
    ["Governança e acesso",`O objetivo não é apenas armazenar documentos, mas definir critérios de acesso, nomenclatura, classificação, revisão e descarte. Isso ajuda a ${goal}, mantendo histórico das decisões e reduzindo dependência de conhecimento informal.`],
    ["Indicadores recomendados",`Acompanhe volume processado, pendências, taxa de retrabalho, tempo médio de localização, documentos sem classificação, solicitações atendidas e itens vencidos para retenção. Indicadores simples tornam o projeto mensurável e ajudam a priorizar melhorias.`],
    ["Próximo passo",`Um diagnóstico inicial com amostragem do acervo permite estimar esforço, equipe, prazo, tecnologia e logística. A Arquindex pode estruturar projeto, operação recorrente ou atendimento sob demanda conforme a necessidade.`]
   ],
   faqs:[
    ["Quais documentos entram no projeto?",`Os mais comuns são ${docs}, além de outros registros definidos no diagnóstico.`],
    ["É possível começar por um piloto?","Sim. Um lote piloto ajuda a validar classificação, qualidade, indexação, produtividade e critérios de aceite antes da expansão."],
    ["A solução pode integrar acervo físico e digital?","Sim. O projeto pode combinar organização física, digitalização, repositório eletrônico, metadados e regras de movimentação conforme o escopo."],
    ["Como é calculado o orçamento?","O valor depende de volume, formatos, preparação, indexação, deslocamento, prazo, requisitos de segurança e tecnologia necessária."]
   ]
  });
 }
}
