# Rodada SEO/GEO/AEO — 17/11/2026 — manhã

## Escopo

Auditoria somente leitura de ARQ-216, ARQ-217, ARQ-218, ARQ-219, ARQ-220 e ARQ-227, com prioridade para Databooks, engenharia, mineração e cidades da RMBH. As URLs foram conferidas diretamente contra a fila antes da consolidação.

## Evidências válidas

- Auditoria técnica: [run 44076902300](https://github.com/arxazure/arquindex/actions/runs/44076902300)
  - job `134017134659`
  - artifact `14324593540`
  - SHA-256 `deee07753727a81690622b8e619cc50c36df2964013513a20d3a122ccd5a1892`
- Mobile/desktop: [run 44076905666](https://github.com/arxazure/arquindex/actions/runs/44076905666)
  - job `134017144551`
  - artifact `14324582407`
  - SHA-256 `a066073a31a875b9378a1dc89453593577e775040f13722335b7afd6b2bfe3f6`
- Fila atualizada: [commit 0a334f6](https://github.com/arxazure/arquindex/commit/0a334f6d0284adcb053547d67a8d617abb28d37b)
- Integridade da fila: [run 44077119165](https://github.com/arxazure/arquindex/actions/runs/44077119165) — sucesso.

Uma execução preliminar com caminhos não correspondentes à fila foi descartada e não foi usada no estado das fichas. Os workflows foram corrigidos nos commits [cd4729c](https://github.com/arxazure/arquindex/commit/cd4729c848434fafcc0f0639478fbc71d4fab15d) e [6f3930c](https://github.com/arxazure/arquindex/commit/6f3930c3820f76585c045c70204b06b34d0d9a48).

## Resultado

| Ficha | Cidade | Evidência positiva | Pendência comprovada |
|---|---|---|---|
| ARQ-216 | Porto Velho | HTTP 200; canonical própria; title/H1/meta; 900 palavras; UTF-8; sem overflow. | Sem logo, menu, WhatsApp ou formulário; fora do sitemap. |
| ARQ-217 | Vespasiano | HTTP 200; canonical própria; title/H1/meta; 865 palavras; UTF-8; sem overflow. | Sem logo, menu, WhatsApp ou formulário; fora do sitemap; fonte preparada ainda não publicada por bloqueio FTPS. |
| ARQ-218 | Ibirité | HTTP 200; canonical própria; title/H1/meta; 894 palavras; UTF-8; sem overflow. | Sem logo, menu, WhatsApp ou formulário; fora do sitemap; fonte preparada ainda não publicada por bloqueio FTPS. |
| ARQ-219 | Ribeirão das Neves | HTTP 200; canonical própria; title/H1/meta; 916 palavras; UTF-8; sem overflow. | Sem logo, menu, WhatsApp ou formulário; fora do sitemap. |
| ARQ-220 | Lagoa Santa | HTTP 200; canonical própria; title/H1/meta; 899 palavras; UTF-8; sem overflow. | Sem logo, menu, WhatsApp ou formulário; fora do sitemap. |
| ARQ-227 | Belém | HTTP 200; canonical própria; title/H1/meta; 889 palavras; UTF-8; sem overflow. | Sem logo, menu, WhatsApp ou formulário; fora do sitemap. |

DNS e TLS foram válidos nas seis URLs. O certificado observado expira em 28/12/2026.

## Publicação e submissão

- Melhorias publicadas em produção: **0**.
- Motivo: não há mapeamento individual da origem publicável, backup restaurável e conexão FTPS confiável comprovados nesta rodada. Alterar seis páginas semelhantes sem essa cadeia também aumentaria o risco de duplicação e doorway.
- Sitemap: nenhuma alteração.
- Search Console, Bing e IndexNow: nenhum envio.
- Divulgação social: nenhuma, preservando a deduplicação.
- Inventário dos 56 subdomínios: não repetido; o consolidado anterior permanece válido até nova mudança de DNS.
- ARQ-007 e ARQ-099: preservadas.
- Indexação, posição e leads: não inferidos.

## Próximas ações seguras

1. Corrigir o certificado/endpoint FTPS e obter backup restaurável antes de publicar ARQ-217 e ARQ-218 já preparadas.
2. Mapear a origem das demais quatro páginas e aplicar identidade/CTA individualmente, com diferenciação editorial verificável.
3. Incluir no sitemap somente após publicação confirmada e revalidação HTTP 200/canonical.
