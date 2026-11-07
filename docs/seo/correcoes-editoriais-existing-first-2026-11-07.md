# Plano de correção editorial — 07/11/2026

**Estado:** proposta pronta para revisão; NÃO publicada. **Origem:** HomeHost declarada em 01/11/2026, mas a raiz e a propagação pública ainda exigem verificação (ver `AGENTS.md` e `config/site-hosting.json`). **Política:** 100% de melhorias em URLs existentes, nenhuma nova URL, nenhuma mudança de canonical sem prova de erro.

## Regras obrigatórias

1. Antes de alterar arquivos: confirmar qual raiz HomeHost serve `https://www.arquindex.com.br/`, backup integral restaurável, FTPS com TLS verificado e inventário dos arquivos originais.
2. Preservar URLs, navegação, layouts, cases, preços comprovados, imagens e conteúdos úteis. Aplicar mudanças localizadas no HTML realmente publicado; não substituir páginas completas por este documento.
3. Conferir cada title/meta/FAQ/schema existente antes de editar. A FAQ visível e FAQPage estruturado, quando aplicável, devem permanecer coerentes; não presumir elegibilidade a rich results.
4. Testar depois de cada deploy: HTTP 200 HTTPS, conteúdo novo, canonical correto, robots/indexabilidade, links e formulários, mobile e rollback. Não enviar sitemap/IndexNow sem publicação comprovada.
5. Não inventar atendimento presencial em Brasília/Salvador, clientes locais, garantias legais, prazos de coleta, preços ou certificações. Evitar termos absolutos como “validade jurídica garantida”, “segurança total”, “sem multas”.
6. Verificar fontes primárias: Decreto 10.278/2020 https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2020/decreto/d10278.htm ; ANPD https://www.gov.br/anpd/pt-br ; CONARQ https://www.gov.br/conarq/pt-br ; Google Search Central https://developers.google.com/search/docs/essentials/spam-policies .
7. Confirmar contatos oficiais em fonte institucional antes de atualizar CTAs: https://www.arquindex.com.br/ ; referência editorial: comercial@arquindex.com.br e WhatsApp (31) 97363-2725.

## 1. /guarda_de_documentos.html — preservar URL e canonical

**Title proposto, somente se o atual for inferior:** Guarda de Documentos Empresariais em BH | Arquindex

**Meta description:** Guarda de documentos com inventário, consulta, controle de movimentações e opções de digitalização. Entenda fatores de preço e solicite avaliação do seu acervo.

**Resposta direta AEO (64 palavras):**
> A guarda de documentos empresariais envolve identificação das caixas, inventário, armazenamento sob controles definidos em contrato e procedimentos para consulta e movimentação. O custo depende do volume, da frequência de acesso, da coleta e dos serviços associados, como digitalização e indexação. Antes de contratar, solicite critérios de segurança, prazos de atendimento, regras de devolução e destinação documental conforme a temporalidade aplicável.

**FAQ original:**
- **O preço da guarda inclui retirada e consultas?** Nem sempre. O orçamento deve discriminar coleta, transporte, armazenagem, consultas, movimentações e eventual digitalização.
- **Como localizar uma caixa depois de armazenada?** Solicite inventário com identificador de caixa, unidade ou departamento, período e regras de atualização após movimentações.
- **Posso eliminar os documentos depois de digitalizar?** Não automaticamente. A destinação depende de requisitos legais, avaliação documental, temporalidade e regras aplicáveis ao tipo de documento.

**CTA:** Solicite orçamento de guarda e, se necessário, inclua digitalização, OCR e inventário no mesmo pedido.

## 2. /gestao_de_colaboradores_documentos.html — preservar URL e canonical

**Title:** Gestão de Dossiês de Funcionários | Digitalização e GED | Arquindex

**Meta description:** Organize dossiês de colaboradores com digitalização, OCR, indexação por funcionário e período, revisão e controles de acesso. Solicite avaliação técnica.

**Resposta AEO (59 palavras):**
> A gestão de dossiês de colaboradores reúne documentos de admissão, contratos, exames e registros trabalhistas em uma estrutura identificável por funcionário, período e tipo documental. A digitalização pode incorporar OCR, indexação e conferência para facilitar buscas. O acesso deve respeitar perfis autorizados, requisitos de proteção de dados e regras de retenção aplicáveis a cada documento.

**FAQ original:**
- **Como evitar que páginas de funcionários diferentes sejam agrupadas?** Use regras de separação por identificadores e revisão humana dos casos ambíguos; não confie exclusivamente no OCR.
- **O sistema pode guardar documentos de funcionários desligados?** Sim, desde que haja base legal, finalidade, controle de acesso e prazo de retenção definido conforme a obrigação aplicável.
- **Como tratar exames e informações de saúde?** Segregar permissões e avaliar os requisitos da LGPD para dados pessoais sensíveis.

**CTA:** Solicite diagnóstico para organização de dossiês ativos e inativos, com critérios de separação e conferência.

## 3. /digitalizacao-documentos-brasilia.html — preservar posição e canonical

**Title:** Digitalização de Documentos em Brasília | Projetos Corporativos | Arquindex

**Meta description:** Planeje a digitalização de acervos empresariais em Brasília: preparação, OCR, indexação, conferência e logística definida em orçamento.

**Resposta AEO (56 palavras):**
> Empresas de Brasília que precisam digitalizar contratos, processos administrativos e dossiês podem começar pelo inventário do acervo e pela definição de critérios de indexação. O projeto deve prever preparação, captura, OCR quando adequado, conferência de qualidade e entrega organizada. Coleta, execução no local e transporte precisam ser confirmados no escopo contratado, sem presumir unidade física na cidade.

**Substituir** a seção autorreferente “Por que criar páginas por cidade” por “Como preparar um orçamento de digitalização para acervos em Brasília”: amostra de documentos; formatos; volume; sensibilidade; indexação; critérios de aceite; logística a confirmar.

**FAQ original:** “A coleta em Brasília está incluída?” Resposta: “A disponibilidade, o endereço de retirada e o custo logístico devem ser confirmados na proposta. Não há compromisso automático de coleta.”

## 4. /digitalizacao-documentos-salvador.html — preservar posição e canonical

**Title:** Digitalização de Documentos em Salvador | Acervos Técnicos | Arquindex

**Meta description:** Avalie digitalização de documentos administrativos e técnicos em Salvador, incluindo formatos especiais, OCR, metadados e critérios de entrega.

**Resposta AEO (58 palavras):**
> A digitalização de acervos empresariais em Salvador exige definir os tipos de documentos, formatos físicos, volumes e metadados necessários à recuperação. Em projetos com relatórios técnicos, desenhos e anexos, é importante especificar captura de grandes formatos quando aplicável, nomenclatura e vinculação de arquivos. Transporte, execução presencial e prazos devem constar da proposta aprovada, sem presumir infraestrutura local.

**Seção exclusiva:** “Como especificar acervos técnicos e anexos”: formatos A4/A3/A0 conforme equipamento e escopo; preservação de vínculos entre índice, relatório e desenho; identificação de revisões; amostragem de conferência.

**FAQ original:** “É possível digitalizar plantas e anexos técnicos?” Resposta: “A viabilidade depende do formato, estado físico e equipamento disponível no projeto. A avaliação inicial deve registrar as dimensões e os critérios de qualidade.”

**Anticanibalização:** Brasília = contratos/processos administrativos e critérios de contratação; Salvador = acervos técnicos e anexos. Não copiar FAQs ou apenas substituir cidades. Confirmar demanda real para esses recortes antes de publicar.

## 5. /lgpd-consultoria.html

**Title:** Consultoria LGPD para Empresas | Diagnóstico e Governança | Arquindex

**Meta description:** Consultoria LGPD com diagnóstico, mapeamento de dados, avaliação de riscos, políticas e orientação sobre governança e atuação do encarregado.

**Resposta AEO (54 palavras):**
> A adequação à LGPD envolve conhecer os dados pessoais tratados, documentar finalidades e bases legais, avaliar riscos e estabelecer controles, políticas e processos para atender direitos dos titulares. O papel do encarregado deve ser analisado conforme a legislação e a regulamentação aplicável. Consultoria e ferramentas apoiam a conformidade, mas não garantem ausência de incidentes ou sanções.

**Revisar:** retirar promessas de “sem multas”, “conformidade garantida”, “certificação LGPD” sem comprovação; não afirmar que toda organização deve nomear encarregado sem examinar regras e exceções da ANPD.

## 6. Homepage, OCR, Alfresco, databook e terceirização

- **Homepage:** conferir telefone, e-mail e WhatsApp clicáveis e coerentes; não criar landing page para a consulta “arquindex telefone”.
- **OCR para empresas:** explicar que OCR pesquisável depende da qualidade da captura e revisão, sem prometer acerto de 100%; incluir limites em tabelas e manuscritos.
- **Alfresco:** distinguir Community de ofertas comerciais e integrações efetivamente implantadas; não atribuir recursos de versões sem documentação.
- **/montagem_databook_organizar.html:** especificar índice, revisão, rastreabilidade, evidências de inspeção e aceite sem inventar certificações.
- **/terceirizacao_arquivos_documentos.html:** detalhar responsabilidades, inventário, consulta, devolução e descarte autorizado.

## 7. Riscos técnicos a INVESTIGAR, não corrigir em massa

- `/index1.html` versus homepage: comparar HTML, intenção, links, canonical e consultas Top 10; só propor consolidação após prova de duplicidade e impacto.
- `/seo-local/` e `?post=`: agrupar por intenção, fonte e canonical; não aplicar noindex ou 301 em lote.
- `Index of /`: verificar listagem em cada subdomínio com resposta pública e logs; bloquear listagem apenas na origem correta e após validar que não afeta download legítimo.
- Consultas incomuns que parecem caminhos internos: checar logs, status HTTP, permissões e exposição real; não inferir invasão nem reproduzir identificadores.
- HTTPS raiz/www: preservar canonical correto `https://www.arquindex.com.br/` na homepage; verificar redirecionamentos e TLS antes de mudar configuração.

## Checklist de aceitação e relatório

- [ ] Origem pública e raiz HomeHost verificadas (Cloudflare/Railway divergentes resolvidos por evidência)
- [ ] Backup completo restaurável com teste de leitura
- [ ] Arquivos reais identificados, diff mínimo revisado
- [ ] 6+ melhorias em URLs existentes, 0 novas URLs
- [ ] Canonicals e URLs Top 10 preservados
- [ ] Sem duplicação de FAQ Brasília/Salvador
- [ ] Testes HTTPS 200, title/meta, FAQ visível, schema, mobile, links e CTA
- [ ] Commit/deploy e URL pública com conteúdo alterado comprovados
- [ ] Sitemap/IndexNow somente após publicação e necessidade confirmadas

**Até completar o checklist:** status `PENDENTE DE DEPLOY`, nenhuma página publicada por este plano.
