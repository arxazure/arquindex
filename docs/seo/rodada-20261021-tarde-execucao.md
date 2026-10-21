# Rodada SEO/GEO/AEO — 21/10/2026, tarde

## Escopo e fila

- Cursor recebido: ARQ-052.
- Fichas lidas: ARQ-052 a ARQ-057.
- URLs auditadas: 6.
- Melhorias substanciais publicadas: 3 — ARQ-054, ARQ-055 e ARQ-057.
- Próximo cursor: ARQ-058; próxima auditoria: ARQ-058 a ARQ-063.
- ARQ-099 preservada.
- Auditoria: https://github.com/arxazure/arquindex/actions/runs/39646166055

## Diagnóstico anterior

| ID | Situação pública antes da mudança |
| --- | --- |
| ARQ-052 | HTTP 200, canonical e H1 únicos, 970 palavras, sem overflow; identidade ausente, nenhum AEO e apenas um link interno |
| ARQ-053 | HTTP 200, canonical e H1 únicos, 971 palavras, sem overflow; identidade ausente, nenhum AEO e apenas um link interno |
| ARQ-054 | HTTP 200; title com “Arquindex” repetido três vezes; canonical apontava para caminho incorreto no domínio principal; sem identidade/AEO/CTA; overflow móvel 554/390 |
| ARQ-055 | HTTP 200; title com “Arquindex” repetido três vezes; canonical incorreto no domínio principal; sem identidade/WhatsApp/CTA/AEO; overflow móvel 422/390 |
| ARQ-056 | HTTP 200 e conteúdo extenso, mas title repetido, canonical incorreto, identidade ausente e overflow 422/390; possível sobreposição BH |
| ARQ-057 | HTTP 200; title com “Arquindex” repetido quatro vezes; canonical incorreto no domínio principal; sem identidade/WhatsApp/CTA/AEO |

ARQ-052 e ARQ-053 foram preservadas para diferenciação frente às páginas de databooks das mesmas cidades. ARQ-056 foi preservada por sobreposição com o grupo de digitalização em BH e porque a consulta observada “guarda documentos BH” não corresponde à intenção declarada da página.

## Antes e depois

| ID | Title anterior | Title publicado |
| --- | --- | --- |
| ARQ-054 | Quais aplicativos facilitam a digitalização de documentos pelo celular - Perguntas frequentes \| Arquindex \| Arquindex \| Arquindex | Digitalização pelo celular: limites e conferência \| Arquindex |
| ARQ-055 | Arquivo Físico e Digital em BH \| Arquindex \| Arquindex \| Arquindex | Guarda de Documentos em BH: Consulta e Controle \| Arquindex |
| ARQ-057 | Vantagens de processamento de documentos com OCR \| Arquindex \| Arquindex \| Arquindex 2 \| Arquindex | OCR de Documentos em São Paulo: Pesquisa e Revisão \| Arquindex |

As três canonicals foram corrigidas para as próprias URLs de subdomínio. Também foram publicados H1s específicos, meta descriptions concisas, identidade oficial, atendimento único, respostas AEO, tabelas práticas, fontes, links contextuais e CTAs com UTM.

- ARQ-054: diferencia captura ocasional por celular de lote corporativo, OCR e conformidade.
- ARQ-055: descreve entrada, solicitação, retirada e devolução com protocolo, sem divulgar endereço operacional restrito.
- ARQ-057: explica limites do OCR e revisão de carimbos, tabelas, imagens degradadas e dados críticos, sem prometer precisão universal ou unidade física local.

## Publicação, backup e validação

- Script: https://github.com/arxazure/arquindex/commit/0ce638e79a023c504039cb70f3d6e3ad33e4bbad
- Publicação FTP: https://github.com/arxazure/arquindex/actions/runs/39646417690 — sucesso.
- Backups: `/seo-backups/rodada-20261021-tarde-20261021T174518Z/`.
- Hashes publicados:
  - ARQ-054: `d2d319fcad221b2f34f106e11e7299b6a04784fd42335b4b56d8e553f0d0da13`
  - ARQ-055 final: `c4b05b710c00a5968ce8a0827c5b72a01e257eb703700e30a7ed2b3f313bc271`
  - ARQ-057: `e9d046ad4d20b13203c754b982a7ce272e6a2f617b53f54e89628bf84b828fda`
- A primeira validação encontrou overflow residual em ARQ-055. Diagnóstico: link técnico longo `sitechecker...` sem quebra, workflow https://github.com/arxazure/arquindex/actions/runs/39646900456.
- Correção isolada com backup: https://github.com/arxazure/arquindex/actions/runs/39647033442.
- Validação final, tentativa 2: https://github.com/arxazure/arquindex/actions/runs/39646783673 — sucesso.

Resultado final em 390×844 e 1440×900: HTTP 200, title esperado, uma canonical própria, um H1, descrição presente, ausência de noindex, sem overflow, logo/menu oficiais, um atendimento flutuante, WhatsApp, proposta e bloco AEO.

## Sitemaps

A verificação inicial mostrou:

- ARQ-054 já presente em `https://aplicativos-facilitam-digitalizacao-documentos-pelo-celular.arquindex.com.br/sitemap.xml`.
- ARQ-055 ausente de `https://arquivo.arquindex.com.br/sitemap.xml`.
- ARQ-057 ausente de `https://solucoes-ocr-sp.arquindex.com.br/sitemap.xml`.

Depois de validar HTTP 200 de todas as URLs existentes, ARQ-055 e ARQ-057 foram adicionadas aos respectivos XMLs, sem duplicatas.

- Primeira tentativa do workflow de publicação falhou antes de qualquer gravação por erro de tratamento de exceção: https://github.com/arxazure/arquindex/actions/runs/39647564123.
- Correção e publicação: https://github.com/arxazure/arquindex/actions/runs/39647669380 — sucesso.
- Backups dos XMLs: `/seo-backups/sitemaps-rodada-20261021-tarde-20261021T175242Z/`.
- Verificação pública final, tentativa 2: https://github.com/arxazure/arquindex/actions/runs/39647332006 — sucesso.

As páginas já existiam; não foram tratadas como URLs novas. Não houve submissão ao Search Console/Bing/IndexNow sem ação autenticada que confirmasse recebimento, e inclusão no sitemap não foi tratada como indexação.

## Search Console — URLs exatas

Período completo: 05–18/10/2026. Comparação: 21/09–04/10/2026, que retornou zero linhas para as seis URLs.

| URL | Consulta | Impressões | Cliques | Posição |
| --- | --- | ---: | ---: | ---: |
| ARQ-054 | quais aplicativos de digitalização... | 1 | 0 | 5,00 |
| ARQ-055 | arquindex | 11 | 0 | 2,45 |
| ARQ-055 | guarda documentos bh | 2 | 0 | 27,50 |
| ARQ-056 | arquindex | 3 | 0 | 1,00 |
| ARQ-056 | guarda documentos bh | 1 | 0 | 30,00 |
| ARQ-057 | ocr gestão de documentos | 1 | 0 | 81,00 |
| ARQ-057 | ocr legal | 3 | 0 | 4,33 |

As amostras são pequenas e não permitem atribuir tendência. A consulta de marca da ARQ-055 não comprova desempenho comercial da intenção “guarda documentos BH”.

## Divulgação e próximas prioridades

- Nenhuma publicação social foi duplicada nesta rotina.
- Nenhum lead, posição Top 3, indexação ou conversão foi presumido.
- Próximas prioridades:
  1. Auditar ARQ-058 a ARQ-063, priorizando URLs com posição média entre 3 e 10 e zero cliques.
  2. Definir papel próprio para ARQ-052/053 antes de ampliar páginas locais.
  3. Resolver a consolidação/canonical da ARQ-056 em rodada própria, sem competir com a página-pilar de BH.
