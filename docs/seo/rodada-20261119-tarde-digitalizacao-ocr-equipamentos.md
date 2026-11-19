# Rodada SEO/GEO/AEO — 19/11/2026 — tarde

## Escopo

Auditoria somente leitura de ARQ-058, ARQ-062, ARQ-065, ARQ-068, ARQ-069 e ARQ-071: digitalização em Belo Horizonte, OCR, solução especializada, equipamentos e contratação. O lote não repete as páginas da manhã nem ARQ-007/ARQ-099.

## Evidências

- Auditoria técnica: [run 44579002704](https://github.com/arxazure/arquindex/actions/runs/44579002704)
  - job `135754184848`
  - artifact `14558396802`
  - SHA-256 `5a5eed3210dd43a5b9352f2b5773a50a6a71966a454152480c9355dcf64b3661`
- Mobile/desktop: [run 44578997966](https://github.com/arxazure/arquindex/actions/runs/44578997966)
  - job `135754168074`
  - artifact `14556344192`
  - SHA-256 `bb778008120a15604e3ba4ae02aadc021a66c3956f5f32482977b719cd5305f6`
- Fila atualizada: [commit 5abd00a](https://github.com/arxazure/arquindex/commit/5abd00a596b0e8917aceab1b8e7f10e14fd35970)
- Integridade da fila: [run 44579321008](https://github.com/arxazure/arquindex/actions/runs/44579321008) — sucesso.

## Resultado comprovado

| Ficha | Página | Resultado comprovado | Pendência |
|---|---|---|---|
| ARQ-058 | Digitalização EXIN BH | HTTP 200; canonical própria; title/H1/meta; `index,follow`; 280 palavras; menu, WhatsApp, 7 links internos e presença no sitemap próprio; sem overflow. | Conteúdo curto e integrante de grupo sobreposto; sem formulário; logo não detectada. |
| ARQ-062 | OCR em regiões metropolitanas | HTTP 200; um H1; 520 palavras; menu e logo detectada; sem overflow. | Canonical aponta para caminho incorreto em `www`; title repete Arquindex quatro vezes; sem WhatsApp/formulário; sitemap próprio não menciona a URL; sobreposição com ARQ-057. |
| ARQ-065 | Digitalização especializada | HTTP 200; canonical própria; 6.015 palavras; logo, menu, WhatsApp e 101 links internos. | Conteúdo/H1 ainda genéricos de BH; overflow móvel 512/390; sem formulário; sitemap próprio não menciona a URL. |
| ARQ-068 | Solução de digitalização | HTTP 200; canonical própria; 6.029 palavras; logo, menu, WhatsApp e 101 links internos. | Intenção genérica e conteúdo BH; overflow móvel 512/390; sem formulário; sitemap próprio não menciona a URL. |
| ARQ-069 | Equipamentos para digitalização | HTTP 200; canonical própria; 6.052 palavras; logo, menu, WhatsApp e 103 links internos. | Title menciona equipamentos, mas H1/meta/conteúdo são genéricos de digitalização BH; overflow móvel 512/390; sem formulário; sitemap próprio não menciona a URL. |
| ARQ-071 | Erros ao contratar digitalização | HTTP 200; um H1; 3.377 palavras; menu, logo e 46 links internos; sem overflow. | Canonical aponta para caminho incorreto em `www`; title repete Arquindex três vezes; sem WhatsApp/formulário; sitemap próprio não menciona a URL. |

As seis páginas responderam em UTF-8 no navegador, sem mojibake. DNS e TLS estavam válidos, com os hosts resolvendo para `177.234.150.42`. O parser HTTP exibiu caracteres corrompidos devido à ausência de charset explícito em algumas respostas; a renderização do navegador confirmou o texto correto.

## Publicação e submissão

- Melhorias publicadas em produção: **0**.
- Motivo: ARQ-065, ARQ-068 e ARQ-069 compartilham um provável template com o mesmo overflow e conteúdo genérico. Corrigir em massa sem identificar a origem e sem backup/restauração comprovados poderia afetar outras páginas. ARQ-062 e ARQ-071 também exigem mapeamento de origem antes da correção de canonical/title.
- FTP/Homehost: nenhuma escrita.
- Script de identidade: não executado indiscriminadamente.
- Sitemap: nenhuma alteração; a ausência no sitemap consultado não comprova exclusão da hierarquia completa.
- Search Console, Bing e IndexNow: nenhum envio, pois não houve alteração publicada.
- Divulgação social: nenhuma; não há novo material útil publicado.
- Inventário dos 56 subdomínios: não repetido; permanece o [consolidado de 13/11/2026](https://github.com/arxazure/arquindex/blob/master/docs/seo/rodada-20261113-tarde-inventario-56-consolidado.md) até mudança observável de DNS.
- ARQ-007 e ARQ-099: preservadas.
- Indexação, posição, conversão e leads: não inferidos.

## Próximas ações seguras

1. Localizar o template comum de ARQ-065/068/069 e identificar o elemento de 512 px antes de preparar uma correção única com testes de regressão.
2. Mapear origem/backup de ARQ-062 e ARQ-071; corrigir canonical/title e adicionar CTA rastreável sem fundir intenções editoriais.
3. Enriquecer ARQ-058 somente com conteúdo original, autoria e fontes, preservando canonical e posição no sitemap.
4. Para ARQ-069, substituir o conteúdo genérico por guia técnico de equipamentos apenas após validar fontes, limites e papel próprio no cluster.
