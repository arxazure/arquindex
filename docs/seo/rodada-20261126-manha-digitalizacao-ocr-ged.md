# Rodada SEO/GEO/AEO — 26/11/2026 — manhã

## Escopo

Foram auditadas seis URLs: ARQ-096, ARQ-097, ARQ-098, ARQ-100, ARQ-101 e ARQ-102. A ARQ-099 foi deliberadamente excluída para preservar sua referência e divulgação já registradas.

A rodada foi somente leitura nos sites públicos. Não houve FTP, deploy, alteração de sitemap, submissão ou divulgação. O inventário consolidado dos 56 subdomínios permanece em `docs/seo/rodada-20261113-tarde-inventario-56-consolidado.md`; não se declara cobertura integral nova.

## Evidências

| Verificação | Run | Job | Artefato | Digest |
|---|---:|---:|---:|---|
| DNS, TLS, HTTP, robots, sitemap e SEO | [45812244872](https://github.com/arxazure/arquindex/actions/runs/45812244872) | 139882777563 | 15112868380 | `sha256:a062c528f3ce1d00c37c793ad0592abd6c6f3a5ca0d6274c064c7527c5c114be` |
| Mobile/desktop | [45812249461](https://github.com/arxazure/arquindex/actions/runs/45812249461) | 139882792002 | 15112423683 | `sha256:4204b4492abcf7dff349cfb605caf4f06d9e1b5d1cc120efa61a535b1fdbbb70` |
| Canonical renderizado | [45812250303](https://github.com/arxazure/arquindex/actions/runs/45812250303) | 139882794922 | 15112523582 | `sha256:53b712713645cadc59f612e1d48f2130f221e7e62d494fe292403489a55988de` |

Commits dos validadores: `bf72b97b86f8bcfd340ef6511c092a3c91980941`, `30292cc64584da836b47c795f20b94462b1cdf7f` e `67d3eecb5b69d70a68a8189c627eeaf0b27acd90`.

## Resultado por ficha

| ID | Verificado | Pendência | Decisão |
|---|---|---|---|
| ARQ-096 | HTTP 200, canonical próprio, 3.517 palavras, identidade, WhatsApp, sitemap e mobile 390/390 | sem formulário | preservar publicação e hash |
| ARQ-097 | HTTP 200, canonical próprio, sitemap, WhatsApp e mobile 390/390 | 280 palavras, 7 links internos, logo não detectado, sem formulário | incorporada à família da [issue #163](https://github.com/arxazure/arquindex/issues/163) |
| ARQ-098 | HTTP 200, canonical próprio, 3.672 palavras, identidade, WhatsApp, sitemap e mobile 390/390 | sem formulário | preservar publicação e hash |
| ARQ-100 | HTTP 200, um H1, 3.350 palavras e mobile 390/390 | canonical incorreto, title triplicado, meta truncada, sem WhatsApp/formulário e fora do sitemap | criada [issue #166](https://github.com/arxazure/arquindex/issues/166) |
| ARQ-101 | HTTP 200, canonical próprio, 6.007 palavras, identidade e WhatsApp | overflow 512/390, sem formulário e fora do sitemap | incorporada à [issue #159](https://github.com/arxazure/arquindex/issues/159) |
| ARQ-102 | HTTP 200, canonical próprio, identidade, WhatsApp, sitemap e mobile 390/390 | somente 529 palavras e sem formulário | criada [issue #165](https://github.com/arxazure/arquindex/issues/165) |

O navegador confirmou UTF-8 correto. Os sinais de mojibake do cliente HTTP são falsos positivos de decodificação.

## Melhorias registradas

1. A issue #163 foi ampliada para a ARQ-097, exigindo diferenciação frente à ARQ-095 e aplicação da identidade oficial.
2. A issue #166 documenta a correção mínima de canonical, title, meta, CTA e sitemap da ARQ-100.
3. A issue #165 documenta o enriquecimento técnico da ARQ-102 sem duplicar páginas Alfresco ou repetir divulgação.

A ARQ-101 também foi registrada na issue #159 como ocorrência adicional de overflow. A fila de 238 fichas foi atualizada preservando hashes, datas, canais e IDs. Commit: [acc90e8](https://github.com/arxazure/arquindex/commit/acc90e8c86cd25780a5b401ab1e74beb11e9fe95).

## Publicação

Nenhuma alteração pública foi feita. ARQ-097, ARQ-100, ARQ-101 e ARQ-102 dependem de origem identificada e backup restaurável. ARQ-096 e ARQ-098 não justificavam republicação. ARQ-099 não foi tocada. Não houve envio a Search Console, Bing ou IndexNow e não se afirma indexação, posição ou leads.
