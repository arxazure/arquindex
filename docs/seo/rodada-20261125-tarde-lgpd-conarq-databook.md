# Rodada SEO/GEO/AEO — 25/11/2026 — tarde

## Escopo e limites

Auditoria de ARQ-084 a ARQ-089, seis fichas distintas das verificadas pela manhã. A rodada foi somente leitura nos sites públicos. Não houve FTP, mudança em produção, publicação social ou submissão a buscadores.

ARQ-007 e ARQ-099 permaneceram preservadas. O inventário consolidado dos 56 subdomínios continua em `docs/seo/rodada-20261113-tarde-inventario-56-consolidado.md`; não se declara nova cobertura integral nesta rodada.

## Evidência

| Verificação | Run | Job | Artefato | Digest | Estado |
|---|---:|---:|---:|---|---|
| DNS, TLS, HTTP, robots, sitemap e SEO estático | [45667985796](https://github.com/arxazure/arquindex/actions/runs/45667985796) | 139395256232 | 15048511314 | `sha256:7d4cb8111035065a303764ca94fe483ddc7339614114e31bdccf039b2aa9c96a` | sucesso |
| Mobile/desktop | [45667987882](https://github.com/arxazure/arquindex/actions/runs/45667987882) | 139395264948 | 15047103628 | `sha256:19abc05e609a30dbd39670041150c59b10b08fffcc952d17e11c9029367bc273` | sucesso |
| Canonical renderizado | [45667990407](https://github.com/arxazure/arquindex/actions/runs/45667990407) | 139395273315 | 15047613409 | `sha256:05901a8340fa4405b54bdea5280099feffe165d44e606c6b9adcca8b9b627d56` | sucesso |

Commits dos validadores: `e49c91a7c950daeb0d69ff99f95fbad4f56061e0`, `090f75f12b97594d19e67ec6e963ba3ae4916d6c` e `82c14a8d8292cf3389df835fcb5f51414418aef8`.

## Resultado por URL

| ID | Resultado | Pendência | Decisão |
|---|---|---|---|
| ARQ-084 | HTTP 200, canonical próprio, title/H1/meta, 6.083 palavras, identidade e WhatsApp | overflow 512/390; sitemap não lista URL; sem formulário; papel sobreposto ao cluster LGPD | registrar na [issue #159](https://github.com/arxazure/arquindex/issues/159); não alterar sem origem e backup |
| ARQ-085 | HTTP 200, canonical próprio, 6.035 palavras, identidade e WhatsApp | overflow 512/390; intenção MG com title/H1/meta de BH; sitemap ausente; atendimento estadual não comprovado | registrar na issue #159; não ampliar promessa |
| ARQ-086 | HTTP 200, canonical próprio, sitemap, identidade, WhatsApp e mobile 390/390 | somente 546 palavras; sem formulário; GBP anterior ainda PROCESSING na fila | criada [issue #162](https://github.com/arxazure/arquindex/issues/162) para enriquecimento seguro |
| ARQ-087 | HTTP 200, canonical próprio, 3.601 palavras, sitemap, identidade, WhatsApp e mobile 390/390 | sem formulário | publicação e hash preservados; sem nova divulgação |
| ARQ-088 | HTTP 200, canonical próprio, 3.493 palavras, sitemap, identidade, WhatsApp e mobile 390/390 | sem formulário | publicação e hash preservados |
| ARQ-089 | HTTP 200, canonical próprio, 3.562 palavras, sitemap, identidade, WhatsApp e mobile 390/390 | sem formulário | publicação e hash preservados |

O navegador confirmou UTF-8 correto nas seis páginas; os sinais de mojibake do cliente HTTP são falsos positivos de decodificação.

## Melhorias persistentes

1. Três validadores foram adicionados e executados com artefatos e digests.
2. A issue #159 recebeu ARQ-084 e ARQ-085, medidas de overflow e contexto editorial; comentário `7169981577`.
3. A issue #162 documenta o plano de enriquecimento técnico da ARQ-086, incluindo limites de não afiliação e critérios de qualidade.

A fila de 238 fichas foi atualizada preservando datas, hashes, canais e IDs anteriores. Commit: [e46a194](https://github.com/arxazure/arquindex/commit/e46a1940a3455d94d98f967558c16e821eceac9c).

## Publicação

Nenhuma publicação foi feita. ARQ-084 e ARQ-085 precisam de correção estrutural e diferenciação antes do sitemap. ARQ-086 precisa localizar origem e backup antes do enriquecimento. ARQ-087 a ARQ-089 não apresentaram benefício real que justificasse republicação. Não houve envio a Search Console, Bing ou IndexNow e não se afirma indexação, posição ou leads.

## Próximas ações

- identificar a origem/template da família 512/390 e efetuar backup;
- confirmar o atendimento estadual da ARQ-085;
- enriquecer ARQ-086 conforme issue #162, com conteúdo técnico original e sem afiliação implícita;
- retestar HTTP, canonical, title, H1, meta, mobile, CTA, sitemap e links;
- publicar e submeter somente depois de validação e resposta autenticada registrada.
