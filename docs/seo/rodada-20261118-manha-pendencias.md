# Rodada SEO/GEO/AEO — 18/11/2026 — manhã

## Escopo

Auditoria somente leitura de quatro URLs elegíveis com revisão antiga e não auditadas nos três lotes de 17/11: ARQ-215, ARQ-228, ARQ-233 e ARQ-236. Os arquivos técnicos Sitechecker foram excluídos por não serem páginas comerciais.

## Evidências

- Auditoria técnica: [run 44297241152](https://github.com/arxazure/arquindex/actions/runs/44297241152)
  - job `134777360949`
  - artifact `14424656313`
  - SHA-256 `91156b4e1801f0a4e92afa3c376b1485cc614f3d601de75280d8512e81b673a9`
- Mobile/desktop: [run 44297243665](https://github.com/arxazure/arquindex/actions/runs/44297243665)
  - job `134777368286`
  - artifact `14424840631`
  - SHA-256 `5ad35863bd10df33c8b5174bd30c98b4fba778369f7f6ddc0f592f9d8186e002`
- Fila atualizada: [commit f3c2542](https://github.com/arxazure/arquindex/commit/f3c2542593b8cffbef2b520f7c1b218f39c71b6e)
- Integridade da fila: [run 44297467112](https://github.com/arxazure/arquindex/actions/runs/44297467112) — sucesso.

## Resultado

| Ficha | Página | Resultado comprovado | Pendência |
|---|---|---|---|
| ARQ-215 | Hub Gestão documental/ECM/Databooks | HTTP 200; canonical própria; title/H1/meta description; 208 palavras; 19 links internos; URL no sitemap raiz; sem overflow. | Sem meta robots, logo, menu, WhatsApp ou formulário; fonte preparada ainda não publicada por bloqueio FTPS. |
| ARQ-228 | Databooks Sabará | HTTP 200; canonical própria; title/H1/meta; index,follow; 849 palavras; sem overflow. | Sem logo, menu, WhatsApp ou formulário; conteúdo distinto sobre acervos frágeis ainda não implementado; não localizada no sitemap raiz. |
| ARQ-233 | Digitalize Sabará | HTTP 200; canonical própria; 1.004 palavras; menu, WhatsApp e 13 links internos; sem overflow. | Sem formulário; detector não identificou imagem de logo; confirmar sitemap dedicado. |
| ARQ-236 | Digitalize Pedro Leopoldo | HTTP 200; canonical própria; 1.021 palavras; menu, WhatsApp e 13 links internos; sem overflow. | Sem formulário; detector não identificou imagem de logo; confirmar sitemap dedicado. |

As quatro páginas foram confirmadas em UTF-8, sem mojibake. DNS e TLS estavam válidos; o certificado observado expira em 28/12/2026.

## Publicação e submissão

- Melhorias publicadas em produção: **0**.
- Motivo: ARQ-215 e ARQ-228 exigem origem publicável, FTPS confiável e backup restaurável. ARQ-233 e ARQ-236 permanecem funcionais e não justificam alteração sem inspeção visual e rastreamento.
- Sitemap: nenhuma alteração.
- Search Console, Bing e IndexNow: nenhum envio.
- Divulgação social: nenhuma.
- Inventário dos 56 subdomínios: não repetido; permanece o consolidado anterior até mudança observável de DNS.
- ARQ-007 e ARQ-099: preservadas.
- Indexação, posição, conversão e leads: não inferidos.

## Próximas ações seguras

1. Desbloquear FTPS/backup e publicar a fonte já preparada do hub ARQ-215.
2. Preparar ARQ-228 com conteúdo realmente distinto sobre acervos antigos e frágeis, somente após confirmar atendimento e origem.
3. Inspecionar visualmente o wordmark de ARQ-233/236 e consultar a hierarquia completa dos sitemaps.
