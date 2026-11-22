# Rodada SEO/GEO/AEO — 22/11/2026 — tarde

## Escopo e segurança

Auditoria pública, somente leitura, das fichas ARQ-030 a ARQ-035. O lote cobre RIPD/LGPD, descarte documental, CONARQ e três páginas comerciais de digitalização em Belo Horizonte.

Foram verificados DNS, TLS, HTTP, estado renderizado de canonical/title/H1/meta description, viewport móvel e desktop, robots, sitemap, links internos, conteúdo, identidade, WhatsApp e formulários.

Nenhuma escrita via FTP, alteração de produção, atualização de sitemap, IndexNow, Search Console, Bing ou divulgação social foi executada. ARQ-007 e ARQ-099 foram preservadas. O inventário de 56 subdomínios permanece no consolidado de 13/11/2026, com 56/56 nomes auditados; não foi refeito nesta rodada para evitar duplicação.

## Evidências reproduzíveis

- Auditoria HTTP/SEO: [run 45050484516](https://github.com/arxazure/arquindex/actions/runs/45050484516)
  - job: `137294277433`
  - artefato: `14765182977`
  - SHA-256: `623d087c32f25c98641aa5d364bf6e08511321576a159689ff42ddaebdc36bb1`
- Validação mobile/desktop: [run 45050481727](https://github.com/arxazure/arquindex/actions/runs/45050481727)
  - job: `137294268533`
  - artefato: `14765765139`
  - SHA-256: `eda8751e8b72b4b224d916cdecf48fe2fda7a8deba7105a499967c0a9a93376d`
- Canonical após JavaScript: [run 45050483986](https://github.com/arxazure/arquindex/actions/runs/45050483986)
  - job: `137294275402`
  - artefato: `14765133425`
  - SHA-256: `0c139c25123338de6244f5e9056de323ae06d9655ee48bf4602cda5bf15fb9bc`
- Fila atualizada: [commit 4bcb8b0e](https://github.com/arxazure/arquindex/commit/4bcb8b0e593886b5493f7c43d59e689dfe5cc1e8)
  - validação determinística: 238 IDs ARQ únicos;
  - ARQ-030 a ARQ-035 com 13 colunas, data de revisão e três runs anexados.
- Defeito compartilhado registrado: [issue #153](https://github.com/arxazure/arquindex/issues/153)
- Inventário de 56 subdomínios: [consolidado de 13/11/2026](https://github.com/arxazure/arquindex/blob/master/docs/seo/rodada-20261113-tarde-inventario-56-consolidado.md)

## Resultado por ficha

| Ficha | Resultado confirmado | Decisão |
|---|---|---|
| ARQ-030 | HTTP 200, DNS/TLS e UTF-8 válidos; artigo RIPD renderiza title/meta próprios, 4 articles e 2 JSON-LD; mobile 390/390 | Bloqueada: 2 H1, 2 canonicals, sem logo/WhatsApp, fora do sitemap e sobreposição com ARQ-017 |
| ARQ-031 | HTTP 200, canonical exato do parâmetro, 1 H1, title/meta próprios, 2 articles, 2 JSON-LD, logo/menu/WhatsApp e mobile 390/390 | Preservar publicação anterior; não afirmar que digitalização autoriza descarte; avaliar sitemap editorial |
| ARQ-032 | HTTP 200, DNS/TLS e UTF-8 válidos; artigo CONARQ renderiza title/meta próprios, 4 articles e 2 JSON-LD; mobile 390/390 | Bloqueada: 2 H1, 2 canonicals, sem logo/WhatsApp, fora do sitemap e duplicação do GUIDE-CONARQ |
| ARQ-033 | HTTP 200, canonical próprio, 1 H1, 5960 palavras no HTML inicial, 9 articles, logo/menu/WhatsApp, 84 links e mobile 390/390 | Preservar; diferenciar da pilar BH antes de ampliar; localizar sitemap correto |
| ARQ-034 | HTTP 200, canonical próprio, 1 H1, 6019 palavras, 9 articles, logo/menu/WhatsApp e 103 links | Bloqueada para nova promoção: overflow móvel 512/390 persiste e sitemap local não lista a raiz |
| ARQ-035 | HTTP 200, 1 H1, 3378 palavras, 3 JSON-LD, logo/menu/WhatsApp | Bloqueada: canonical aponta para caminho incorreto em www, title repete Arquindex, overflow 422/390 e sitemap sem a URL |

Nenhuma das seis páginas contém formulário. Todos os robots e sitemaps consultados responderam HTTP 200, mas nenhum sitemap contém a URL auditada. A camada HTTP sem navegador interpretou incorretamente alguns acentos; a renderização real confirmou `UTF-8` e ausência de mojibake nas seis páginas.

## Melhorias e pendências

1. A fila persistente foi atualizada com estado, evidências, decisões e próximas ações das seis fichas.
2. A issue #153 consolidou oito páginas afetadas pelo template dinâmico com H1/canonical duplicados e definiu critérios de aceite, backup e deduplicação.
3. Os três workflows da rodada guardaram evidências separadas de HTTP, mobile e estado pós-JavaScript.

Não foi aplicada correção em produção porque a origem/FTP dos templates não está mapeada nesta rodada e o backup HomeHost não possui restauração integral comprovada. A correção mínima depende de mapear arquivo e destino, validar backup/restauração isolada e então retestar URL por URL.

## Publicação, indexação e divulgação

ARQ-031 e ARQ-033 já tinham publicação anterior verificada e foram preservadas. Não houve material novo com benefício suficiente para republicação. ARQ-030, ARQ-032, ARQ-034 e ARQ-035 não foram promovidas ou submetidas.

Não há afirmação de indexação, posição, lead, preço atual, oferta ou caso autorizado.
