# Execução SEO/GEO/AEO — 22/10/2026, manhã

## Escopo e decisão

Foram auditadas as fichas ARQ-064 a ARQ-069 em mobile (390×844) e desktop (1440×900). A publicação foi limitada a três URLs com intenção distinta e problema técnico/conteúdo concreto: ARQ-064, ARQ-066 e ARQ-067. ARQ-065 e ARQ-068 foram preservadas por sobreposição com páginas genéricas de digitalização; ARQ-069 foi preservada porque URL, brief e conteúdo não descrevem a mesma intenção editorial.

- Auditoria pública: [run 39772221402](https://github.com/arxazure/arquindex/actions/runs/39772221402), job 119802315630, sucesso.
- Publicação FTP com backup: [run 39772497400](https://github.com/arxazure/arquindex/actions/runs/39772497400), sucesso.
- Validação pública pós-publicação: [run 39772887454](https://github.com/arxazure/arquindex/actions/runs/39772887454), sucesso.
- Atualização e validação de sitemaps: [run 39773066711](https://github.com/arxazure/arquindex/actions/runs/39773066711), sucesso.

## Search Console

Propriedade: `sc-domain:arquindex.com.br`.

Comparação de períodos completos usada na decisão:

- atual: 06/10/2026 a 19/10/2026;
- anterior: 22/09/2026 a 05/10/2026.

| ID | Atual: impressões / cliques / posição | Anterior: impressões / cliques / posição | Leitura |
|---|---:|---:|---|
| ARQ-064 | 12 / 0 / 6,83 | 7 / 0 / 21,29 | visibilidade cresceu; amostra ainda pequena |
| ARQ-065 | 7 / 0 / 6,57 | 1 / 0 / 8,00 | preservar até resolver sobreposição |
| ARQ-066 | 16 / 0 / 5,63 | 2 / 0 / 5,00 | consultas misturam marca e guarda documental |
| ARQ-067 | 12 / 0 / 9,58 | 3 / 0 / 24,67 | oportunidade comercial clara |
| ARQ-068 | 6 / 0 / 8,67 | 2 / 0 / 5,00 | uma impressão veio de “digitação de documentos”; intenção precisa ser definida |
| ARQ-069 | 7 / 0 / 7,43 | 2 / 0 / 9,00 | não publicar enquanto URL, brief e conteúdo divergirem |

Consultas observadas: ARQ-066 teve “guarda de documentos belo horizonte” (2 impressões, posição 13,5), “guarda documentos bh” (1, posição 7) e “arquindex” (1, posição 6). ARQ-067 teve “serviço de digitalização de documentos” (3, posição 13,67) e variação plural (1, posição 26).

Os dados não comprovam melhora de ranking, indexação ou geração de leads.

## Alterações publicadas

### ARQ-064 — digitalização de arquivos empresariais em São Paulo

URL: https://digitalizar-arquivos-sp.arquindex.com.br/

- title anterior: `Digitalização de arquivos empresariais em São Paulo | Arquindex`
- title novo: `Digitalização de Arquivos Empresariais em São Paulo | Arquindex`
- H1: mantido semanticamente específico para arquivos empresariais em São Paulo.
- melhoria substantiva: identidade oficial responsiva, atendimento flutuante único, resposta AEO com inventário, amostra, OCR e aceite, links contextuais e CTA de proposta com UTM.
- contexto local: logística apresentada como etapa a confirmar, sem alegar unidade física em São Paulo.
- hash público: `085ac3b9c551a1d66c592060c0296332d835a36728f3495f119a2f4297a73295`.
- sitemap: a URL já estava presente; não houve reenvio repetido.

### ARQ-066 — segurança da informação e governança documental

URL: https://seguranca.arquindex.com.br/

- title anterior: `Seguranca | gestão da informação e documentos em Belo Horizonte | Arquindex`
- title novo: `Segurança da Informação e Documentos | Arquindex`
- H1 anterior: `gestão da informação e documentos em Belo Horizonte para empresas.`
- H1 novo: `Segurança da informação e governança documental`
- melhoria substantiva: identidade oficial, remoção do widget antigo, matriz AEO sobre repositórios, acessos, ciclo de vida e riscos, links para gestão documental/LGPD/ANPD e CTA de proposta com UTM.
- hash público: `7e4da5966ca862b384c425fa5c4243a46f0e3fac8aec58997c8a691e9becec82`.
- sitemap: URL incluída e XML público validado; 10 URLs após a atualização.
- hash do sitemap público: `a7232176fcd11bfdf2ec87f6e1dcabe13a7d1c55730773c3c9792980410da782`.

### ARQ-067 — contratação de digitalização com armazenamento

URL: https://contratar-servicos-digitalizacao-documentos-com-armazenamento.arquindex.com.br/

- title anterior: `Como contratar digitalização de documentos em Belo Horizonte | Arquindex`
- title novo: `Digitalização com Armazenamento: Como Contratar | Arquindex`
- H1 anterior: `digitalização de documentos em Belo Horizonte para empresas.`
- H1 novo: `Como contratar digitalização de documentos com armazenamento`
- melhoria substantiva: identidade oficial, remoção do widget antigo, checklist AEO de captura, OCR, indexação, armazenamento, acesso, exportação, backup, suporte e saída, links contextuais e CTA de proposta com UTM.
- hash público: `dcb1bc67f9e2d096fc77986b012018a28eef177be6896113a0585223d751fa6a`.
- sitemap: URL incluída e XML público validado; 12 URLs após a atualização.
- hash do sitemap público: `1e2aa3a0c3dca2f85f2fc24180381519ca2baf6168385f7e5abd0149eda4b69b`.

## Backup, rollback e verificação

Backup remoto preservado em `/seo-backups/rodada-20261022-manha-20261022T114300Z/`.

Hashes anteriores:

- ARQ-064: `e7f51e2d98026a5122248ae03b0acc32e5a909cf93f2ad62554c180df4fa3472`
- ARQ-066: `927c100cc5a100a5c3125608a2f29c2b9311964645008890f93cd8b8279e10a6`
- ARQ-067: `ccea56537f90957b3cfb8228c2e152e6b25d9d6aae4d58e0f0c6bf14b80a2c2b`

Backups de sitemap em `/seo-backups/sitemaps-rodada-20261022-manha-20261022T114609Z/`.

Todas as três páginas passaram em mobile e desktop com:

- HTTP 200;
- canonical único e correspondente à URL;
- um H1;
- `index,follow` e ausência de `noindex`;
- logo oficial, menu responsivo e um único `#arq-floating`;
- zero widgets antigos;
- bloco AEO visível;
- CTA de proposta com UTM;
- ausência de overflow horizontal dentro da tolerância de 2 px.

## Commits e arquivos operacionais

- auditoria: `ecaaf6e13e3487068d90231fa2f344ce914cf8ae`
- script de conteúdo/publicação: `34cbe7e944a54ec58e1b009ac240b645e4da0271`
- workflow de publicação: `64aab0d00221e3226fb2c8424bc731781c44a10d`
- workflow de validação: `bd90f81261c9f469f3b6d7687dcd37751bdbac3e`
- checagem de sitemaps: `fe696405366119937ee48f535953247e72832352`
- script de sitemaps: `66402d701f7f5482af8d22ba2217e7517261a7f7`
- workflow de sitemaps: `471f350fd4bf66bfe5eac74a3e335482d33fcdda`
- atualização da fila: `8e9fe691f4d55b45ab3cd6af23a49270193ef9cc`, com correção de hashes em `4f629014d0116d5494c93b9e8d1773d6a2960a14`

## Descoberta e divulgação

Não houve submissão ao Google Search Console, Bing Webmaster ou IndexNow: nesta execução não havia ação autenticada de escrita que confirmasse recebimento. Os sitemaps foram publicados e validados, o que não equivale a indexação.

Nenhuma publicação social foi criada nesta rodada, evitando duplicação com a rotina social dedicada. ARQ-007 e ARQ-099 não foram republicadas.

Não foi criada notícia artificial: a rodada concentrou-se nas melhorias comerciais/técnicas verificadas.

## Continuidade

Cursor: **ARQ-070**.

Próxima auditoria: ARQ-070 a ARQ-075, com prioridade para OCR Mauá, digitalização em Minas Gerais e mapeamento para educação somente quando intenção, atendimento e diferenciação estiverem confirmados.
