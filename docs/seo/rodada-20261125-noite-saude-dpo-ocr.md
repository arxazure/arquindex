# Rodada SEO/GEO/AEO — 25/11/2026 — noite

## Escopo e limites

Foram auditadas ARQ-090 a ARQ-095, completando 18 URLs distintas nas três rodadas de 25/11/2026. A verificação foi somente leitura sobre os sites públicos. Não houve FTP, deploy, alteração de sitemap, submissão a buscadores ou nova divulgação.

ARQ-007 e ARQ-099 permaneceram preservadas. O inventário consolidado dos 56 subdomínios continua em `docs/seo/rodada-20261113-tarde-inventario-56-consolidado.md`; esta rodada não representa nova auditoria integral dos 56.

## Evidência reproduzível

| Verificação | Run | Job | Artefato | Digest | Estado |
|---|---:|---:|---:|---|---|
| DNS, TLS, HTTP, robots, sitemap e SEO estático | [45723435018](https://github.com/arxazure/arquindex/actions/runs/45723435018) | 139587180801 | 15073790630 | `sha256:183047c62c974ed319d3bc2db9da006fffa6f636dd4f1afdb2289b1ec0c636a0` | sucesso |
| Mobile/desktop | [45723436107](https://github.com/arxazure/arquindex/actions/runs/45723436107) | 139587184547 | 15073546163 | `sha256:be8eee23e7b0c74d994cb23b9642d73a306807e894fd667e065832ea20c55495` | sucesso |
| Canonical renderizado | [45723439048](https://github.com/arxazure/arquindex/actions/runs/45723439048) | 139587194909 | 15072952520 | `sha256:59f0c63ae3389b9a1fa10f1a6cf0f8188f1b6526dc209dcf6a74cdea35540281` | sucesso |

Commits dos validadores: `421f8217679f45e74d63303bf23a319cb66a413c`, `fa93b64f277c3e534195a6bffe8a1628716c95e7` e `51f01d8f285d7b3816446593c1861fd4244a3921`.

## Resultado por URL

| ID | Verificado | Pendência | Decisão |
|---|---|---|---|
| ARQ-090 | HTTP 200, canonical próprio, 3.543 palavras, identidade, WhatsApp, sitemap e mobile 390/390 | sem formulário; capacidade local deve permanecer confirmada antes de novas alegações | preservar publicação e hash |
| ARQ-091 | HTTP 200, canonical próprio, 6.047 palavras, identidade e WhatsApp | overflow 512/390; conteúdo genérico de BH; sitemap ausente; sem formulário | anexada à [issue #159](https://github.com/arxazure/arquindex/issues/159) |
| ARQ-092 | HTTP 200, canonical próprio, 6.033 palavras, identidade e WhatsApp | overflow 512/390; intenção pouco diferenciada; sitemap ausente; sem formulário | anexada à issue #159 |
| ARQ-093 | HTTP 200, canonical próprio, 6.038 palavras, identidade e WhatsApp | overflow 512/390; cluster de mapeamento pouco diferenciado; sitemap ausente; sem formulário | anexada à issue #159 |
| ARQ-094 | HTTP 200, canonical próprio, 6.056 palavras, identidade, WhatsApp, sitemap e mobile 390/390 | sem formulário | preservar publicação e hash |
| ARQ-095 | HTTP 200, canonical próprio, sitemap, WhatsApp, menu e mobile 390/390 | apenas 282 palavras, sete links internos, logo oficial não detectado, sem formulário | criada [issue #163](https://github.com/arxazure/arquindex/issues/163) |

O navegador confirmou UTF-8 correto nas seis páginas; o mojibake indicado pelo cliente HTTP é um falso positivo de decodificação.

## Melhorias persistentes

1. Três validadores independentes foram adicionados e executados com artefatos e digests.
2. ARQ-091, ARQ-092 e ARQ-093 foram incorporadas à issue #159; comentário `7177977548`.
3. A issue #163 foi criada para corrigir identidade e conteúdo da ARQ-095 sem perder canonical, sitemap ou critérios de aceite já publicados.

A fila foi atualizada preservando hashes, datas, canais e IDs existentes. Commit: [3160a3b](https://github.com/arxazure/arquindex/commit/3160a3be258c2e250d0dd67a5033d96e031caadf).

## Publicação e submissão

Nenhuma mudança pública foi feita. ARQ-091 a ARQ-093 dependem de origem/template e backup antes da correção estrutural. ARQ-095 também depende de origem e backup antes de aplicar a identidade oficial e enriquecer o conteúdo. ARQ-090 e ARQ-094 não justificavam republicação. Nenhuma peça social foi repetida e não há alegação nova de indexação, posição, GBP processado ou leads.

## Próximas ações

- localizar a origem da família com overflow e fazer backup restaurável;
- definir intenções próprias para ARQ-091, ARQ-092 e ARQ-093 antes de incluí-las em sitemap;
- executar a issue #163 com identidade institucional e guia técnico original de OCR;
- validar links contextuais, CTA com UTM e evento de lead somente após confirmar medição;
- retestar e submeter apenas após deploy comprovado.
