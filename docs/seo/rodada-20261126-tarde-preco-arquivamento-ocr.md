# Rodada SEO/GEO/AEO — 26/11/2026 — tarde

## Escopo e limites

Rodada executada sobre seis fichas consecutivas da fila: ARQ-103 a ARQ-108. ARQ-099 foi preservada e não foi republicada. Não houve acesso FTP, alteração em produção, postagem social, submissão a mecanismos de busca ou alegação de indexação, posição ou lead.

O inventário consolidado de 56 subdomínios permanece referenciado em `docs/seo/rodada-20261113-tarde-inventario-56-consolidado.md` (56/56 naquela evidência). Esta rodada não repetiu a varredura integral e, portanto, não declara nova cobertura total.

## Evidências executadas

| Verificação | Run | Artefato | Digest |
|---|---|---|---|
| DNS, TLS, HTTP, SEO, robots e sitemap | [45870236703](https://github.com/arxazure/arquindex/actions/runs/45870236703) | 15142866016 | `sha256:16f0c31dacc959171586721bcb192730b28b1e360b8819b88680b595c178646a` |
| Mobile 390 px e desktop 1440 px | [45870243070](https://github.com/arxazure/arquindex/actions/runs/45870243070) | 15143136016 | `sha256:cc4579ac7eb9d442e9fd574d68f2a3d52bc75a90951a99aa35118157a8810c2f` |
| Canonical e metadados renderizados | [45870239074](https://github.com/arxazure/arquindex/actions/runs/45870239074) | 15142567032 | `sha256:573be3b646c703878324352679e5877bd81bc029cde4e4ab7e91889acb2b3b78` |

Todos os workflows concluíram com sucesso. A detecção de mojibake do cliente HTTP foi descartada como falso positivo, pois o navegador confirmou UTF-8 e ausência de mojibake nas seis URLs.

## Resultado por ficha

| Ficha | Resultado comprovado | Estado |
|---|---|---|
| ARQ-103 | HTTP 200, DNS/TLS, UTF-8, sem overflow; canonical aponta para caminho inválido no domínio principal; title repete Arquindex quatro vezes; sem WhatsApp/formulário; fora do sitemap local | pendência [#167](https://github.com/arxazure/arquindex/issues/167) |
| ARQ-104 | HTTP 200, canonical própria, title/H1, identidade, WhatsApp, 390/1440 sem overflow e URL no sitemap | preservada |
| ARQ-105 | HTTP 200, DNS/TLS, UTF-8, sem overflow; canonical aponta para caminho inválido no domínio principal; title repete Arquindex quatro vezes; sem WhatsApp/formulário; fora do sitemap local | pendência [#167](https://github.com/arxazure/arquindex/issues/167) |
| ARQ-106 | HTTP 200, canonical própria, title/H1, identidade, WhatsApp, 6.012 palavras, sem overflow e URL no sitemap | preservada; região/logística não ampliadas |
| ARQ-107 | HTTP 200, canonical própria, title/H1, identidade, WhatsApp, critérios de OCR, sem overflow e URL no sitemap | preservada |
| ARQ-108 | HTTP 200, canonical própria, identidade e WhatsApp; mobile 512/390, desktop 1440/1440; sem formulário; raiz fora do sitemap | deduplicada na [#159](https://github.com/arxazure/arquindex/issues/159#issuecomment-7199614232) |

## Ações registradas

1. Criada a issue #167 para tratar ARQ-103 e ARQ-105 como família, exigindo document root, backup/restauração e decisão editorial antes de canonical, title, CTA ou sitemap.
2. ARQ-108 adicionada à issue #159 existente, evitando nova pendência duplicada.
3. Fila de 238 fichas atualizada nas seis entradas, preservando hashes e registros anteriores de ARQ-104, ARQ-106 e ARQ-107. Commit: [aa49c583](https://github.com/arxazure/arquindex/commit/aa49c58372cbd9633f3ed25cab610381484fdb7f).

## Pendências e bloqueios

- Não alterar ARQ-103/105 em lote: falta origem/template e backup restaurável; também falta decisão de consolidar ou diferenciar conteúdo.
- Não corrigir ARQ-108 isoladamente até localizar a origem comum do overflow.
- Não criar artigo ou peça social nesta rodada: não surgiu fonte/material novo que justificasse publicação, e ARQ-099 permanece deduplicada.
- Não atualizar sitemap nem enviar Search Console/Bing/IndexNow antes de existir URL canônica mantida e publicação confirmada.
- Não afirmar preços, ofertas, casos, cobertura regional, indexação, posição ou leads.
