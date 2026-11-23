# Rodada SEO/GEO/AEO — 23/11/2026 — manhã

## Escopo e segurança

Auditoria pública, somente leitura, das fichas ARQ-042 a ARQ-047: páginas institucionais de digitalização, Alfresco, gestão documental, LGPD e Databooks em Belo Horizonte e Nova Lima.

Foram verificados DNS, TLS, HTTP, canonical, title, H1, meta description, mobile/desktop, robots, sitemap, links internos, conteúdo, identidade, WhatsApp e formulários.

Nenhuma escrita via FTP, alteração de produção, sitemap, IndexNow, Search Console, Bing ou divulgação social foi executada. ARQ-007 e ARQ-099 foram preservadas. O inventário de 56 subdomínios permanece no consolidado de 13/11/2026, com 56/56 nomes auditados, sem repetição nesta rodada.

## Evidências reproduzíveis

- HTTP/SEO: [run 45167383914](https://github.com/arxazure/arquindex/actions/runs/45167383914)
  - job: `137667742718`
  - artefato: `14814961894`
  - SHA-256: `63991485c03c5707b9f17867d66ac5992f692c4e9de92b6826ea56ec59e81535`
- Mobile/desktop: [run 45167388598](https://github.com/arxazure/arquindex/actions/runs/45167388598)
  - job: `137667758414`
  - artefato: `14813439645`
  - SHA-256: `6807f74bd4929269259945024843b08148ba54f84742f5fc9839b3d813b8e0d8`
- Canonical renderizada: [run 45167380946](https://github.com/arxazure/arquindex/actions/runs/45167380946)
  - job: `137667731827`
  - artefato: `14814054543`
  - SHA-256: `58b00f5f0ce9359d4a081336b143018ceca2cc248543af0fec07827efe2f94d7`
- Fila atualizada: [commit f4592714](https://github.com/arxazure/arquindex/commit/f45927146ae00ce9e715aba1af5dd328da8a21e5)
  - 238 IDs ARQ únicos;
  - ARQ-042 a ARQ-047 com 13 colunas, data e três evidências.
- Identidade pendente registrada na [issue #155](https://github.com/arxazure/arquindex/issues/155).
- Inventário de 56 subdomínios: [consolidado](https://github.com/arxazure/arquindex/blob/master/docs/seo/rodada-20261113-tarde-inventario-56-consolidado.md).

## Resultado por ficha

| Ficha | Resultado confirmado | Decisão |
|---|---|---|
| ARQ-042 | HTTP 200, canonical próprio, 1 H1, 1520 palavras, logo/menu/WhatsApp, 32 links e mobile 390/390 | Preservar; localizar sitemap correto e ampliar somente com diferenciação técnica |
| ARQ-043 | HTTP 200, canonical próprio, 1 H1, 1160 palavras, 6 articles, 2 JSON-LD, menu/WhatsApp e mobile estável | Preservar SEO; logo oficial não detectado, apenas 5 links e sitemap ausente |
| ARQ-044 | HTTP 200, canonical próprio, 1 H1, 1250 palavras, 4 articles, 2 JSON-LD, menu/WhatsApp e mobile estável | Preservar SEO; logo oficial não detectado, apenas 5 links e sitemap ausente |
| ARQ-045 | HTTP 200, canonical próprio, 1 H1, 1253 palavras, 4 articles, 2 JSON-LD, menu/WhatsApp e mobile estável | Preservar SEO; logo oficial não detectado, apenas 5 links e sitemap ausente |
| ARQ-046 | HTTP 200, canonical próprio, 1 H1, 1127 palavras, logo/menu/WhatsApp, 32 links e mobile 390/390 | Preservar; confirmar logística sem alegar unidade local e localizar sitemap |
| ARQ-047 | HTTP 200, canonical próprio, 1 H1, 1038 palavras, 1 JSON-LD, 12 links e mobile 390/390 | Bloqueada para promoção: sem logo, menu, WhatsApp ou sitemap |

Todas as páginas têm robots e sitemap raiz respondendo HTTP 200, mas nenhuma URL aparece no sitemap consultado. Nenhuma possui formulário. Não houve overflow ou mojibake.

## Melhorias e pendências

1. A fila persistente foi atualizada com estado, evidência e próxima ação das seis páginas.
2. A issue #155 consolida a correção de identidade de ARQ-043/044/045/047, preservando os elementos SEO já válidos.
3. Os três workflows guardam evidências independentes de HTTP, mobile e canonical pós-renderização.

A aplicação da identidade não foi executada porque arquivo/template e destino FTP ainda precisam ser associados, e a restauração integral do backup HomeHost não está comprovada. O script de padronização não deve ser usado em lote; cada página exige `DESIGN_TARGET`, backup e teste individual.

## Publicação e divulgação

ARQ-042, ARQ-043, ARQ-044, ARQ-045 e ARQ-046 foram preservadas sem republicação. ARQ-047 não foi promovida. Não houve material novo com fonte e benefício suficientes para postagem própria, nem afirmação de indexação, posição, preço, oferta ou lead.
