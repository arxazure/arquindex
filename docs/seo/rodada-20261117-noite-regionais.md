# Rodada SEO/GEO/AEO — 17/11/2026 — noite

## Escopo

Auditoria somente leitura de ARQ-221 a ARQ-226: Boa Vista, Manaus, Cuiabá, Pedro Leopoldo, Santa Luzia e Macapá. O lote comparou quatro páginas ainda sem identidade comprovada com duas páginas publicadas anteriormente por FTPS HomeHost.

## Evidências

- Auditoria técnica: [run 44201760911](https://github.com/arxazure/arquindex/actions/runs/44201760911)
  - job `134457373579`
  - artifact `14382056267`
  - SHA-256 `a184c2420c7115bcfd9fcb04a1bd0bf2ad3aacb3c3fb7729a3af752de2681563`
- Mobile/desktop: [run 44201762102](https://github.com/arxazure/arquindex/actions/runs/44201762102)
  - job `134457376307`
  - artifact `14381397520`
  - SHA-256 `2175eb5a48f9ad931e0639ac82c6b16d6c8e4ac2c2cd3b3fbd3e9af9829518ce`
- Fila atualizada: [commit e04ea6d](https://github.com/arxazure/arquindex/commit/e04ea6df2886ded08afde4e7a03c58b58b20ef81)
- Integridade da fila: [run 44201969627](https://github.com/arxazure/arquindex/actions/runs/44201969627) — sucesso.

## Resultado

| Ficha | Cidade | Resultado comprovado | Pendência |
|---|---|---|---|
| ARQ-221 | Boa Vista | HTTP 200; canonical própria; title/H1/meta; 900 palavras; UTF-8; sem overflow. | Sem logo, menu, WhatsApp ou formulário; não localizada no sitemap raiz consultado. |
| ARQ-222 | Manaus | HTTP 200; canonical própria; title/H1/meta; 892 palavras; UTF-8; sem overflow. | Sem logo, menu, WhatsApp ou formulário; não localizada no sitemap raiz consultado. |
| ARQ-223 | Cuiabá | HTTP 200; canonical própria; title/H1/meta; 890 palavras; UTF-8; sem overflow. | Sem logo, menu, WhatsApp ou formulário; não localizada no sitemap raiz consultado. |
| ARQ-224 | Pedro Leopoldo | HTTP 200; canonical própria; 1.076 palavras; logo, menu, WhatsApp e 18 links internos preservados; sem overflow. | Sem formulário; confirmar sitemap dedicado, pois a URL não aparece diretamente no sitemap raiz. |
| ARQ-225 | Santa Luzia | HTTP 200; canonical própria; 1.097 palavras; logo, menu, WhatsApp e 18 links internos preservados; sem overflow. | Sem formulário; confirmar sitemap dedicado, pois a URL não aparece diretamente no sitemap raiz. |
| ARQ-226 | Macapá | HTTP 200; canonical própria; title/H1/meta; 882 palavras; UTF-8; sem overflow. | Sem logo, menu, WhatsApp ou formulário; não localizada no sitemap raiz consultado. |

DNS e TLS foram válidos nas seis URLs. O certificado observado expira em 28/12/2026. Não houve mojibake.

## Publicação e submissão

- Melhorias publicadas em produção: **0**.
- Motivo: Pedro Leopoldo e Santa Luzia não apresentaram regressão; as quatro páginas restantes exigem localização da origem e backup restaurável antes da identidade/CTA.
- Sitemap: nenhuma alteração; a ausência no sitemap raiz não comprova ausência em sitemap dedicado.
- Search Console, Bing e IndexNow: nenhum envio.
- Divulgação social: nenhuma.
- Inventário dos 56 subdomínios: não repetido; permanece o consolidado anterior até mudança observável de DNS.
- ARQ-007 e ARQ-099: preservadas.
- Indexação, posição, conversão e leads: não inferidos.

## Próximas ações seguras

1. Mapear origem e backup de Boa Vista, Manaus, Cuiabá e Macapá antes de aplicar identidade.
2. Consultar a hierarquia completa dos sitemaps para as seis páginas.
3. Preservar Pedro Leopoldo e Santa Luzia e avaliar formulário somente após evidência de rastreamento, sem competir com o WhatsApp.
