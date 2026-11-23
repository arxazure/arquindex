# Rodada SEO/GEO/AEO — Databooks e Digitalize

**Data:** 23/11/2026 (tarde, America/Sao_Paulo)  
**Escopo:** ARQ-048 a ARQ-053  
**Modo:** auditoria somente leitura em produção; registros e automações no GitHub

## Resultado executivo

Foram auditadas seis URLs prioritárias. Todas resolveram para `177.234.150.42`, apresentaram TLS válido, HTTP 200, canonical absoluta e própria, title, meta description, um H1, JSON-LD e renderização sem overflow em 390 px e 1440 px.

ARQ-048 e ARQ-049 permanecem saudáveis e foram preservadas. ARQ-050 a ARQ-053 têm menu e WhatsApp funcionais, porém o detector não encontrou imagem de logo oficial. Nenhuma das seis URLs apareceu no sitemap raiz consultado; isso não comprova ausência em toda a hierarquia de sitemaps. Nenhuma possui formulário.

ARQ-053 apresenta melhora observável frente ao registro anterior: agora foram detectados menu, WhatsApp e oito links internos. A auditoria não atribui essa recuperação a esta rodada, pois nenhuma alteração de produção foi realizada.

## Evidências

- Auditoria HTTP/SEO: [run 45229448877](https://github.com/arxazure/arquindex/actions/runs/45229448877)
  - job: `137884683893`
  - artefato: `14844968846`
  - digest: `sha256:5675d42e005c09d1a4e5ea20efcdda390d7ed31e3fd0623308684e6ceb606956`
- Validação mobile/desktop: [run 45229444389](https://github.com/arxazure/arquindex/actions/runs/45229444389)
  - job: `137884667882`
  - artefato: `14845413144`
  - digest: `sha256:599b14c71f20cc0cc9550bedbae167291be00a5da55db655ad38581347e8c6c6`
- Canonical dinâmico: [run 45229451865](https://github.com/arxazure/arquindex/actions/runs/45229451865)
  - job: `137884692822`
  - artefato: `14846796429`
  - digest: `sha256:030f51256ee6591ab5b9cbfef3124d237a999875ea2ae8193776778f2df76374`

Workflows criados e executados com sucesso:

- `.github/workflows/auditoria-prioridades-20261123-tarde.yml` — commit `fdc1d698f74acf8b883330cc5e6463bec10c14b0`
- `.github/workflows/validar-mobile-prioridades-20261123-tarde.yml` — commit `d04d340a5a0070dec758cff873977465741e07c5`
- `.github/workflows/validar-canonical-dinamico-20261123-tarde.yml` — commit `2f11928028e6d3b93d33a0ba389fded7613268f9`

## Registro e deduplicação

- Fila atualizada no commit [`f9d7e980f5a063af40496b7db4a77a6a62a8766a`](https://github.com/arxazure/arquindex/commit/f9d7e980f5a063af40496b7db4a77a6a62a8766a).
- Validação determinística: 238 IDs ARQ únicos; ARQ-048 a ARQ-053 com 13 colunas, data e três runs anexados.
- Pendência compartilhada da família Digitalize: [issue #156](https://github.com/arxazure/arquindex/issues/156).
- Inventário de 56 subdomínios: [consolidado de 13/11/2026](https://github.com/arxazure/arquindex/blob/master/docs/seo/rodada-20261113-tarde-inventario-56-consolidado.md), com 56/56 nomes auditados; não repetido sem mudança observável de DNS.

## Resultado por ficha

| Ficha | URL | Conteúdo e links | Identidade | Estado e próxima ação |
|---|---|---:|---|---|
| ARQ-048 | [Databooks Betim](https://www.arquindex.com.br/seo-regional/gestao-documental-ecm-databooks/betim/) | 1.175 palavras; 32 links internos | logo, menu e WhatsApp detectados | Preservar; confirmar escopo industrial/logística sem alegar unidade local e localizar sitemap aplicável. |
| ARQ-049 | [Databooks Contagem](https://www.arquindex.com.br/seo-regional/gestao-documental-ecm-databooks/contagem/) | 1.189 palavras; 32 links internos | logo, menu e WhatsApp detectados | Preservar; validar fluxo/logística reais antes de novas alegações e localizar sitemap aplicável. |
| ARQ-050 | [Digitalize Belo Horizonte](https://www.arquindex.com.br/digitalize/belo-horizonte/) | 998 palavras; 8 links internos | menu e WhatsApp; logo não detectado | Mapear origem e backup; aplicar logo por alvo individual e evitar canibalização da página pilar. |
| ARQ-051 | [Digitalize Contagem](https://www.arquindex.com.br/digitalize/contagem/) | 981 palavras; 8 links internos | menu e WhatsApp; logo não detectado | Mapear origem e backup; aplicar logo por alvo individual e preservar diferenciação logística. |
| ARQ-052 | [Digitalize Betim](https://www.arquindex.com.br/digitalize/betim/) | 979 palavras; 8 links internos | menu e WhatsApp; logo não detectado | Mapear origem e backup; aplicar logo por alvo individual e preservar distinção de Databooks Betim. |
| ARQ-053 | [Digitalize Nova Lima](https://www.arquindex.com.br/digitalize/nova-lima/) | 981 palavras; 8 links internos | menu e WhatsApp; logo não detectado | Preservar recuperação parcial; aplicar logo por alvo individual e manter distinção de Databooks Nova Lima. |

## Limites e pendências

Nenhuma escrita via FTP/Homehost, alteração de produção, artigo, preço, oferta, caso, formulário, sitemap, IndexNow, Search Console, Bing ou divulgação social foi executada. Como não houve publicação, não houve motivo para submissão de URLs.

O script `scripts/padronizar-identidade-arquindex.py` não foi executado indiscriminadamente. A correção da família Digitalize deve começar pelo mapeamento da origem e por backup/restauração verificáveis, usando `DESIGN_TARGET` individualmente.

ARQ-007 e ARQ-099 foram preservadas sem republicação ou nova divulgação. Não se inferiram indexação, posição, tráfego, conversão ou leads.
