# Rodada SEO/GEO/AEO — 22/11/2026 — manhã

## Escopo e segurança

Auditoria pública, somente leitura, das fichas ARQ-024 a ARQ-029. Foram verificados DNS, TLS, HTTP, canonical após JavaScript, title, H1, meta description, mobile, robots, sitemap, links internos, identidade, WhatsApp e formulários.

Nenhuma alteração de produção, FTP, sitemap, IndexNow, Search Console, Bing ou divulgação social foi executada. ARQ-007 e ARQ-099 foram preservadas sem republicação. O inventário histórico dos 56 subdomínios permanece no consolidado de 13/11/2026, com cobertura registrada de 56/56; ele não foi refeito nesta rodada para evitar duplicação.

## Evidências reproduzíveis

- Auditoria HTTP/SEO: [run 45018456030](https://github.com/arxazure/arquindex/actions/runs/45018456030)
  - job: `137195817155`
  - artefato: `14752588470`
  - SHA-256: `1c0f393fc1a65b970e7c06281d0e4f5e146ff65cf6813e3ba42f6a3390e6b219`
- Validação mobile: [run 45018457069](https://github.com/arxazure/arquindex/actions/runs/45018457069)
  - job: `137195819854`
  - artefato: `14752497822`
  - SHA-256: `a1fa8a5b9d78028e33917f5d56a454e5537bd722efc3c57ff647b12c1a9b93d1`
- Canonical dinâmico após JavaScript: [run 45018459557](https://github.com/arxazure/arquindex/actions/runs/45018459557)
  - job: `137195827425`
  - artefato: `14752747028`
  - SHA-256: `9339ee071460aec9b8a686706a37f4bb2d74a70c46b9a6e4ff3e3867ffa406eb`
- Fila de 238 fichas atualizada:
  - [commit 394df568](https://github.com/arxazure/arquindex/commit/394df5683fd2561491b4bf458a76a554894b34a2)
  - [correção estrutural 7d243538](https://github.com/arxazure/arquindex/commit/7d243538c3972a9d66178126a3c9ffdca87a0142)
  - validação local determinística: 238 IDs ARQ únicos; as seis linhas desta rodada possuem 13 colunas e as três evidências anexadas.
- Inventário de 56 subdomínios: [consolidado de 13/11/2026](https://github.com/arxazure/arquindex/blob/master/docs/seo/rodada-20261113-tarde-inventario-56-consolidado.md)

## Resultado por ficha

| Ficha | Resultado confirmado | Pendência / decisão |
|---|---|---|
| ARQ-024 | HTTP 200, TLS válido, canonical exato do parâmetro, title/meta/H1 próprios, 1 H1, 1 article, 3 JSON-LD, logo/menu/WhatsApp, 58 links internos e mobile 390/390 | Preservar; avaliar sitemap editorial sem substituir pilar e sem nova divulgação |
| ARQ-025 | HTTP 200, TLS válido, canonical exato, title/meta/H1 próprios, 1 H1, 2 articles, 2 JSON-LD, logo/menu/WhatsApp, 69 links e mobile 390/390 | Amostra anonimizada somente com autorização; avaliar sitemap |
| ARQ-026 | HTTP 200 e TLS válido; artigo renderizado; WhatsApp/menu | Bloqueada: 2 H1, 2 canonicals (base inválido + artigo correto), sem logo, fora do sitemap e overflow móvel 554/390 |
| ARQ-027 | HTTP 200 e TLS válido; artigo renderizado; WhatsApp/menu | Bloqueada: 2 H1, 2 canonicals, sem logo, fora do sitemap, overflow 554/390 e sobreposição com ARQ-021 |
| ARQ-028 | HTTP 200, TLS válido, canonical exato, title/meta/H1 próprios, 1 H1, 4 articles, 2 JSON-LD, logo/menu/WhatsApp, 61 links e mobile 390/390 | Preservar; não alegar unidade local em São Paulo sem comprovação; avaliar sitemap |
| ARQ-029 | HTTP 200, TLS válido, artigo renderizado, logo/menu/WhatsApp e mobile 390/390 | Bloqueada: 2 H1, 2 canonicals, fora do sitemap e sobreposição com ARQ-031 |

Todas as seis URLs têm robots acessível e sitemap HTTP 200, mas nenhuma URL parametrizada aparece no sitemap correspondente. Nenhuma possui formulário. A renderização em navegador confirmou UTF-8 sem mojibake.

## Diagnóstico consolidado

ARQ-026, ARQ-027 e ARQ-029 ampliam o mesmo grupo de defeito já observado em ARQ-015, ARQ-019 e ARQ-020: o template mantém H1 e canonical da página-base e acrescenta os elementos do artigo. ARQ-026 e ARQ-027 também apresentam overflow móvel de 554 px em viewport de 390 px.

A correção adequada é única e controlada por origem: inventariar o template compartilhado, obter backup verificável, restaurar em ambiente isolado, remover apenas o H1/canonical base quando houver artigo dinâmico, aplicar o logo oficial e retestar cada URL. O script de identidade não deve ser executado em lote sem essa associação.

## Publicação e indexação

Nenhuma das três páginas bloqueadas foi alterada ou promovida. As três páginas saudáveis foram preservadas, pois já possuem material verificado e não havia benefício real que justificasse republicação. Não há afirmação de indexação, posição, lead, preço, oferta ou caso autorizado.
