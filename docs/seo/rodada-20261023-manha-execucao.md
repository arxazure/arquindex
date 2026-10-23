# Rodada SEO/GEO/AEO — 23/10/2026, manhã

## Resultado

Foram auditadas ARQ-083 a ARQ-088. Três páginas receberam melhorias substanciais e foram publicadas no Homehost por FTPS, com backup, validação pública e rollback preparado:

- ARQ-086 — https://databook-petrobras-elaboracao.arquindex.com.br/
- ARQ-087 — https://decreto10278-nova-lima.arquindex.com.br/custo.html
- ARQ-088 — https://encontrar-consultoria-conformidade-lgpd-bom-custo-beneficio.arquindex.com.br/comparativo.html

ARQ-083, ARQ-084 e ARQ-085 foram auditadas e preservadas sem alteração, respectivamente por sobreposição com ARQ-054, sobreposição com ARQ-075/pilar LGPD e falta de comprovação documental de atendimento estadual.

## Evidências técnicas

- Auditoria: https://github.com/arxazure/arquindex/actions/runs/39947384548 — sucesso.
- Publicação: https://github.com/arxazure/arquindex/actions/runs/39947610227 — sucesso.
- Validação independente: https://github.com/arxazure/arquindex/actions/runs/39948095478 — sucesso.
- Commit do publicador: db559775df0e4dd29f7dd2c67ffaf783b9bf0c6d.
- Commit do workflow: 1a9d4656d675e40f815a7a9bb358e3ac463e7d3f.
- Commit do validador: 5f1f2cf9790d9dd947d5e9349ca60b0a114a9cb4.
- Backup: /seo-backups/rodada-20261023-manha-20261023T114047Z.
- Artefato de identidade: 12499375562.

A validação confirmou, nas três URLs e em 390 px/1440 px: HTTP 200, canonical próprio, um H1, ausência de noindex, identidade Arquindex, menu responsivo, atendimento único, bloco AEO visível, CTA com UTM, ausência de overflow e sitemap XML público contendo a URL.

## Antes e depois

| ID | title anterior | title publicado | correção |
|---|---|---|---|
| ARQ-086 | Databook Petrobras Elaboracao | Arquindex | Arquindex | Montagem de Databook: Índice, Revisões e Aceite | Arquindex | canonical interno corrigido; conteúdo técnico de índice, revisões, vínculo e aceite; ressalva de não afiliação |
| ARQ-087 | Custo de digitalização certificada conforme Decreto 10.278/2020 Nova Lima | Arquindex | Arquindex | Arquindex | Orçamento de Digitalização em Nova Lima: Como Calcular | Arquindex | canonical interno corrigido; composição do orçamento e limites de validade/logística |
| ARQ-088 | Onde encontrar consultoria de conformidade LGPD com bom custo-benefício - Comparativo | Arquindex | Arquindex | Arquindex | Preço da Consultoria LGPD: Escopo e Entregáveis | Arquindex | canonical interno corrigido; comparação por escopo, entregáveis e responsabilidade |

Sitemaps atualizados e validados:

- https://databook-petrobras-elaboracao.arquindex.com.br/sitemap.xml
- https://decreto10278-nova-lima.arquindex.com.br/sitemap.xml
- https://encontrar-consultoria-conformidade-lgpd-bom-custo-beneficio.arquindex.com.br/sitemap.xml

Não houve submissão a Google Search Console, Bing Webmaster ou IndexNow: as integrações autenticadas disponíveis não expõem ação de submissão e não foi usada chave IndexNow não validada. Presença em sitemap não significa indexação.

## Search Console e Bing Webmaster

Períodos completos comparados: 07–20/10/2026 contra 23/09–06/10/2026.

- Google Search Console, seis URLs: somente ARQ-086 teve linha no período recente — consulta "site:www.b3.com.br/ ext:xlsx petrobras", 1 impressão, 0 clique, posição média 10. No período anterior, nenhuma das seis URLs teve linha. A amostra é insuficiente para concluir ganho ou perda.
- Bing Webmaster, propriedade https://arquindex.com.br/: 42 impressões e 1 clique no período recente contra 65 impressões e 3 cliques no anterior. O conector não oferece dimensão por página; portanto, esses totais não foram atribuídos às seis URLs. Houve consulta sobre índice de databook no período anterior (1 impressão) e nenhuma linha equivalente no recente.

## Divulgação oficial — apenas ARQ-086

Imagem: https://www.arquindex.com.br/assets/social-arq083-088/databook-controle-revisoes-20261023.jpg

- Instagram Arquindex: media 17994200952019291.
- LinkedIn Arquindex: urn:li:share:7519363317245558784.
- Google Business Arquindex BH: localPosts/2934846749896264639, estado PROCESSING.

ARQ-087 e ARQ-088 têm artes verificadas, mas não foram divulgadas para preservar a rotação e evitar três promoções na mesma manhã.

## Próximas prioridades

1. Auditar ARQ-089 a ARQ-094, avançando o cursor sem retornar às páginas já divulgadas.
2. Reavaliar ARQ-083 e ARQ-084 somente após decidir diferenciação frente a ARQ-054/ARQ-075.
3. Medir ARQ-086/087/088 em janelas completas de 7, 14 e 28 dias; não inferir ranking, indexação ou leads antes dos dados.
