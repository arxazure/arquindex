# Rodada SEO/GEO/AEO — 20/11/2026 — tarde

## Escopo

Auditoria somente leitura de ARQ-100, ARQ-101, ARQ-103, ARQ-105, ARQ-108 e ARQ-112: checklist de contratação, digitalização genérica/corporativa e páginas de preço. O lote não repete a rodada da manhã nem ARQ-099.

## Evidências

- Auditoria técnica: [run 44784935839](https://github.com/arxazure/arquindex/actions/runs/44784935839)
  - job `136457150408`
  - artifact `14653996233`
  - SHA-256 `33a166d5e8d263dd4e4821b9fffcd893ff3e2b7a844b6d9228d9591e49de9b1a`
- Mobile/desktop: [run 44784939549](https://github.com/arxazure/arquindex/actions/runs/44784939549)
  - job `136457164159`
  - artifact `14653497036`
  - SHA-256 `00f507a43bfa2d1639d4e36d4fcf3f5cc69ca8db4cace05efe9c2fce0b9c888b`
- Fila atualizada: [commit 6cfc805](https://github.com/arxazure/arquindex/commit/6cfc805e3efeaf81b61a76ca393318fe66d28fb9)
- Integridade da fila: [run 44785224387](https://github.com/arxazure/arquindex/actions/runs/44785224387) — sucesso.

## Resultado comprovado

| Ficha | Página | Resultado comprovado | Pendência |
|---|---|---|---|
| ARQ-100 | Checklist de empresas | HTTP 200; um H1; 3.350 palavras; menu, logo e 46 links internos; sem overflow. | Canonical incorreta em `www`; title repete Arquindex três vezes; sem WhatsApp/formulário; sitemap próprio não menciona a URL; sobreposição com ARQ-096. |
| ARQ-101 | Digitalizar | HTTP 200; canonical própria; 6.007 palavras; logo, menu, WhatsApp e 103 links internos. | Conteúdo genérico BH; overflow 512/390; sem formulário; sitemap próprio não menciona a URL; papel frente à pilar/ARQ-098 indefinido. |
| ARQ-103 | Preço para empresas | HTTP 200; um H1; 3.365 palavras; menu, logo e 43 links internos; sem overflow. | Canonical incorreta em `www`; title repete Arquindex quatro vezes; sem WhatsApp/formulário; sitemap próprio não menciona a URL; sobreposição com ARQ-099. |
| ARQ-105 | O que é digitalização | HTTP 200; um H1; 3.384 palavras; menu, logo e 43 links internos; sem overflow. | Canonical incorreta em `www`; title repete Arquindex quatro vezes; sem WhatsApp/formulário; sitemap próprio não menciona a URL; sobreposição com ARQ-098. |
| ARQ-108 | Digitalização corporativa BH | HTTP 200; canonical própria; 6.020 palavras; logo, menu, WhatsApp e 101 links internos. | Overflow 512/390; sem formulário; sitemap próprio não menciona a URL; diferenciação editorial pendente. |
| ARQ-112 | Preços, escopo e critérios | HTTP 200; canonical própria; title de preço; 6.029 palavras; logo, menu, WhatsApp e 101 links internos. | H1/meta genéricos de digitalização BH; overflow 512/390; sem formulário; sitemap próprio não menciona a URL; sobreposição com ARQ-099/109. |

As seis páginas renderizaram em UTF-8, sem mojibake. DNS e TLS estavam válidos, resolvendo para `177.234.150.42`.

## Diagnóstico de famílias

- ARQ-100, ARQ-103 e ARQ-105 pertencem ao padrão de páginas internas com canonical montada incorretamente no domínio `www`, repetição de marca no title e ausência de CTA WhatsApp.
- ARQ-101, ARQ-108 e ARQ-112 pertencem ao template extenso com overflow móvel de 512 px em viewport de 390 px.
- Os dois grupos exigem origens e testes diferentes; não devem receber uma substituição genérica única.

## Publicação e submissão

- Melhorias publicadas em produção: **0**.
- Motivo: não há backup integral com restauração comprovada nem mapeamento inequívoco das origens. As páginas também possuem sobreposição editorial que deve ser resolvida antes de alterar sinais canônicos.
- FTP/Homehost: nenhuma escrita.
- Script de identidade: não executado indiscriminadamente.
- Sitemap: nenhuma alteração.
- Search Console, Bing e IndexNow: nenhum envio.
- Divulgação social: nenhuma.
- Inventário dos 56 subdomínios: não repetido; permanece o [consolidado de 13/11/2026](https://github.com/arxazure/arquindex/blob/master/docs/seo/rodada-20261113-tarde-inventario-56-consolidado.md) até mudança observável de DNS.
- ARQ-007 e ARQ-099: preservadas.
- Indexação, posição, conversão e leads: não inferidos.

## Próximas ações seguras

1. Localizar o gerador das páginas internas ARQ-100/103/105 e preparar correção mínima de canonical/title/CTA com regressão.
2. Localizar o elemento de 512 px no template de ARQ-101/108/112.
3. Definir consolidação/diferenciação de preço antes de alterar ARQ-103/112, preservando ARQ-099.
4. Não enviar qualquer URL aos mecanismos de busca antes de publicação e verificação pública.
