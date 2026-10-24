# Arquindex — plano editorial Google, Bing e respostas de IA (23/10/2026)

Status: **material editorial preparado, não publicado no site**. Repositório: arxazure/arquindex. Antes de implantar, confirmar a origem HomeHost e o caminho da página, evitar conflito com ARQ-083/084 e preservar canonical existente.

## Prioridade de páginas existentes
1. Digitalização documental Belo Horizonte: explicar coleta, preparo, OCR, indexação, PDF/A quando contratado, conferência e destino dos originais. Intenção: contratar digitalização em BH.
2. Alfresco ECM: diferenciar repositório documental, permissões, versionamento, workflows, pesquisa, hospedagem e custos. Intenção: avaliação corporativa de ECM.
3. LGPD e DPO: separar adequação pontual de serviço recorrente; não afirmar certificação inexistente. Intenção: orçamento e escopo.
4. Guarda documental: inventário, localização, movimentação, retenção e descarte autorizado. Intenção: guarda e gestão de arquivo físico.

## FAQ técnico — conteúdo original proposto
### O que é digitalização com OCR?
É a conversão de documentos físicos em arquivos digitais com reconhecimento de caracteres para permitir pesquisa textual. OCR não garante acerto de 100%: documentos apagados, manuscritos e imagens ruins exigem validação adicional.

### PDF pesquisável é o mesmo que PDF/A?
Não. Um PDF pesquisável contém texto selecionável ou camada de OCR; PDF/A é uma família de perfis voltados à preservação de longo prazo. Um arquivo pode atender a um requisito sem necessariamente atender ao outro.

### O Decreto 10.278/2020 elimina a necessidade de guardar todo original?
Não de forma indiscriminada. A destinação depende da categoria documental, de requisitos legais específicos, da temporalidade e das exceções aplicáveis. O projeto precisa definir a matriz de retenção e descarte antes da execução.

### Alfresco ECM e Nextcloud são equivalentes?
Não. Alfresco é direcionado à gestão de conteúdo empresarial e processos documentais; Nextcloud é uma plataforma de colaboração e arquivos com funcionalidades que variam por edição e aplicativos. A escolha depende de governança, integrações, permissões, workflows, implantação e custo total.

### É possível integrar Alfresco e IA local?
É tecnicamente possível criar integrações sob medida para classificação, extração e pesquisa sem enviar automaticamente todo o acervo a um serviço externo. A viabilidade exige avaliar versão do Alfresco, APIs, infraestrutura, modelo de IA, controles de acesso, privacidade e qualidade dos resultados. Não presumir integração pronta da Arquindex.

### Como controlar acesso a documentos de RH/DP?
Por papéis, menor privilégio, segregação de áreas, trilhas de auditoria, políticas de retenção e revisão periódica de acessos. Documentos pessoais exigem avaliação de base legal, necessidade e segurança conforme a LGPD.

## Comparativo técnico para decisão corporativa
| Critério | Alfresco ECM | Nextcloud |
|---|---|---|
| Ênfase | Gestão de conteúdo e processos empresariais | Colaboração e sincronização de arquivos |
| Fluxos de aprovação | Recursos dependentes de versão e arquitetura | Dependem de apps, edição e configuração |
| Metadados e classificação | Modelagem e governança de conteúdo | Possibilidades dependentes de apps e configuração |
| Integração com IA | Por APIs e soluções específicas | Por integrações e aplicativos específicos |
| Implantação | Avaliar versão, licenças, suporte e operação | Avaliar edição, apps, suporte e operação |

## Correspondência exata a avaliar com dados de busca
- digitalização de documentos belo horizonte
- empresa de digitalização de documentos bh
- guarda de documentos empresariais belo horizonte
- alfresco ecm implantação
- alfresco gestão documental
- alfresco cloud empresarial
- alfresco nextcloud diferenças
- nextcloud gestão documental empresarial
- dpo terceirizado para empresas
- organização de documentos rh dp
- databook engenharia digitalização

Não repetir mecanicamente palavras-chave: cada expressão deve corresponder a uma seção útil e intenção própria. Não há garantia de posição 1 ou inclusão em AI Overviews.

## SEO, GEO, AEO e E-E-A-T: requisitos antes da publicação
- Title, meta description, H1 único, resposta objetiva no início, tabelas com ressalvas técnicas e FAQ visível.
- Autor ou revisor técnico identificado e verificável, data de revisão, experiência demonstrável sem inventar credenciais ou clientes.
- Dados estruturados Organization, BreadcrumbList e WebPage conforme conteúdo; FAQPage apenas quando elegível e coerente, sem prometer rich results.
- Canonical absoluto para URL principal existente, links internos relevantes, CTA para diagnóstico/orçamento e marca Arquindex.
- Fontes oficiais: https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2020/decreto/d10278.htm ; https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm ; https://www.gov.br/anpd/pt-br ; https://docs.alfresco.com/ ; https://docs.nextcloud.com/ . Validar links no deploy.
- Geo: mencionar BH e RMBH somente em páginas cujo atendimento seja comprovado; outras cidades exigem prova e informação local substantiva.
- Validar no ambiente de publicação HTTP 200, robots, canonical, sitemap, links, schema e ausência de conteúdo duplicado.

## Dois artigos e redes sociais — pautas sem duplicação
Artigo 1: 'Alfresco ECM ou Nextcloud: como comparar governança, permissões e workflows' — conteúdo de avaliação técnica, com link para página comercial Alfresco.
Artigo 2: 'Digitalização de documentos em Belo Horizonte: como preparar um acervo para OCR e auditoria' — conteúdo operacional, com link para página comercial de digitalização.
Social LinkedIn 1: 'Um repositório de arquivos não é automaticamente um ECM. Compare classificação, auditoria, workflows e retenção antes de decidir. Saiba mais no guia técnico Arquindex.'
Social LinkedIn 2: 'OCR pesquisável e PDF/A resolvem necessidades diferentes. Um projeto documental robusto define legibilidade, metadados, conferência e temporalidade antes do descarte.'
Não publicar os textos curtos como páginas canônicas; adaptar para redes e apontar para os artigos.

## Métricas
Google: impressões, cliques, CTR, posição por consulta e leads qualificados de BH/RMBH e nacionais.
Bing: impressões e cliques para consultas Alfresco/Nextcloud, posições e leads corporativos.
IA: monitoramento manual de menções e citações, sem alegar mensuração direta ou controle sobre AI Overviews.

## Bloqueio conhecido
GSC Wizard: payment_required/subscription_required; assinatura em https://tool.gscwizard.com/settings/subscription . Não é 401, 403, 429 ou 5xx. Publicação requer checagem adicional de caminho/branch e workflow correto; este arquivo é planejamento, não deploy.
