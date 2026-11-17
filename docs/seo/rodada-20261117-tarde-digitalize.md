# Rodada SEO/GEO/AEO — 17/11/2026 — tarde

## Escopo

Auditoria somente leitura de ARQ-229, ARQ-230, ARQ-231, ARQ-232, ARQ-234 e ARQ-235. O lote cobre o hub Digitalize e cinco páginas locais prioritárias: Santa Luzia, Ribeirão das Neves, Ibirité, Vespasiano e Lagoa Santa.

## Evidências

- Auditoria técnica: [run 44138829378](https://github.com/arxazure/arquindex/actions/runs/44138829378)
  - job `134235673313`
  - artifact `14353796203`
  - SHA-256 `e736681a44d33e810a44efcf28398dbd5d0074103fd6d957e7435f14c50ee015`
- Mobile/desktop: [run 44138832365](https://github.com/arxazure/arquindex/actions/runs/44138832365)
  - job `134235683811`
  - artifact `14352418854`
  - SHA-256 `3c441df39eba5fbe6b7871e0f9c00281b56cf9cb7bafd0cebe7d19e4f644cca9`
- Fila atualizada: [commit 4bd7d2a](https://github.com/arxazure/arquindex/commit/4bd7d2aeeccfc5d9497d4f106432468d725b62fc)
- Integridade da fila: [run 44139121424](https://github.com/arxazure/arquindex/actions/runs/44139121424) — sucesso.

## Resultado

| Ficha | URL/município | Resultado comprovado | Pendência |
|---|---|---|---|
| ARQ-229 | Hub Digitalize | HTTP 200; canonical própria; title/H1/meta; 484 palavras; menu, WhatsApp, 29 links internos; URL no sitemap raiz; sem overflow. | Sem formulário; detector automatizado não identificou imagem de logo. |
| ARQ-230 | Santa Luzia | HTTP 200; canonical própria; 990 palavras; menu e WhatsApp; sem overflow. | Sem formulário; URL não localizada no sitemap raiz consultado; confirmar sitemap dedicado e logo por inspeção visual. |
| ARQ-231 | Ribeirão das Neves | HTTP 200; canonical própria; 992 palavras; menu e WhatsApp; sem overflow. | Sem formulário; URL não localizada no sitemap raiz consultado; confirmar sitemap dedicado e logo por inspeção visual. |
| ARQ-232 | Ibirité | HTTP 200; canonical própria; 973 palavras; menu e WhatsApp; sem overflow. | Sem formulário; URL não localizada no sitemap raiz consultado; confirmar sitemap dedicado e logo por inspeção visual. |
| ARQ-234 | Vespasiano | HTTP 200; canonical própria; 1.005 palavras; menu, WhatsApp e 13 links internos; sem overflow. | Sem formulário; URL não localizada no sitemap raiz consultado; confirmar sitemap dedicado e logo por inspeção visual. |
| ARQ-235 | Lagoa Santa | HTTP 200; canonical própria; 1.019 palavras; menu, WhatsApp e 13 links internos; sem overflow. | Sem formulário; URL não localizada no sitemap raiz consultado; confirmar sitemap dedicado e logo por inspeção visual. |

As seis páginas foram confirmadas em UTF-8, sem mojibake. DNS e TLS estavam válidos; o certificado observado expira em 28/12/2026.

## Publicação e submissão

- Melhorias publicadas em produção: **0**.
- Motivo: as páginas permanecem funcionais, e o teste do sitemap raiz não é suficiente para concluir exclusão dos sitemaps dedicados. Alterar sitemap, identidade ou formulário sem confirmar a origem, o backup e a hierarquia atual criaria risco desnecessário.
- Search Console, Bing e IndexNow: nenhum envio.
- Divulgação social: nenhuma.
- Inventário dos 56 subdomínios: não repetido; permanece o consolidado anterior até mudança observável de DNS.
- ARQ-007 e ARQ-099: preservadas.
- Indexação, posição, conversão e leads: não inferidos.

## Próximas ações seguras

1. Consultar a hierarquia completa de sitemaps e confirmar a presença das cinco URLs locais antes de qualquer edição.
2. Validar visualmente o componente de logo, porque o detector procura imagem e pode não reconhecer wordmark em texto/CSS.
3. Só avaliar formulário adicional após evidência de rastreamento e sem competir com o CTA de WhatsApp já funcional.
