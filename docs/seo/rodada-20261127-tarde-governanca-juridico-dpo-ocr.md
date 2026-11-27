# Rodada SEO/GEO/AEO — 27/11/2026 — tarde

## Escopo e limites

Foram auditadas ARQ-121 a ARQ-126. ARQ-007 e ARQ-099 permaneceram preservadas. Não houve FTP, deploy, postagem social, alteração de sitemap ou submissão a Search Console/Bing/IndexNow.

O inventário consolidado dos 56 subdomínios permanece em `docs/seo/rodada-20261113-tarde-inventario-56-consolidado.md`. Esta rodada não repetiu as 56 verificações e não declara nova cobertura total.

## Evidências

| Verificação | Run | Artefato | Digest |
|---|---|---|---|
| DNS, TLS, HTTP, SEO, robots e sitemap | [46043576494](https://github.com/arxazure/arquindex/actions/runs/46043576494) | 15221152608 | `sha256:c2af60f4cf3a5ff8f24a7f097c444e9291d888490336ac600ac4ca98728747f1` |
| Mobile 390 px e desktop 1440 px | [46043573646](https://github.com/arxazure/arquindex/actions/runs/46043573646) | 15221082662 | `sha256:b3a96fbd3a5fc57807b1588955e91e3f153ddc56bb453575c30862733fe5a53b` |
| Canonical renderizada | [46043571982](https://github.com/arxazure/arquindex/actions/runs/46043571982) | 15220498576 | `sha256:cd912ecc04533b71e46c15684b46bb0f1cdd146df270fcdf39df051208c48169` |

Todos os workflows concluíram com sucesso. O navegador confirmou UTF-8 correto nas seis páginas.

## Resultado por ficha

| Ficha | Resultado | Estado |
|---|---|---|
| ARQ-121 | HTTP 200, canonical própria; intenção MG ainda usa conteúdo de BH; overflow 512/390; fora do sitemap | [#159](https://github.com/arxazure/arquindex/issues/159#issuecomment-7224685131) |
| ARQ-122 | HTTP 200, canonical própria; conteúdo genérico e sobreposto; overflow 512/390; fora do sitemap | [#159](https://github.com/arxazure/arquindex/issues/159#issuecomment-7224685131) |
| ARQ-123 | HTTP 200, canonical própria; conteúdo jurídico ainda genérico; overflow 512/390; preparação não publicada | [#159](https://github.com/arxazure/arquindex/issues/159#issuecomment-7224685131) |
| ARQ-124 | HTTP 200, canonical própria; intenção de preço sobreposta; overflow 512/390; fora do sitemap | [#159](https://github.com/arxazure/arquindex/issues/159#issuecomment-7224685131) |
| ARQ-125 | HTTP 200, canonical própria, title/H1 de DPO, 3.382 palavras e sem overflow; meta genérica/truncada e fora do sitemap | [#170](https://github.com/arxazure/arquindex/issues/170) |
| ARQ-126 | HTTP 200, canonical própria, 6.172 palavras e sem overflow; title/H1/meta não correspondem a OCR e raiz fora do sitemap | [#170](https://github.com/arxazure/arquindex/issues/170) |

## Ações substanciais

1. ARQ-121 a 124 foram deduplicadas na issue móvel #159 com os requisitos editoriais próprios de cada URL.
2. Criada a issue #170 para alinhar DPO e OCR antes de inclusão em sitemap, exigindo preços atuais, critérios de aceite e backup.
3. Fila persistente atualizada nas seis fichas. Commit: [d822df74](https://github.com/arxazure/arquindex/commit/d822df741168186c3e55ffd7a346b6b511dae36a).

## Pendências

- Confirmar atendimento estadual antes de regionalizar ARQ-121.
- Consolidar ou diferenciar ARQ-122/124 sem páginas artificiais ou preços não confirmados.
- Revisar o script preparado para ARQ-123; preparação não equivale a publicação.
- Corrigir meta da ARQ-125 somente após verificar fatores e faixas vigentes de DPO.
- Diferenciar ARQ-126 com precisão medida, revisão humana, formatos, exceções e aceite.
- Atualizar sitemap e submeter apenas após publicação confirmada e reteste.
- Sem comprovação nova de indexação, posição ou leads.
