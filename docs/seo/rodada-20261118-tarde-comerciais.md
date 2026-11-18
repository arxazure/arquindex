# Rodada SEO/GEO/AEO — 18/11/2026 — tarde

## Escopo

Auditoria somente leitura de seis intenções comerciais distintas: ARQ-002, ARQ-003, ARQ-036, ARQ-038, ARQ-039 e ARQ-043. O lote cobre OCR, digitalização em BH, digitalização certificada em Nova Lima, GED/ECM, prontuários em Contagem e Alfresco.

## Evidências

- Auditoria técnica: [run 44361203348](https://github.com/arxazure/arquindex/actions/runs/44361203348)
  - job `135002762058`
  - artifact `14454551182`
  - SHA-256 `91478ec3f58af0d5cbeb70d43bd5240d1f8df640ed590fcb00381e312c0473d8`
- Mobile/desktop: [run 44361207222](https://github.com/arxazure/arquindex/actions/runs/44361207222)
  - job `135002775902`
  - artifact `14454431357`
  - SHA-256 `a614b4fcfd7d43b9c11a588ecb27dcb989fa3a33cedb7e56e37617a565da1ab4`
- Fila atualizada: [commit c0f475f](https://github.com/arxazure/arquindex/commit/c0f475fe5abbba000209ba8f08fa896b601df3d3)
- Integridade da fila: [run 44361633630](https://github.com/arxazure/arquindex/actions/runs/44361633630) — sucesso.

## Resultado

| Ficha | Página | Resultado comprovado | Pendência |
|---|---|---|---|
| ARQ-002 | OCR BH | HTTP 200; canonical própria; index,follow; 286 palavras; menu, WhatsApp e sitemap próprio; sem overflow. | Conteúdo curto; sem formulário; detector não identificou imagem de logo. |
| ARQ-003 | Digitalização BH | HTTP 200; canonical própria; 3.352 palavras; logo, menu, WhatsApp e 36 links internos. | **Overflow móvel 422/390**; sem formulário; URL não localizada no sitemap próprio consultado. |
| ARQ-036 | Digitalização certificada Nova Lima | HTTP 200; canonical própria; 5.964 palavras; logo, menu, WhatsApp e 84 links internos; sem overflow. | Sem formulário; URL não localizada no sitemap próprio consultado. |
| ARQ-038 | GED/ECM BH | HTTP 200; canonical própria; 3.578 palavras; logo, menu, WhatsApp e 60 links internos. | **Recorrência de overflow móvel 414/390** após correção anterior; sem formulário; URL não localizada no sitemap próprio. |
| ARQ-039 | OCR prontuários Contagem | HTTP 200; canonical própria; 5.969 palavras; logo, menu, WhatsApp e 84 links internos; sem overflow. | Sem formulário; URL não localizada no sitemap próprio consultado. |
| ARQ-043 | Alfresco BH | HTTP 200; canonical própria; 1.160 palavras; menu e WhatsApp; sem overflow. | Sem formulário; detector não identificou imagem de logo; URL não localizada no sitemap raiz consultado. |

O navegador confirmou UTF-8 e ausência de mojibake nas seis páginas. A leitura HTTP sem charset gerou falso positivo de codificação em cinco subdomínios; esse sinal foi descartado em favor da renderização do Chromium.

## Melhoria de registro

A linha ARQ-039 continha ponto e vírgula não escapado no campo de próxima ação. Ela foi normalizada para 13 campos CSV durante a atualização, e o validador de integridade concluiu com sucesso.

## Publicação e submissão

- Melhorias publicadas em produção: **0**.
- Motivo: as duas correções de overflow exigem localizar o elemento causador e confirmar o backup individual antes de alterar CSS/HTML.
- Sitemap: nenhuma alteração; a ausência no sitemap consultado precisa ser confrontada com a hierarquia completa.
- Search Console, Bing e IndexNow: nenhum envio.
- Divulgação social: nenhuma.
- Inventário dos 56 subdomínios: não repetido; permanece o consolidado anterior até mudança observável de DNS.
- ARQ-007 e ARQ-099: preservadas.
- Indexação, posição, conversão e leads: não inferidos.

## Próximas ações seguras

1. Diagnosticar o elemento de 422 px em ARQ-003 e o de 414 px em ARQ-038.
2. Confirmar backups restauráveis e corrigir cada overflow isoladamente, com reteste 390/1440.
3. Consultar os sitemaps dedicados antes de qualquer submissão.
