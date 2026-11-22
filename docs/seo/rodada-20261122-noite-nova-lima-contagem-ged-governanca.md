# Rodada SEO/GEO/AEO — 22/11/2026 — noite

## Escopo e segurança

Auditoria pública, somente leitura, das fichas ARQ-036 a ARQ-041. O lote cobre digitalização certificada em Nova Lima, digitalização em BH, GED/ECM, OCR de prontuários em Contagem e governança da informação.

Foram verificados DNS, TLS, HTTP e redirecionamentos, canonical, title, H1, meta description, mobile/desktop, robots, sitemap, links internos, conteúdo, identidade, WhatsApp e formulários.

Nenhuma escrita via FTP, alteração de produção, sitemap, IndexNow, Search Console, Bing ou divulgação social foi executada. ARQ-007 e ARQ-099 foram preservadas. O inventário consolidado de 56 subdomínios continua registrado com cobertura 56/56 em 13/11/2026 e não foi repetido.

## Evidências reproduzíveis

- Auditoria HTTP/SEO: [run 45084725093](https://github.com/arxazure/arquindex/actions/runs/45084725093)
  - job: `137400626541`
  - artefato: `14778596392`
  - SHA-256: `4cef431e3680f96ade1d8623dbd5b9a11df3db608265c8a5593354fca95e8881`
- Validação mobile/desktop: [run 45084724352](https://github.com/arxazure/arquindex/actions/runs/45084724352)
  - job: `137400624284`
  - artefato: `14777914393`
  - SHA-256: `bab1683fc3a280d992f1d1b2edd3465a7f83548f1b814a9b622fced70d843773`
- Canonical renderizada: [run 45084722703](https://github.com/arxazure/arquindex/actions/runs/45084722703)
  - job: `137400618626`
  - artefato: `14778329906`
  - SHA-256: `d85215e05dfc012384d55422f88ac9ef2d18fe45b654cc2405863b3b2ed5422a`
- Fila atualizada: [commit 591daeb6](https://github.com/arxazure/arquindex/commit/591daeb67c6439032baba4c17888b256129425e7)
  - 238 IDs ARQ únicos;
  - ARQ-036 a ARQ-041 com 13 colunas, data e três evidências.
- ARQ-040 registrada na [issue #154](https://github.com/arxazure/arquindex/issues/154).
- Inventário de 56 subdomínios: [consolidado de 13/11/2026](https://github.com/arxazure/arquindex/blob/master/docs/seo/rodada-20261113-tarde-inventario-56-consolidado.md)

## Resultado por ficha

| Ficha | Resultado confirmado | Decisão |
|---|---|---|
| ARQ-036 | HTTP 200, canonical próprio, 1 H1, 5964 palavras, 9 articles, logo/menu/WhatsApp, 84 links e mobile 390/390 | Preservar; não alegar unidade local em Nova Lima sem comprovação; localizar sitemap correto |
| ARQ-037 | HTTP 200, canonical próprio, 1 H1, 6017 palavras, 9 articles, identidade e WhatsApp | Bloqueada para promoção: overflow 512/390, sobreposição com pilar BH e sitemap sem a raiz |
| ARQ-038 | HTTP 200, canonical próprio, 1 H1, 3578 palavras, 3 JSON-LD, identidade e WhatsApp | Preservar publicação anterior, mas corrigir overflow 414/390 antes de nova promoção |
| ARQ-039 | HTTP 200, canonical próprio, 1 H1, 5969 palavras, 9 articles, identidade/WhatsApp, 84 links e mobile 390/390 | Preservar; manter limites do OCR e não anunciar precisão universal ou unidade local |
| ARQ-040 | HTTP/www responde 200 sem redirecionar; canonical aponta HTTPS sem www; 6015 palavras, identidade e WhatsApp | Bloqueada: variantes concorrentes, conteúdo de digitalização em vez de governança, overflow 512/390 e sitemap ausente |
| ARQ-041 | HTTP 200, canonical próprio, 1 H1, 3416 palavras, 3 JSON-LD, identidade/WhatsApp, 51 links e mobile 390/390 | Preservar; diferenciar de ARQ-040 e localizar sitemap correto |

Todos os robots e sitemaps consultados responderam 200, mas nenhum sitemap contém a URL correspondente. Nenhuma das seis páginas possui formulário. A renderização confirmou UTF-8 e ausência de mojibake; a leitura HTTP sem navegador exibiu apenas decodificação incorreta do cliente de auditoria.

## Melhorias e pendências

1. A fila persistente recebeu evidências, estado e próxima ação das seis fichas.
2. A issue #154 documenta a correção mínima de ARQ-040: 301 HTTP/www para HTTPS sem www, escolha editorial, ajuste móvel e critérios de aceite.
3. Três workflows independentes preservam evidência de HTTP, mobile e canonical renderizada.

A correção em produção não foi aplicada porque arquivo/template e destino FTP ainda precisam ser associados, e não há restauração integral do backup HomeHost comprovada. Nenhuma URL bloqueada foi submetida ou divulgada.

## Fechamento do dia

Foram auditadas 18 fichas distintas, ARQ-024 a ARQ-041, em três lotes sem repetição:

- 8 páginas preservadas por apresentarem base técnica estável;
- 10 páginas bloqueadas para nova promoção por canonical/H1, overflow, sobreposição editorial, identidade incompleta ou redirecionamento;
- 2 issues abertas: [#153](https://github.com/arxazure/arquindex/issues/153) para o template dinâmico e [#154](https://github.com/arxazure/arquindex/issues/154) para ARQ-040;
- nenhuma publicação, indexação, divulgação ou alegação de posição/lead.

Não houve material novo com fonte e benefício suficientes para justificar republicação social.
