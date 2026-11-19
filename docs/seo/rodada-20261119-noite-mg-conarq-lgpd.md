# Rodada SEO/GEO/AEO — 19/11/2026 — noite

## Escopo

Auditoria somente leitura de ARQ-072, ARQ-074, ARQ-077, ARQ-079, ARQ-080 e ARQ-083: digitalização em Minas Gerais, gestão documental corporativa, mapeamento em Niterói, preparação CONARQ, LGPD jurídica e digitalização pelo celular. O lote não repete as rodadas anteriores nem ARQ-007/ARQ-099.

## Evidências

- Auditoria técnica: [run 44640231703](https://github.com/arxazure/arquindex/actions/runs/44640231703)
  - job `135969110074`
  - artifact `14585444141`
  - SHA-256 `a5ed495810f2455fda3eea121bdc1118d95df491b494338cca3b11c654cd4cbf`
- Mobile/desktop: [run 44640229221](https://github.com/arxazure/arquindex/actions/runs/44640229221)
  - job `135969101120`
  - artifact `14585827682`
  - SHA-256 `3ae949d8124dbc03e3864bba564369b6adcecd0ce99ee94c446468ea0cf397fe`
- Fila atualizada: [commit da34fec](https://github.com/arxazure/arquindex/commit/da34fec5fe9866d86e3833b25ebee901bd2a2092)
- Integridade da fila: [run 44640530863](https://github.com/arxazure/arquindex/actions/runs/44640530863) — sucesso.

## Resultado comprovado

| Ficha | Página | Resultado comprovado | Pendência |
|---|---|---|---|
| ARQ-072 | Digitalização MG | HTTP 200; canonical própria; 6.029 palavras; logo, menu, WhatsApp e 101 links internos. | Title/H1/meta estão restritos a BH apesar da intenção Minas Gerais; overflow 512/390; sem formulário; sitemap próprio não menciona a URL. |
| ARQ-074 | Corporativo | HTTP 200; canonical própria; 6.045 palavras; logo, menu, WhatsApp e 103 links internos. | Conteúdo ainda genérico de BH; overflow 512/390; sem formulário; sitemap próprio não menciona a URL. |
| ARQ-077 | Mapeamento Niterói | HTTP 200; canonical própria; title/H1/meta locais; 6.040 palavras; logo, menu, WhatsApp e 101 links internos. | Overflow 512/390; sem formulário; sitemap próprio não menciona a URL; atendimento local ainda não comprovado. |
| ARQ-079 | Preparação CONARQ | HTTP 200; canonical própria; 6.019 palavras; logo, menu, WhatsApp e 101 links internos. | Title cita CONARQ, mas H1/meta/conteúdo são genéricos de digitalização BH; overflow 512/390; sem formulário; sitemap próprio não menciona a URL. |
| ARQ-080 | LGPD jurídica em Sete Lagoas | HTTP 200; um H1; 3.452 palavras; menu, logo e 43 links internos; sem overflow. | Canonical aponta para caminho incorreto em `www`; title repete Arquindex três vezes; sem WhatsApp/formulário; sitemap próprio não menciona a URL; atendimento local não comprovado. |
| ARQ-083 | Digitalização pelo celular | HTTP 200; canonical própria; 6.055 palavras; logo, menu, WhatsApp e 103 links internos. | Title cita aplicativos, mas H1/meta/conteúdo são genéricos de digitalização BH; overflow 512/390; sem formulário; sitemap próprio não menciona a URL. |

As seis páginas responderam em UTF-8 no navegador, sem mojibake. DNS e TLS estavam válidos, com resolução para `177.234.150.42`. O parser HTTP exibiu caracteres corrompidos pela ausência de charset explícito em algumas respostas; a renderização confirmou o texto correto.

## Diagnóstico de família

ARQ-072, ARQ-074, ARQ-077, ARQ-079 e ARQ-083 apresentam o mesmo padrão técnico: largura móvel de 512 px para viewport de 390 px, estrutura visual comum e blocos extensos que nem sempre correspondem à intenção declarada pela URL. O achado reforça que a correção deve ocorrer no template/origem identificado, com teste de regressão em páginas irmãs, e não por substituições isoladas indiscriminadas.

## Publicação e submissão

- Melhorias publicadas em produção: **0**.
- Motivo: cinco páginas compartilham provável template comum e ARQ-080 exige correção de origem/canonical. Não há backup integral com restauração comprovada nem mapeamento inequívoco dos arquivos de produção.
- FTP/Homehost: nenhuma escrita.
- Script de identidade: não executado indiscriminadamente.
- Sitemap: nenhuma alteração.
- Search Console, Bing e IndexNow: nenhum envio, pois não houve alteração publicada.
- Divulgação social: nenhuma; não houve novo material publicado.
- Inventário dos 56 subdomínios: não repetido; permanece o [consolidado de 13/11/2026](https://github.com/arxazure/arquindex/blob/master/docs/seo/rodada-20261113-tarde-inventario-56-consolidado.md) até mudança observável de DNS.
- ARQ-007 e ARQ-099: preservadas.
- Indexação, posição, conversão e leads: não inferidos.

## Próximas ações seguras

1. Localizar o template comum das cinco páginas com overflow e identificar o elemento de 512 px antes de preparar correção única com testes.
2. Corrigir ARQ-072, ARQ-079 e ARQ-083 editorialmente somente depois de definir papel próprio e preservar a página pilar/guia canônico.
3. Corrigir canonical/title/CTA da ARQ-080 após confirmar origem, backup e atendimento em Sete Lagoas.
4. Não promover ARQ-077 como página local antes de confirmar capacidade comercial/logística em Niterói.
