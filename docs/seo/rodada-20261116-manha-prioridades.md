# Rodada SEO/GEO/AEO — 16/11/2026 — manhã

## Escopo

Auditoria somente leitura de seis fichas sem revalidação recente: ARQ-168, ARQ-170, ARQ-172, ARQ-173, ARQ-182 e ARQ-184. Foram verificados DNS, TLS, HTTP, canonical, title, H1, meta description, meta robots, robots.txt, sitemap, conteúdo, links internos, identidade, WhatsApp, formulários e renderização em 390 px e 1440 px.

ARQ-007 e ARQ-099 foram preservadas. O inventário consolidado dos 56 subdomínios não foi repetido sem mudança de DNS comprovada.

## Evidências

- Auditoria técnica: [run 43861581535](https://github.com/arxazure/arquindex/actions/runs/43861581535)
  - job: `133279467376`
  - artifact: `14223451895`
  - SHA-256: `8dcc1e5eeda347e10295d8f2b401fa98399b6f14c30cd8079d33957ce3021715`
- Validação mobile/desktop: [run 43861587492](https://github.com/arxazure/arquindex/actions/runs/43861587492)
  - job: `133279486388`
  - artifact: `14223711004`
  - SHA-256: `7e0b36389ca0b9b143db21736a64af104875730324e8ff6b06c448c22a7501a1`
- Fila atualizada: [commit f0d3350](https://github.com/arxazure/arquindex/commit/f0d335058a6b4a614fb99f13e6e0beea50c40685)
- Integridade da fila: [run 43861898417](https://github.com/arxazure/arquindex/actions/runs/43861898417) — sucesso.

## Resultado por ficha

| Ficha | Resultado comprovado | Risco/pendência |
|---|---|---|
| ARQ-168 | DNS/TLS válidos; HTTP 200; canonical própria; `index,follow`; 6.037 palavras; logo, menu e WhatsApp; desktop 1440/1440. | A URL é de São Paulo, mas title, H1 e description continuam em Belo Horizonte. Mobile 512/390; URL ausente do sitemap; sem formulário. Não promover. |
| ARQ-170 | DNS/TLS válidos; HTTP 200; canonical própria; title/H1 coerentes com São Vicente e saúde; 6.051 palavras; identidade e WhatsApp; desktop 1440/1440. | Atendimento/logística regional e requisitos de saúde não comprovados. Mobile 512/390; URL ausente do sitemap; sem formulário. |
| ARQ-172 | DNS/TLS válidos; HTTP 200; canonical própria; 817 palavras; logo, menu, WhatsApp e um formulário; sem overflow em 390/390 e 1440/1440; sitemap contém a URL. | H1 vazio, meta robots ausente e robots.txt 404. Origem FTP continua não mapeada. |
| ARQ-173 | DNS/TLS válidos; HTTP 200; canonical própria; `index,follow`; 6.032 palavras; identidade e WhatsApp; desktop 1440/1440. | A URL é de São Paulo, mas title, H1 e description continuam em Belo Horizonte. Mobile 512/390; sitemap sem URL; sem formulário. Não promover. |
| ARQ-182 | DNS/TLS válidos e HTTP 200; sem overflow. | Publica apenas “Index of /” com 24 palavras. Não possui canonical, description, meta robots, logo, menu, WhatsApp, formulário, robots.txt ou sitemap. Exposição de listagem de diretório deve ser tratada na origem. |
| ARQ-184 | DNS/TLS válidos; HTTP 200; 3.305 palavras; H1 único; `index,follow`; logo, menu e WhatsApp. | Canonical aponta para caminho incorreto no domínio www; title repete “Arquindex” três vezes; comparativo/ranking sem evidência documentada; mobile 554/390; sitemap sem URL; sem formulário. Não promover. |

O Chromium confirmou UTF-8 e ausência de mojibake em todas as páginas. A decodificação incorreta vista no cliente HTTP simples decorre do cabeçalho `text/html` sem charset explícito em cinco URLs, não do texto renderizado no navegador.

## Implementação e publicação

- Melhorias substanciais publicadas: **0**.
- Motivo: nenhuma das páginas com erro possui mapeamento individual de origem/FTP e backup restaurável comprovados nesta rodada. ARQ-168, ARQ-170 e ARQ-173 também dependem de validação regional/comercial.
- Sitemaps alterados: **0**.
- Search Console, Bing e IndexNow: **nenhum envio**, pois não houve publicação.
- Divulgação social: **nenhuma**.
- Indexação, posição e leads: não declarados.

## Prioridade de correção

1. ARQ-182: desabilitar a listagem de diretório na origem e só reconstruir com conteúdo próprio, canonical e identidade.
2. ARQ-184: remover a alegação comparativa sem evidência e corrigir canonical/title/overflow após backup.
3. ARQ-172: corrigir H1 vazio, meta robots e robots.txt 404 preservando o formulário e a URL já presente no sitemap.
